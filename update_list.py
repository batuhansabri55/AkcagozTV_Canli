import requests
import re
import os

# --- AYARLAR ---
CF_ACCOUNT_ID = os.environ.get('CF_ACCOUNT_ID')
CF_API_TOKEN = os.environ.get('CF_API_TOKEN')
CF_D1_ID = os.environ.get('CF_D1_ID')
FILE_PATH = "tr.m3u"

# BU LİSTEDEKİLER SENİN GÖZBEBEĞİN, ASLA SİLİNMEZ VE EN ÜSTE ÇIKAR
DOKUNULMAZLAR = ["premiumstream.in", "workers.dev", "mywire.org", "token=DeaTHLesS", "goldvod.site"]

# YEDEK KAYNAKLAR (Yeni linkleri beslemek için)
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
    endpoint = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/d1/database/{CF_D1_ID}/query"
    headers = {"Authorization": f"Bearer {CF_API_TOKEN}", "Content-Type": "application/json"}
    payload = {"sql": sql, "params": params or []}
    try:
        r = requests.post(endpoint, json=payload, headers=headers, timeout=15)
        return r.json()
    except: return None

def update_m3u():
    # 1. YENİ LİNKLERİ BUL VE D1'E EKLE
    for s_url in YEDEK_KAYNAKLAR:
        try:
            res = requests.get(s_url, timeout=10)
            if res.status_code == 200:
                matches = re.findall(r"#EXTINF:.*?,(.*?)\n(http.*)", res.text)
                for kanal_adi, url in matches:
                    u = url.strip()
                    k_adi = kanal_adi.strip()
                    # Dokunulmaz linkleri internetten gelenlerle ezme (Sadece yeni olanları ekle)
                    if any(d in u for d in DOKUNULMAZLAR):
                        continue
                    d1_sorgu("INSERT OR IGNORE INTO channel_backups (channel_name, backup_url, status, is_manual) VALUES (?, ?, 'ONLINE', 0)", [k_adi, u])
        except: continue

    # 2. TÜM LİSTEYİ HAZIRLA (SADECE ONLINE OLANLAR)
    print("🔄 Veritabanından ONLINE olanlar çekiliyor...")
    data = d1_sorgu("SELECT channel_name, backup_url FROM channel_backups WHERE status = 'ONLINE'")
    
    if not data or not data.get("success"):
        print("❌ D1 Bağlantı Hatası!")
        return

    res_list = data["result"][0]["results"]
    
    dokunulmaz_parçalar = []
    normal_parçalar = []
    islenen_normal_urls = set()

    for row in res_list:
        name = row['channel_name']
        url = row['backup_url']
        
        # Format ayarı (Logo ve Grup bilgilerini korur)
        if name.startswith("#EXTINF"):
            line = f"{name}\n{url}\n"
        else:
            line = f"#EXTINF:-1,{name}\n{url}\n"
            
        # Dokunulmazlık kontrolü
        if any(d in url for d in DOKUNULMAZLAR):
            # Dokunulmaz ise süzgeçsiz ekle
            dokunulmaz_parçalar.append(line)
        else:
            # Normal link ise mükerrer engelle (Aynı kanaldan 5 tane olmasın)
            if url not in islenen_normal_urls:
                normal_parçalar.append(line)
                islenen_normal_urls.add(url)

    # 3. YAZMA İŞLEMİ (Önce Dokunulmazlar)
    final_m3u = "#EXTM3U\n" + "".join(dokunulmaz_parçalar) + "".join(normal_parçalar)
    
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(final_m3u)
    
    print(f"✅ Bitti. {len(dokunulmaz_parçalar)} Dokunulmaz ve {len(normal_parçalar)} Normal kanal yazıldı.")

if __name__ == "__main__":
    update_m3u()
