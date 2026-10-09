import os
import re
import sys
import signal
import logging
import requests
from typing import Optional, List, Tuple, Set
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
from concurrent.futures import ThreadPoolExecutor, as_completed
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

logging.basicConfig(level=logging.INFO, format='%(levelname)-8s | %(message)s')


class UltraProfesyonelKlonlayici:
    def __init__(self, url: str):
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
        self._setup_signals()

    def _setup_signals(self) -> None:
        signal.signal(signal.SIGINT, self._graceful_exit)
        signal.signal(signal.SIGTERM, self._graceful_exit)

    def _graceful_exit(self, signum: int, frame) -> None:
        logging.warning("\nİşlem kullanıcı tarafından iptal edildi. Temizleniyor...")
        sys.exit(0)

    def klasor_hazirla(self) -> None:
        dirs = [
            os.path.join(self.base_dir, 'assets', 'css'),
            os.path.join(self.base_dir, 'assets', 'js'),
            os.path.join(self.base_dir, 'assets', 'images'),
            os.path.join(self.base_dir, 'assets', 'fonts'),
            os.path.join(self.base_dir, 'assets', 'icons'),
            os.path.join(self.base_dir, 'assets', 'media'),
            os.path.join(self.base_dir, 'assets', 'external')
        ]
        for d in dirs:
            os.makedirs(d, exist_ok=True)
        logging.info(f"Klasör: '{self.base_dir}'")

    def guvenli_dosya_adi(self, url: str) -> str:
        parsed = urlparse(url)
        path = unquote(parsed.path)
        name = os.path.basename(path)
        if not name or '.' not in name:
            name = f"dosya_{abs(hash(url)) % 10000}.tmp"
        name = re.sub(r'[^\w\-_\.]', '_', name)
        return name[:50]

    def _get_asset_path(self, asset_url: str, asset_type: str) -> Tuple[str, str]:
        parsed = urlparse(asset_url)
        is_external = parsed.netloc and parsed.netloc not in [self.domain, '']

        filename = self.guvenli_dosya_adi(asset_url)
        if is_external:
            safe_domain = parsed.netloc.replace('.', '_')
            filename = f"{safe_domain}_{filename}"
            base_path = os.path.join(self.base_dir, 'assets', 'external', filename)
        elif asset_type == 'css':
            base_path = os.path.join(self.base_dir, 'assets', 'css', filename)
        elif asset_type == 'js':
            base_path = os.path.join(self.base_dir, 'assets', 'js', filename)
        elif asset_type == 'img':
            base_path = os.path.join(self.base_dir, 'assets', 'images', filename)
        elif asset_type == 'icon':
            base_path = os.path.join(self.base_dir, 'assets', 'icons', filename)
        elif asset_type in ['video', 'audio']:
            base_path = os.path.join(self.base_dir, 'assets', 'media', filename)
        else:
            base_path = os.path.join(self.base_dir, 'assets', filename)

        rel_path = os.path.relpath(base_path, self.base_dir).replace('\\', '/')
        return base_path, rel_path

    def _rewrite_css_urls(self, css_content: str, base_url: str) -> str:
        pattern = r'url\(\s*[\'"]?([^\'")]+)[\'"]?\s*\)'

        def replacer(match: re.Match) -> str:
            asset_url = match.group(1)
            if asset_url.startswith('data:'):
                return match.group(0)

            full_url = urljoin(base_url, asset_url)
            _, rel_path = self._get_asset_path(full_url, 'font' if any(
                ext in asset_url for ext in ['.woff', '.ttf', '.eot', '.otf']) else 'img')

            try:
                resp = self.session.get(full_url, timeout=10)
                resp.raise_for_status()
                abs_path = os.path.join(self.base_dir, rel_path)
                os.makedirs(os.path.dirname(abs_path), exist_ok=True)
                with open(abs_path, 'wb') as f:
                    f.write(resp.content)

                css_dir = os.path.join(self.base_dir, 'assets', 'css')
                final_rel = os.path.relpath(abs_path, css_dir).replace('\\', '/')
                return f'url("{final_rel}")'
            except Exception:
                return match.group(0)

        return re.sub(pattern, replacer, css_content)

    def varlik_indir(self, asset_url: str, asset_type: str) -> Optional[str]:
        try:
            response = self.session.get(asset_url, timeout=10)
            if response.status_code == 404:
                return None
            response.raise_for_status()

            abs_path, rel_path = self._get_asset_path(asset_url, asset_type)

            if asset_type == 'css':
                processed_css = self._rewrite_css_urls(response.text, asset_url)
                with open(abs_path, 'w', encoding='utf-8') as f:
                    f.write(processed_css)
            else:
                with open(abs_path, 'wb') as f:
                    f.write(response.content)

            return rel_path
        except Exception:
            return None

    def baslat(self) -> None:
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
        except (PlaywrightTimeout, Exception) as e:
            logging.warning(f"Playwright başarısız, temel mod ile devam ediliyor. ({e})")
            try:
                rendered_html = self.session.get(self.url, timeout=15).text
            except Exception as req_err:
                logging.error(f"Sayfa alınamadı: {req_err}")
                return

        soup = BeautifulSoup(rendered_html, 'html.parser')
        islemler: List[Tuple[str, str, any, str]] = []

        for link in soup.find_all('link', rel='stylesheet'):
            if link.get('href'): islemler.append((urljoin(self.url, link['href']), 'css', link, 'href'))

        for script in soup.find_all('script', src=True):
            islemler.append((urljoin(self.url, script['src']), 'js', script, 'src'))

        for img in soup.find_all('img'):
            src = img.get('data-src') or img.get('data-lazy-src') or img.get('src')
            if src: islemler.append((urljoin(self.url, src), 'img', img, 'src'))
            if img.get('srcset'):
                for item in img['srcset'].split(','):
                    src_url = item.strip().split(' ')[0]
                    if src_url: islemler.append((urljoin(self.url, src_url), 'img', img, 'srcset'))

        for media in soup.find_all(['video', 'audio']):
            if media.get('src'): islemler.append((urljoin(self.url, media['src']), media.name, media, 'src'))

        for icon in soup.find_all('link', rel=lambda x: x and any(i in x for i in ['icon', 'shortcut', 'apple'])):
            if icon.get('href'): islemler.append((urljoin(self.url, icon['href']), 'icon', icon, 'href'))

        for meta in soup.find_all('meta', property='og:image'):
            if meta.get('content'): islemler.append((urljoin(self.url, meta['content']), 'img', meta, 'content'))

        benzersiz_islemler = []
        seen: Set[str] = set()
        for item in islemler:
            if item[0] not in seen:
                seen.add(item[0])
                benzersiz_islemler.append(item)

        logging.info(f"İndirilecek: {len(benzersiz_islemler)} benzersiz varlık")

        basarili = 0
        with ThreadPoolExecutor(max_workers=12) as executor:
            futures = {
                executor.submit(self.varlik_indir, url, tip): (tag, attr)
                for url, tip, tag, attr in benzersiz_islemler
            }
            for future in as_completed(futures):
                tag, attr = futures[future]
                try:
                    yerel_yol = future.result()
                    if yerel_yol and attr != 'srcset':
                        tag[attr] = yerel_yol
                        basarili += 1
                except Exception:
                    pass

        logging.info(f"Tamamlandı: {basarili} varlık")

        imza_html = """
        <footer style="position: fixed; bottom: 0; width: 100%; background: rgba(0,0,0,0.9); color: #00ff00; text-align: center; padding: 12px 0; font-family: 'Courier New', monospace; font-size: 13px; border-top: 2px solid #00ff00; z-index: 99999; backdrop-filter: blur(5px); box-shadow: 0 -4px 10px rgba(0,0,0,0.5);">
            Powered by <strong>mucahidbalci</strong> | 
            <a href="https://mucahidbalci.github.io" style="color: #00ffff; text-decoration: none; font-weight: bold; transition: all 0.3s ease;" onmouseover="this.style.color='#ffffff'; this.style.textShadow='0 0 8px #00ffff'" onmouseout="this.style.color='#00ffff'; this.style.textShadow='none'">mucahidbalci.github.io</a>
        </footer>
        <style>body { padding-bottom: 60px !important; margin-bottom: 0 !important; }</style>
        """

        target = soup.body if soup.body else soup.html
        target.append(BeautifulSoup(imza_html, 'html.parser'))

        html_yolu = os.path.join(self.base_dir, 'index.html')
        with open(html_yolu, 'w', encoding='utf-8') as f:
            f.write(str(soup))

        logging.info(f"Bitti: '{self.base_dir}' klasöründe.")


if __name__ == "__main__":
    print("\nUYARI: Sadece eğitim, arşivleme ve izinli test amaçlıdır.\n")
    hedef_url = input("Hedef siteyi girin: ").strip()

    if not hedef_url:
        logging.error("URL boş olamaz!")
    else:
        klonlayici = UltraProfesyonelKlonlayici(hedef_url)
        klonlayici.baslat()
