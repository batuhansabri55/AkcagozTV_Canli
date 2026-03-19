import requests
import re
import base64
from concurrent.futures import ThreadPoolExecutor

# --- AYARLAR ---
# Senin bana verdiğin yeni ve taze anahtar
GITHUB_TOKEN = "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" 
REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

# Bu kelimeleri içeren linkler TEST EDİLMEDEN eklenir
DOKUNULMAZLAR = [
    "premiumstream.in", 
    "workers.dev", 
    "mywire.org", 
    "token=DeaTHLesS"
]

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
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}", 
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Mevcut dosyanın SHA bilgisini al (Güncelleme için şart)
    r = requests.get(url, headers=headers)
    sha = r.json().get('sha') if r.status_code == 200 else None

    data = {
        "message": "Liste guncellendi (Anahtar Yenilendi)",
        "content": base64.b64encode(icerik.encode("utf-8")).decode("utf-8")
    }
    if sha: data["sha"] = sha

    r = requests.put(url, json=data, headers=headers)
    if r.status_code in [200, 201]: 
        print("✅ GITHUB TAMAM! Liste başarıyla güncellendi.")
    else: 
        print(f"❌ HATA: {r.text}")

def link_test_et(item):
    info, url = item
    url_clean = url.lower().strip()
    if any(ozel in url_clean for ozel in DOKUNULMAZLAR): 
        return (info, url)
    try:
        with requests.get(url, timeout=5, stream=True) as r:
            if r.status_code == 200: 
                return (info, url)
    except: 
        pass
    return None

def update_m3u():
    adaylar = []
    eklenen_linkler = set()
    
    print("🔄 Kaynaklar taranıyor...")
    for s_url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(s_url, timeout=10)
            if r.status_code == 200:
                matches = re.findall(r"(#EXTINF:[^\n]*)\n(http[^\n]*)", r.text.replace('\r', ''))
                for info, url in matches:
                    u = url.strip()
                    if u not in eklenen_linkler:
                        adaylar.append((info, u))
                        eklenen_linkler.add(u)
        except: 
            continue

    print(f"📡 {len(adaylar)} kanal bulundu, testler başlıyor...")
    with ThreadPoolExecutor(max_workers=30) as executor:
        sonuclar = list(filter(None, executor.map(link_test_et, adaylar)))

    print(f"✅ {len(sonuclar)} aktif kanal GitHub'a gönderiliyor...")
    output = "#EXTM3U\n" + "\n".join([f"{i}\n{u}" for i, u in sonuclar])
    github_yukle(output)

if __name__ == "__main__":
    update_m3u()
