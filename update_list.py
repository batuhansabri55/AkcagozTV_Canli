import requests
import re
import base64
import os
import json
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

# --- AYARLAR ---
GITHUB_TOKEN = os.environ.get('GH_TOKEN') 
CF_ACCOUNT_ID = os.environ.get('CF_ACCOUNT_ID')
CF_API_TOKEN = os.environ.get('CF_API_TOKEN')
CF_D1_ID = os.environ.get('CF_D1_ID')

REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

# BU LİSTEDEKİLER SENİN GÖZBEBEĞİN, ASLA SİLİNMEZ VE HER ZAMAN EN ÜSTTEDİR
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
    try: requests.post(endpoint, json=payload, headers=headers, timeout=10)
    except: pass

def github_yukle(icerik):
    if not GITHUB_TOKEN: return
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers)
    sha = r.json().get('sha') if r.status_code == 200 else None
    data = {"message": "D1 Senkronize + 6 Yedek Limiti", "content": base64.b64encode(icerik.encode("utf-8")).decode("utf-8")}
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
    mevcut_kanallar = []
    eklenen_linkler = set()
    
    # 1. GITHUB'DAN MEVCUTLARI ÇEK
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    r = requests.get(f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}", headers=headers)
    
    if r.status_code == 200:
        content = base64.b64decode(r.json()['content']).decode('utf-8')
        matches = re.findall(r"(#EXTINF:[^\n]*)\n(http[^\n]*)", content.replace('\r', ''))
        for info, url in matches:
            u = url.strip()
            mevcut_kanallar.append((info, u))
            eklenen_linkler.add(u)

    # 2. KAYNAKLARDAN YENİLERİ BUL
    adaylar = []
    for s_url in YEDEK_KAYNAKLAR:
        try:
            res = requests.get(s_url, timeout=10)
            if res.status_code == 200:
                matches = re.findall(r"(#EXTINF:[^\n]*,([^\n]*))\n(http[^\n]*)", res.text.replace('\r', ''))
                for full_info, kanal_adi, url in matches:
                    u = url.strip()
                    if u not in eklenen_linkler:
                        d1_veritabanina_yaz(kanal_adi.strip(), u)
                        adaylar.append((full_info, u))
        except: continue

    # 3. TEST ET
    with ThreadPoolExecutor(max_workers=30) as executor:
        yeni_sonuclar = list(filter(None, executor.map(link_test_et, adaylar)))

    # --- 4. ADIM: 6 YEDEK SINIRI VE SIRALAMA ---
    hepsi = mevcut_kanallar + yeni_sonuclar
    kanal_gruplari = defaultdict(list)
    
    for info, url in hepsi:
        # Kanal adını temizle
        temiz_ad = info.split(",")[-1].strip() if "," in info else info
        # Dokunulmaz linklere öncelik ver (0=en üst, 1=diğerleri)
        puan = 0 if any(d in url for d in DOKUNULMAZLAR) else 1
        kanal_gruplari[temiz_ad].append((puan, info, url))

    final_list = []
    for kanal in kanal_gruplari:
        # Önce puana (dokunulmazlar başa), sonra geliş sırasına göre sırala
        sirali = sorted(kanal_gruplari[kanal], key=lambda x: x[0])
        # Her kanaldan sadece İLK 6 TANEYİ al (Hani dediğin kısım burası)
        for _, info, url in sirali[:6]:
            final_list.append(f"{info}\n{url}")

    output = "#EXTM3U\n" + "\n".join(final_list)
    github_yukle(output)
    print(f"✅ Bitti! Kanallar en iyi 6 yedekle (Dokunulmazlar dahil) güncellendi.")

if __name__ == "__main__":
    update_m3u()
