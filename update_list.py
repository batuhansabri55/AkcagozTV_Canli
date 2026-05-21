import requests
import re
import os
import datetime
import shutil
from concurrent.futures import ThreadPoolExecutor
import urllib3

# SSL hatalarını tamamen sustur
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
ZIRH_LIMIT = 3950
THREADS = 4        

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

# --- YASAKLI VE YEDEK LİSTELERİ ---
# Not: Uluslararası belgesel kanallarının (Nat Geo, Discovery vb.) silinmemesi için 
# "YASAKLI_GRUPLAR" listesindeki genel yabancı ülke isimleri filtrenizle çakışmıyor, gayet temiz.
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
    "https://tinyurl.com/bdd2tz6h",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    
    # --- NOKTA ATIŞI BELGESEL KAYNAKLARI ---
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/categories/documentary.m3u",
    "https://iptv-org.github.io/iptv/categories/documentary.m3u"
]

def github_taze_link_avla():
    """GITHUB'DA SON 48 SAATTE PAYLAŞILAN TAZE LİNKLERİ BULUR"""
    yeni_kaynaklar = []
    tarih = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
    
    # Sadece trt1 değil, belgesel arayan güncel depoları da radara alıyoruz
    arama_terimleri = ["trt1", "documentary", "belgesel"]
    
    for terim in arama_terimleri:
        search_url = f"https://api.github.com/search/code?q=extension:m3u+{terim}+pushed:>{tarih}&sort=indexed"
        try:
            print(f"🕵️  GitHub'da derin arama yapılıyor (Filtre: {terim} >{tarih})...")
            r = requests.get(search_url, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                items = r.json().get('items', [])
                for item in items:
                    raw = item['html_url'].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
                    if raw not in yeni_kaynaklar:
                        yeni_kaynaklar.append(raw)
                    if len(yeni_kaynaklar) >= 15: break # Kotayı biraz esnettik
        except:
            print(f"⚠️  GitHub API limiti veya bağlantı sorunu ({terim}).")
            continue
            
    return yeni_kaynaklar[:12]

def link_saglam_mi(url):
    """
    MODİFİYELİ ULTRA KUSURSUZ SÜZGEÇ: 
    Yavaş açılan canlı yayınları öldürmez, sahte 200 OK veren token tuzaklarını imha eder.
    """
    try:
        # Önce hızlıca bir HEAD isteği atıp sunucu durumuna bakıyoruz (Trafiği ve zamanı korur)
        h = requests.head(url, headers=HEADERS, timeout=3, verify=False, allow_redirects=True)
        if h.status_code != 200:
            return False
            
        content_type = h.headers.get('Content-Type', '').lower()
        
        # HTML veya JSON ise bu bir hata/panel sayfasıdır, direkt ele
        if 'text/html' in content_type or 'application/json' in content_type:
            return False
            
        # Akış testi için GET isteği (Bağlantı kilitlenmelerini önlemek için stream=True)
        with requests.get(url, headers=HEADERS, timeout=4, stream=True, verify=False, allow_redirects=True) as r:
            if r.status_code != 200: 
                return False
                
            # Sunucudan gelen ilk ufak veriyi güvenli oku (Çökme/Zaman aşımı korumalı)
            try:
                # ham stream'den maksimum 1024 bayt oku (Daha hızlı ve güvenli)
                chunk = r.raw.read(1024)
            except:
                return False
                
            if not chunk or len(chunk) < 10:
                return False

            content_text = chunk.decode('utf-8', errors='ignore').lower()

            # --- M3U8 VEYA TEXT TABANLI LİSTE KONTROLÜ ---
            if "#extm3u" in content_text or "#extinf" in content_text:
                # Eğer alt alta dizilmiş m3u8 ise geçerli say
                if any(ext in content_text for ext in [".ts", ".m3u8", ".mp4", "http"]):
                    return True
                return False
            
            # --- DİREKT TS / STREAM AKIŞI KONTROLÜ ---
            # Token patlamışsa ekranda hata kelimeleri yazar, onları yakala
            hata_kelimeleri = ["expired", "invalid", "error", "forbidden", "unauthorized", "not found", "bad token", "denied"]
            if any(hata in content_text for hata in hata_kelimeleri):
                return False
            
            # Video akış türü doğrulaması
            if any(t in content_type for t in ['video/', 'mpegurl', 'stream', 'octet-stream']):
                return True
                
            # Eğer TS video akışı ise ham veri (binary) içinde "G" (0x47) Sync byte kontrolü
            if chunk.startswith(b'\x47') or b'\x47' in chunk[:188]:
                return True

            return False
    except: 
        return False

def kanal_isleme(kanal_metni, eklenen_urller):
    satir_grubu = kanal_metni.strip().split('\n')
    if len(satir_grubu) < 2: return None
    
    ext_satiri = satir_grubu[0]
    link_satiri = satir_grubu[-1].strip()
    
    # 1. Mükerrer Kontrolü
    if link_satiri in eklenen_urller: return None

    # 2. Yasaklı Filtresi
    if any(yasak.lower() in ext_satiri.lower() for yasak in YASAKLI_GRUPLAR):
        return None

    # 3. KUSURSUZ Canlılık Testi
    if link_saglam_mi(link_satiri):
        # İsim Temizleme (HEVC, 4K vb. temizle)
        isim_temiz = re.sub(r'\s*\|\s*[A-Z0-9+]+\b', '', ext_satiri)
        isim_temiz = re.sub(r'\b(HEVC|RAW|PLUS|HD|FHD|SD|UHD|4K)\b', '', isim_temiz, flags=re.I)
        
        # YEDEK kanallar için boşluk silme ve bitişik yazma kuralı (Örn: TRT1 YEDEK -> TRT1YEDEK)
        isim_temiz = re.sub(r'\s+YEDEK', 'YEDEK', isim_temiz, flags=re.IGNORECASE)
        
        print(f" ✅ GERÇEK CANLI: {link_satiri[:50]}...")
        return f"{isim_temiz}\n{link_satiri}"
    
    return None

def main():
    print(f"🛡️  USTA SİSTEM V3.1: Belgesel Takviyeli Canlı Yayın Avı Başlıyor!")
    
    if os.path.exists(FILE_PATH):
        shutil.copyfile(FILE_PATH, FILE_PATH + ".bak")

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

    # 1. Kaynakları Tara
    for kaynak in guncel_kaynak_listesi:
        try:
            print(f"📡 Kaynak Okunuyor: {kaynak[:50]}...")
            r = requests.get(kaynak, headers=HEADERS, timeout=10, verify=False)
            if r.status_code == 200:
                bulunan = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", r.text, re.DOTALL)
                ham_bulunanlar.extend(bulunan)
        except: continue

    # 2. Mükerrerleri Ele
    unique_adaylar = []
    gorulen_linkler = set()
    for k in ham_bulunanlar:
        link = k.strip().split('\n')[-1].strip()
        if link not in eklenen_urller and link not in gorulen_linkler:
            unique_adaylar.append(k)
            gorulen_linkler.add(link)

    print(f"🔍 {len(unique_adaylar)} yeni benzersiz aday izlemeye alındı. Tavizsiz test başlıyor...")

    # 3. Çoklu Test (Threads: 4)
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        results = list(executor.map(lambda k: kanal_isleme(k, eklenen_urller), unique_adaylar))
        final_listesi = [r for r in results if r is not None]

    # 4. Dosyaya Yaz
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(ana_liste_zirh)
        f.write(f"\n# --- TAVİZSİZ GERÇEK TEMİZLİK ({datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}) --- #\n")
        for k in final_listesi:
            f.write(k + "\n")

    print(f"\n🏁 İŞLEM BİTTİ USTA! Filtreleri aşabilen gerçek anlamda SAĞLAM {len(final_listesi)} kanal eklendi.")

if __name__ == "__main__":
    main()
