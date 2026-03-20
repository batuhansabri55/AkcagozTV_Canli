import requests
import re
import base64
import os
from concurrent.futures import ThreadPoolExecutor

# --- AYARLAR (GitHub Secrets'tan gelir) ---
GITHUB_TOKEN = os.environ.get('GH_TOKEN') 
CF_ACCOUNT_ID = os.environ.get('CF_ACCOUNT_ID')
CF_API_TOKEN = os.environ.get('CF_API_TOKEN')
CF_D1_ID = os.environ.get('CF_D1_ID')

REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

YEDEK_KAYNAKLAR = [
    "https://mth.tc/DsGo",
    "https://raw.githubusercontent.com/sultansmgr/smart/refs/heads/main/viziTV.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://streams.uzunmuhalefet.com/lists/tr.m3u"
]

def temizle(metin):
    return re.sub(r'[^a-z0-9]', '', metin.lower())

def d1_sorgu(sql, params=None):
    endpoint = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/d1/database/{CF_D1_ID}/query"
    headers = {"Authorization": f"Bearer {CF_API_TOKEN}", "Content-Type": "application/json"}
    payload = {"sql": sql, "params": params or []}
    try:
        r = requests.post(endpoint, json=payload, headers=headers, timeout=15)
        return r.json()
    except: return None

def update_m3u():
    # 1. D1'DEN SENİN 365 KANALINI ÇEK
    data = d1_sorgu("SELECT name FROM channels")
    if not data or 'result' not in data:
        print("❌ D1 bağlantısı başarısız!")
        return
    
    # Senin 365 kanalının isimlerini filtre için hazırla
    ana_kanallar = {temizle(r['name']): r['name'] for r in data['result'][0]['results']}
    print(f"✅ {len(ana_kanallar)} ana kanal filtre için yüklendi.")

    # 2. ESKİ YEDEKLERİ SİL (Karmaşayı bitir)
    d1_sorgu("DELETE FROM channel_backups")

    yeni_yedekler = []
    eklenen_linkler = set()

    # 3. KAYNAKLARI TARA VE FİLTRELE
    for s_url in YEDEK_KAYNAKLAR:
        try:
            res = requests.get(s_url, timeout=10)
            matches = re.findall(r"(#EXTINF:[^\n]*,([^\n]*))\n(http[^\n]*)", res.text.replace('\r', ''))
            for full_info, kanal_adi, url in matches:
                temiz_ad = temizle(kanal_adi)
                link = url.strip()
                
                # FİLTRE: Eğer kanal senin 365 kanalından biriyse ekle
                if temiz_ad in ana_kanallar and link not in eklenen_linkler:
                    gercek_ad = ana_kanallar[temiz_ad]
                    # D1'e yaz
                    d1_sorgu("INSERT INTO channel_backups (channel_name, backup_url, status) VALUES (?, ?, 'ONLINE')", [gercek_ad, link])
                    yeni_yedekler.append(f"#EXTINF:-1,{gercek_ad}\n{link}")
                    eklenen_linkler.add(link)
        except: continue

    # 4. GITHUB'I GÜNCELLE
    output = "#EXTM3U\n" + "\n".join(yeni_yedekler)
    # (Buraya mevcut github_yukle fonksiyonunu ekleyebilirsin)
    print(f"✅ İşlem tamam! Sadece senin 365 kanalın için yedekler güncellendi.")

if __name__ == "__main__":
    update_m3u()
