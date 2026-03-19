import requests
import re
import base64
import os
import json
from concurrent.futures import ThreadPoolExecutor

# --- AYARLAR (GitHub Secrets'a bunları girdiğinden emin ol) ---
GITHUB_TOKEN = os.environ.get('GH_TOKEN') 
CF_ACCOUNT_ID = os.environ.get('CF_ACCOUNT_ID')
CF_API_TOKEN = os.environ.get('CF_API_TOKEN')
CF_D1_ID = os.environ.get('CF_D1_ID')

REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

# Senin özel linklerin
DOKUNULMAZLAR = ["premiumstream.in", "workers.dev", "mywire.org", "token=DeaTHLesS", "goldvod.site"]

# Kaynaklar
YEDEK_KAYNAKLAR = [
    "https://mth.tc/DsGo",
    "https://raw.githubusercontent.com/sultansmgr/smart/refs/heads/main/viziTV.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://streams.uzunmuhalefet.com/lists/tr.m3u"
]

def d1_veritabanina_yaz(kanal_adi, url):
    """Bulunan yedekleri Cloudflare D1'e basar."""
    if not all([CF_ACCOUNT_ID, CF_API_TOKEN, CF_D1_ID]):
        print("⚠️ Cloudflare bilgileri eksik!")
        return
    
    endpoint = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/d1/database/{CF_D1_ID}/query"
    headers = {
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # SENİN TABLO SÜTUNLARINA GÖRE GÜNCELLEDİM
    sql = "INSERT OR IGNORE INTO channel_backups (channel_name, backup_url, status, is_manual) VALUES (?, ?, 'ONLINE', 0)"
    
    payload = {"params": [kanal_adi, url], "sql": sql}
    
    try:
        response = requests.post(endpoint, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"✅ D1 Başarılı: {kanal_adi}")
        else:
            print(f"❌ D1 Hatası ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"❌ Bağlantı Hatası: {e}")

def github_yukle(icerik):
    if not GITHUB_TOKEN: return
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers)
    sha = r.json().get('sha') if r.status_code == 200 else None
    data = {"message": "D1 Senkronize Edildi", "content": base64.b64encode(icerik.encode("utf-8")).decode("utf-8")}
    if sha: data["sha"] = sha
    requests.put(url, json=data, headers=headers)

def link_test_et(item):
    info, url = item
    if any(ozel in url.lower() for ozel in DOKUNULMAZLAR): return (info, url)
    try:
        with requests.get(url, timeout=5, stream=True) as r:
            if r.status_code == 200: return (info, url)
    except: pass
    return None

def update_m3u():
    mevcut_kanallar = []
    eklenen_linkler = set()
    
    # 1. GITHUB'DAN MEVCUTLARI OKU
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    r = requests.get(f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}", headers=headers)
    
    if r.status_code == 200:
        content = base64.b64decode(r.json()['content']).decode('utf-8')
        matches = re.findall(r"(#EXTINF:[^\n]*)\n(http[^\n]*)", content.replace('\r', ''))
        for info, url in matches:
            u = url.strip()
            mevcut_kanallar.append((info, u))
            eklenen_linkler.add(u)

    # 2. YENİ YEDEKLERİ BUL VE HEMEN D1'E GÖNDER
    adaylar = []
    for s_url in YEDEK_KAYNAKLAR:
        try:
            res = requests.get(s_url, timeout=10)
            if res.status_code == 200:
                # Kanal adını daha sağlam çekmek için regex güncellendi
                matches = re.findall(r"#EXTINF:.*?,(.*?)\n(http.*)", res.text)
                for kanal_adi, url in matches:
                    u = url.strip()
                    k_adi = kanal_adi.strip()
                    # Sadece TRT 1, Kanal D gibi senin istediğin ana kanalları filtrele (Opsiyonel)
                    if u not in eklenen_linkler:
                        d1_veritabanina_yaz(k_adi, u) # ANINDA D1'E BASAR
                        adaylar.append((f"#EXTINF:-1,{k_adi}", u))
                        eklenen_linkler.add(u)
        except: continue

    # 3. TEST VE BİTİRİŞ
    with ThreadPoolExecutor(max_workers=30) as executor:
        yeni_sonuclar = list(filter(None, executor.map(link_test_et, adaylar)))

    hepsi = mevcut_kanallar + yeni_sonuclar
    output = "#EXTM3U\n" + "\n".join([f"{i}\n{u}" for i, u in hepsi])
    github_yukle(output)
    print("🚀 İşlem başarıyla tamamlandı!")

if __name__ == "__main__":
    update_m3u()
