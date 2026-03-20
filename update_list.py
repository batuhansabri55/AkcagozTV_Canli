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

# 🛡️ DOKUNULMAZLAR (Asla silinmez, her zaman en üstte kalır)
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

def d1_sorgu(sql, params=[]):
    if not all([CF_ACCOUNT_ID, CF_API_TOKEN, CF_D1_ID]): return None
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/d1/database/{CF_D1_ID}/query"
    headers = {"Authorization": f"Bearer {CF_API_TOKEN}", "Content-Type": "application/json"}
    try:
        res = requests.post(url, json={"sql": sql, "params": params}, headers=headers, timeout=10)
        return res.json()
    except: return None

def d1_temizle():
    print("🧹 Tablo temizliği yapılıyor (Eski kopyalar siliniyor)...")
    # Dokunulmazlar hariç, aynı isimdeki eski kayıtları temizle
    sql = f"DELETE FROM channel_backups WHERE id NOT IN (SELECT MIN(id) FROM channel_backups GROUP BY channel_name, backup_url)"
    d1_sorgu(sql)

def d1_yaz(kanal_adi, url):
    sql = "INSERT OR IGNORE INTO channel_backups (channel_name, backup_url, status, is_manual) VALUES (?, ?, 'ONLINE', 0)"
    d1_sorgu(sql, [kanal_adi, url])

def github_guncelle(icerik):
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    r = requests.get(url, headers=headers)
    sha = r.json().get('sha') if r.status_code == 200 else None
    data = {
        "message": "🔄 Liste ve D1 Tablosu Tazelendi",
        "content": base64.b64encode(icerik.encode("utf-8")).decode("utf-8"),
        "sha": sha
    }
    requests.put(url, json=data, headers=headers)

def link_test_et(item):
    k, u = item
    try:
        if requests.get(u, timeout=5, stream=True).status_code == 200:
            d1_yaz(k, u) # Çalışan her linki D1 tablosuna doldur!
            return f"#EXTINF:-1,{k}\n{u}"
    except: pass
    return None

def baslat():
    # 1. Önce D1'deki çöpleri temizle
    d1_temizle()
    
    # 2. Mevcut dokunulmazları GitHub'dan çek (Korumaya al)
    dokunulmazlar = []
    try:
        r = requests.get(f"https://raw.githubusercontent.com/{REPO_NAME}/main/{FILE_PATH}")
        if r.status_code == 200:
            parcalar = re.findall(r"(#EXTINF:.*?\nhttp.*)", r.text)
            dokunulmazlar = [p for p in parcalar if any(d in p for d in DOKUNULMAZLAR)]
    except: pass

    # 3. Yeni linkleri topla ve test ederek TABLOYU DOLDUR
    adaylar = []
    eklenenler = set()
    for s_url in YEDEK_KAYNAKLAR:
        try:
            res = requests.get(s_url, timeout=10)
            matches = re.findall(r"#EXTINF:[^,]*,(.*?)\n(http.*)", res.text)
            for k, l in matches:
                if l.strip() not in eklenenler:
                    adaylar.append((k.strip(), l.strip()))
                    eklenenler.add(l.strip())
        except: continue

    with ThreadPoolExecutor(max_workers=30) as ex:
        yeni_list = list(filter(None, ex.map(link_test_et, adaylar)))

    # 4. Final: Dosyayı GitHub'a yaz
    github_guncelle("#EXTM3U\n" + "\n".join(dokunulmazlar + yeni_list))
    print(f"✅ Bitti! Tablo dolsun diye {len(yeni_list)} taze link işlendi.")

if __name__ == "__main__":
    baslat()
