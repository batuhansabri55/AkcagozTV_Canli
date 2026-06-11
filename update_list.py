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
THREADS = 64         # 5600 link için tam güç hız ayarı!

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

# ⚠️ USTA ÖZEL AYARI: Tamamı patlak olan ve süzgeci yanıltan sunucu IP'leri
YASAKLI_IP_LISTESI = [
    "87.121.104.29:1071"
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
            print(f"🕵️  GitHub'da derin arama yapılıyor (Filtre: {terim} >{tarih})...")
            r = requests.get(search_url, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                items = r.json().get('items', [])
                for item in items:
                    raw = item['html_url'].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
                    if raw not in yeni_kaynaklar:
                        yeni_kaynaklar.append(raw)
                    if len(yeni_kaynaklar) >= 15: break
        except:
            print(f"⚠️  GitHub API limiti veya bağlantı sorunu ({terim}).")
            continue
            
    return yeni_kaynaklar[:12]

def link_saglam_mi(url):
    """XTREAM VE WORKER HİLELERİNİ SIFIRLAYAN ULTRA V6 AKIŞ SÜZGECİ"""
    if "atv-switch" in url.lower() or "vizitv" in url.lower():
        return True

    try:
        # 1. AŞAMA: Bağlantı ve İçerik Türü Kontrolü
        with requests.get(url, headers=HEADERS, timeout=5, stream=True, verify=False, allow_redirects=True) as r:
            if r.status_code not in [200, 206]: 
                return False
                
            content_type = r.headers.get('Content-Type', '').lower()
            if 'text/html' in content_type or 'application/json' in content_type:
                return False
                
            try:
                chunk = r.raw.read(4096)
            except:
                return False

            if not chunk:
                return False

            content_text = chunk.decode('utf-8', errors='ignore')
            content_text_lower = content_text.lower()
            
            hata_kelimeleri = ["expired", "invalid", "unauthorized", "bad token", "denied", "forbidden", "403", "error"]
            if any(hata in content_text_lower for hata in hata_kelimeleri):
                return False
            
            # 2. AŞAMA: M3U8 VE XTREAM İÇİN GERÇEK VİDEO PARÇASI (SEGMENT) TESTİ
            if "#extm3u" in content_text_lower or "#extinf" in content_text_lower or "media-sequence" in content_text_lower:
                lines = content_text.split('\n')
                video_segment_url = None
                
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        if "http" in line or ".ts" in line or ".m3u8" in line or "stream" in line:
                            if not line.startswith("http"):
                                video_segment_url = urljoin(url, line)
                            else:
                                video_segment_url = line
                            break
                
                # Akış doğrulaması (Token/Süre kontrolü)
                if video_segment_url:
                    try:
                        with requests.get(video_segment_url, headers=HEADERS, timeout=4, stream=True, verify=False) as vr:
                            if vr.status_code in [200, 206]:
                                v_chunk = vr.raw.read(512)
                                if v_chunk and len(v_chunk) >= 256:
                                    return True 
                            return False 
                    except:
                        return False
                return False
                
            if any(t in content_type for t in ['video/', 'mpegurl', 'stream', 'octet-stream']):
                return True

            return False
    except: 
        return False

def kanal_isleme(kanal_metni, kaynak_url, eklenen_urller):
    satir_grubu = kanal_metni.strip().split('\n')
    if len(satir_grubu) < 2: return None
    
    ext_satiri = satir_grubu[0]
    link_satiri = satir_grubu[-1].strip()
    
    # 🚫 USTA IP ENGELİ: Eğer link yasaklı IP listesindeki bir adresi içeriyorsa teste sokmadan direkt REDDET!
    if any(yasak_ip in link_satiri for yasak_ip in YASAKLI_IP_LISTESI):
        return None
        
    if link_satiri in eklenen_urller: return None
    if any(yasak.lower() in ext_satiri.lower() for yasak in YASAKLI_GRUPLAR): return None

    if "tvando.m3u" in kaynak_url.lower():
        link_onayli = True
    else:
        link_onayli = link_saglam_mi(link_satiri)

    if link_onayli:
        isim_temiz = re.sub(r'\s*\|\s*[A-Z0-9+]+\b', '', ext_satiri)
        isim_temiz = re.sub(r'\b(HEVC|RAW|PLUS|HD|FHD|SD|UHD|4K)\b', '', isim_temiz, flags=re.I)
        isim_temiz = re.sub(r'\s+YEDEK', 'YEDEK', isim_temiz, flags=re.IGNORECASE)
        
        print(f" ✅ LİSTEYE ALINDI ({'TVANDO' if 'tvando.m3u' in kaynak_url.lower() else 'TESTED'}): {link_satiri[:60]}...")
        return f"{isim_temiz}\n{link_satiri}"
    
    return None

def main():
    print(f"🛡️  USTA SİSTEM V6.0: IP Kara Listesi ve Canlı Akış Kontrolü Aktif!")
    
    if os.path.exists(FILE_PATH):
        shutil.copyfile(FILE_PATH, FILE_PATH + ".bak")

    avlananlar = github_taze_link_avla()
    guncel_kaynak_listesi = list(set(YEDEK_KAYNAKLAR + avlananlar))
    
    eklenen_urller = set()
    ana_liste_zirh = []
    ham_bulunanlar = []

    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_lines = f.readlines()
            ana_liste_zirh = tum_lines[:ZIRH_LIMIT]
            for s in ana_liste_zirh:
                if s.strip().startswith("http"):
                    eklenen_urller.add(s.strip())

    for kaynak in guncel_kaynak_listesi:
        try:
            print(f"📡 Kaynak Okunuyor: {kaynak[:70]}...")
            r = requests.get(kaynak, headers=HEADERS, timeout=12, verify=False)
            if r.status_code == 200:
                bulunan = re.findall(r"(#EXTINF:.*?\n+https?.*?)(?=#EXTINF|$)", r.text, re.DOTALL | re.IGNORECASE)
                for b in bulunan:
                    ham_bulunanlar.append((b, kaynak))
            else:
                print(f"❌ Kaynak Yanıt Vermedi: {kaynak[:40]}...")
        except: continue

    unique_adaylar = []
    gorulen_linkler = set()
    for k, kaynak_url in ham_bulunanlar:
        link = k.strip().split('\n')[-1].strip()
        if link not in eklenen_urller and link not in gorulen_linkler:
            unique_adaylar.append((k, kaynak_url))
            gorulen_linkler.add(link)

    print(f"🔍 {len(unique_adaylar)} yeni benzersiz aday izlemeye alındı. Derin zırhlı test başlıyor...")

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        results = list(executor.map(lambda item: kanal_isleme(item[0], item[1], eklenen_urller), unique_adaylar))
        final_listesi = [r for r in results if r is not None]

    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(ana_liste_zirh)
        f.write(f"\n# --- VIZITV ENTEGRELİ GÜNCEL ULTRA TEMİZ LİSTE ({datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}) --- #\n")
        for k in final_listesi:
            f.write(k + "\n")

    print(f"\n🏁 İŞLEM BİTTİ USTA! Kara listedeki IP'ler elendi, çalışan {len(final_listesi)} sağlam yedek alta eklendi.")

if __name__ == "__main__":
    main()
