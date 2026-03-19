import requests
import re
import base64
import os
import json
from concurrent.futures import ThreadPoolExecutor

# --- AYARLAR ---
GITHUB_TOKEN = os.environ.get('GH_TOKEN') 
CF_ACCOUNT_ID = os.environ.get('CF_ACCOUNT_ID')
CF_API_TOKEN = os.environ.get('CF_API_TOKEN')
CF_D1_ID = os.environ.get('CF_D1_ID')

REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

DOKUNULMAZLAR = ["premiumstream.in", "workers.dev", "mywire.org", "token=DeaTHLesS", "goldvod.site"]

YEDEK_KAYNAKLAR = [
    "https://mth.tc/DsGo",
    "https://raw.githubusercontent.com/sultansmgr/smart/refs/heads/main/viziTV.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://streams.uzunmuhalefet.com/lists/tr.m3u"
]

def d1_veritabanina_yaz(kanal_adi, url):
    if not all([CF_ACCOUNT_ID, CF_API_TOKEN, CF_D1_ID]): return
    endpoint = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/d1/database/{CF_D1_ID}/query"
    headers = {"Authorization": f"Bearer {CF_API_TOKEN}", "Content-Type": "application/json"}
    sql = "INSERT OR IGNORE INTO channel_backups (channel_name, backup_url, status, is_manual) VALUES (?, ?, 'ONLINE', 0)"
    payload = {"params": [kanal_adi, url], "sql": sql}
    try:
        requests.post(endpoint, json=payload, headers=headers, timeout=10)
    except: pass

def github_yukle(icerik):
    # Yerel dosyayı her ihtimale karşı oluştur (Workflow hata vermesin diye)
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(icerik)
    
    if not GITHUB_TOKEN: return
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    
    r = requests.get(url, headers=headers)
    sha = r.json().get('sha') if r.status_code == 200 else None
    
    data = {
        "message": "D1 ve M3U Senkronize Edildi",
        "content": base64.b64encode(icerik.encode("utf-8")).decode("utf-8"),
        "branch": "main"
    }
    if sha: data["sha"] = sha
    
    res = requests.put(url, json=data, headers=headers)
    if res.status_code in [200, 201]:
        print("✅ GitHub Dosyası Güncellendi!")
    else:
        print(f"❌ GitHub Hatası: {res.text}")

def link_test_et(item):
    info, url = item
    if any(ozel in url.lower() for ozel in DOKUNULMAZLAR): return (info, url)
    try:
        with requests.get(url, timeout=5, stream=True) as r:
            if r.status_code == 200: return (info, url)
    except: pass
    return None

def update_m3u():
    mevcut_kanallar = []
    eklenen_linkler = set()
    
    # Mevcut dosyayı çek
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    r = requests.get(f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}", headers=headers)
    
    if r.status_code == 200:
        content = base64.b64decode(r.json()['content']).decode('utf-8')
        matches = re.findall(r"(#EXTINF:[^\n]*)\n(http[^\n]*)", content.replace('\r', ''))
        for info, url in matches:
            u = url.strip()
            mevcut_kanallar.append((info, u))
            eklenen_linkler.add(u)

    # Yeni yedekleri bul
    adaylar = []
    for s_url in YEDEK_KAYNAKLAR:
        try:
            res = requests.get(s_url, timeout=10)
            if res.status_code == 200:
                matches = re.findall(r"#EXTINF:.*?,(.*?)\n(http.*)", res.text)
                for kanal_adi, url in matches:
                    u = url.strip()
                    if u not in eklenen_linkler:
                        d1_veritabanina_yaz(kanal_adi.strip(), u)
                        adaylar.append((f"#EXTINF:-1,{kanal_adi.strip()}", u))
                        eklenen_linkler.add(u)
        except: continue

    with ThreadPoolExecutor(max_workers=20) as executor:
        yeni_sonuclar = list(filter(None, executor.map(link_test_et, adaylar)))

    hepsi = mevcut_kanallar + yeni_sonuclar
    output = "#EXTM3U\n" + "\n".join([f"{i}\n{u}" for i, u in hepsi])
    github_yukle(output)

if __name__ == "__main__":
    update_m3u()
