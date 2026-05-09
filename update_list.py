import requests
import re
import os
import datetime
import shutil
import time
from concurrent.futures import ThreadPoolExecutor
import urllib3

# SSL hatalarını sustur
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
ZIRH_LIMIT = 3891
THREADS = 4        

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

# --- SENİN TAM YASAKLI LİSTEN (Eksiksiz) ---
YASAKLI_GRUPLAR = [
    "FreeShot", "Webteizle", "TR FILM", "ARZU FILM", "ERLER FILM", 
    "Taşacak Bu Deniz", "EZEL", "FilmMedya", "Keloğlan", "PolskieTV", 
    "MediabayTV", "SarkorTV", "GLWIZ", "PERSIAN", "GledaiTV", "RDS TV", 
    "TouchTV", "Slovakia", "Bulgaria", "Romania", "Azerbeycan",
    "Superxfilm", "CINEMAMOD", "Adult", "XXX"
]

YEDEK_KAYNAKLAR = [
    "https://streams.uzunmuhalefet.com/lists/tr.m3u",
    "https://tinyurl.com/ytpatron",
    "https://urlz.fr/v1Xo",
    "https://raw.githubusercontent.com/hayatiptv/iptv/master/index.m3u",
    "https://raw.githubusercontent.com/smartgmr/cdn/refs/heads/main/Perfect.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://files.manuscdn.com/user_upload_by_module/session_file/310519663091167371/lXQCJEWGepXILedX.m3u8",
    "https://tinyurl.com/bdd2tz6h",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u"
]

def github_taze_link_avla():
    """GITHUB'DA SON 48 SAATTE PAYLAŞILAN TAZE LİNKLERİ BULUR"""
    yeni_kaynaklar = []
    # Son 2 günün tarihini alarak daha geniş ama taze bir tarama yapar
    tarih = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
    search_url = f"https://api.github.com/search/code?q=extension:m3u+trt1+pushed:>{tarih}&sort=indexed"
    
    try:
        print(f"🕵️  GitHub'da derin arama yapılıyor (Filtre: >{tarih})...")
        r = requests.get(search_url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            items = r.json().get('items', [])
            for item in items:
                # GitHub linkini RAW (ham) linke çevirme işlemi
                raw = item['html_url'].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
                yeni_kaynaklar.append(raw)
                if len(yeni_kaynaklar) >= 10: break # En taze 10 kaynağı yakala
    except:
        print("⚠️  GitHub API limiti veya bağlantı sorunu. Mevcut listeden devam ediliyor.")
    
    return yeni_kaynaklar

def link_saglam_mi(url):
    """DERİN KONTROL: VERİ AKIŞI TESTİ"""
    try:
        with requests.get(url, headers=HEADERS, timeout=10, stream=True, verify=False) as r:
            if r.status_code != 200: return False
            # İlk 1KB veriyi oku, m3u8 veya stream yapısı var mı bak
            content_start = next(r.iter_content(chunk_size=1024)).decode('utf-8', errors='ignore')
            if "#EXTM3U" in content_start or "#EXT-X-STREAM-INF" in content_start or r.headers.get('Content-Type', '').startswith('video/'):
                return True
            return False
    except: return False

def kanal_isleme(kanal_metni, eklenen_urller):
    satir_grubu = kanal_metni.strip().split('\n')
    if len(satir_grubu) < 2: return None
    
    ext_satiri = satir_grubu[0]
    link_satiri = satir_grubu[-1].strip()
    
    # 1. Mükerrer Kontrolü
    if link_satiri in eklenen_urller: return None

    # 2. Yasaklı Filtresi (TAM LİSTE)
    if any(yasak.lower() in ext_satiri.lower() for yasak in YASAKLI_GRUPLAR):
        return None

    # 3. Canlılık Testi
    if link_saglam_mi(link_satiri):
        # İsim Temizleme (HEVC, 4K vb. temizle)
        isim_temiz = re.sub(r'\s*\|\s*[A-Z0-9+]+\b', '', ext_satiri)
        isim_temiz = re.sub(r'\b(HEVC|RAW|PLUS|HD|FHD|SD|UHD|4K)\b', '', isim_temiz, flags=re.I)
        
        print(f" ✅ CANLI: {link_satiri[:45]}...")
        return f"{isim_temiz}\n{link_satiri}"
    
    return None

def main():
    print(f"🛡️  USTA SİSTEM: Derin temizlik ve taze av başlıyor!")
    
    if os.path.exists(FILE_PATH):
        shutil.copyfile(FILE_PATH, FILE_PATH + ".bak")

    # 1. Taze kaynakları avla ve birleştir
    avlananlar = github_taze_link_avla()
    guncel_kaynak_listesi = list(set(YEDEK_KAYNAKLAR + avlananlar))
    
    eklenen_urller = set()
    ana_liste_zirh = []
    ham_bulunanlar = []

    # Zırhı ve Mevcut Linkleri Oku
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_lines = f.readlines()
            ana_liste_zirh = tum_lines[:ZIRH_LIMIT]
            for s in ana_liste_zirh:
                if s.strip().startswith("http"):
                    eklenen_urller.add(s.strip())

    # 2. Kaynakları Tara
    for kaynak in guncel_kaynak_listesi:
        try:
            print(f"📡 Kaynak Okunuyor: {kaynak[:50]}...")
            r = requests.get(kaynak, headers=HEADERS, timeout=12, verify=False)
            if r.status_code == 200:
                bulunan = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", r.text, re.DOTALL)
                ham_bulunanlar.extend(bulunan)
        except: continue

    # 3. Mükerrerleri Ele ve Test Et
    unique_adaylar = []
    gorulen_linkler = set()
    for k in ham_bulunanlar:
        link = k.strip().split('\n')[-1].strip()
        if link not in eklenen_urller and link not in gorulen_linkler:
            unique_adaylar.append(k)
            gorulen_linkler.add(link)

    print(f"🔍 {len(unique_adaylar)} yeni aday bulundu. Derin test yapılıyor...")

    # 4. Çoklu Test (Threads: 4)
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        results = list(executor.map(lambda k: kanal_isleme(k, eklenen_urller), unique_adaylar))
        final_listesi = [r for r in results if r is not None]

    # 5. Dosyaya Yaz
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(ana_liste_zirh)
        f.write(f"\n# --- DERİN TEMİZLİK VE TAZE AV ({datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}) --- #\n")
        for k in final_listesi:
            f.write(k + "\n")

    print(f"\n🏁 BİTTİ USTA! {len(final_listesi)} yeni sağlam kanal eklendi.")

if __name__ == "__main__":
    main()
