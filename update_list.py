import requests
import os
import re
from concurrent.futures import ThreadPoolExecutor

# Bu kelimeleri içeren linkler TEST EDİLMEDEN kabul edilir
DOKUNULMAZLAR = ["workers.dev", "cdn-vizi", "viziTV"]

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
    url_clean = url.lower()
    
    # VIP Kontrol: Dokunulmazları direkt geçir
    if any(ozel in url_clean for ozel in DOKUNULMAZLAR):
        return (info, url)

    # Normal Test
    try:
        r = requests.get(url, timeout=5, stream=True, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            # İlk 128 byte'ı alabiliyorsak yayın canlıdır
            content = next(r.iter_content(chunk_size=128), None)
            r.close()
            if content: return (info, url)
    except: pass
    return None

def update_m3u():
    aday_listesi = []
    eklenen_linkler = set()

    # Mevcut dosyayı oku
    if os.path.exists("tr.m3u"):
        with open("tr.m3u", "r", encoding="utf-8") as f:
            matches = re.findall(r"(#EXTINF:.*)\n(http.*)", f.read())
            aday_listesi.extend(matches)

    # Dış kaynakları tara
    for s_url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(s_url, timeout=10)
            if r.status_code == 200:
                matches = re.findall(r"(#EXTINF:.*)\n(http.*)", r.text)
                aday_listesi.extend(matches)
        except: continue

    # Testleri yap (15 kanalda bir aynı anda)
    with ThreadPoolExecutor(max_workers=15) as executor:
        results = list(executor.map(link_test_et, aday_listesi))
        
    temiz_kanallar = []
    for res in results:
        if res and res[1] not in eklenen_linkler:
            temiz_kanallar.append(res)
            eklenen_linkler.add(res[1])

    # Dosyaya yaz
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for info, url in temiz_kanallar:
            f.write(f"{info}\n{url}\n")

if __name__ == "__main__":
    update_m3u()
