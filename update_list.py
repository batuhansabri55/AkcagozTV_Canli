import requests
import re
import os
import datetime
import shutil
from concurrent.futures import ThreadPoolExecutor
import urllib3
import yt_dlp  # Usta, YouTube için eklediğimiz yeni canavar modül

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

# --- YENİ: YOUTUBE HABER KANALLARI ADRESLERİ ---
YOUTUBE_KANALLAR = {
    "Sozcu TV": "https://www.youtube.com/@SozcuTelevizyonu/live",
    "CNN Turk": "https://www.youtube.com/@cnnturk/live",
    "HaberTurk": "https://www.youtube.com/@haberturk/live",
    "NTV": "https://www.youtube.com/@NTV/live",
    "Haber Global": "https://www.youtube.com/@HaberGlobal/live",
    "TV100": "https://www.youtube.com/@tv100/live",
    "TV NET": "https://www.youtube.com/@tvnet/live"
}

def youtube_linkleri_al():
    """YOUTUBE CANLI YAYIN SAYFALARINDAN ANLIK .M3U8 AKIŞLARINI ÇÖZER"""
    linkler = {}
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False
    }
    
    print("\n🚀 YouTube Canlı Yayın Linkleri Çözülüyor...")
    for isim, url in YOUTUBE_KANALLAR.items():
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                stream_url = info.get('url')
                if stream_url:
                    linkler[isim] = stream_url
                    print(f"   🟢 {isim} başarıyla çözüldü.")
        except Exception as e:
            print(f"   ❌ {isim} çözülemedi (Kanal yayında olmayabilir): {e}")
    return linkler

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
    """ULTRA KUSURSUZ SÜZGEÇ"""
    try:
        with requests.get(url, headers=HEADERS, timeout=4, stream=True, verify=False) as r:
            if r.status_code != 200: 
                return False
            
            content_type = r.headers.get('Content-Type', '').lower()
            
            if 'text/html' in content_type or 'application/json' in content_type:
                return False
                
            try:
                chunk = next(r.iter_content(chunk_size=2048))
            except StopIteration:
                return False
                
            if len(chunk) < 200:
                return False

            content_text = chunk.decode('utf-8', errors='ignore').lower()

            if "#extm3u" in content_text:
                has_video_chunks = any(ext in content_text for ext in [".ts", ".m3u8", ".mp4", ".aac"])
                satir_sayisi = len(content_text.strip().split('\n'))
                if has_video_chunks and satir_sayisi >= 4:
                    return True
                return False
            
            hata_kelimeleri = ["expired", "invalid", "error", "forbidden", "unauthorized", "not found", "bad token"]
            if any(hata in content_text for hata in hata_kelimeleri):
                return False
            
            if 'video/' in content_type or 'mpegurl' in content_type or 'stream' in content_type or 'octet-stream' in content_type:
                return True
                
            return False
    except: 
        return False

def kanal_isleme(kanal_metni, eklenen_urller):
    satir_grubu = kanal_metni.strip().split('\n')
    if len(satir_grubu) < 2: return None
    
    ext_satiri = satir_grubu[0]
    link_satiri = satir_grubu[-1].strip()
    
    if link_satiri in eklenen_urller: return None

    if any(yasak.lower() in ext_satiri.lower() for yasak in YASAKLI_GRUPLAR):
        return None

    if link_saglam_mi(link_satiri):
        isim_temiz = re.sub(r'\s*\|\s*[A-Z0-9+]+\b', '', ext_satiri)
        isim_temiz = re.sub(r'\b(HEVC|RAW|PLUS|HD|FHD|SD|UHD|4K)\b', '', isim_temiz, flags=re.I)
        isim_temiz = re.sub(r'\s+YEDEK', 'YEDEK', isim_temiz, flags=re.IGNORECASE)
        
        print(f" ✅ GERÇEK CANLI: {link_satiri[:50]}...")
        return f"{isim_temiz}\n{link_satiri}"
    
    return None

def main():
    print(f"🛡️  USTA SİSTEM V3: Tavizsiz temizlik ve gerçek canlı yayın avı başlıyor!")
    
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
            # Eğer dosya boş değilse ve ilk satır #EXTM3U değilse ekleyelim
            if tum_lines and not tum_lines[0].strip().startswith("#EXTM3U"):
                ana_liste_zirh.append("#EXTM3U\n")
            
            ana_liste_zirh.extend(tum_lines[:ZIRH_LIMIT])
            for s in ana_liste_zirh:
                if s.strip().startswith("http"):
                    eklenen_urller.add(s.strip())
    else:
        ana_liste_zirh.append("#EXTM3U\n")

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

    # --- YENİ: YOUTUBE LİNKLERİNİ ÇEKME ADIMI ---
    yt_linkleri = youtube_linkleri_al()

    # 4. Dosyaya Yaz (Zırh + Filtreleri geçenler + En son taze YouTube Haber Kanalları)
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(ana_liste_zirh)
        f.write(f"\n# --- TAVİZSİZ GERÇEK TEMİZLİK ({datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}) --- #\n")
        
        # Süzgeçten geçen standart kanalları yaz
        for k in final_listesi:
            f.write(k + "\n")
            
        # En alta her zaman güncel kalacak YouTube Haber paketini ekle usta
        if yt_linkleri:
            f.write("\n# --- YOUTUBE CANLI HABER PAKETİ --- #\n")
            for isim, link in yt_linkleri.items():
                f.write(f'#EXTINF:-1 tvg-name="{isim}" group-title="YouTube Haber",{isim}\n')
                f.write(f"{link}\n")

    print(f"\n🏁 İŞLEM BİTTİ USTA! Sağlam {len(final_listesi)} standart kanal ve {len(yt_linkleri)} YouTube haber kanalı başarıyla eklendi.")

if __name__ == "__main__":
    main()
