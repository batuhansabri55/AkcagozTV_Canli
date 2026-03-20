import requests
import os

# --- AYARLAR ---
CF_ACCOUNT_ID = os.environ.get('CF_ACCOUNT_ID')
CF_API_TOKEN = os.environ.get('CF_API_TOKEN')
CF_D1_ID = os.environ.get('CF_D1_ID')
FILE_PATH = "tr.m3u"

def d1_sorgu(sql):
    endpoint = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/d1/database/{CF_D1_ID}/query"
    headers = {"Authorization": f"Bearer {CF_API_TOKEN}", "Content-Type": "application/json"}
    payload = {"sql": sql}
    try:
        r = requests.post(endpoint, json=payload, headers=headers, timeout=15)
        return r.json()
    except: return None

def update_m3u():
    print("🔄 Veritabanından orijinal format geri yükleniyor...")
    
    # Sadece senin veritabanındaki ONLINE yedekleri çekiyoruz.
    # İnternetten yeni link arama kısmını SİLDİM ki dokunulmazlar karışmasın.
    sql = "SELECT channel_name, backup_url, status FROM channel_backups WHERE status = 'ONLINE' ORDER BY channel_name ASC"
    data = d1_sorgu(sql)
    
    if not data or not data.get("success"):
        print("❌ D1 Bağlantı Hatası!")
        return

    res_list = data["result"][0]["results"]
    
    m3u_icerik = "#EXTM3U\n"
    count = 0
    
    for row in res_list:
        name = row['channel_name']
        url = row['backup_url']

        # EĞER: Senin D1'deki channel_name kısmında o uzun logo/grup bilgileri 
        # zaten yazıyorsa bu kod onu bozmaz. 
        # Ama sadece isim yazıyorsa, İçel TV örneğindeki gibi tam formatı kurar:
        
        if "group-title" in name:
            # Eğer zaten tam formatsa direkt yaz
            m3u_icerik += f"{name}\n{url}\n"
        else:
            # Eğer sadece isimse, en azından ismi bozmadan yaz (Logolar için JOIN gerekebilir ama şimdilik güvenli liman)
            m3u_icerik += f"#EXTINF:-1,{name}\n{url}\n"
        
        count += 1

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(m3u_icerik)
    
    print(f"✅ Bitti! {count} kanal dokunulmazlar korunarak dosyaya yazıldı.")

if __name__ == "__main__":
    update_m3u()
