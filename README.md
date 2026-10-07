# PyWebClone - Advanced Dynamic Web Mirroring & OSINT Forensic Tool

PyWebClone; sızma testleri (penetrasyon testleri), siber tehdit istihbaratı (OSINT) ve adli bilişim (forensic) süreçlerinde hedef web sitelerinin statik mimarilerini, tüm varlıkları (assets) ve dinamik içerikleriyle birlikte çevrimdışı (offline) ortamlarda analiz etmek amacıyla geliştirilmiş **üst düzey bir web kopyalama ve otomasyon aracıdır**.

Sıradan kopyalayıcıların aksine; modern JavaScript framework'leri (React, Vue, Next.js vb.) ile yazılmış dinamik web sitelerini tam uyumlu şekilde simüle eder ve güvenli bir şekilde yerel ortama aktarır.

## 🚀 Öne Çıkan Gelişmiş Özellikler

* **🧠 Dinamik İçerik & JavaScript Desteği (Playwright):** Arka planda Headless Chrome (Gizli Tarayıcı) açarak sayfadaki tüm JavaScript döngülerinin tamamlanmasını ve API isteklerinin (networkidle) yüklenmesini bekler. Modern SPA (Single Page Application) siteleri kusursuzca klonlar.
* **⚡ Süper Hızlı Eşzamanlı İndirme (Concurrency):** `ThreadPoolExecutor` mimarisi kullanarak tüm asset dosyalarını paralel olarak 10 koldan indirir. Zaman yönetimini optimize ederek indirme sürelerini %90 oranında kısaltır.
* **🔗 Akıllı URL Dönüşümü (Local URL Rewriting):** İndirilen tüm varlıkların (`src`, `href`) bağlamlarını yerel dosya yollarına haritalandırır. Klonlanan web sitesi, internet bağlantısı tamamen kesik olsa bile (offline) lokalde kusursuz çalışır.
* **📸 Gelişmiş Medya & Lazy-Load Desteği:** Tembel yükleme (`data-src`, `data-lazy-src`) ve responsive görsel senaryolarını (`srcset`) parse ederek, ekrana kaydırılmadan yüklenmeyen gizli medyaları bile tespit edip indirir.
* **🛡️ Güvenli Dosya Adı Yönetimi (Path Traversal Protection):** URL parametrelerini ve geçersiz karakterleri Regex (Düzenli İfadeler) ile temizler. Windows/Linux dosya sistemlerinde "Geçersiz dosya adı" hatalarını önler ve Directory Traversal (Dizin Geçişi) zafiyetlerine karşı güvenli mimari sağlar.
* **📦 Tekilleştirme (Deduplication):** Mükerrer dosyaları hafızasında analiz ederek mükemmel optimizasyon sağlar. Aynı CSS veya görsel kaynak kodda yüzlerce kez geçse bile diske yalnızca 1 kez indirilir.
* **🕵️‍♂️ Anti-Bot & Tarayıcı Kimliği (Stealth Headers):** `requests.Session()` üzerinden gerçekçi `User-Agent`, `Accept-Language` ve `Referer` başlıkları enjekte ederek Cloudflare veya basit Web Uygulaması Güvenlik Duvarı (WAF) engellemelerini bypass eder.
* **🛠️ Endüstriyel Hata Yönetimi & Loglama:** Yerleşik `logging` modülü kullanır. 404 (Bulunamadı) veya Timeout (Zaman Aşımı) hatalarında sistemin çökmesini (crash) engelleyerek asenkron akışı bozmadan çalışmaya devam eder.
* **📂 Otomatik Klasör Hiyerarşisi:** İndirilen verileri yapılandırılmış bir düzende saklar: `assets/css`, `assets/js`, `assets/images`, `assets/fonts`.
* **✍️ Otomatik İmza Enjeksiyonu (Signature Injection):** Klonlanan DOM yapısının en altına (`</body>` öncesi) CSS tabanlı, buzlu cam efektli (`backdrop-filter`) ve hover animasyonlu özel bir geliştirici imzası enjekte eder.

## 🛠️ Teknik Gereksinimler & Bağımlılıklar

Projenin kararlı çalışması için aşağıdaki Python kütüphaneleri kullanılmaktadır:
* **Playwright** (Dinamik DOM rendering için)
* **BeautifulSoup4** (HTML parsing süreçleri için)
* **Requests** (Senkron asset transferleri için)

### Kurulum

1. Depoyu klonlayın:
```bash
git clone https://github.com
cd PyWebClone
```

2. Gerekli kütüphaneleri ve Playwright tarayıcı çekirdeklerini yükleyin:
```bash
pip install -r requirements.txt
playwright install
```

### Kullanım

Aracı terminal üzerinden başlatın ve hedef URL'yi girin:
```bash
python main.py
```

## ⚠️ Yasal Uyarı / Disclaimer

**TR:** Bu yazılım tamamen eğitim, yerel yedekleme, OSINT analizleri ve yasal sızma testleri süreçlerinde statik kaynak kod incelemesi yapmak amacıyla geliştirilmiştir. Bu aracın izinsiz veya telif hakkı içeren web siteleri üzerinde kötü amaçlı kullanımı tamamen kullanıcının sorumluluğundadır. Geliştirici (Mücahid Balcı), oluşabilecek yasal sorunlardan veya kötüye kullanımlardan dolayı hiçbir sorumluluk kabul etmez.

**EN:** This software is developed strictly for educational purposes, local backups, OSINT forensics, and legal penetration testing to perform static source code analysis. Any unauthorized or malicious use of this tool on copyrighted or unauthorized websites is entirely the responsibility of the user. The developer (Mücahid Balcı) assumes no liability and is not responsible for any misuse or damage caused by this program.

## 👤 Geliştirici / Developer

* **Mücahid Balcı** - *Genç Girişimci & Siber Güvenlik Araştırmacısı*
* **GitHub:** [@mucahhtd](https://github.com)
* **Web Sitesi:** [mucahidinc.freedev.app](https://freedev.app)
