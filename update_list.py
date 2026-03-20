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

# BU LİSTEDEKİLERİ SAKIN ELLEME VE EKLEME YAPARKEN KONTROL ET
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
    # 1. VERİTABANINDAN TÜM DETAYLARI ÇEK (Logo, Grup, EPG dahil)
    print("🔄 Liste tüm detaylarıyla (Logo, Grup, EPG) hazırlanıyor...")
    # Not: Eğer sütun isimlerin farklıysa (örneğin category_name gibi), burayı ona göre düzenleriz.
    # Şimdilik standart M3U sütunlarını çektiğimizi varsayıyorum.
    sql = "SELECT channel_name, backup_url, category, logo, tvg_id, tvg_url FROM channel_backups WHERE status = 'ONLINE' ORDER BY channel_name"
    data = d1_sorgu(sql)
    
    if not data or not data.get("success"):
        print("❌ D1 Bağlantı Hatası!")
        return

    raw_results = data["result"][0]["results"]
    if not raw_results:
        print("⚠️ Yazılacak veri yok.")
        return

    m3u_icerik = "#EXTM3U\n"
    count = 0

    for row in raw_results:
        name = row.get('channel_name', 'Bilinmiyor')
        url = row.get('backup_url', '')
        group = row.get('category', 'Genel')
        logo = row.get('logo', '')
        tid = row.get('tvg_id', '')
        turl = row.get('tvg_url', '')

        # DOKUNULMAZ KONTROLÜ (Eğer internetten gelen yeni çöpler varsa süzmek için)
        # Ama veritabanında halihazırda varsa dokunmuyoruz.

        # İŞTE O SİLİNEN KISIMLARI TEKRAR KURUYORUZ:
        m3u_icerik += f'#EXTINF:-1 group-title="{group}" tvg-logo="{logo}" tvg-url="{turl}" tvg-id="{tid}",{name}\n{url}\n'
        count += 1

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(m3u_icerik)
    
    print(f"✅ Bitti. {count} kanal tüm detaylarıyla (Logo/Grup) tr.m3u dosyasına yazıldı.")

if __name__ == "__main__":
    update_m3u()
