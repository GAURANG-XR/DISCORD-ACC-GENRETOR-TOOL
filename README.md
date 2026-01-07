# 🚀 Discord Account Utility Tool

A high-performance, automated tool designed for Discord account management and generation. This tool simplifies the process of creating and verifying accounts for testing or community management purposes.

## ✨ Features

* **⚡ High Speed:** Optimized for rapid processing using asynchronous requests.
* **🛡️ Proxy Support:** Support for HTTP, HTTPS, and SOCKS5 proxies to prevent IP flagging.
* **🧩 Captcha Solving:** Integrated support for popular captcha-solving services (2Captcha, Anti-Captcha).
* **📧 Email Integration:** Support for temporary email services or the "Gmail dot trick."
* **💾 Auto-Save:** Automatically saves tokens, passwords, and emails to a structured `.txt` or `.json` file.
* **🕵️ Undetected:** Uses stealth headers and browser fingerprints to mimic human behavior.

---

## 🛠️ Installation

### Prerequisites

* [Python 3.9+](https://www.python.org/downloads/)
* A stable internet connection (VPN recommended)

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/discord-gen-tool.git
cd discord-gen-tool

```


2. **Install dependencies:**
```bash
pip install -r requirements.txt

```


3. **Configure the tool:**
Rename `config.example.json` to `config.json` and add your API keys:
```json
{
  "captcha_key": "YOUR_API_KEY",
  "use_proxies": true,
  "threads": 5
}

```



---

## 🚀 Usage

Run the main script to start the process:

```bash
python main.py

```

Follow the on-screen prompts to select the number of accounts and the specific modules you wish to run.

---

## ⚠️ Disclaimer

> [!IMPORTANT]
> **Educational Purposes Only.** This tool is created for educational and testing purposes. Using this tool to violate [Discord's Terms of Service](https://discord.com/terms) (such as spamming or automated account creation for malicious intent) may result in your IP being banned or accounts being disabled.
> The developer assumes **no liability** for how this tool is used. Use at your own risk.

---


