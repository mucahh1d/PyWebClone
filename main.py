import os
import re
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
from concurrent.futures import ThreadPoolExecutor, as_completed
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format='%(levelname)-8s | %(message)s')

class UltraProfesyonelKlonlayici:
    def __init__(self, url):
        self.url = url if url.startswith('http') else 'http://' + url
        self.domain = urlparse(self.url).netloc.replace('www.', '')
        self.base_dir = f"klon_{self.domain}"

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': self.url
        })

    def klasor_hazirla(self):
        dirs = [
            os.path.join(self.base_dir, 'assets', 'css'),
            os.path.join(self.base_dir, 'assets', 'js'),
            os.path.join(self.base_dir, 'assets', 'images'),
            os.path.join(self.base_dir, 'assets', 'fonts'),
            os.path.join(self.base_dir, 'assets', 'icons')
        ]
        for d in dirs:
            os.makedirs(d, exist_ok=True)
        logging.info(f"Klasör: '{self.base_dir}'")

    def guvenli_dosya_adi(self, url):
        parsed = urlparse(url)
        path = unquote(parsed.path)
        name = os.path.basename(path)
        if not name or '.' not in name:
            name = f"dosya_{abs(hash(url)) % 10000}.tmp"
        name = re.sub(r'[^\w\-_\.]', '_', name)
        return name[:50]

    def varlik_indir(self, asset_url, asset_type):
        try:
            response = self.session.get(asset_url, timeout=10)
            if response.status_code == 404:
                return None
            response.raise_for_status()

            filename = self.guvenli_dosya_adi(asset_url)

            if asset_type == 'css':
                path = os.path.join(self.base_dir, 'assets', 'css', filename)
            elif asset_type == 'js':
                path = os.path.join(self.base_dir, 'assets', 'js', filename)
            elif asset_type == 'img':
                path = os.path.join(self.base_dir, 'assets', 'images', filename)
            elif asset_type == 'icon':
                path = os.path.join(self.base_dir, 'assets', 'icons', filename)
            else:
                path = os.path.join(self.base_dir, 'assets', filename)

            with open(path, 'wb') as f:
                f.write(response.content)

            return os.path.relpath(path, self.base_dir).replace('\\', '/')
        except Exception:
            return None

    def baslat(self):
        logging.info(f"Hedef: {self.url}")
        self.klasor_hazirla()

        rendered_html = ""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(self.url, wait_until='networkidle', timeout=30000)
                rendered_html = page.content()
                browser.close()
        except Exception as e:
            logging.error(f"Hata: {e}")
            return

        soup = BeautifulSoup(rendered_html, 'html.parser')
        islemler = []

        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href: islemler.append((urljoin(self.url, href), 'css', link, 'href'))

        for script in soup.find_all('script', src=True):
            src = script.get('src')
            if src: islemler.append((urljoin(self.url, src), 'js', script, 'src'))

        for img in soup.find_all('img'):
            src = img.get('data-src') or img.get('data-lazy-src') or img.get('src')
            if src:
                islemler.append((urljoin(self.url, src), 'img', img, 'src'))

            srcset = img.get('srcset')
            if srcset:
                for srcset_item in srcset.split(','):
                    srcset_url = srcset_item.strip().split(' ')[0]
                    if srcset_url:
                        islemler.append((urljoin(self.url, srcset_url), 'img', img, 'srcset'))

        for icon in soup.find_all('link', rel=lambda x: x in ['icon', 'shortcut icon', 'apple-touch-icon'] if x else False):
            href = icon.get('href')
            if href: islemler.append((urljoin(self.url, href), 'icon', icon, 'href'))

        benzersiz_islemler = []
        seen_urls = set()
        for item in islemler:
            if item[0] not in seen_urls:
                seen_urls.add(item[0])
                benzersiz_islemler.append(item)

        logging.info(f"İndirilecek: {len(benzersiz_islemler)} varlık")

        basarili_sayisi = 0
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_tag = {
                executor.submit(self.varlik_indir, url, tip): (tag, attr)
                for url, tip, tag, attr in benzersiz_islemler
            }

            for future in as_completed(future_to_tag):
                tag, attr = future_to_tag[future]
                try:
                    yerel_yol = future.result()
                    if yerel_yol:
                        if attr != 'srcset':
                            tag[attr] = yerel_yol
                        basarili_sayisi += 1
                except Exception:
                    pass

        logging.info(f"Tamamlandı: {basarili_sayisi} varlık")

        imza_html = """
        <footer style="position: fixed; bottom: 0; width: 100%; background: rgba(0,0,0,0.85); color: #00ff00; text-align: center; padding: 12px 0; font-family: 'Courier New', monospace; font-size: 14px; border-top: 2px solid #00ff00; z-index: 99999; backdrop-filter: blur(4px);">
            Designed by <strong>mucahidbalci</strong> | 
            <a href="https://mucahidinc.freedev.app" style="color: #00ffff; text-decoration: none; font-weight: bold; transition: color 0.3s;" onmouseover="this.style.color='#ffffff'" onmouseout="this.style.color='#00ffff'">mucahidinc.freedev.app</a>
        </footer>
        <style>body { padding-bottom: 60px !important; margin-bottom: 0 !important; }</style>
        """

        if soup.body:
            soup.body.append(BeautifulSoup(imza_html, 'html.parser'))
        else:
            soup.html.append(BeautifulSoup(imza_html, 'html.parser'))

        html_yolu = os.path.join(self.base_dir, 'index.html')
        with open(html_yolu, 'w', encoding='utf-8') as f:
            f.write(str(soup))

        logging.info(f"Bitti: '{self.base_dir}' klasöründe.")


if __name__ == "__main__":
    print("\nUYARI: Sadece eğitim ve izinli test amaçlıdır.\n")
    hedef_url = input("Hedef siteyi girin: ").strip()

    if not hedef_url:
        logging.error("URL boş olamaz!")
    else:
        klonlayici = UltraProfesyonelKlonlayici(hedef_url)
        klonlayici.baslat()
