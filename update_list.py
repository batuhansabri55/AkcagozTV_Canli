import requests
import os
import re
from concurrent.futures import ThreadPoolExecutor

# --- LOGO AYARLARI (SENİN DEPO) ---
# Yüklediğin klasör yapısına göre tam yol budur:
MY_LOGO_BASE = "https://raw.githubusercontent.com/batuhansabri55/AkcagozTV_Canli/main/logos/logos/"

# Kanal adı ile yüklediğin dosya adını eşleştiriyoruz
LOGO_MAP = {
    "atv": "atv.png",
    "trt 1": "trt1.png"
}

def fix_logo(info_line):
    name_match = re.search(r",(.+)$", info_line)
    if name_match:
        ch_name = name_match.group(1).lower()
        for key, filename in LOGO_MAP.items():
            if key in ch_name:
                new_logo_url = MY_LOGO_BASE + filename
                if 'tvg-logo="' in info_line:
                    return re.sub(r'tvg-logo="[^"]*"', f'tvg-logo="{new_logo_url}"', info_line)
                else:
                    return info_line.replace("#EXTINF:-1", f'#EXTINF:-1 tvg-logo="{new_logo_url}"')
    return info_line

# --- LİSTE GÜNCELLEME MOTORU ---
DOKUNULMAZLAR = ["premiumstream.in", "workers.dev", "cdn-vizi", "viziTV"]

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
    if any(ozel in url_clean for ozel in DOKUNULMAZLAR):
        return (fix_logo(info), url)

    try:
        r = requests.get(url, timeout=5, stream=True, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            content = next(r.iter_content(chunk_size=128), None)
            r.close()
            if content: return (fix_logo(info), url)
    except: pass
    return None

def update_m3u():
    aday_listesi = []
    korunanlar = []
    eklenen_linkler = set()

    if os.path.exists("tr.m3u"):
        with open("tr.m3u", "r", encoding="utf-8") as f:
            matches = re.findall(r"(#EXTINF:.*)\n(http.*)", f.read())
            for info, url in matches:
                if any(ozel in url.lower() for ozel in DOKUNULMAZLAR):
                    korunanlar.append((fix_logo(info), url))
                    eklenen_linkler.add(url)
                else:
                    aday_listesi.append((info, url))

    for s_url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(s_url, timeout=10)
            if r.status_code == 200:
                matches = re.findall(r"(#EXTINF:.*)\n(http.*)", r.text)
                aday_listesi.extend(matches)
        except: continue

    with ThreadPoolExecutor(max_workers=15) as executor:
        results = list(executor.map(link_test_et, aday_listesi))
        
    temiz_kanallar = korunanlar
    for res in results:
        if res and res[1] not in eklenen_linkler:
            temiz_kanallar.append(res)
            eklenen_linkler.add(res[1])

    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for info, url in temiz_kanallar:
            f.write(f"{info}\n{url}\n")

if __name__ == "__main__":
    update_m3u()
