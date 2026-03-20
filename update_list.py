import requests
import os

# --- AYARLAR ---
CF_ACCOUNT_ID = os.environ.get('CF_ACCOUNT_ID')
CF_API_TOKEN = os.environ.get('CF_API_TOKEN')
CF_D1_ID = os.environ.get('CF_D1_ID')
FILE_PATH = "tr.m3u"

# BU LİSTEDEKİLER SENİN GÖZBEBEĞİN, ASLA SİLİNMEZ, EN ÜSTE ÇIKAR
DOKUNULMAZLAR = ["premiumstream.in", "workers.dev", "mywire.org", "token=DeaTHLesS", "goldvod.site"]

def d1_sorgu(sql):
    endpoint = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/d1/database/{CF_D1_ID}/query"
    headers = {"Authorization": f"Bearer {CF_API_TOKEN}", "Content-Type": "application/json"}
    payload = {"sql": sql}
    try:
        r = requests.post(endpoint, json=payload, headers=headers, timeout=15)
        return r.json()
    except: return None

def update_m3u():
    print("🚀 Dokunulmazları koruma ve temizleme operasyonu başladı...")
    
    # Sadece ONLINE olanları çekiyoruz
    sql = "SELECT channel_name, backup_url FROM channel_backups WHERE status = 'ONLINE'"
    data = d1_sorgu(sql)
    
    if not data or not data.get("success"):
        print("❌ D1 Bağlantı Hatası!")
        return

    res_list = data["result"][0]["results"]
    
    # AYNI LİNKİ TEKRAR YAZMAMAK İÇİN SET KULLANIYORUZ
    islenen_linkler = set()
    dokunulmaz_listesi = []
    normal_liste = []

    for row in res_list:
        name = row['channel_name']
        url = row['backup_url']
        
        # Eğer bu linki zaten eklediysek atla (5 tane 360 TV olmasın diye)
        if url in islenen_linkler:
            continue
        
        line = f"{name}\n{url}\n"
        
        # Dokunulmazlık kontrolü
        is_dokunulmaz = any(d in url for d in DOKUNULMAZLAR)
        
        if is_dokunulmaz:
            dokunulmaz_listesi.append(line)
        else:
            normal_liste.append(line)
            
        islenen_linkler.add(url)

    # ÖNCE DOKUNULMAZLAR, SONRA DİĞERLERİ
    final_liste = "#EXTM3U\n" + "".join(dokunulmaz_listesi) + "".join(normal_liste)

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(final_liste)
    
    print(f"✅ Temizlendi! Toplam {len(islenen_linkler)} benzersiz link yazıldı.")

if __name__ == "__main__":
    update_m3u()
