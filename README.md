# 🕷️ PyWebClone Pro

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/mucahidbalci/PyWebClone?style=social)](https://github.com/mucahidbalci/PyWebClone)

Enterprise-grade web cloning and archiving tool. Renders JavaScript, bypasses bot protection, and downloads complete websites with all assets intact.

⭐ **If you like this project, please give it a star!**

---

## ✨ Features

- **🌐 Dynamic JS Rendering:** Uses Playwright to execute JavaScript and wait for `networkidle`, ensuring React, Vue, or Next.js sites are fully rendered before cloning.
- **⚡ Concurrent Downloads:** Utilizes `ThreadPoolExecutor` to download up to 12 assets simultaneously, drastically reducing cloning time.
- **🔗 Smart URL Rewriting:** Automatically rewrites `src`, `href`, and even internal CSS `url()` references to point to local relative paths.
- **🖼️ Advanced Media Support:** Detects and downloads Lazy-Loaded images (`data-src`), responsive `srcset` images, videos, audio, and Open Graph meta images.
- **🛡️ Graceful Fallback:** If Playwright is blocked or fails, the tool seamlessly falls back to standard `requests` without crashing.
- **📂 Intelligent Asset Management:** Organizes files into structured directories (`css`, `js`, `images`, `fonts`, `external`) and sanitizes filenames to prevent OS errors.
- **🛑 Graceful Shutdown:** Safely handles `Ctrl+C` interruptions without corrupting files or leaving messy stack traces.

---

## 📦 Installation

```bash
git clone https://github.com/mucahidbalci/PyWebClone.git
cd PyWebClone
pip install -r requirements.txt
playwright install chromium
```

---

## 💻 Usage

Run the script from your terminal:

```bash
python main.py
```

The tool will prompt you for a URL:

```text
UYARI: Sadece eğitim, arşivleme ve izinli test amaçlıdır.

Hedef siteyi girin: https://example.com
```

It will automatically create a folder named `klon_example.com` and populate it with the fully functional, offline-ready website.

---

## 📂 Output Structure

```text
klon_example.com/
│
├── index.html
└── assets/
    ├── css/
    ├── js/
    ├── images/
    ├── fonts/
    ├── icons/
    ├── media/
    └── external/
```

---

## ⚠️ Legal & Ethical Disclaimer

This tool is developed strictly for **educational purposes, personal web archiving, and authorized security testing**.

- Do not use this tool to clone websites you do not own or have explicit permission to test.
- Respect `robots.txt` and website Terms of Service.
- The author is not responsible for any misuse of this software.

---

## 🛠️ Tech Stack

- **Core:** Python 3
- **Browser Automation:** Playwright (Chromium)
- **HTML Parsing:** BeautifulSoup4
- **Networking:** Requests, ThreadPoolExecutor
- **URL Handling:** urllib.parse, re (Regex)

---

> **Powered by [mucahidbalci](https://mucahidbalci.github.io)**
> *Built for performance, reliability, and clean architecture.*
