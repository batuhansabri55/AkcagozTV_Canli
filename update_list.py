import requests
import os

YEDEK_KAYNAKLAR = [
    "https://raw.githubusercontent.com/sultansmgr/smart/refs/heads/main/viziTV.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://streams.uzunmuhalefet.com/lists/tr.m3u"
]

def link_test_et(url):
    """Linkin gerçekten çalışıp çalışmadığını hızlıca kontrol eder."""
    try:
        # 3 saniye içinde cevap vermezse veya hata verirse 'False' döner
        r = requests.head(url, timeout=3, allow_redirects=True)
        return r.status_code < 400
    except:
        return False

def update_m3u():
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # 1. Mevcut manuel linklerini oku (Bunları test etmiyoruz, senin linklerin kutsaldır)
    manuel_icerik = ""
    if os.path.exists("tr.m3u"):
        with open("tr.m3u", "r", encoding="utf-8") as f:
            manuel_icerik = f.read()

    added_links = set()
    for line in manuel_icerik.splitlines():
        if line.startswith("http"): added_links.add(line.strip())

    # 2. Online yedekleri tara ve ÇALIŞANLARI ayıkla
    yeni_linkler = "\n# --- OTOMATİK TEMİZ YEDEKLER --- #\n"
    for url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                lines = r.text.splitlines()
                info = ""
                for l in lines:
                    if l.startswith("#EXTINF"): info = l
                    elif l.startswith("http") and info:
                        link = l.strip()
                        # DAHA ÖNCE EKLENMEMİŞSE VE ÇALIŞIYORSA EKLE
                        if link not in added_links:
                            if link_test_et(link):
                                yeni_linkler += f"{info}\n{link}\n"
                                added_links.add(link)
                        info = ""
        except: continue

    # 3. Tertemiz dosyayı oluştur
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(manuel_icerik.strip() + "\n" + yeni_linkler)

if __name__ == "__main__":
    update_m3u()
