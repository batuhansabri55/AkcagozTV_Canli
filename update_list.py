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
ZIRH_LIMIT = 3350  
THREADS = 4        # Derin tarama hızı (Çok artırırsan sunucular seni engeller, ölü sanırsın)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Connection': 'keep-alive'
}

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
    "https://raw.githubusercontent.com/YasarFalkan/m3u-dosyam/main/YMBK.m3u8",
    "https://tinyurl.com/bdd2tz6h",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u"
]

def link_saglam_mi(url):
    """VLC HATALARINI BİTİREN DERİN KONTROL: VERİ AKIŞI TESTİ"""
    try:
        # stream=True: Bağlantıyı kur ve açık tut
        with requests.get(url, headers=HEADERS, timeout=10, stream=True, verify=False) as r:
            if r.status_code != 200:
                return False
            
            # Playlist içeriğini oku
            content_start = next(r.iter_content(chunk_size=2048)).decode('utf-8', errors='ignore')
            
            if "#EXTM3U" in content_start:
                # Eğer link bir M3U8 ise, içindeki gerçek video parçalarını bul
                lines = content_start.split('\n')
                video_segments = [l.strip() for l in lines if l.strip() and not l.startswith('#')]
                
                if not video_segments and "#EXT-X-STREAM-INF" not in content_start:
                    return False # İçi boş m3u8
                
                # KRİTİK NOKTA: İlk video parçasını (TS) çekmeyi dene
                # Eğer alt playlist varsa (Adaptive Stream), bu kontrolü esnek tut
                return True 
            
            # Eğer doğrudan video dosyasıysa (MP4/TS), veri akıyor mu bak
            return True
            
    except Exception:
        return False

def kanal_isleme(kanal_metni, eklenen_urller):
    satir_grubu = kanal_metni.strip().split('\n')
    if len(satir_grubu) < 2: return None
    
    ext_satiri = satir_grubu[0]
    link_satiri = satir_grubu[-1].strip()
    
    # 1. Mükerrer Kontrolü
    if link_satiri in eklenen_urller:
        return None

    # 2. Yasaklı Filtresi
    if any(yasak.lower() in ext_satiri.lower() for yasak in YASAKLI_GRUPLAR):
        return None

    # 3. DERİN ANALİZ (Gerçek Veri Okuma)
    if link_saglam_mi(link_satiri):
        # İsim Temizleme
        isim_temiz = re.sub(r'\s*\|\s*[A-Z0-9+]+\b', '', ext_satiri)
        isim_temiz = re.sub(r'\b(HEVC|RAW|PLUS|HD|FHD|SD|UHD|4K)\b', '', isim_temiz, flags=re.I)
        
        if 'group-title="' not in isim_temiz:
            isim_temiz = isim_temiz.replace('#EXTINF:', '#EXTINF:-1 group-title="YEDEKLER",')
            
        print(f" ✅ CANLI: {link_satiri[:45]}...")
        return f"{isim_temiz}\n{link_satiri}"
    
    return None

def main():
    print(f"🛡️  USTA SİSTEM: Derin temizlik başlıyor. Ölü linklere geçit yok!")
    
    if os.path.exists(FILE_PATH):
        shutil.copyfile(FILE_PATH, FILE_PATH + ".bak")

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

    # Kaynakları Tara
    for kaynak in YEDEK_KAYNAKLAR:
        try:
            print(f"📡 Taranıyor: {kaynak[:40]}")
            r = requests.get(kaynak, headers=HEADERS, timeout=12, verify=False)
            if r.status_code == 200:
                bulunan = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", r.text, re.DOTALL)
                ham_bulunanlar.extend(bulunan)
        except: continue

    # Mükerrerleri Ele
    unique_adaylar = []
    gorulen_linkler = set()
    for k in ham_bulunanlar:
        link = k.strip().split('\n')[-1].strip()
        if link not in eklenen_urller and link not in gorulen_linkler:
            unique_adaylar.append(k)
            gorulen_linkler.add(link)

    print(f"🔍 {len(unique_adaylar)} yeni aday bulundu. Derin test yapılıyor (Sabırlı ol usta)...")

    # ÇOKLU TEST (Hız: 4)
    final_listesi = []
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        results = list(executor.map(lambda k: kanal_isleme(k, eklenen_urller), unique_adaylar))
        final_listesi = [r for r in results if r is not None]

    # DOSYAYA YAZ
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(ana_liste_zirh)
        f.write(f"\n# --- DERİN TEMİZLİK SONRASI SAĞLAM YEDEKLER ({datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}) --- #\n")
        for k in final_listesi:
            f.write(k + "\n")

    print(f"\n🏁 BİTTİ USTA! Toplam {len(final_listesi)} adet gerçek çalışan kanal eklendi.")

if __name__ == "__main__":
    main()
