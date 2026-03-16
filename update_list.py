import requests
import os
import re
from concurrent.futures import ThreadPoolExecutor

# SADECE BU İKİSİ TEST EDİLMEDEN KABUL EDİLİR VE SİLİNMEZ
DOKUNULMAZLAR = ["premiumstream.in", "workers.dev"]

YEDEK_KAYNAKLAR = [
    "https://mth.tc/DsGo",
    "https://raw.githubusercontent.com/sultansmgr/smart/refs/heads/main/viziTV.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://streams.uzunmuhalefet.com/lists/tr.m3u"
]

def link_test_et(item):
    info, url = item
    url_clean = url.lower().strip()
    
    # Dokunulmaz olanları test etmeden direkt geçir
    if any(ozel in url_clean for ozel in DOKUNULMAZLAR):
        return (info, url)

    try:
        # viziTV ve diğerleri artık burada test edilecek
        with requests.get(url, timeout=5, stream=True, headers={"User-Agent": "Mozilla/5.0"}) as r:
            if r.status_code == 200:
                # Bağlantı kurulabiliyorsa kanalı kabul et
                return (info, url)
    except:
        pass
    return None

def update_m3u():
    adaylar = []
    eklenen_linkler = set()
    icerik_havuzu = ""

    # 1. Mevcut dosyadaki verileri oku
    if os.path.exists("tr.m3u"):
        with open("tr.m3u", "r", encoding="utf-8") as f:
            icerik_havuzu += f.read() + "\n"

    # 2. Dış kaynaklardaki verileri topla
    for s_url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(s_url, timeout=10)
            if r.status_code == 200:
                icerik_havuzu += r.text + "\n"
        except:
            continue

    # 3. Regex ile ayıkla ve TEKİLLEŞTİR (Aynı linkten 1 tane kalacak şekilde)
    # Satır sonu karakterlerini temizleyip eşleştirme yapıyoruz
    matches = re.findall(r"(#EXTINF:[^\n]*)\n(http[^\n]*)", icerik_havuzu.replace('\r', ''))
    
    for info, url in matches:
        url_strip = url.strip()
        if url_strip not in eklenen_linkler:
            adaylar.append((info, url_strip))
            eklenen_linkler.add(url_strip)

    # 4. Kanalları test et (Hızlı sonuç için 25 kanal aynı anda)
    print(f"Toplam {len(adaylar)} benzersiz kanal işleniyor...")
    with ThreadPoolExecutor(max_workers=25) as executor:
        sonuclar = list(filter(None, executor.map(link_test_et, adaylar)))

    # 5. Dosyayı SIFIRDAN yaz (Bu işlem eski ve bozuk verileri temizler)
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for info, url in sonuclar:
            f.write(f"{info}\n{url}\n")
    
    print(f"Bitti! {len(sonuclar)} aktif kanal 'tr.m3u' dosyasına kaydedildi.")

if __name__ == "__main__":
    update_m3u()
