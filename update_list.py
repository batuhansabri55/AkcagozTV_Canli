import requests
import re
import os
import datetime
import shutil
from concurrent.futures import ThreadPoolExecutor
import urllib3
from urllib.parse import urljoin

# SSL hatalarını tamamen sustur
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
ZIRH_LIMIT = 3750
THREADS = 64

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}

# --- YASAKLI VE YEDEK LİSTELERİ ---
YASAKLI_GRUPLAR = [
    "FreeShot", "Webteizle", "TR FILM", "ARZU FILM", "ERLER FILM", 
    "Taşacak Bu Deniz", "EZEL", "FilmMedya", "Keloğlan", "PolskieTV", 
    "MediabayTV", "SarkorTV", "GLWIZ", "PERSIAN", "GledaiTV", "RDS TV", 
    "TouchTV", "Slovakia", "Bulgaria", "Romania", "Azerbeycan",
    "Superxfilm", "CINEMAMOD", "Adult", "XXX"
]

YEDEK_KAYNAKLAR = [
    "https://raw.githubusercontent.com/smartwebos/cdn/refs/heads/main/viziTV.m3u",
    "https://streams.uzunmuhalefet.com/lists/tr.m3u",
    "https://link.testworkery0.workers.dev/patron.m3u",
    "https://raw.githubusercontent.com/hayatiptv/iptv/master/index.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://www.dropbox.com/scl/fi/p58t5o980tah2hz3234a5/SmartGO.m3u?rlkey=w44w0ycaa83uyn21uph77pp6v&st=mj0n6byr&raw=1",
    "https://raw.githubusercontent.com/hydrokin/M3U/e4e9ba44d54d360ff3de6388220a4dc1019bf34e/tvando.m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u"
]

def github_taze_link_avla():
    yeni_kaynaklar = []
    tarih = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
    arama_terimleri = ["trt1", "documentary", "belgesel"]
    
    for terim in arama_terimleri:
        search_url = f"https://api.github.com/search/code?q=extension:m3u+{terim}+pushed:>{tarih}&sort=indexed"
        try:
            r = requests.get(search_url, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                items = r.json().get('items', [])
                for item in items:
                    raw = item['html_url'].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
                    if raw not in yeni_kaynaklar:
                        yeni_kaynaklar.append(raw)
                    if len(yeni_kaynaklar) >= 15: break
        except: continue
    return yeni_kaynaklar[:12]

def link_saglam_mi(url):
    """Diğer kaynaklar için doğrulama yapar."""
    try:
        with requests.get(url, headers=HEADERS, timeout=5, stream=True, verify=False, allow_redirects=True) as r:
            if r.status_code != 200: return False
            return True
    except: return False

def kanal_isleme(kanal_metni, kaynak_url, eklenen_urller):
    satir_grubu = kanal_metni.strip().split('\n')
    if len(satir_grubu) < 2: return None
    
    ext_satiri = satir_grubu[0]
    link_satiri = satir_grubu[-1].strip()
    
    # 🎯 1. PATRON LİSTESİNE TAM GÜVEN (Filtre yok, test yok, değişiklik yok)
    if "patron.m3u" in kaynak_url.lower():
        if link_satiri in eklenen_urller: return None
        # Hiçbir isimlendirme yapma, olduğu gibi gönder
        return f"{ext_satiri}\n{link_satiri}"

    # --- 2. DİĞER YEDEKLER İÇİN SIKI KONTROL ---
    if link_satiri in eklenen_urller: return None
    if any(yasak.lower() in ext_satiri.lower() for yasak in YASAKLI_GRUPLAR): return None

    # Diğer kaynaklar teste tabi
    if link_saglam_mi(link_satiri):
        return f"{ext_satiri}\n{link_satiri}"
    
    return None

def main():
    print(f"🛡️  USTA SİSTEM V9.5: Patron'a Tam Güven Sürümü Aktif!")
    
    if os.path.exists(FILE_PATH):
        shutil.copyfile(FILE_PATH, FILE_PATH + ".bak")

    avlananlar = github_taze_link_avla()
    guncel_kaynak_listesi = list(set(YEDEK_KAYNAKLAR + avlananlar))
    
    eklenen_urller = set()
    ana_liste_zirh = []
    
    # Mevcut listeyi koru
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_lines = f.readlines()
            ana_liste_zirh = tum_lines[:ZIRH_LIMIT]
            for s in ana_liste_zirh:
                if s.strip().startswith("http"):
                    eklenen_urller.add(s.strip())

    ham_bulunanlar = []
    for kaynak in guncel_kaynak_listesi:
        try:
            print(f"📡 Kaynak Okunuyor: {kaynak[:60]}...")
            r = requests.get(kaynak, headers=HEADERS, timeout=15, verify=False, allow_redirects=True)
            if r.status_code in [200, 301, 302]:
                # Regex ile blokları yakala
                bulunan = re.findall(r"(#EXTINF:.*?\n+https?.*?)(?=#EXTINF|$)", r.text, re.DOTALL | re.IGNORECASE)
                for b in bulunan:
                    ham_bulunanlar.append((b, kaynak))
        except: continue

    print(f"🔍 {len(ham_bulunanlar)} kanal işleniyor (Patron'a dokunulmazlık verildi)...")

    final_listesi = []
    # Sırayla işle (Patron kanalları en başa eklemek için listeyi ters çevirebilirsin ama işlem sırası önemli değil)
    for k, kaynak_url in ham_bulunanlar:
        sonuc = kanal_isleme(k, kaynak_url, eklenen_urller)
        if sonuc:
            final_listesi.append(sonuc)
            eklenen_urller.add(sonuc.split('\n')[-1].strip())

    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(ana_liste_zirh)
        f.write(f"\n# --- GÜNCEL LİSTE ({datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}) --- #\n")
        for k in final_listesi:
            f.write(k + "\n")

    print(f"\n🏁 İŞLEM BİTTİ! Patron kanalları olduğu gibi eklendi.")

if __name__ == "__main__":
    main()
