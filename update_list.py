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

def d1_sorgu(sql, params=None):
    """Cloudflare D1'e sorgu atar."""
    endpoint = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/d1/database/{CF_D1_ID}/query"
    headers = {"Authorization": f"Bearer {CF_API_TOKEN}", "Content-Type": "application/json"}
    payload = {"sql": sql, "params": params or []}
    try:
        r = requests.post(endpoint, json=payload, headers=headers, timeout=15)
        return r.json()
    except: return None

def update_m3u():
    # 1. ÖNCE İNTERNETTEN YENİ LİNKLERİ BUL VE D1'E EKLE (Besleme)
    for s_url in YEDEK_KAYNAKLAR:
        try:
            res = requests.get(s_url, timeout=10)
            if res.status_code == 200:
                matches = re.findall(r"#EXTINF:.*?,(.*?)\n(http.*)", res.text)
                for kanal_adi, url in matches:
                    u = url.strip()
                    k_adi = kanal_adi.strip()
                    # Veritabanına yeni olanı ekle
                    d1_sorgu("INSERT OR IGNORE INTO channel_backups (channel_name, backup_url, status, is_manual) VALUES (?, ?, 'ONLINE', 0)", [k_adi, u])
        except: continue

    # 2. ŞİMDİ D1'DEKİ TÜM YEDEKLERİ ÇEK (Panelde gördüğün o 1855 yedek)
    print("🔄 Veritabanındaki tüm yedekler çekiliyor...")
    data = d1_sorgu("SELECT channel_name, backup_url FROM channel_backups WHERE status = 'ONLINE'")
    
    m3u_icerik = "#EXTM3U\n"
    count = 0
    
    if data and data.get("success") and data["result"][0]["results"]:
        for row in data["result"][0]["results"]:
            k_adi = row["channel_name"]
            u = row["backup_url"]
            m3u_icerik += f"#EXTINF:-1,{k_adi}\n{u}\n"
            count += 1
    
    # 3. GITHUB'A YÜKLE
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(m3u_icerik)
    
    print(f"✅ Toplam {count} kanal dosyaya yazıldı.")

if __name__ == "__main__":
    update_m3u()
