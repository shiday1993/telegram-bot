const FAILOVER_STATUS = new Set([502, 503, 504, 520, 521, 522, 523, 524]);
const BODYLESS_METHODS = new Set(["GET", "HEAD"]);

function jsonResponse(data, status = 200) {
    return Response.json(data, {
        status,
        headers: {
            "cache-control": "no-store",
        },
    });
}

function cleanBaseUrl(value) {
    return String(value || "").replace(/\/+$/, "");
}

function getTimeout(env) {
    const timeout = Number(env.REQUEST_TIMEOUT_MS || 7000);

    if (!Number.isFinite(timeout) || timeout < 1000) {
        return 7000;
    }

    return timeout;
}

function getBackendTargets(env) {
    return [
        {
            name: "primary",
            url: cleanBaseUrl(env.PRIMARY_BACKEND_URL),
        },
        {
            name: "secondary",
            url: cleanBaseUrl(env.SECONDARY_BACKEND_URL),
        },
    ].filter((target) => target.url);
}

function createBackendUrl(baseUrl, incomingUrl) {
    const target = new URL(baseUrl);

    const basePath = target.pathname.replace(/\/+$/, "");
    const requestPath = incomingUrl.pathname.startsWith("/")
        ? incomingUrl.pathname
        : `/${incomingUrl.pathname}`;

    target.pathname = `${basePath}${requestPath}`;
    target.search = incomingUrl.search;

    return target;
}

function createForwardHeaders(request, env, targetName) {
    const headers = new Headers(request.headers);

    headers.delete("host");
    headers.delete("content-length");
    headers.delete("connection");

    headers.set("x-forwarded-host", new URL(request.url).host);
    headers.set("x-forwarded-proto", new URL(request.url).protocol.slice(0, -1));
    headers.set("x-worker-backend", targetName);

    if (env.BACKEND_GATEWAY_SECRET) {
        headers.set("x-backend-gateway-secret", env.BACKEND_GATEWAY_SECRET);
    }

    return headers;
}

async function fetchWithTimeout(url, options, timeoutMs) {
    const controller = new AbortController();

    const timeoutId = setTimeout(() => {
        controller.abort();
    }, timeoutMs);

    try {
        return await fetch(url, {
            ...options,
            signal: controller.signal,
            redirect: "manual",
        });
    } finally {
        clearTimeout(timeoutId);
    }
}

async function forwardRequest({ request, incomingUrl, target, body, env }) {
    const backendUrl = createBackendUrl(target.url, incomingUrl);
    const options = {
        method: request.method,
        headers: createForwardHeaders(request, env, target.name),
    };

    if (!BODYLESS_METHODS.has(request.method.toUpperCase())) {
        options.body = body;
    }

    return fetchWithTimeout(backendUrl.toString(), options, getTimeout(env));
}

function validateTelegramWebhook(request, incomingUrl, env) {
    const webhookPath = env.TELEGRAM_WEBHOOK_PATH || "/webhook";
    if (incomingUrl.pathname !== webhookPath) {
        return null;
    }

    if (request.method !== "POST") {
        return jsonResponse({
                ok: false,
                message: "Method not allowed",
            },405,
        );
    }

    if (!env.TELEGRAM_WEBHOOK_SECRET) {
        console.error("TELEGRAM_WEBHOOK_SECRET belum diatur");
        return jsonResponse(
            {
                ok: false,
                message: "Worker configuration error",
            },
            500,
        );
    }

    const incomingSecret = request.headers.get("X-Secret-Token");

    if (incomingSecret !== env.TELEGRAM_WEBHOOK_SECRET) {
        return jsonResponse(
            {
                ok: false,
                message: "Unauthorized webhook",
            },
            401,
        );
    }

    return null;
}

async function proxyWithFailover(request, env) {
    const incomingUrl = new URL(request.url);
    const targets = getBackendTargets(env);

    if (!targets.length) {
        console.error("Tidak ada backend URL yang dikonfigurasi");

        return jsonResponse(
            {
                ok: false,
                message: "Backend belum dikonfigurasi",
            },
            500,
        );
    }

    const body = BODYLESS_METHODS.has(request.method.toUpperCase()) ? null : await request.arrayBuffer();
    const errors = [];

    for (const target of targets) {
        try {
            const response = await forwardRequest({
                request,
                incomingUrl,
                target,
                body,
                env,
            });

            if (!FAILOVER_STATUS.has(response.status)) {
                console.log(
                    JSON.stringify({
                        event: "proxy_success",
                        backend: target.name,
                        method: request.method,
                        path: incomingUrl.pathname,
                        status: response.status,
                    }),
                );

                return response;
            }

            errors.push({
                backend: target.name,
                status: response.status,
                reason: "gateway_error",
            });

            console.warn(
                JSON.stringify({
                    event: "proxy_failover",
                    backend: target.name,
                    method: request.method,
                    path: incomingUrl.pathname,
                    status: response.status,
                }),
            );
        } catch (error) {
            const reason =
                error?.name === "AbortError"
                    ? "timeout"
                    : error?.message || "network_error";

            errors.push({
                backend: target.name,
                reason,
            });

            console.warn(
                JSON.stringify({
                    event: "proxy_failover",
                    backend: target.name,
                    method: request.method,
                    path: incomingUrl.pathname,
                    reason,
                }),
            );
        }
    }

    console.error(
        JSON.stringify({
            event: "all_backends_failed",
            method: request.method,
            path: incomingUrl.pathname,
            errors,
        }),
    );

    return jsonResponse(
        {
            ok: false,
            message: "Semua backend tidak dapat diakses",
        },
        503,
    );
}

export default {
    async fetch(request, env) {
        const url = new URL(request.url);
        if (request.method === "GET" && url.pathname === "/__worker/health") {
            return jsonResponse({
                ok: true,
                service: "telegram-failover-gateway",
                primary_configured: Boolean(env.PRIMARY_BACKEND_URL),
                secondary_configured: Boolean(env.SECONDARY_BACKEND_URL),
            });
        }

        const validationError = validateTelegramWebhook(request, url, env);
        if (validationError) {
            return validationError;
        }

        return proxyWithFailover(request, env);
    },
};
