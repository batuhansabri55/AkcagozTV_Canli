import requests
import os
import re
from concurrent.futures import ThreadPoolExecutor

# SADECE BU İKİSİ TEST EDİLMEZ VE SİLİNMEZ
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
    
    if any(ozel in url_clean for ozel in DOKUNULMAZLAR):
        return (info, url)

    try:
        # Stream=True ve context manager ile hızlı ve güvenli test
        with requests.get(url, timeout=5, stream=True, headers={"User-Agent": "Mozilla/5.0"}) as r:
            if r.status_code == 200:
                return (info, url)
    except:
        pass
    return None

def update_m3u():
    eklenen_linkler = set()
    havuz = []
    tum_metin = ""

    # 1. Eski dosyayı ve uzak kaynakları tek bir metinde topla
    if os.path.exists("tr.m3u"):
        with open("tr.m3u", "r", encoding="utf-8") as f:
            tum_metin += f.read() + "\n"

    for s_url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(s_url, timeout=10)
            if r.status_code == 200:
                tum_metin += r.text + "\n"
        except: continue

    # 2. Regex ile ayıkla ve mükerrerleri (tekrar edenleri) sil
    matches = re.findall(r"(#EXTINF:[^\n]*)\n(http[^\n]*)", tum_metin.replace('\r', ''))
    
    for info, url in matches:
        url_strip = url.strip()
        if url_strip not in eklenen_linkler:
            havuz.append((info, url_strip))
            eklenen_linkler.add(url_strip)

    # 3. Test aşaması (viziTV dahil her şey burada elenir)
    print(f"Sistem taranıyor: {len(havuz)} benzersiz kanal bulundu...")
    with ThreadPoolExecutor(max_workers=50) as executor:
        final_liste = list(filter(None, executor.map(link_test_et, havuz)))

    # 4. Dosyayı 'w' moduyla SIFIRDAN yaz (Eskiler burada temizlenir)
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for info, url in final_liste:
            f.write(f"{info}\n{url}\n")
    
    print(f"İşlem bitti! 'tr.m3u' artık tertemiz ve {len(final_liste)} kanal aktif.")

if __name__ == "__main__":
    update_m3u()
