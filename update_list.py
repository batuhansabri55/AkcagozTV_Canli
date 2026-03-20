import requests
import re
import os
import base64
from concurrent.futures import ThreadPoolExecutor

# --- AYARLAR ---
CF_ACCOUNT_ID = os.environ.get('CF_ACCOUNT_ID')
CF_API_TOKEN = os.environ.get('CF_API_TOKEN')
CF_D1_ID = os.environ.get('CF_D1_ID')
GITHUB_TOKEN = os.environ.get('GH_TOKEN')

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

def d1_yaz(kanal_adi, url):
    if not all([CF_ACCOUNT_ID, CF_API_TOKEN, CF_D1_ID]): return
    endpoint = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/d1/database/{CF_D1_ID}/query"
    headers = {"Authorization": f"Bearer {CF_API_TOKEN}", "Content-Type": "application/json"}
    sql = "INSERT OR IGNORE INTO channel_backups (channel_name, backup_url, status, is_manual) VALUES (?, ?, 'ONLINE', 0)"
    payload = {"params": [kanal_adi, url], "sql": sql}
    try: requests.post(endpoint, json=payload, headers=headers, timeout=10)
    except: pass

def github_dosya_guncelle(icerik):
    if not GITHUB_TOKEN:
        print("❌ Hata: GH_TOKEN bulunamadı!")
        return
    
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Mevcut dosyanın SHA bilgisini al (Güncelleme için bu şart)
    r = requests.get(url, headers=headers)
    sha = r.json().get('sha') if r.status_code == 200 else None
    
    # İçeriği Base64 formatına çevir
    encoded_content = base64.b64encode(icerik.encode("utf-8")).decode("utf-8")
    
    payload = {
        "message": "🔄 Otomatik Liste Güncelleme",
        "content": encoded_content,
        "branch": "main"
    }
    if sha:
        payload["sha"] = sha
        
    res = requests.put(url, json=payload, headers=headers)
    if res.status_code in [200, 201]:
        print(f"✅ GitHub Başarılı: {FILE_PATH} güncellendi!")
    else:
        print(f"❌ GitHub Hatası ({res.status_code}): {res.text}")

def link_test_et(item):
    kanal_adi, url = item
    if any(ozel in url.lower() for ozel in DOKUNULMAZLAR):
        d1_yaz(kanal_adi, url)
        return f"#EXTINF:-1,{kanal_adi}\n{url}"
    try:
        with requests.get(url, timeout=5, stream=True) as r:
            if r.status_code == 200:
                d1_yaz(kanal_adi, url)
                return f"#EXTINF:-1,{kanal_adi}\n{url}"
    except: pass
    return None

def baslat():
    print("🔄 Tarama başlıyor...")
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

    with ThreadPoolExecutor(max_workers=25) as executor:
        m3u_satirlari = list(filter(None, executor.map(link_test_et, adaylar)))

    if m3u_satirlari:
        yeni_m3u_icerik = "#EXTM3U\n" + "\n".join(m3u_satirlari)
        github_dosya_guncelle(yeni_m3u_icerik)
        print(f"✅ Toplam {len(m3u_satirlari)} kanal işlendi.")
    else:
        print("⚠️ Hiç çalışan link bulunamadı.")

if __name__ == "__main__":
    baslat()
