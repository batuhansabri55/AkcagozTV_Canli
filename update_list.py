import requests
import re
import base64
import os
from concurrent.futures import ThreadPoolExecutor

# --- AYARLAR ---
GITHUB_TOKEN = os.environ.get('GH_TOKEN') 
REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

# Test edilmeden direkt eklenecek linkler (Senin özel kaynakların)
DOKUNULMAZLAR = ["premiumstream.in", "workers.dev", "mywire.org", "token=DeaTHLesS", "goldvod.site"]

# Kaynak listesi
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
    if not GITHUB_TOKEN: return
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers)
    sha = r.json().get('sha') if r.status_code == 200 else None
    data = {"message": "Manuel Kanallar Korundu + Yeniler Eklendi", "content": base64.b64encode(icerik.encode("utf-8")).decode("utf-8")}
    if sha: data["sha"] = sha
    requests.put(url, json=data, headers=headers)

def link_test_et(item):
    info, url = item
    if any(ozel in url.lower() for ozel in DOKUNULMAZLAR): return (info, url)
    try:
        with requests.get(url, timeout=5, stream=True) as r:
            if r.status_code == 200: return (info, url)
    except: pass
    return None

def update_m3u():
    # 1. ADIM: MEVCUT TR.M3U İÇİNDEKİ 2000 KANALI OKU (SİLİNMEMESİ İÇİN)
    mevcut_kanallar = []
    eklenen_linkler = set()
    
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    r = requests.get(f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}", headers=headers)
    
    if r.status_code == 200:
        content = base64.b64decode(r.json()['content']).decode('utf-8')
        matches = re.findall(r"(#EXTINF:[^\n]*)\n(http[^\n]*)", content.replace('\r', ''))
        for info, url in matches:
            u = url.strip()
            mevcut_kanallar.append((info, u))
            eklenen_linkler.add(u)
        print(f"📂 Mevcut {len(mevcut_kanallar)} kanal korumaya alındı.")

    # 2. ADIM: İNTERNETTEN YENİ KANALLARI ARA
    adaylar = []
    for s_url in YEDEK_KAYNAKLAR:
        try:
            res = requests.get(s_url, timeout=10)
            if res.status_code == 200:
                matches = re.findall(r"(#EXTINF:[^\n]*)\n(http[^\n]*)", res.text.replace('\r', ''))
                for info, url in matches:
                    u = url.strip()
                    if u not in eklenen_linkler: # Eğer bizde yoksa ekle
                        adaylar.append((info, u))
        except: continue

    # 3. ADIM: SADECE YENİ BULUNANLARI TEST ET
    with ThreadPoolExecutor(max_workers=30) as executor:
        yeni_sonuclar = list(filter(None, executor.map(link_test_et, adaylar)))

    # 4. ADIM: ESKİLER + YENİLERİ BİRLEŞTİR VE YÜKLE
    hepsi = mevcut_kanallar + yeni_sonuclar
    output = "#EXTM3U\n" + "\n".join([f"{i}\n{u}" for i, u in hepsi])
    github_yukle(output)
    print(f"✅ İşlem Tamam: Toplam {len(hepsi)} kanal kaydedildi.")

if __name__ == "__main__":
    update_m3u()
