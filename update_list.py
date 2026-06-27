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
import socket

# --- GLOBAL SOKET TIMEOUT (Askıda kalmayı kesin engeller) ---
socket.setdefaulttimeout(6)

# SSL hatalarını sustur
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
THREADS = 64 

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}

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
        except Exception:
            continue
    return yeni_kaynaklar[:12]

# ==============================================================================
# 🔥 NET VE TAVİZSİZ CANLI YAYIN TESTİ
# ==============================================================================
def link_saglam_mi(url):
    if any(x in url.lower() for x in ["atv-switch", "vizitv"]):
        return True

    try:
        with session.get(url, timeout=4, stream=True, allow_redirects=True) as r:
            if r.status_code not in [200, 206]: 
                return False
                
            try:
                chunk = r.raw.read(1500)
            except Exception:
                return False

            if not chunk:
                return False

            content_text = chunk.decode('utf-8', errors='ignore').lower()
            
            hata_kelimeleri = ["expired", "invalid", "unauthorized", "bad token", "denied", "forbidden", "403", "error", "html", "login"]
            if any(hata in content_text for hata in hata_kelimeleri):
                return False
            
            if "media-sequence" in content_text or "#ext-x-stream-inf" in content_text:
                for line in content_text.split('\n'):
                    line = line.strip()
                    if line and not line.startswith("#"):
                        video_segment_url = line if line.startswith("http") else urljoin(url, line)
                        try:
                            with session.get(video_segment_url, timeout=3, stream=True) as vr:
                                if vr.status_code in [200, 206]:
                                    v_chunk = vr.raw.read(256)
                                    return bool(v_chunk and len(v_chunk) >= 64)
                        except Exception:
                            return False
                return False
                
            return True
    except Exception: 
        return False

# ==============================================================================
# HAVUZ PANELLERİNİ ÖN DOĞRULAMA YAPARAK BULAN FONKSİYON
# ==============================================================================
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
                    # VOD ve Dizi Kalıcı Filtresi (Havuz Panelleri İçin)
                    if re.search(r'\bS\d+E\d+\b', satir, re.I) or re.search(r'\bS\d+\s*E\d+\b', satir, re.I):
                        continue
                    if any(yasak.lower() in satir.lower() for yasak in HAVUZ_YASAKLI_KELIMELER):
                        continue
                        
                    if any(isaret in satir.upper() for isaret in tr_isaretleri):
                        if i + 1 < len(satirlar) and satirlar[i+1].startswith("http"):
                            kanal_linki = satirlar[i+1]
                            
                            if any(yasak.lower() in kanal_linki.lower() for yasak in HAVUZ_YASAKLI_KELIMELER):
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
            
            # Panelde yeterli TR kanal varsa ve rastgele 3 kanaldan en az 2'si aktifse paneli kabul et
            if len(sadece_tr_linkleri) >= 15:
                test_edilecekler = random.sample(sadece_tr_linkleri, min(3, len(sadece_tr_linkleri)))
                if sum(1 for link in test_edilecekler if link_saglam_mi(link)) >= 2:
                    print(f"🟢 BÜYÜK HAVUZDAN SAĞLAM PANEL SEÇİLDİ: {test_url}")
                    return bulunan_tr_kanallari
    except Exception:
        pass
    return None

def havuzdan_canli_kanallari_getir():
    link_listesi = havuzu_indir()
    if not link_listesi: return []
    print("⚡ Tam 3 adet BENZERSİZ ve aktif Türkçe TV paneli taranıyor...")
    
    ham_havuz_kanallari = []
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
                
            kanal_listesi = gosterge.result()
            if kanal_listesi: 
                ham_havuz_kanallari.extend(kanal_listesi)
                bulunan_domainler.add(domain)  
                bulunan_adet += 1
                print(f"📡 Sağlam Panel Bulundu: {bulunan_adet}/3 -> (Eklenen: {domain})")
                if bulunan_adet >= 3:
                    executor.shutdown(wait=False, cancel_futures=True)
                    break
                    
    return ham_havuz_kanallari

# ==============================================================================
# KANAL FİLTRELEME VE ADLANDIRMA
# ==============================================================================
def kanal_isleme(kanal_metni):
    satir_grubu = kanal_metni.strip().split('\n')
    if len(satir_grubu) < 2: return None
    
    ext_satiri = satir_grubu[0].strip()
    link_satiri = satir_grubu[-1].strip()
    
    ext_lower = ext_satiri.lower()
    link_lower = link_satiri.lower()
    
    # Kesin VOD ve Dizi Koruma Kalkanı (Regex tabanlı)
    if re.search(r'\bS\d+E\d+\b', ext_satiri, re.I) or re.search(r'\bS\d+\s*E\d+\b', ext_satiri, re.I):
        return None
    
    if any(yasak.lower() in ext_lower for yasak in YASAKLI_GRUPLAR):
        return None
    if any(yasak.lower() in ext_lower or yasak.lower() in link_lower for yasak in HAVUZ_YASAKLI_KELIMELER):
        return None

    # İSTİSNASIZ HER KANAL TEK TEK BURADA CANLI TESTİNDEN GEÇER
    if link_saglam_mi(link_satiri):
        isim = re.sub(r'\s*\|\s*[A-Z0-9+]+\b', '', ext_satiri)
        isim = re.sub(r'\b(HEVC|RAW|PLUS|HD|FHD|SD|UHD|4K)\b', '', isim, flags=re.I)
        isim = re.sub(r'\s+YEDEK', 'YEDEK', isim, flags=re.IGNORECASE)
        return f"{isim}\n{link_satiri}"
    
    return None

# ==============================================================================
# 🚀 ANA MAIN FONKSİYONU
# ==============================================================================
def main():
    print("🛡️ USTA SİSTEM V11.6: Havuz Kanallarına Tavizsiz Tekil Test Sürümü!")
    
    if os.path.exists(FILE_PATH):
        shutil.copyfile(FILE_PATH, FILE_PATH + ".bak")

    ham_adaylar = []
    gorulen_linkler = set()

    # 1. ADIM: Mevcut tr.m3u dosyasındaki eski linkleri tara
    if os.path.exists(FILE_PATH):
        print("📂 Mevcut tr.m3u dosyasındaki eski linkler ayıklanıyor...")
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            satirlar = f.readlines()
            for i in range(len(satirlar)):
                if satirlar[i].strip().upper().startswith("#EXTINF"):
                    k = i + 1
                    while k < len(satirlar) and not satirlar[k].strip().startswith("http"):
                        k += 1
                    if k < len(satirlar):
                        link = satirlar[k].strip()
                        if "HAVUZ CANLI" in satirlar[i] or "# --- BÜYÜK HAVUZDAN" in satirlar[i]:
                            continue
                        if link not in gorulen_linkler:
                            ham_adaylar.append(f"{satirlar[i].strip()}\n{link}")
                            gorulen_linkler.add(link)

    # 2. ADIM: İnternetteki yedek kaynakları ve GitHub'ı tara
    print("🔄 İnternetteki yedek kaynaklar ve GitHub taranıyor...")
    avlananlar = github_taze_link_avla()
    guncel_kaynak_listesi = list(set(YEDEK_KAYNAKLAR + avlananlar))

    for kaynak in guncel_kaynak_listesi:
        try:
            r = session.get(kaynak, timeout=10, allow_redirects=True)
            if r.status_code == 200:
                satirlar = r.text.splitlines()
                for i in range(len(satirlar)):
                    if satirlar[i].strip().upper().startswith("#EXTINF"):
                        k = i + 1
                        while k < len(satirlar) and not satirlar[k].strip().startswith("http"):
                            k += 1
                        if k < len(satirlar):
                            link = satirlar[k].strip()
                            if link not in gorulen_linkler:
                                ham_adaylar.append(f"{satirlar[i].strip()}\n{link}")
                                gorulen_linkler.add(link)
        except Exception: 
            continue

    # 3. ADIM: Büyük Havuzdan 3 adet sağlam panel bul ve kanallarını tek tek aday listesine ekle!
    print("\n🔮 Adım 3: Büyük havuzdan 3 sağlam panel indiriliyor ve kanalları TEKİL TEST için ayrıştırılıyor...")
    havuz_aday_kanallari = havuzdan_canli_kanallari_getir()
    
    for havuz_kanali in havuz_aday_kanallari:
        link = havuz_kanali.strip().split('\n')[-1].strip()
        if link not in gorulen_linkler:
            ham_adaylar.append(havuz_kanali)
            gorulen_linkler.add(link)

    # 4. ADIM: Toplanan İSTİSNASIZ TÜM LİNK LİSTESİNİ (Yedekler + Havuz) canlılık testine sok!
    print(f"\n🔬 Toplam {len(ham_adaylar)} adet link (Yedekler ve Havuz Kanalları Dahil) tavizsiz tekil teste alınıyor...")
    
    final_canli_liste = []
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        results = list(executor.map(kanal_isleme, ham_adaylar))
        final_canli_liste = [r for r in results if r is not None]

    # 5. ADIM: Sadece testten başarıyla geçen canlı kanalları dosyaya yaz!
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        if final_canli_liste:
            f.write(f"\n# --- %100 CANLI DOĞRULANMIŞ AKÇAGÖZ TV ULTRA TEMİZ LİSTE ({datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}) --- #\n")
            f.write("\n".join(final_canli_liste) + "\n")

    print(f"\n🏁 İŞLEM BİTTİ USTA! Havuzdan gelen patlak panellerin çöpleri de dahil hepsi imha edildi. Toplam canli kanal: {len(final_canli_liste)}")

if __name__ == "__main__":
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass
    main()
