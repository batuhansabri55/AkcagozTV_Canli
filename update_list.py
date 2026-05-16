import requests
import re
import os
import datetime
import shutil
from concurrent.futures import ThreadPoolExecutor
import urllib3
import yt_dlp

# SSL hatalarını tamamen sustur
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- AYARLAR (TAM İSTEDİĞİN GİBİ BURADA USTA) ---
FILE_PATH = "tr.m3u"
ZIRH_LIMIT = 3950
THREADS = 4        

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

# --- DOKUNULMAZ YOUTUBE CANLI YAYIN LİSTESİ ---
YOUTUBE_KANALLAR = {
    "Sozcu TV": "https://www.youtube.com/@SozcuTelevizyonu/live",
    "CNN Turk": "https://www.youtube.com/@cnnturk/live",
    "HaberTurk": "https://www.youtube.com/@haberturk/live",
    "NTV": "https://www.youtube.com/@NTV/live",
    "Haber Global": "https://www.youtube.com/@HaberGlobal/live",
    "TV100": "https://www.youtube.com/@tv100/live",
    "TV NET": "https://www.youtube.com/@tvnet/live"
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

def youtube_link_coz(isim, url):
    """YouTube canlı yayın linkini IPTV oynatıcıların açacağı m3u8 formatına çevirir"""
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'socket_timeout': 10
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            canli_url = info.get('manifest_url') or info.get('url')
            if canli_url:
                print(f"  🟢 YouTube Çözüldü: {isim}")
                return f'#EXTINF:-1 tvg-name="{isim}" group-title="YouTube Canli",{isim}\n{canli_url}\n'
    except:
        print(f"  ❌ YouTube Çözülemedi: {isim}")
    return ""

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
    print(f"🛡️  USTA SİSTEM V4: Tavizsiz temizlik ve Zırh Limiti ({ZIRH_LIMIT}) devrede!")
    
    if os.path.exists(FILE_PATH):
        shutil.copyfile(FILE_PATH, FILE_PATH + ".bak")

    eklenen_urller = set()
    ana_liste_zirh = []

    # --- 1. ADIM: MEVCUT DOSYADAKİ ZIRHLI ALANI KORU ---
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_lines = f.readlines()
            # Senin orijinal ZIRH_LIMIT mantığın aynen korundu
            ana_liste_zirh = tum_lines[:ZIRH_LIMIT]
            for s in ana_liste_zirh:
                if s.strip().startswith("http"):
                    eklenen_urller.add(s.strip())

    # --- 2. ADIM: DOKUNULMAZ YOUTUBE KANALLARINI ÇÖZ VE EKLE ---
    print("\n📺 Dokunulmaz YouTube Canlı Yayınları Çözülüyor...")
    youtube_blok = ""
    for isim, url in YOUTUBE_KANALLAR.items():
        kanal_m3u_metni = youtube_link_coz(isim, url)
        if kanal_m3u_metni:
            cozulmus_url = kanal_m3u_metni.strip().split('\n')[-1].strip()
            # Eğer bu youtube linki zırhlı alanda veya eklenenlerde yoksa bloğa ekle
            if cozulmus_url not in eklenen_urller:
                youtube_blok += kanal_m3u_metni
                eklenen_urller.add(cozulmus_url)

    # --- 3. ADIM: İNTERNETTEN TAZE LİNKLERİ TOPLA ---
    avlananlar = github_taze_link_avla()
    guncel_kaynak_listesi = list(set(YEDEK_KAYNAKLAR + avlananlar))
    ham_bulunanlar = []

    for kaynak in guncel_kaynak_listesi:
        try:
            print(f"📡 Kaynak Okunuyor: {kaynak[:50]}...")
            r = requests.get(kaynak, headers=HEADERS, timeout=10, verify=False)
            if r.status_code == 200:
                bulunan = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", r.text, re.DOTALL)
                ham_bulunanlar.extend(bulunan)
        except: continue

    # --- 4. ADIM: MÜKERRER KONTROLÜ ---
    unique_adaylar = []
    gorulen_linkler = set()
    for k in ham_bulunanlar:
        link = k.strip().split('\n')[-1].strip()
        if link not in eklenen_urller and link not in gorulen_linkler:
            unique_adaylar.append(k)
            gorulen_linkler.add(link)

    print(f"🔍 {len(unique_adaylar)} yeni benzersiz aday izlemeye alındı. Threads: {THREADS} ile test başlıyor...")

    # --- 5. ADIM: ÇOKLU İŞ PARÇACIĞI TESTİ ---
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        results = list(executor.map(lambda k: kanal_isleme(k, eklenen_urller), unique_adaylar))
        final_listesi = [r for r in results if r is not None]

    # --- 6. ADIM: DOSYAYA YAZMA (ZIRH + YOUTUBE + YENİ LİNKLER) ---
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        # Eğer dosya tamamen boşsa veya yeni açılıyorsa #EXTM3U koy
        if not ana_liste_zirh:
            f.write("#EXTM3U\n")
        else:
            f.writelines(ana_liste_zirh)
            
        # Çözülen güncel YouTube kanallarını zırhın hemen altına basıyoruz
        if youtube_blok:
            f.write("\n# --- GÜNCEL YOUTUBE CANLI YAYINLARI --- #\n")
            f.write(youtube_blok)
            
        f.write(f"\n# --- TAVİZSİZ GERÇEK TEMİZLİK ({datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}) --- #\n")
        for k in final_listesi:
            f.write(k + "\n")

    print(f"\n🏁 İŞLEM BİTTİ USTA! Zırh korundu, YouTube güncellendi ve süzgeçten geçen {len(final_listesi)} yeni kanal eklendi.")

if __name__ == "__main__":
    main()
