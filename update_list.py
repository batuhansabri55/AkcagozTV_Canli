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

# 🛡️ DOKUNULMAZ KRİTERLERİ (Bu kelimeleri içeren hiçbir satır silinmez)
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
    if not GITHUB_TOKEN: return
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    
    r = requests.get(url, headers=headers)
    sha = r.json().get('sha') if r.status_code == 200 else None
    
    data = {
        "message": "🔄 Dokunulmazlar Korundu + Liste Güncellendi",
        "content": base64.b64encode(icerik.encode("utf-8")).decode("utf-8"),
        "branch": "main"
    }
    if sha: data["sha"] = sha
    res = requests.put(url, json=data, headers=headers)
    if res.status_code in [200, 201]:
        print("✅ GitHub başarıyla güncellendi.")
    else:
        print(f"❌ GitHub hatası: {res.status_code}")

def link_test_et(item):
    kanal_adi, url = item
    try:
        with requests.get(url, timeout=5, stream=True) as r:
            if r.status_code == 200:
                d1_yaz(kanal_adi, url)
                return f"#EXTINF:-1,{kanal_adi}\n{url}"
    except: pass
    return None

def baslat():
    print("🔄 İşlem başlıyor...")
    
    # 1. Mevcut dosyayı GitHub'dan oku ve DOKUNULMAZLARI ayır
    dokunulmaz_listesi = []
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            mevcut_icerik = base64.b64decode(r.json()['content']).decode('utf-8')
            parcalar = re.findall(r"(#EXTINF:.*?\nhttp.*)", mevcut_icerik)
            for p in parcalar:
                if any(d in p for d in DOKUNULMAZLAR):
                    dokunulmaz_listesi.append(p)
        print(f"🛡️ {len(dokunulmaz_listesi)} dokunulmaz kanal korumaya alındı.")
    except:
        print("⚠️ Mevcut dosya okunamadı, sıfırdan oluşturuluyor.")

    # 2. Yeni kaynaklardan link topla
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

    # 3. Yeni linkleri test et
    with ThreadPoolExecutor(max_workers=25) as executor:
        yeni_kanallar = list(filter(None, executor.map(link_test_et, adaylar)))

    # 4. Birleştir (Önce Dokunulmazlar, Sonra Yeniler)
    tam_liste = ["#EXTM3U"] + dokunulmaz_listesi + yeni_kanallar
    github_dosya_guncelle("\n".join(tam_liste))
    print(f"✅ Bitti! {len(dokunulmaz_listesi)} sabit, {len(yeni_kanallar)} taze kanal.")

if __name__ == "__main__":
    baslat()
