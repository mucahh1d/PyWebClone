# 🕷️ PyWebClone Pro

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Playwright-Chromium-2EAD33" alt="Playwright">
  <img src="https://img.shields.io/github/stars/mucahidbalci/PyWebClone?style=social" alt="Stars">
</p>

<h3 align="center">Enterprise-grade web cloning and archiving tool</h3>

<p align="center">
  Renders JavaScript, bypasses bot protection, and downloads complete websites with all assets intact — fully offline.
</p>

<p align="center">
  ⭐ <strong>If this project helps you, please give it a star!</strong> It motivates me to build more.
</p>

---

## 📸 Preview

<p align="center">
  <img width="100%" alt="PyWebClone Demo" src="https://github.com/user-attachments/assets/9d35844e-ea4e-461f-8d61-e80df583e766">
</p>

---

## ✨ Features

### 🌐 Dynamic JavaScript Rendering
Uses **Playwright** to execute JavaScript and wait for `networkidle`, ensuring modern frameworks like **React, Vue, and Next.js** are fully rendered before cloning.

### ⚡ Concurrent Downloads
Utilizes `ThreadPoolExecutor` with **12 workers** to download assets simultaneously, drastically reducing cloning time by up to 90%.

### 🔗 Smart URL Rewriting
Automatically rewrites:
- `src` and `href` attributes
- Internal CSS `url()` references
- `srcset` responsive image declarations

All references are converted to local relative paths for **100% offline functionality**.

### 🖼️ Advanced Media Support
Detects and downloads:
- Lazy-loaded images (`data-src`, `data-lazy-src`)
- Responsive `srcset` images
- Videos and audio files
- Open Graph meta images
- Favicons (icon, shortcut, apple-touch-icon)

### 🛡️ Graceful Fallback
If Playwright is blocked or fails (e.g., WAF detection), the tool **seamlessly falls back** to standard `requests` without crashing.

### 📂 Intelligent Asset Management
Organizes files into structured directories and sanitizes filenames to prevent OS-specific errors:

```text
assets/
├── css/        # All stylesheets (with rewritten URLs)
├── js/         # JavaScript files
├── images/     # PNG, JPG, SVG, WebP, AVIF
├── fonts/      # WOFF, WOFF2, TTF, OTF, EOT
├── icons/      # Favicons and icon sets
├── media/      # Videos and audio
└── external/   # Third-party resources
```

### 🛑 Graceful Shutdown
Safely handles `Ctrl+C` (SIGINT) and SIGTERM interruptions without corrupting files or leaving messy stack traces.

### 🕵️ Anti-Bot Protection
Injects realistic headers (`User-Agent`, `Accept-Language`, `Referer`) to bypass basic WAF and bot protection mechanisms.

### ✍️ Automatic Signature Injection
Injects a custom, glassmorphism-styled developer signature with hover effects into the cloned DOM before the closing `</body>` tag.

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step-by-Step

```bash
# 1. Clone the repository
git clone https://github.com/mucahidbalci/PyWebClone.git

# 2. Navigate to the project directory
cd PyWebClone

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Playwright browser (Chromium)
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

It will automatically create a folder named `klon_example.com` and populate it with a fully functional, offline-ready website.

### 🎯 Example Use Cases

| Scenario | Description |
|----------|-------------|
| 🔍 **OSINT Investigation** | Archive a company's website before it goes down |
| 🛡️ **Penetration Testing** | Clone the app for offline vulnerability analysis |
| 📚 **Web Archiving** | Preserve a website that might disappear |
| 🎓 **Education** | Study real-world website architecture locally |

---

## 📂 Output Structure

After cloning, you'll get a clean, organized folder structure:

```text
klon_target.com/
│
├── index.html              # Main entry point (fully offline)
└── assets/
    ├── css/                # All stylesheets (URLs rewritten)
    ├── js/                 # JavaScript files
    ├── images/             # PNG, JPG, SVG, WebP, AVIF
    ├── fonts/              # WOFF, WOFF2, TTF, OTF, EOT
    ├── icons/              # Favicons and icon sets
    ├── media/              # Videos and audio
    └── external/           # Third-party resources
```

---

## ⚠️ Legal & Ethical Disclaimer

This tool is developed strictly for **educational purposes, personal web archiving, and authorized security testing**.

### 🚫 DO NOT use this tool to:
- Clone websites you do not own or have explicit permission to test
- Violate `robots.txt` or website Terms of Service
- Conduct unauthorized scraping or data harvesting
- Distribute copyrighted content without permission

### ✅ DO use this tool to:
- Archive your own websites for backup
- Perform authorized penetration testing
- Conduct legal OSINT research
- Learn about web technologies and security

> **The developer (Mücahid Balcı) assumes no liability for any misuse or damage caused by this program. Users assume full responsibility for their actions.**

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Core Language** | Python 3.8+ | Main application |
| **Browser Automation** | Playwright (Chromium) | Dynamic JS rendering |
| **HTML Parsing** | BeautifulSoup4 | DOM manipulation |
| **HTTP Requests** | Requests | Asset downloading |
| **Concurrency** | ThreadPoolExecutor | Parallel downloads (12 workers) |
| **URL Handling** | urllib.parse, re (Regex) | URL rewriting and sanitization |

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a **Pull Request**

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 👤 About the Developer

**Mücahid Balcı** — *Young Entrepreneur & Cybersecurity Researcher*

- 🌐 **Portfolio:** [mucahidbalci.github.io](https://mucahidbalci.github.io)
- 💻 **GitHub:** [@mucahidbalci](https://github.com/mucahidbalci)
- 📧 **Contact:** balcimucahid4@gmail.com

### 🚀 My Other Projects

- **[AutoReconX](https://github.com/mucahidbalci/AutoReconX)** — Advanced cybersecurity vulnerability scanner
- **[PyScanPro](https://github.com/mucahidbalci/PyScanPro)** — 150-thread port scanner with modern GUI

---

<p align="center">
  <strong>Built with ❤️ for the cybersecurity community</strong><br>
  <sub>© 2026 Mücahid Balcı. All rights reserved.</sub>
</p>
