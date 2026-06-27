import requests
import re
import os
import datetime
import shutil
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib3
from urllib.parse import urljoin, urlparse
import sys
import socket  # Kilitlemeleri engellemek için eklendi

# --- GLOBAL SOKET TIMEOUT (Yayınların askıda kalmasını kesin engeller) ---
socket.setdefaulttimeout(7)

# SSL hatalarını tamamen sustur
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
ZIRH_LIMIT = 1900
THREADS = 64 

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}

# Bağlantıları hızlandırmak için Session kullanımı
session = requests.Session()
session.headers.update(HEADERS)
session.verify = False

# --- YASAKLI VE YEDEK LİSTELERI ---
YASAKLI_GRUPLAR = [
    "FreeShot", "Webteizle", "TR FILM", "ARZU FILM", "ERLER FILM", 
    "Taşacak Bu Deniz", "EZEL", "FilmMedya", "Keloğlan", "PolskieTV", 
    "MediabayTV", "SarkorTV", "GLWIZ", "PERSIAN", "GledaiTV", "RDS TV", 
    "TouchTV", "Slovakia", "Bulgaria", "Romania", "Azerbeycan",
    "Superxfilm", "CINEMAMOD", "Adult", "XXX", "+18", "Yetişkin", "Yetiskin",
    "Pink", "Redlight", "Playboy", "Penthouse", "Vivid", "Hustler", "Erotic", "Forbidden"
]

HAVUZ_YASAKLI_KELIMELER = [
    "S01", "S02", "S03", "E01", "E02", "E03", "E04", "E05", "1080p.m3u8",
    "FILM", "MOVIES", "MOVIE", "SERIES", "DIZI", "DIZILERI", "DIZILER",
    "RADIO", "RADYO", "FM", "BEST FM", "ALEM FM", "JOY TURK", "SUPER FM",
    "EXXEN", "GAIN", "BLUTV", "NETFLIX", "TOD ORIGINAL", "GUMRUK MUHAFAZA",
    "BELGESEL DIZILER", "K-POP", "EXATLON", "TURK TUTKUSU",
    "7/24", "GENEL | EĞLENCE", "GENEL | EGLENCE", "DISNEY+", "SCREEN SAVER", "SS SCREEN",
    "ADULT", "XXX", "+18", "YETISKIN", "YETİŞKİN", "PINK", "REDLIGHT", "PLAYBOY", 
    "PENTHOUSE", "VIVID", "HUSTLER", "EROTIC", "FORBIDDEN"
]

YASAKLI_IP_LISTESI = [
    "87.121.104.29",
    "87.121.104.29:1071"
]

# USTA DİKKAT: Hatalı GitHub arayüz linki düzeltilip çalışan RAW haline getirildi!
YEDEK_KAYNAKLAR = [
    "https://streams.uzunmuhalefet.com/lists/tr.m3u",
    "https://raw.githubusercontent.com/hayatiptv/iptv/master/index.m3u",
    "https://raw.githubusercontent.com/hydrokin/M3U/e4e9ba44d54d360ff3de6388220a4dc1019bf34e/tvando.m3u",
    "https://link.testworkery0.workers.dev/patron.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://www.dropbox.com/scl/fi/p58t5o980tah2hz3234a5/SmartGO.m3u?rlkey=w44w0ycaa83uyn21uph77pp6v&st=mj0n6byr&raw=1",
    "https://raw.githubusercontent.com/kadirsener1/avva/537423d13dd489dd9ec1627c5b5b2bad765e25a5/playlist.m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u"
]

BUYUK_HAVUZ_URL = "https://raw.githubusercontent.com/batuhansabri55/AkcagozTV_Canli/refs/heads/main/paneller.txt"

# ==============================================================================
# ROBOT FONKSIYONLAR
# ==============================================================================
def havuz_kanal_ismini_temizle(extinf_satiri):
    if "," in extinf_satiri:
        prefix, kanal_adi = extinf_satiri.split(",", 1)
    else:
        prefix = '#EXTINF:-1 tvg-id="" group-title="HAVUZ CANLI"'
        kanal_adi = extinf_satiri

    kanal_adi = re.sub(r'(?i)\b(TR:|TR\s*\||TR\s*-|TURKISH|TÜRKÇE|TURKCE|TÜRK)\b', '', kanal_adi)
    kanal_adi = re.sub(r'(?i)\b(FHD|HD|SD|UHD|4K|HEVC|RAW|PLUS|1080P|720P|30FPS|60FPS)\b', '', kanal_adi)
    kanal_adi = re.sub(r'(?i)\b(YEDEK|BACKUP|ALT|TEST)\b', '', kanal_adi)
    
    kanal_adi = kanal_adi.replace("::", "").replace("-", "").replace("|", "").strip()
    kanal_adi = " ".join(kanal_adi.split()).upper()
    
    return f'{prefix},{kanal_adi}' if kanal_adi else extinf_satiri

def havuzu_indir():
    print("📥 Büyük havuz listesi indiriliyor...")
    try:
        response = session.get(BUYUK_HAVUZ_URL, timeout=10)
        if response.status_code == 200:
            linkler = re.findall(r'(http://[^\s"\']+get\.php\?[^\s"\']+)', response.text)
            return list(dict.fromkeys(linkler))
    except requests.RequestException:
        pass
    return []

def havuz_yayin_canli_mi(test_url):
    try:
        with session.get(test_url, timeout=4, stream=True, allow_redirects=True) as r:
            if r.status_code not in [200, 206]: 
                return False
                
            content_type = r.headers.get('Content-Type', '').lower()
            if 'text/html' in content_type or 'application/json' in content_type:
                return False
                
            chunk = r.raw.read(1024)
            if not chunk: 
                return False

            content_text = chunk.decode('utf-8', errors='ignore').lower()
            hata_kelimeleri = ["expired", "invalid", "unauthorized", "bad token", "denied", "forbidden", "403", "error", "html"]
            if any(hata in content_text for hata in hata_kelimeleri):
                return False
                
            return True
    except Exception:
        return False

def havuz_paneli_test_et(url):
    test_url = url.replace("type=m3u_plus", "type=m3u").replace("type=m3u", "type=m3u_plus")
    tr_isaretleri = ["TR:", "TR|", "TR -", "TURKISH", "TÜRKÇE", "TURKCE", 'GROUP-TITLE="TR', "TÜRK"]
    try:
        response = session.get(test_url, timeout=10)
        if response.status_code == 200 and "#EXTM3U" in response.text:
            satirlar = response.text.splitlines()
            bulunan_tr_kanallari = []
            sadece_tr_linkleri = []
            
            for i in range(len(satirlar)):
                satir = satirlar[i]
                if satir.startswith("#EXTINF"):
                    # USTA DİKKAT: Sıkı ADULT ve dizi temizliği filtresi
                    if any(yasak.lower() in satir.lower() for yasak in HAVUZ_YASAKLI_KELIMELER):
                        continue
                        
                    if any(isaret in satir.upper() for isaret in tr_isaretleri):
                        if i + 1 < len(satirlar) and satirlar[i+1].startswith("http"):
                            kanal_linki = satirlar[i+1]
                            
                            # USTA DİKKAT: Havuzdan gelirken de yasaklı IP'yi ve kelimeleri filtrele
                            if any(yasak.lower() in kanal_linki.lower() for yasak in HAVUZ_YASAKLI_KELIMELER) or any(yasak_ip in kanal_linki for yasak_ip in YASAKLI_IP_LISTESI):
                                continue
                                
                            temiz_link = kanal_linki.replace("type=m3u_plus", "output=ts").replace("type=m3u", "output=ts")
                            
                            if "output=ts" not in temiz_link:
                                if "?" in temiz_link:
                                    temiz_link += "&output=ts"
                                elif not any(temiz_link.lower().split('?')[0].endswith(ext) for ext in [".ts", ".m3u8", ".mkv", ".mp4"]):
                                    temiz_link += "?output=ts"
                            
                            temiz_satir = havuz_kanal_ismini_temizle(satir)
                            bulunan_tr_kanallari.append(f"{temiz_satir}\n{temiz_link}")
                            sadece_tr_linkleri.append(temiz_link)
            
            if len(sadece_tr_linkleri) >= 15:
                test_edilecekler = random.sample(sadece_tr_linkleri, min(3, len(sadece_tr_linkleri)))
                if sum(1 for link in test_edilecekler if havuz_yayin_canli_mi(link)) >= 2:
                    print(f"🟢 BÜYÜK HAVUZDAN CANLI PANEL BULUNDU: {test_url}")
                    return "\n".join(bulunan_tr_kanallari)
    except Exception:
        pass
    return None

def havuzdan_canli_kanallari_getir():
    link_listesi = havuzu_indir()
    if not link_listesi: return ""
    print("⚡ Tam 3 adet BENZERSİZ canlı ve aktif Türkçe TV paneli aranıyor, lütfen bekleyin...")
    
    bulunan_panellerin_icerikleri = []
    bulunan_domainler = set()  
    bulunan_adet = 0
    
    with ThreadPoolExecutor(max_workers=30) as executor:
        random.shuffle(link_listesi)
        gorevler = {executor.submit(havuz_paneli_test_et, url): url for url in link_listesi}
        
        for gosterge in as_completed(gorevler):
            url = gorevler[gosterge]
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            
            if domain in bulunan_domainler:
                continue
                
            sonuc = gosterge.result()
            if sonuc:
                bulunan_panellerin_icerikleri.append(sonuc)
                bulunan_domainler.add(domain)  
                bulunan_adet += 1
                print(f"📡 Sağlam Farklı Panel Sayısı: {bulunan_adet}/3 -> (Eklenen: {domain})")
                if bulunan_adet >= 3:
                    executor.shutdown(wait=False, cancel_futures=True)
                    break
                    
    return "\n".join(bulunan_panellerin_icerikleri) if bulunan_panellerin_icerikleri else ""

def github_taze_link_avla():
    yeni_kaynaklar = []
    tarih = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
    arama_terimleri = ["trt1", "documentary", "belgesel"]
    
    github_headers = HEADERS.copy()
    if github_token := os.environ.get("GITHUB_TOKEN"):
        github_headers["Authorization"] = f"token {github_token}"
    
    for terim in arama_terimleri:
        search_url = f"https://api.github.com/search/code?q=extension:m3u+{terim}+pushed:>{tarih}&sort=indexed"
        try:
            r = requests.get(search_url, headers=github_headers, timeout=10)
            if r.status_code == 200:
                for item in r.json().get('items', []):
                    raw = item['html_url'].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
                    if raw not in yeni_kaynaklar:
                        yeni_kaynaklar.append(raw)
                    if len(yeni_kaynaklar) >= 15: break
        except requests.RequestException:
            continue
            
    return yeni_kaynaklar[:12]

def link_saglam_mi(url):
    if any(x in url.lower() for x in ["atv-switch", "vizitv"]):
        return True

    try:
        with session.get(url, timeout=4, stream=True, allow_redirects=True) as r:
            if r.status_code not in [200, 206]: 
                return False
                
            content_type = r.headers.get('Content-Type', '').lower()
            if 'text/html' in content_type or 'application/json' in content_type:
                return False
                
            try:
                chunk = r.raw.read(4096)
            except Exception:
                return False

            if not chunk:
                return False

            content_text = chunk.decode('utf-8', errors='ignore').lower()
            
            hata_kelimeleri = ["expired", "invalid", "unauthorized", "bad token", "denied", "forbidden", "403", "error"]
            if any(hata in content_text for hata in hata_kelimeleri):
                return False
            
            if any(key in content_text for key in ["#extm3u", "#extinf", "media-sequence"]):
                for line in content_text.split('\n'):
                    line = line.strip()
                    if line and not line.startswith("#"):
                        if any(x in line for x in ["http", ".ts", ".m3u8", "stream", "channel"]):
                            video_segment_url = line if line.startswith("http") else urljoin(url, line)
                            try:
                                with session.get(video_segment_url, timeout=3, stream=True) as vr:
                                    if vr.status_code in [200, 206]:
                                        v_chunk = vr.raw.read(512)
                                        return bool(v_chunk and len(v_chunk) >= 256)
                            except Exception:
                                return False
                        break
                return False
                
            return any(t in content_type for t in ['video/', 'mpegurl', 'stream', 'octet-stream'])
    except Exception: 
        return False

def kanal_isleme(kanal_metni, kaynak_url, eklenen_urller):
    satir_grubu = kanal_metni.strip().split('\n')
    if len(satir_grubu) < 2: return None
    
    ext_satiri = satir_grubu[0]
    link_satiri = satir_grubu[-1].strip()

    # 1. EN BÜYÜK FİLTRE: Kaynak ne olursa olsun, IP yasaklıysa anında çöpe at!
    if any(yasak_ip in link_satiri for yasak_ip in YASAKLI_IP_LISTESI):
        return None

    # 2. Önceden eklenmiş mi kontrolü
    if link_satiri in eklenen_urller:
        return None

    # 3. Yetişkin/Dizi kelimeleri ortak filtre
    if any(yasak.lower() in ext_satiri.lower() for yasak in YASAKLI_GRUPLAR) or any(yasak.lower() in link_satiri.lower() for yasak in HAVUZ_YASAKLI_KELIMELER):
        return None

    # 4. YEDEK/ÖZEL KAYNAKLAR BÖLÜMÜ
    # USTA DİKKAT: Artık ayrıcalık yok, bu kaynaklar da çalışıyor mu diye test edilecek!
    if any(x in kaynak_url.lower() for x in ["tvando.m3u", "testworkery0", "patron.m3u"]):
        if link_saglam_mi(link_satiri):
            isim_temiz = re.sub(r'\s*\|\s*[A-Z0-9+]+\b', '', ext_satiri)
            isim_temiz = re.sub(r'\b(HEVC|RAW|PLUS|HD|FHD|SD|UHD|4K)\b', '', isim_temiz, flags=re.I)
            return f"{isim_temiz}\n{link_satiri}"
        return None # Çalışmıyorsa testten geçemez

    # 5. DİĞER STANDART KAYNAKLAR BÖLÜMÜ
    if link_saglam_mi(link_satiri):
        isim_temiz = re.sub(r'\s*\|\s*[A-Z0-9+]+\b', '', ext_satiri)
        isim_temiz = re.sub(r'\b(HEVC|RAW|PLUS|HD|FHD|SD|UHD|4K)\b', '', isim_temiz, flags=re.I)
        isim_temiz = re.sub(r'\s+YEDEK', 'YEDEK', isim_temiz, flags=re.IGNORECASE)
        return f"{isim_temiz}\n{link_satiri}"
    
    return None

# ==============================================================================
# 🚀 ANA MAIN FONKSİYONU
# ==============================================================================
def main():
    print("🛡️ USTA SİSTEM V11.2: Sağlamlık Testi Zorunlu ve Tam Korumalı Sürüm!")
    
    if os.path.exists(FILE_PATH):
        shutil.copyfile(FILE_PATH, FILE_PATH + ".bak")

    avlananlar = github_taze_link_avla()
    guncel_kaynak_listesi = list(set(YEDEK_KAYNAKLAR + avlananlar))
    
    eklenen_urller = set()
    ana_liste_zirh = []
    ham_bulunanlar = []
    eski_havuz_metni = ""
    eski_havuz_canli_mi = False

    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_lines = f.readlines()
            ana_liste_zirh = tum_lines[:ZIRH_LIMIT]
            
            # --- ZIRH İÇİN YASAKLI IP TEMİZLİĞİ ---
            temiz_zirh = []
            for s in ana_liste_zirh:
                if any(yasak_ip in s for yasak_ip in YASAKLI_IP_LISTESI):
                    if temiz_zirh and temiz_zirh[-1].startswith("#EXTINF"):
                        temiz_zirh.pop() 
                    continue
                temiz_zirh.append(s)
            ana_liste_zirh = temiz_zirh
            # -------------------------------------

            for s in ana_liste_zirh:
                if s.strip().startswith("http"):
                    eklenen_urller.add(s.strip())
            
            havuz_header_index = next((idx for idx, line in enumerate(tum_lines) if "# --- BÜYÜK HAVUZDAN" in line), -1)
            
            if havuz_header_index != -1:
                ana_liste_zirh = tum_lines[:min(ZIRH_LIMIT, havuz_header_index)]
                eski_havuz_satirlari = tum_lines[havuz_header_index+1:]
                eski_havuz_linkleri = [s.strip() for s in eski_havuz_satirlari if s.strip().startswith("http")]
                
                if eski_havuz_linkleri:
                    print("🕵️ Eski havuz paneli bulundu, canlılığı test ediliyor...")
                    test_edilecekler = random.sample(eski_havuz_linkleri, min(3, len(eski_havuz_linkleri)))
                    if sum(1 for link in test_edilecekler if havuz_yayin_canli_mi(link)) >= 2:
                        print("\n🟢 ESKİ HAVUZ PANELİ HALA CANLI VE AKTİF! Kod yorulmayacak, aynen korunuyor.")
                        
                        # --- ESKİ HAVUZ İÇİN YASAKLI IP TEMİZLİĞİ ---
                        temiz_eski_havuz = []
                        for s in eski_havuz_satirlari:
                            if any(yasak_ip in s for yasak_ip in YASAKLI_IP_LISTESI):
                                if temiz_eski_havuz and temiz_eski_havuz[-1].startswith("#EXTINF"):
                                    temiz_eski_havuz.pop()
                                continue
                            temiz_eski_havuz.append(s)
                            
                        eski_havuz_metni = "".join(temiz_eski_havuz)
                        # --------------------------------------------
                        eski_havuz_canli_mi = True
                    else:
                        print("\n🔴 ESKİ HAVUZ PANELİ PATLAMIŞ! Büyük havuzdan 3 adet taze panel aranacak...")

    for kaynak in guncel_kaynak_listesi:
        try:
            r = session.get(kaynak, timeout=10, allow_redirects=True)
            if r.status_code in [200, 301, 302]:
                bulunan = re.findall(r"(#EXTINF:.*?\n+https?.*?)(?=#EXTINF|$)", r.text, re.DOTALL | re.IGNORECASE)
                ham_bulunanlar.extend((b, kaynak) for b in bulunan)
        except Exception: 
            continue

    unique_adaylar = []
    gorulen_linkler = set()
    for k, kaynak_url in ham_bulunanlar:
        link = k.strip().split('\n')[-1].strip()
        if link not in eklenen_urller and link not in gorulen_linkler:
            unique_adaylar.append((k, kaynak_url))
            gorulen_linkler.add(link)

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        results = list(executor.map(lambda item: kanal_isleme(item[0], item[1], eklenen_urller), unique_adaylar))
        final_listesi = [r for r in results if r is not None]

    if eski_havuz_canli_mi:
        print("\n🔮 Adım 3: Mevcut havuz canlı olduğu için büyük havuz taraması atlandı, eski listeye sadık kalındı.")
        havuz_canli_metni = eski_havuz_metni
    else:
        print("\n🔮 Adım 3: Büyük havuzdan 3 adet sağlam panel taranıyor ve TV kanalları ayrıştırılıyor...")
        havuz_canli_metni = havuzdan_canli_kanallari_getir()

    if not ana_liste_zirh or not ana_liste_zirh[0].startswith("#EXTM3U"):
        ana_liste_zirh.insert(0, "#EXTM3U\n")

    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(ana_liste_zirh)
        
        if final_listesi:
            f.write(f"\n# --- GÜNCEL ULTRA TEMİZ LİSTE ({datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}) --- #\n")
            f.write("\n".join(final_listesi) + "\n")
            
        if havuz_canli_metni.strip():
            f.write("\n# --- BÜYÜK HAVUZDAN %100 CANLI TÜRKÇE PANELLER (SABİT İSİMLİ) --- #\n")
            f.write(havuz_canli_metni.strip() + "\n")

    print(f"\n🏁 İŞLEM BİTTİ USTA! 3 sağlam panelden sadece TV kanalları eklendi, dizi, radyo ve yetişkin içerikler temizlendi.")

if __name__ == "__main__":
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass
    main()
