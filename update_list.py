import os
import re
import sys
import shutil
import random
import socket
import logging
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse

import requests
from requests.adapters import HTTPAdapter
import urllib3

# --- LOGGING YAPILANDIRMASI ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    datefmt='%H:%M:%S'
)

# --- GLOBAL SOKET TIMEOUT ---
socket.setdefaulttimeout(7)

# SSL uyarısını sustur
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
ZIRH_LIMIT = 2000
THREADS = 64

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
}

# --- OPTİMİZE EDİLMİŞ THREAD-SAFE SESSION ---
def create_optimized_session():
    s = requests.Session()
    adapter = HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=1)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    s.headers.update(HEADERS)
    s.verify = False
    return s

session = create_optimized_session()

# --- TEKİLLEŞTİRİLMİŞ VE DÜZENLENMİŞ YASAKLI LİSTESİ ---
YASAKLI_SET = {
    # Genel Yetişkin & Film/Dizi
    "freeshot", "webteizle", "tr film", "arzu film", "erler film", "taşacak bu deniz", "ezel", 
    "filmmedya", "keloğlan", "polskietv", "mediabaytv", "sarkortv", "glwiz", "persian", 
    "gledaitv", "rds tv", "touchtv", "slovakia", "bulgaria", "romania", "azerbeycan", 
    "superxfilm", "cinemamod", "adult", "xxx", "+18", "yetişkin", "yetiskin", "pink", 
    "redlight", "playboy", "penthouse", "vivid", "hustler", "erotic", "forbidden",
    "s01", "s02", "s03", "e01", "e02", "e03", "e04", "e05", "1080p.m3u8", "film", "movies", 
    "movie", "series", "dizi", "dizileri", "diziler", "radio", "radyo", "fm", "best fm", 
    "alem fm", "joy turk", "super fm", "exxen", "gain", "blutv", "netflix", "tod original", 
    "gumruk muhafaza", "belgesel diziler", "k-pop", "exatlon", "turk tutkusu", "7/24", 
    "genel | eğlence", "genel | eglence", "disney+", "screen saver", "ss screen",
    
    # Kökten Silinecek Ana Kelimeler
    "glife", "cinelux", "max", "TABIISPOR", "TABII",
    
    # Cine, Spor ve Yeşilçam Grupları
    "tabii spor", "tivibuspor", "tivibu spor", "exxen sports", "cine yesilcam", "cine office"
}

YASAKLI_PATTERN = re.compile(
    r'(' + '|'.join(re.escape(k) for k in sorted(YASAKLI_SET, key=len, reverse=True)) + r')', 
    re.IGNORECASE
)

YASAKLI_IP_LISTESI = [
    "87.121.104.29",
    "87.121.104.29:1071"
]

YEDEK_KAYNAKLAR = [
    "http://raw.githubusercontent.com/batuhansabri55/AkcagozTV_Film/refs/heads/main/FilmDizi.m3u",
    "https://raw.githubusercontent.com/smtv62/smtv/bfe2fd49dfaf43fb3219abd1893dcd4f47e26781/turkce.m3u",
    "https://raw.githubusercontent.com/efendikral54-max/M3u-Listen/refs/heads/main/IPTVSevenler.m3u",
    "https://raw.githubusercontent.com/hayatiptv/iptv/master/index.m3u",
    "https://link.testworkery0.workers.dev/patron.m3u",
    "https://raw.githubusercontent.com/hydrokin/M3U/e4e9ba44d54d360ff3de6388220a4dc1019bf34e/tvando.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://files.manuscdn.com/user_upload_by_module/session_file/310519663091167371/lXQCJEWGepXILedX.m3u8",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://raw.githubusercontent.com/kadirsener1/avva/537423d13dd489dd9ec1627c5b5b2bad765e25a5/playlist.m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u"
]

BUYUK_HAVUZ_URL = "https://raw.githubusercontent.com/batuhansabri55/AkcagozTV_Canli/refs/heads/main/paneller.txt"

# REGEX ÖNBELLEKLERİ
TR_KANAL_REGEX = re.compile(r'(\[TR\]|\bTR\b|\.TR\b|TURKEY|TÜRK|TURKISH|TÜRKÇE)', re.IGNORECASE)

# GÜNCELLENDİ: Europe, FPS, 50fps, 60fps ve kalite takıları temizleme regex'i
KALITE_REGEX = re.compile(
    r'\b(FHD|HD|SD|UHD|4K|HEVC|RAW|PLUS|1080P|720P|30FPS|60FPS|50FPS|FPS|EUROPE|EURO|EUR|EU|VIP|MOBILE|HQ|'
    r'ғʜᴅ|ʜᴅ|sᴅ|ᴜʜᴅ|4ᴋ|ʜᴇᴠc|ʀᴀᴡ|ᴘʟᴜs|ᴇᴜƦᴏᴘᴇ|ғᴘs)\b', 
    re.IGNORECASE
)
YEDEK_REGEX = re.compile(r'\b(YEDEK|BACKUP|ALT|TEST)\b', re.IGNORECASE)
DIL_REGEX = re.compile(r'\b(TURKISH|TÜRKÇE|TURKCE|TÜRK)\b', re.IGNORECASE)
PRE_TR_HABER = re.compile(r'\bTR\.HABER\b', re.IGNORECASE)
PRE_TR = re.compile(r'\bTR\b[\.\:\-\|]?\s*', re.IGNORECASE)
BRACKETS_REGEX = re.compile(r'\[.*?\]|\(.*?\)')

# REKLAM VE SITE UZANTILARI REGEX
REKLAM_REGEX = re.compile(r'\b(KODLUK\.COM|KODLUK|\b[\w\-]+\.(COM|NET|ORG|TV|SITE|ONLINE|CLUB|INFO|XYZ|ME)\b)', re.IGNORECASE)

# SEMBOLLER VE SÜSLÜ RESİMLER/EMOJİLER TEMİZLEME REGEX'İ
SEMBOL_REGEX = re.compile(r'[^\w\s]', re.UNICODE)

# ==============================================================================
# ROBOT FONKSİYONLAR
# ==============================================================================
def yasakli_mi(metin: str) -> bool:
    """Tek bir hızlı regex sorgusu ile yasaklı kelime kontrolü yapar."""
    return bool(YASAKLI_PATTERN.search(metin))

def havuz_kanal_ismini_temizle(extinf_satiri: str) -> str:
    if "," in extinf_satiri:
        prefix, kanal_adi = extinf_satiri.split(",", 1)
    else:
        prefix = '#EXTINF:-1 tvg-id="" group-title="HAVUZ CANLI"'
        kanal_adi = extinf_satiri

    # 1. Parantez içleri ve reklam/site uzantılarını uçur
    kanal_adi = BRACKETS_REGEX.sub('', kanal_adi)
    kanal_adi = REKLAM_REGEX.sub('', kanal_adi)
    
    # 2. Ön takıları, dil isimlerini ve yedek ibarelerini temizle
    kanal_adi = PRE_TR_HABER.sub('', kanal_adi)
    kanal_adi = PRE_TR.sub('', kanal_adi)
    kanal_adi = YEDEK_REGEX.sub('', kanal_adi)
    kanal_adi = DIL_REGEX.sub('', kanal_adi)

    # 3. Süslü veya Standart Kalite/Bölge takılarını (Europe, 50FPS, FHD vb.) temizle
    kanal_adi = KALITE_REGEX.sub('', kanal_adi)
    
    # 4. Sembolleri, emojileri, bayrakları uçur
    kanal_adi = SEMBOL_REGEX.sub(' ', kanal_adi)
    
    # 5. Fazla boşlukları toparla ve tam büyük harf yap
    kanal_adi = " ".join(kanal_adi.split()).upper()
    
    # 6. USTA İSTEDİĞİ FORMAT: "[TR] ▶️ KANAL ADI" şeklinde giydir
    if kanal_adi:
        kanal_adi = f"[TR] ▶️ {kanal_adi}"
    
    return f'{prefix},{kanal_adi}' if kanal_adi else extinf_satiri

def havuzu_indir():
    logging.info("📥 Büyük havuz listesi indiriliyor...")
    try:
        response = session.get(BUYUK_HAVUZ_URL, timeout=10)
        if response.status_code == 200:
            linkler = re.findall(r'(https?://[^\s"\']+get\.php\?[^\s"\']+)', response.text)
            return list(dict.fromkeys(linkler))
    except requests.RequestException:
        pass
    return []

def havuz_yayin_canli_mi(test_url: str) -> bool:
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

def havuz_paneli_test_et(url: str):
    test_url = url.replace("type=m3u_plus", "type=m3u").replace("type=m3u", "type=m3u_plus")
    
    try:
        response = session.get(test_url, timeout=10)
        if response.status_code == 200 and "#EXTM3U" in response.text:
            satirlar = response.text.splitlines()
            bulunan_tr_kanallari = []
            
            vip_test_linkleri = {
                "cnn": None,
                "kanald": None,
                "discovery": None,
                "sinema": None
            }
            
            for i in range(len(satirlar)):
                satir = satirlar[i]
                if satir.startswith("#EXTINF"):
                    if yasakli_mi(satir):
                        continue
                    
                    if i + 1 < len(satirlar) and satirlar[i+1].startswith("http"):
                        kanal_linki = satirlar[i+1]
                        if yasakli_mi(kanal_linki) or any(yasak_ip in kanal_linki for yasak_ip in YASAKLI_IP_LISTESI):
                            continue
                            
                        temiz_link = kanal_linki.replace("type=m3u_plus", "output=ts").replace("type=m3u", "output=ts")
                        if "output=ts" not in temiz_link:
                            if "?" in temiz_link:
                                temiz_link += "&output=ts"
                            elif not any(temiz_link.lower().split('?')[0].endswith(ext) for ext in [".ts", ".m3u8", ".mkv", ".mp4"]):
                                temiz_link += "?output=ts"
                        
                        temiz_satir = havuz_kanal_ismini_temizle(satir)
                        
                        if TR_KANAL_REGEX.search(satir):
                            bulunan_tr_kanallari.append(f"{temiz_satir}\n{temiz_link}")
                        
                        satir_upper = satir.upper()
                        if not vip_test_linkleri["cnn"] and re.search(r'CNN\s*T[UÜ]RK', satir_upper):
                            vip_test_linkleri["cnn"] = temiz_link
                        elif not vip_test_linkleri["kanald"] and re.search(r'KANAL\s*D', satir_upper):
                            vip_test_linkleri["kanald"] = temiz_link
                        elif not vip_test_linkleri["discovery"] and "DISCOVERY CHANNEL" in satir_upper:
                            vip_test_linkleri["discovery"] = temiz_link
                        elif not vip_test_linkleri["sinema"] and re.search(r'S[Iİ]NEMA\s*(TV|1)', satir_upper):
                            vip_test_linkleri["sinema"] = temiz_link
            
            test_edilecekler = [link for link in vip_test_linkleri.values() if link is not None]
            
            if len(test_edilecekler) >= 3:
                calisan_sayisi = sum(1 for link in test_edilecekler if havuz_yayin_canli_mi(link))
                if calisan_sayisi >= 3:
                    logging.info(f"🟢 VIP KANALLARI ÇALIŞAN PANEL BULUNDU: {test_url}")
                    return "\n".join(bulunan_tr_kanallari)
                    
    except Exception:
        pass
    return None

def havuzdan_canli_kanallari_getir():
    link_listesi = havuzu_indir()
    if not link_listesi: return ""
    logging.info("⚡ Tam 3 adet BENZERSİZ canlı ve VIP testinden geçmiş Türkçe TV paneli aranıyor, lütfen bekleyin...")
    
    bulunan_panellerin_icerikleri = []
    bulunan_domainler = set()  
    bulunan_adet = 0
    
    with ThreadPoolExecutor(max_workers=30) as executor:
        random.shuffle(link_listesi)
        gorevler = {executor.submit(havuz_paneli_test_et, url): url for url in link_listesi}
        for gosterge in as_completed(gorevler):
            url = gorevler[gosterge]
            domain = urlparse(url).netloc
            if domain in bulunan_domainler:
                continue
            
            sonuc = gosterge.result()
            if sonuc:
                bulunan_panellerin_icerikleri.append(sonuc)
                bulunan_domainler.add(domain)  
                bulunan_adet += 1
                logging.info(f"📡 Sağlam Farklı Panel Sayısı: {bulunan_adet}/3 -> (Eklenen: {domain})")
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
    else:
        logging.warning("⚠️ GITHUB_TOKEN bulunamadı. GitHub API istekleri sınırlamaya takılabilir.")

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

def link_saglam_mi(url: str) -> bool:
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

def kanal_isleme(kanal_metni: str, kaynak_url: str, eklenen_urller: set):
    satir_grubu = kanal_metni.strip().split('\n')
    if len(satir_grubu) < 2: return None
    ext_satiri = satir_grubu[0]
    link_satiri = satir_grubu[-1].strip()
    
    if any(yasak_ip in link_satiri for yasak_ip in YASAKLI_IP_LISTESI):
        return None
    if link_satiri in eklenen_urller:
        return None
        
    if "FilmDizi.m3u" not in kaynak_url:
        if yasakli_mi(ext_satiri) or yasakli_mi(link_satiri):
            return None
    
    if any(x in kaynak_url.lower() for x in ["tvando.m3u", "testworkery0", "patron.m3u", "filmdizi.m3u"]):
        isim_temiz = havuz_kanal_ismini_temizle(ext_satiri)
        return f"{isim_temiz}\n{link_satiri}"
        
    if link_saglam_mi(link_satiri):
        isim_temiz = havuz_kanal_ismini_temizle(ext_satiri)
        return f"{isim_temiz}\n{link_satiri}"
    return None

# ==============================================================================
# 🚀 ANA MAIN FONKSİYONU
# ==============================================================================
def main():
    logging.info("🛡️ USTA SİSTEM V12.0: ZIRHLI LİSTE KESİNLİKLE KORUMAYA ALINDI!")
    
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
            
            for s in ana_liste_zirh:
                if s.strip().startswith("http"):
                    eklenen_urller.add(s.strip())

            geriye_kalan_satirlar = tum_lines[ZIRH_LIMIT:]
            havuz_header_index = next((idx for idx, line in enumerate(geriye_kalan_satirlar) if "# --- BÜYÜK HAVUZDAN" in line), -1)
            
            if havuz_header_index != -1:
                eski_havuz_satirlari = geriye_kalan_satirlar[havuz_header_index+1:]
                eski_havuz_linkleri = [s.strip() for s in eski_havuz_satirlari if s.strip().startswith("http")]
                
                if eski_havuz_linkleri:
                    logging.info("🕵️ Eski havuz paneli bulundu, VIP test canlılığı deneniyor...")
                    test_edilecekler = random.sample(eski_havuz_linkleri, min(3, len(eski_havuz_linkleri)))
                    if sum(1 for link in test_edilecekler if havuz_yayin_canli_mi(link)) >= 2:
                        logging.info("🟢 ESKİ HAVUZ PANELİ HALA CANLI VE AKTİF! Temizlik süzgecinden geçiriliyor...")
                        
                        temiz_eski_havuz = []
                        baslik_yasakli_mi = False
                        
                        for s in eski_havuz_satirlari:
                            if s.startswith("#EXTINF"):
                                if yasakli_mi(s):
                                    baslik_yasakli_mi = True
                                    continue
                                else:
                                    baslik_yasakli_mi = False
                                    s = havuz_kanal_ismini_temizle(s) + "\n"
                            
                            if baslik_yasakli_mi:
                                continue
                                
                            if yasakli_mi(s) or any(yasak_ip in s for yasak_ip in YASAKLI_IP_LISTESI):
                                if temiz_eski_havuz and temiz_eski_havuz[-1].startswith("#EXTINF"):
                                    temiz_eski_havuz.pop()
                                continue
                                
                            temiz_eski_havuz.append(s)
                            
                        eski_havuz_metni = "".join(temiz_eski_havuz)
                        eski_havuz_canli_mi = True
                    else:
                        logging.warning("🔴 ESKİ HAVUZ PANELİ PATLAMIŞ! Büyük havuzdan 3 adet taze panel aranacak...")

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
        logging.info("🔮 Adım 3: Mevcut havuz canlı olduğu için büyük havuz taraması atlandı, eski liste temizlenerek korundu.")
        havuz_canli_metni = eski_havuz_metni
    else:
        logging.info("🔮 Adım 3: Büyük havuzdan 3 adet sağlam panel taranıyor ve TV kanalları ayrıştırılıyor...")
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

    logging.info("🏁 İŞLEM BİTTİ USTA! Zırhlı listen %100 korundu. Sağlam ve pürüzsüz kanallar eklendi.")

if __name__ == "__main__":
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass
    main()
