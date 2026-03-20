import requests
import re
import os
import base64
from concurrent.futures import ThreadPoolExecutor

# --- AYARLAR (GitHub Secrets'dan çekilir) ---
CF_ACCOUNT_ID = os.environ.get('CF_ACCOUNT_ID')
CF_API_TOKEN = os.environ.get('CF_API_TOKEN')
CF_D1_ID = os.environ.get('CF_D1_ID')

# Senin resimdeki kaynakların
YEDEK_KAYNAKLAR = [
    "https://mth.tc/DsGo",
    "https://raw.githubusercontent.com/sultansmgr/smart/refs/heads/main/viziTV.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://streams.uzunmuhalefet.com/lists/tr.m3u"
]

def d1_yaz(kanal_adi, url):
    """Bulunan linki D1 'channel_backups' tablosuna ekler."""
    if not all([CF_ACCOUNT_ID, CF_API_TOKEN, CF_D1_ID]): return
    
    endpoint = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/d1/database/{CF_D1_ID}/query"
    headers = {
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # SQL: Eğer URL zaten varsa ekleme, yoksa 'ONLINE' olarak ekle
    sql = "INSERT OR IGNORE INTO channel_backups (channel_name, backup_url, status, is_manual) VALUES (?, ?, 'ONLINE', 0)"
    
    payload = {"params": [kanal_adi, url], "sql": sql}
    try:
        requests.post(endpoint, json=payload, headers=headers, timeout=10)
    except: pass

def link_test_et(item):
    kanal_adi, url = item
    try:
        # Hızlı kontrol: 5 saniyede cevap veriyorsa sağlamdır
        with requests.get(url, timeout=5, stream=True) as r:
            if r.status_code == 200:
                d1_yaz(kanal_adi, url)
                return True
    except: pass
    return False

def baslat():
    print("🔄 Sistem taranıyor...")
    eklenenler = set()
    adaylar = []

    for s_url in YEDEK_KAYNAKLAR:
        try:
            res = requests.get(s_url, timeout=10)
            if res.status_code == 200:
                matches = re.findall(r"#EXTINF:[^,]*,(.*?)\n(http.*)", res.text)
                for kanal, link in matches:
                    l = link.strip()
                    if l not in eklenenler:
                        adaylar.append((kanal.strip(), l))
                        eklenenler.add(l)
        except: continue

    print(f"🔍 {len(adaylar)} link bulundu, test ediliyor...")
    with ThreadPoolExecutor(max_workers=25) as executor:
        executor.map(link_test_et, adaylar)
    
    print("✅ D1 Veritabanı güncellendi!")

if __name__ == "__main__":
    baslat()
