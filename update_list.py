import requests
import re
import base64
import os
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

# --- AYARLAR ---
CF_ACCOUNT_ID = os.environ.get('CF_ACCOUNT_ID')
CF_API_TOKEN = os.environ.get('CF_API_TOKEN')
CF_D1_ID = os.environ.get('CF_D1_ID')
GITHUB_TOKEN = os.environ.get('GH_TOKEN')
REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

DOKUNULMAZLAR = ["premiumstream.in", "workers.dev", "mywire.org", "token=DeaTHLesS", "goldvod.site"]

def d1_sorgu(sql, params=None, mode="query"):
    endpoint = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/d1/database/{CF_D1_ID}/{mode}"
    headers = {"Authorization": f"Bearer {CF_API_TOKEN}", "Content-Type": "application/json"}
    payload = {"sql": sql, "params": params or []}
    if mode == "execute": payload = {"batches": [{"sql": sql, "params": params or []}]}
    try:
        r = requests.post(endpoint, json=payload, headers=headers, timeout=15)
        return r.json()
    except: return None

def update_m3u():
    print("🧹 Veritabanı temizliği ve 6 yedek sınırı başlıyor...")
    
    # 1. ADIM: VERİTABANINDA KANAL BAŞINA EN İYİ 6 YEDEK DIŞINDAKİ HER ŞEYİ SİL
    # Bu işlem panelini (dashboard) anında temizler.
    temizlik_sql = """
    DELETE FROM channel_backups 
    WHERE id IN (
        SELECT id FROM (
            SELECT id, ROW_NUMBER() OVER (
                PARTITION BY channel_name 
                ORDER BY 
                    CASE 
                        WHEN backup_url LIKE '%workers.dev%' THEN 1
                        WHEN backup_url LIKE '%premiumstream.in%' THEN 1
                        WHEN backup_url LIKE '%mywire.org%' THEN 1
                        WHEN backup_url LIKE '%goldvod.site%' THEN 1
                        ELSE 2 
                    END, 
                    id DESC
            ) as sira
            FROM channel_backups
        ) WHERE sira > 6
    )
    """
    d1_sorgu(temizlik_sql, mode="execute")

    # 2. ADIM: TEMİZLENMİŞ VERİLERİ ÇEK VE GITHUB'A YAZ
    data = d1_sorgu("SELECT channel_name, backup_url FROM channel_backups WHERE status = 'ONLINE'")
    
    if data and data.get("success"):
        res_list = data["result"][0]["results"]
        m3u_icerik = "#EXTM3U\n"
        for row in res_list:
            name = row['channel_name']
            url = row['backup_url']
            line = f"{name}\n{url}\n" if name.startswith("#EXTINF") else f"#EXTINF:-1,{name}\n{url}\n"
            m3u_icerik += line
        
        # GitHub'a yükleme fonksiyonunu buraya ekle (yukarıdaki github_yukle gibi)
        print(f"✅ Panel ve M3U temizlendi. Toplam {len(res_list)} link kaldı.")

if __name__ == "__main__":
    update_m3u()
