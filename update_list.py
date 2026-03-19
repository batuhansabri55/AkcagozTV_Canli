import requests
import re
import base64
import os
from concurrent.futures import ThreadPoolExecutor

# --- AYARLAR ---
# GitHub Ayarlarındaki GH_TOKEN ismini kullanır
GITHUB_TOKEN = os.environ.get('GH_TOKEN') 
REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

DOKUNULMAZLAR = ["premiumstream.in", "workers.dev", "mywire.org", "token=DeaTHLesS"]

YEDEK_KAYNAKLAR = [
    "https://mth.tc/DsGo",
    "https://raw.githubusercontent.com/sultansmgr/smart/refs/heads/main/viziTV.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://streams.uzunmuhalefet.com/lists/tr.m3u"
]

def github_yukle(icerik):
    if not GITHUB_TOKEN:
        print("❌ HATA: GH_TOKEN bulunamadı!")
        return
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers)
    sha = r.json().get('sha') if r.status_code == 200 else None
    data = {"message": "Otomatik Guncelleme", "content": base64.b64encode(icerik.encode("utf-8")).decode("utf-8")}
    if sha: data["sha"] = sha
    r = requests.put(url, json=data, headers=headers)
    if r.status_code in [200, 201]: print("✅ GITHUB TAMAM!")
    else: print(f"❌ HATA: {r.text}")

def link_test_et(item):
    info, url = item
    if any(ozel in url.lower() for ozel in DOKUNULMAZLAR): return (info, url)
    try:
        with requests.get(url, timeout=5, stream=True) as r:
            if r.status_code == 200: return (info, url)
    except: pass
    return None

def update_m3u():
    adaylar = []
    eklenen_linkler = set()
    for s_url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(s_url, timeout=10)
            if r.status_code == 200:
                matches = re.findall(r"(#EXTINF:[^\n]*)\n(http[^\n]*)", r.text.replace('\r', ''))
                for info, url in matches:
                    if url.strip() not in eklenen_linkler:
                        adaylar.append((info, url.strip()))
                        eklenen_linkler.add(url.strip())
        except: continue
    with ThreadPoolExecutor(max_workers=30) as executor:
        sonuclar = list(filter(None, executor.map(link_test_et, adaylar)))
    output = "#EXTM3U\n" + "\n".join([f"{i}\n{u}" for i, u in sonuclar])
    github_yukle(output)

if __name__ == "__main__":
    update_m3u()
