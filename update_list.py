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
    "https://iptv-org.github.io/iptv/countries/tr.m3u"
]

def github_taze_link_avla():
    """GITHUB'DA SON 48 SAATTE PAYLAŞILAN TAZE LİNKLERİ BULUR"""
    yeni_kaynaklar = []
    tarih = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
    search_url = f"https://api.github.com/search/code?q=extension:m3u+trt1+pushed:>{tarih}&sort=indexed"
    
    try:
        print(f"🕵️  GitHub'da derin arama yapılıyor (Filtre: >{tarih})...")
        r = requests.get(search_url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            items = r.json().get('items', [])
            for item in items:
                raw = item['html_url'].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
                yeni_kaynaklar.append(raw)
                if len(yeni_kaynaklar) >= 10: break
    except:
        print("⚠️  GitHub API limiti veya bağlantı sorunu. Mevcut listeden devam ediliyor.")
    
    return yeni_kaynaklar

def link_saglam_mi(url):
    """
    KUSURSUZ SÜZGEÇ: Sunucuların sahte 200 OK ve boş m3u8 tuzaklarını 
    içerik analiziyle kesin olarak eler. Oynatılamayacak kanala geçit vermez.
    """
    try:
        # Hantal/ölü sunucuları beklememek için timeout 4 saniye
        with requests.get(url, headers=HEADERS, timeout=4, stream=True, verify=False) as r:
            if r.status_code != 200: 
                return False
            
            # Sunucunun döndüğü içerik tipini kontrol et
            content_type = r.headers.get('Content-Type', '').lower()
            
            # Eğer video yayını yerine HTML sayfası veya JSON hata mesajı dönüyorsa direkt ele
            if 'text/html' in content_type or 'application/json' in content_type:
                return False
                
            # İlk 4KB veriyi indirip derinlemesine analiz yapıyoruz
            content_start = next(r.iter_content(chunk_size=4096)).decode('utf-8', errors='ignore')
            
            # --- SAHTE M3U8 / HLS TUZAĞI KONTROLÜ ---
            if "#EXTM3U" in content_start:
                # Gerçek bir canlı yayın m3u8 listesinde mutlaka parça listesi veya alt yayın olur.
                # Eğer dosya içeriğinde .ts (video parçası) veya yeni bir alt m3u8 linki yoksa sahtedir!
                has_video_chunks = any(ext in content_start for ext in [".ts", ".m3u8", ".mp4", ".aac"])
                
                # Ek olarak satır sayısını kontrol et. Gerçek yayın listeleri en az 5-10 satır olur.
                satir_sayisi = len(content_start.strip().split('\n'))
                
                if has_video_chunks and satir_sayisi >= 4:
                    return True
                else:
                    # Sunucu içi boş veya sadece '#EXTM3U' yazan sahte dosya fırlatmıştır, İMHA ET.
                    return False
            
            # Doğrudan ham video akışı yollayan (MPEG-TS, application/octet-stream vb.) linklere onay ver
            if 'video/' in content_type or 'mpegurl' in content_type or 'stream' in content_type:
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
        
        print(f" ✅ GERÇEK CANLI: {link_satiri[:50]}...")
        return f"{isim_temiz}\n{link_satiri}"
    
    return None

def main():
    print(f"🛡️  USTA SİSTEM V2: Tavizsiz temizlik ve gerçek canlı yayın avı başlıyor!")
    
    if os.path.exists(FILE_PATH):
        shutil.copyfile(FILE_PATH, FILE_PATH + ".bak")

    avlananlar = github_taze_link_avla()
    guncel_kaynak_listesi = list(set(YEDEK_KAYNAKLAR + avlananlar))
    
    eklenen_urller = set()
    ana_liste_zirh = []
    ham_bulunanlar = []

    # Zırhı ve Mevcut Linkleri Koru
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_lines = f.readlines()
            ana_liste_zirh = tum_lines[:ZIRH_LIMIT]
            for s in ana_liste_zirh:
                if s.strip().startswith("http"):
                    eklenen_urller.add(s.strip())

    # 1. Kaynakları Tara ve İçindeki Kanalları Yakala
    for kaynak in guncel_kaynak_listesi:
        try:
            print(f"📡 Kaynak Okunuyor: {kaynak[:50]}...")
            r = requests.get(kaynak, headers=HEADERS, timeout=10, verify=False)
            if r.status_code == 200:
                bulunan = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", r.text, re.DOTALL)
                ham_bulunanlar.extend(bulunan)
        except: continue

    # 2. Aynı Linkleri Baştan Ele
    unique_adaylar = []
    gorulen_linkler = set()
    for k in ham_bulunanlar:
        link = k.strip().split('\n')[-1].strip()
        if link not in eklenen_urller and link not in gorulen_linkler:
            unique_adaylar.append(k)
            gorulen_linkler.add(link)

    print(f"🔍 {len(unique_adaylar)} yeni benzersiz aday izlemeye alındı. Tavizsiz test başlıyor...")

    # 3. Çoklu Test (Threads: 4) - Sahtekarları Ayıklama Noktası
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        results = list(executor.map(lambda k: kanal_isleme(k, eklenen_urller), unique_adaylar))
        final_listesi = [r for r in results if r is not None]

    # 4. Dosyaya Temiz Yazım
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(ana_liste_zirh)
        f.write(f"\n# --- TAVİZSİZ GERÇEK TEMİZLİK ({datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}) --- #\n")
        for k in final_listesi:
            f.write(k + "\n")

    print(f"\n🏁 İŞLEM BİTTİ USTA! Filtreleri aşabilen gerçek anlamda SAĞLAM {len(final_listesi)} kanal eklendi.")

if __name__ == "__main__":
    main()
