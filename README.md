# 🤖 Telegram Notification Service

Service Telegram sederhana berbasis **Python + FastAPI** untuk mengirim notifikasi dari server atau aplikasi lain melalui **Telegram Bot API**.

Project ini masih dalam tahap pengembangan. Saat ini service hanya digunakan untuk **mengirim pesan/notifikasi ke Telegram**. Fitur untuk menerima dan memproses perintah dari Telegram belum tersedia dan akan dikembangkan menggunakan **Telegram Webhook**.

## 🚧 Status Saat Ini

Saat ini fitur yang sudah tersedia:

* ✅ Mengirim pesan ke Telegram
* ✅ Mengirim pesan ke default `chat_id`
* ✅ Mengirim pesan ke custom `chat_id`
* ✅ REST API menggunakan FastAPI
* ✅ Membaca update Telegram untuk kebutuhan development
* ⏳ Menerima perintah dari Telegram
* ⏳ Memproses command bot
* ⏳ Telegram Webhook

## 📌 TODO

* [ ] Implementasi Telegram Webhook
* [ ] Menerima pesan dari Telegram
* [ ] Membuat command handler
* [ ] Menambahkan command `/start`
* [ ] Menambahkan command `/status`
* [ ] Menambahkan command `/ping`
* [ ] Authorization berdasarkan Telegram User ID
* [ ] Support notifikasi ke Telegram Group
* [ ] Error handling dan logging
* [ ] Dokumentasi deployment production

Rencana alur komunikasi dua arah:

```text id="jz0xcu"
Telegram User
      │
      │ /status
      ▼
Telegram Bot API
      │
      │ Webhook
      ▼
FastAPI
      │
      ▼
Command Handler
      │
      ├── /start
      ├── /status
      └── /ping
      │
      ▼
Telegram Bot API
      │
      ▼
Telegram User
```

Untuk saat ini alur yang sudah berjalan hanya:

```text id="imx0v6"
Aplikasi / Server
       │
       │ tele.send(...)
       ▼
Telegram Bot API
       │
       ▼
Telegram User
```

## ✨ Fitur

* 📤 Mengirim notifikasi ke Telegram
* ⚡ REST API menggunakan FastAPI
* 🔐 Konfigurasi melalui `.env`
* 🤖 Terhubung langsung ke Telegram Bot API
* 📨 Mendukung custom `chat_id`
* 🩺 Health check sederhana
* 📥 Membaca update Telegram untuk development
* 🪝 Struktur disiapkan untuk pengembangan webhook
* 🧩 Dependency minimal
