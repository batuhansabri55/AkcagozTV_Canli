import requests
import re
import os

# --- AYARLAR ---
GITHUB_TOKEN = os.environ.get('GH_TOKEN') 
CF_ACCOUNT_ID = os.environ.get('CF_ACCOUNT_ID')
CF_API_TOKEN = os.environ.get('CF_API_TOKEN')
CF_D1_ID = os.environ.get('CF_D1_ID')

REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

# BU LİSTEDEKİLERİ SAKIN ELLEME (KORUMA KALKANI)
DOKUNULMAZLAR = ["premiumstream.in", "workers.dev", "mywire.org", "token=DeaTHLesS", "goldvod.site"]

def d1_sorgu(sql, params=None):
    endpoint = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/d1/database/{CF_D1_ID}/query"
    headers = {"Authorization": f"Bearer {CF_API_TOKEN}", "Content-Type": "application/json"}
    payload = {"sql": sql, "params": params or []}
    try:
        r = requests.post(endpoint, json=payload, headers=headers, timeout=15)
        return r.json()
    except: return None

def update_m3u():
    # 1. VERİTABANINDAN TÜM YEDEKLERİ ÇEK (Sadece sende olan sütunlarla)
    print("🔄 Veritabanındaki yedekler çekiliyor...")
    # Sadece senin D1 tablonda olan sütunları seçiyoruz:
    sql = "SELECT channel_name, backup_url FROM channel_backups WHERE status = 'ONLINE' ORDER BY channel_name"
    data = d1_sorgu(sql)
    
    if not data or not data.get("success"):
        print("❌ D1 Bağlantı Hatası! Lütfen Secrets bilgilerini kontrol et.")
        return

    res_list = data["result"][0]["results"]
    if not res_list:
        print("⚠️ Yazılacak veri bulunamadı.")
        return

    m3u_icerik = "#EXTM3U\n"
    count = 0

    for row in res_list:
        name = row['channel_name']
        url = row['backup_url']
        
        # M3U formatına ekle
        m3u_icerik += f"#EXTINF:-1,{name}\n{url}\n"
        count += 1
    
    # 2. GITHUB DOSYASINI GÜNCELLE
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(m3u_icerik)
    
    print(f"✅ İşlem Başarılı: {count} kanal tr.m3u dosyasına yazıldı.")

if __name__ == "__main__":
    update_m3u()
