# 📡 LocalDrop — Wireless File Transfer

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-4682B4?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Privacy](https://img.shields.io/badge/Privacy-100%25%20Offline-brightgreen?style=for-the-badge)

**Seamless, lightning-fast wireless file transfer between your iPhone and PC.**  
*No internet required • No cables • Zero apps to install on iPhone*

</div>

---

## ⚡ Overview

**LocalDrop** brings an AirDrop-like experience to Windows, Linux, and macOS setups. By hosting an ultra-lightweight, embedded web server on your computer, LocalDrop lets you transfer photos, videos, documents, and files directly over your local Wi-Fi network in seconds.

Everything stays strictly inside your local home network — no third-party cloud servers, no bandwidth throttling, and complete privacy.

---

## ✨ Key Features

- **📱 Zero App Installation:** Operates directly inside Safari or any mobile browser on iOS.
- **⚡ Maximum Local Speed:** Transfers files at native Wi-Fi speeds without cloud bottlenecking.
- **🔒 100% Private & Offline:** Data never leaves your local area network (LAN).
- **🔄 Two-Way Transfer:**
  - **iPhone ➔ PC:** Tap to send photos, videos, or files directly to `~/LocalDrop_Received/`.
  - **PC ➔ iPhone:** Place files in `~/LocalDrop_Share/` and download them with a single tap.
- **📷 Terminal QR Code:** Scan the automatically generated terminal QR code with your iPhone camera to instantly connect.
- **📦 Zero Heavy Dependencies:** Built on Python's native standard library with a sleek, responsive dark-mode UI embedded.

---

## 📋 Requirements

- **Python 3.8** or newer (standard on most systems or available at [python.org](https://python.org))
- Both **PC and iPhone connected to the SAME Wi-Fi network**
- *(Optional)* `qrcode` package for terminal QR visualization:
  ```bash
  pip install qrcode
  ```

---

## 🚀 Quick Start

### 1. Start the Server

- **Windows:** Double-click `start_localdrop.bat`
- **Terminal (Windows / macOS / Linux):**
  ```bash
  python3 server.py
  ```

### 2. Connect Your iPhone

1. A URL like `http://192.168.x.x:8765` will display in your terminal.
2. **Scan the QR code** in your terminal using your iPhone's camera app *(or manually type the URL into Safari)*.

### 3. Transfer Files

| Transfer Mode | iPhone Steps | File Destination on PC |
| :--- | :--- | :--- |
| **📤 iPhone ➔ PC** | Tap **"Send to PC"** tab, pick files/photos | Saved to `~/LocalDrop_Received/` |
| **📥 PC ➔ iPhone** | Copy files into `~/LocalDrop_Share/`, tap **"Get from PC"** on phone, then tap **Save** | Downloaded to iPhone Safari Downloads |

---

## 🛠️ Troubleshooting

<details>
<summary><b>❓ "iPhone can't connect to the server"</b></summary>

- Verify that PC and iPhone are connected to the **exact same Wi-Fi network**.
- Windows Users: Allow Python through **Windows Defender Firewall** when prompted.
- Ensure AP/Client Isolation is disabled on your Wi-Fi router if applicable.
</details>

<details>
<summary><b>❓ "Port already in use"</b></summary>

Open `server.py` in any text editor and change `PORT = 8765` to a different number (e.g., `8766` or `9000`).
</details>

<details>
<summary><b>❓ "Photos not showing in iPhone Photo Library after downloading"</b></summary>

In Safari on iOS:
1. Tap the downloaded file in Safari's download manager.
2. Tap the **Share** button (box with upward arrow).
3. Select **Save Image** or **Save Video** to move it to your camera roll.
</details>

---

## 🛑 Stopping the Server

Press `Ctrl + C` in the terminal window to shut down the server safely.

---

## 📜 License

This project is licensed under the MIT License — see the repository for details.
