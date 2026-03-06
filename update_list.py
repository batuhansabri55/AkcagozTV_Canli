import requests
import os
import re

YEDEK_KAYNAKLAR = [
    "https://raw.githubusercontent.com/sultansmgr/smart/refs/heads/main/viziTV.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://streams.uzunmuhalefet.com/lists/tr.m3u"
]

def link_test_et(url):
    """Link aktif mi kontrol eder (Timeout 3 saniye)"""
    try:
        # Bazı sunucular HEAD isteğine 403/405 verebilir, o yüzden GET ile 1 byte deniyoruz
        r = requests.get(url, timeout=3, stream=True, headers={"User-Agent": "Mozilla/5.0"})
        r.close()
        return r.status_code < 400
    except:
        return False

def update_m3u():
    temiz_kanallar = [] # (info, url) şeklinde tutulacak
    eklenen_linkler = set()

    # 1. MEVCUT DOSYADAKİ HER ŞEYİ KONTROL ET
    if os.path.exists("tr.m3u"):
        with open("tr.m3u", "r", encoding="utf-8") as f:
            content = f.read()
            # EXTINF ve URL çiftlerini regex ile yakala
            matches = re.findall(r"(#EXTINF:.*)\n(http.*)", content)
            for info, url in matches:
                url = url.strip()
                if link_test_et(url):
                    temiz_kanallar.append((info, url))
                    eklenen_linkler.add(url)

    # 2. DIŞ KAYNAKLARI TARA VE SADECE ÇALIŞANLARI EKLE
    for s_url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(s_url, timeout=10)
            if r.status_code == 200:
                matches = re.findall(r"(#EXTINF:.*)\n(http.*)", r.text)
                for info, url in matches:
                    url = url.strip()
                    if url not in eklenen_linkler and link_test_et(url):
                        temiz_kanallar.append((info, url))
                        eklenen_linkler.add(url)
        except: continue

    # 3. DOSYAYI SIFIRDAN YAZ (SADECE AKTİFLER)
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for info, url in temiz_kanallar:
            f.write(f"{info}\n{url}\n")

if __name__ == "__main__":
    update_m3u()
