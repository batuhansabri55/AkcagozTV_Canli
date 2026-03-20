import requests
import re
import base64
import os
import json
from concurrent.futures import ThreadPoolExecutor

# --- AYARLAR (GitHub Secrets'tan gelir) ---
GITHUB_TOKEN = os.environ.get('GH_TOKEN') 
CF_ACCOUNT_ID = os.environ.get('CF_ACCOUNT_ID')
CF_API_TOKEN = os.environ.get('CF_API_TOKEN')
CF_D1_ID = os.environ.get('CF_D1_ID')

REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

# --- DOKUNULMAZ KELİME LİSTESİ ---
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
    data = {"message": "🔄 Ana Linkler + Yedekler Güncellendi", "content": base64.b64encode(icerik.encode("utf-8")).decode("utf-8")}
    if sha: data["sha"] = sha
    requests.put(url, json=data, headers=headers)

def update_m3u():
    # 1. D1'DEN SENİN ANA KANALLARINI VE LİNKLERİNİ ÇEK (Uçmaması için şart!)
    # Burada 'url' senin D1'deki ana dokunulmaz linkindir.
    res = d1_sorgu("SELECT name, url FROM channels")
    if not res or 'result' not in res or not res['result'][0].get('results'):
        print("❌ D1'den ana kanallar çekilemedi!")
        return
    
    # Ana listeyi hazırla (Hem isim hem ana link)
    ana_liste_bilgi = {}
    m3u_cikti = []
    eklenen_linkler = set()

    for r in res['result'][0]['results']:
        temiz_ad = temizle(r['name'])
        ana_link = r.get('url', '').strip()
        ana_liste_bilgi[temiz_ad] = r['name']
        
        # ANA LİNKİ EN BAŞA EKLE (Burası uçmayı engeller)
        if ana_link:
            m3u_cikti.append(f"#EXTINF:-1,{r['name']}\n{ana_link}")
            eklenen_linkler.add(ana_link)

    print(f"✅ {len(ana_liste_bilgi)} ana kanal ve dokunulmaz linkler yüklendi.")

    # 2. ESKİ YEDEKLERİ SİL
    d1_sorgu("DELETE FROM channel_backups")

    # 3. KAYNAKLARI TARA VE SADECE EŞLEŞENLERİ YEDEK OLARAK EKLE
    bulunan_yedek_sayisi = 0
    for s_url in YEDEK_KAYNAKLAR:
        try:
            res_tarama = requests.get(s_url, timeout=10)
            if res_tarama.status_code != 200: continue
            
            matches = re.findall(r"(#EXTINF:[^\n]*,([^\n]*))\n(http[^\n]*)", res_tarama.text.replace('\r', ''))
            for full_info, kanal_adi, url in matches:
                temiz_ad = temizle(kanal_adi)
                link = url.strip()
                
                # Sadece senin listende varsa ve henüz eklenmemişse
                if temiz_ad in ana_liste_bilgi and link not in eklenen_linkler:
                    gercek_ad = ana_liste_bilgi[temiz_ad]
                    
                    # D1'e yedek tablosuna yaz
                    d1_sorgu("INSERT INTO channel_backups (channel_name, backup_url, status) VALUES (?, ?, 'ONLINE')", [gercek_ad, link])
                    
                    # M3U dosyasına yedek olarak ekle
                    m3u_cikti.append(f"#EXTINF:-1,{gercek_ad} (YEDEK)\n{link}")
                    eklenen_linkler.add(link)
                    bulunan_yedek_sayisi += 1
        except: continue

    # 4. GITHUB'I GÜNCELLE
    if m3u_cikti:
        tam_icerik = "#EXTM3U\n" + "\n".join(m3u_cikti)
        github_yukle(tam_icerik)
        print(f"✅ İşlem bitti! {bulunan_yedek_sayisi} yeni yedek eklendi. Ana linkler korundu.")

if __name__ == "__main__":
    update_m3u()
