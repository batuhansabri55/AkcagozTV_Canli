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

# --- DOKUNULMAZLAR LİSTESİ ---
# Bu kelimeleri içeren linkler sorgusuz sualsiz "sağlam" kabul edilir.
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

def temizle(metin):
    if not metin: return ""
    return re.sub(r'[^a-z0-9]', '', metin.lower())

def d1_sorgu(sql, params=None):
    endpoint = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/d1/database/{CF_D1_ID}/query"
    headers = {"Authorization": f"Bearer {CF_API_TOKEN}", "Content-Type": "application/json"}
    payload = {"sql": sql, "params": params or []}
    try:
        r = requests.post(endpoint, json=payload, headers=headers, timeout=15)
        return r.json()
    except: return None

def github_yukle(icerik):
    if not GITHUB_TOKEN: return
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers)
    sha = r.json().get('sha') if r.status_code == 200 else None
    data = {"message": "🔄 Dokunulmazlar Korundu + Yedekler Güncellendi", "content": base64.b64encode(icerik.encode("utf-8")).decode("utf-8")}
    if sha: data["sha"] = sha
    requests.put(url, json=data, headers=headers)

def update_m3u():
    # 1. D1'DEN SENİN 365 KANALINI ÇEK
    data = d1_sorgu("SELECT name FROM channels")
    if not data or 'result' not in data:
        print("❌ D1 bağlantısı başarısız!")
        return
    
    ana_kanallar = {temizle(r['name']): r['name'] for r in data['result'][0]['results']}
    print(f"✅ {len(ana_kanallar)} ana kanal filtre için yüklendi.")

    # 2. ESKİ YEDEKLERİ SİL
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
                
                # FİLTRE 1: Eğer kanal senin listenizdeyse
                if temiz_ad in ana_kanallar and link not in eklenen_linkler:
                    gercek_ad = ana_kanallar[temiz_ad]
                    
                    # FİLTRE 2: Dokunulmaz mı? (İçinde özel kelime geçiyor mu?)
                    is_dokunulmaz = any(d in link.lower() for d in DOKUNULMAZLAR)
                    
                    # D1'e yaz (Dokunulmazsa direk ekle, değilse de ekle ama istersen burada test kodu açabiliriz)
                    d1_sorgu("INSERT INTO channel_backups (channel_name, backup_url, status) VALUES (?, ?, 'ONLINE')", [gercek_ad, link])
                    yeni_yedekler.append(f"#EXTINF:-1,{gercek_ad}\n{link}")
                    eklenen_linkler.add(link)
        except: continue

    # 4. GITHUB'I GÜNCELLE
    if yeni_yedekler:
        output = "#EXTM3U\n" + "\n".join(yeni_yedekler)
        github_yukle(output)
        print(f"✅ Bitti! {len(yeni_yedekler)} yedek (dokunulmazlar dahil) işlendi.")

if __name__ == "__main__":
    update_m3u()
