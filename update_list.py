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

# --- GLOBAL SOKET TIMEOUT ---
socket.setdefaulttimeout(7)
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

# --- YASAKLI VE YEDEK LİSTELERİ ---
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
# ROBOT FONKSİYONLAR
# ==============================================================================
def havuz_kanal_ismini_temizle(extinf_satiri):
    if "," in extinf_satiri:
        prefix, kanal_adi = extinf_satiri.split(",", 1)
    else:
        prefix = '#EXTINF:-1 tvg-id="" group-title="YENI EKLENEN"'
        kanal_adi = extinf_satiri

    kanal_adi = re.sub(r'(?i)\bTR\.HABER\b', '', kanal_adi)
    kanal_adi = re.sub(r'(?i)\bTR\b[\.\:\-\|]?\s*', '', kanal_adi)
    kanal_adi = re.sub(r'\[.*?\]', '', kanal_adi)
    kanal_adi = re.sub(r'\(.*?\)', '', kanal_adi)
    kalite_regex = r'(?i)\b(FHD|HD|SD|UHD|4K|HEVC|RAW|PLUS|1080P|720P|30FPS|60FPS|50FPS|VIP|MOBILE|HQ|ʜᴅ)\b'
    kanal_adi = re.sub(kalite_regex, '', kanal_adi)
    kanal_adi = re.sub(r'(?i)\b(YEDEK|BACKUP|ALT|TEST)\b', '', kanal_adi)
    kanal_adi = re.sub(r'(?i)\b(TURKISH|TÜRKÇE|TURKCE|TÜRK)\b', '', kanal_adi)
    kanal_adi = kanal_adi.replace("::", "").replace("-", "").replace("|", "").replace("+", "").strip()
    kanal_adi = " ".join(kanal_adi.split()).upper()
    return f'{prefix},{kanal_adi}' if kanal_adi else extinf_satiri

def github_taze_link_avla():
    print("🕸️ GitHub'da son 2 günün taze IPTV listeleri aranıyor...")
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
        except requests.RequestException: continue
    return yeni_kaynaklar[:12]

def link_saglam_mi(url):
    try:
        with session.get(url, timeout=4, stream=True, allow_redirects=True) as r:
            if r.status_code not in [200, 206]: return False
            content_type = r.headers.get('Content-Type', '').lower()
            if 'text/html' in content_type or 'application/json' in content_type: return False
            try: chunk = r.raw.read(4096)
            except Exception: return False
            if not chunk: return False
            content_text = chunk.decode('utf-8', errors='ignore').lower()
            hata_kelimeleri = ["expired", "invalid", "unauthorized", "bad token", "denied", "forbidden", "403", "error"]
            if any(hata in content_text for hata in hata_kelimeleri): return False
            if any(key in content_text for key in ["#extm3u", "#extinf", "media-sequence"]): return False
            return any(t in content_type for t in ['video/', 'mpegurl', 'stream', 'octet-stream'])
    except Exception: return False

def kanal_isleme(kanal_metni, kaynak_url, eklenen_urller):
    satir_grubu = kanal_metni.strip().split('\n')
    if len(satir_grubu) < 2: return None
    
    ext_satiri = satir_grubu[0]
    link_satiri = satir_grubu[-1].strip()

    if any(yasak_ip in link_satiri for yasak_ip in YASAKLI_IP_LISTESI): return None
    if link_satiri in eklenen_urller: return None
    if any(yasak.lower() in ext_satiri.lower() for yasak in YASAKLI_GRUPLAR) or any(yasak.lower() in link_satiri.lower() for yasak in HAVUZ_YASAKLI_KELIMELER):
        return None

    if link_saglam_mi(link_satiri):
        isim_temiz = havuz_kanal_ismini_temizle(ext_satiri)
        return f"{isim_temiz}\n{link_satiri}"
    return None

def havuzu_indir():
    try:
        response = session.get(BUYUK_HAVUZ_URL, timeout=10)
        if response.status_code == 200:
            linkler = re.findall(r'(http://[^\s"\']+get\.php\?[^\s"\']+)', response.text)
            return list(dict.fromkeys(linkler))
    except Exception: pass
    return []

def havuz_paneli_adaylari_topla(url):
    test_url = url.replace("type=m3u_plus", "type=m3u").replace("type=m3u", "type=m3u_plus")
    tr_isaretleri = ["TR:", "TR|", "TR -", "TURKISH", "TÜRKÇE", "TURKCE", 'GROUP-TITLE="TR', "TÜRK"]
    bulunan_adaylar = []
    try:
        response = session.get(test_url, timeout=10)
        if response.status_code == 200 and "#EXTM3U" in response.text:
            satirlar = response.text.splitlines()
            for i in range(len(satirlar)):
                satir = satirlar[i]
                if satir.startswith("#EXTINF"):
                    if any(yasak.lower() in satir.lower() for yasak in HAVUZ_YASAKLI_KELIMELER): continue
                    if any(isaret in satir.upper() for isaret in tr_isaretleri):
                        if i + 1 < len(satirlar) and satirlar[i+1].startswith("http"):
                            kanal_linki = satirlar[i+1]
                            if any(yasak_ip in kanal_linki for yasak_ip in YASAKLI_IP_LISTESI): continue
                            temiz_link = kanal_linki.replace("type=m3u_plus", "output=ts").replace("type=m3u", "output=ts")
                            if "output=ts" not in temiz_link:
                                if "?" in temiz_link: temiz_link += "&output=ts"
                                elif not any(temiz_link.lower().split('?')[0].endswith(ext) for ext in [".ts", ".m3u8", ".mkv", ".mp4"]):
                                    temiz_link += "?output=ts"
                            bulunan_adaylar.append((havuz_kanal_ismini_temizle(satir), temiz_link))
    except Exception: pass
    return bulunan_adaylar

def havuzdan_canli_kanallari_getir(eklenen_urller):
    link_listesi = havuzu_indir()
    if not link_listesi: return ""
    print("⚡ Tam 3 adet BENZERSİZ Türkçe TV paneli aranıyor...")
    
    tum_aday_kanallar = []
    bulunan_domainler = set()  
    bulunan_adet = 0
    random.shuffle(link_listesi)
    
    for url in link_listesi:
        domain = urlparse(url).netloc
        if domain in bulunan_domainler: continue
        adaylar = havuz_paneli_adaylari_topla(url)
        if len(adaylar) >= 15:
            # Panele ait rastgele 3 kanalı hızlıca test et
            test_ornekleri = random.sample([link for ext, link in adaylar], min(3, len(adaylar)))
            calisan = sum(1 for link in test_ornekleri if link_saglam_mi(link))
            if calisan >= 2:
                tum_aday_kanallar.extend(adaylar)
                bulunan_domainler.add(domain)
                bulunan_adet += 1
                print(f"📡 Panel Onaylandı: {bulunan_adet}/3 -> ({domain})")
                if bulunan_adet >= 3: break

    if not tum_aday_kanallar: return ""
    
    print(f"🔬 3 Panelden toplam {len(tum_aday_kanallar)} kanal çekildi. Tek tek canlılık testine giriyor...")
    kesin_calisan_icerik = []
    
    def kanal_test_et_ve_ekle(kanal_item):
        ext_satir, link = kanal_item
        if link not in eklenen_urller and link_saglam_mi(link):
            return f"{ext_satir}\n{link}"
        return None

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        sonuclar = list(executor.map(kanal_test_et_ve_ekle, tum_aday_kanallar))
        for sonuc in sonuclar:
            if sonuc: kesin_calisan_icerik.append(sonuc)

    return "\n".join(kesin_calisan_icerik)

# ==============================================================================
# 🚀 ANA MAIN FONKSİYONU
# ==============================================================================
def main():
    print("🛡️ USTA SİSTEM V15.0: Yedek Kaynaklar + Büyük Havuz Tam Korumalı Sürüm!")
    
    if not os.path.exists(FILE_PATH):
        print(f"🔴 {FILE_PATH} dosyası bulunamadı!")
        return

    shutil.copyfile(FILE_PATH, FILE_PATH + ".bak")

    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        tum_icerik = f.read()

    # ZIRH BÖLGESİNİ BULMA (GÜNCEL LİSTE veya BÜYÜK HAVUZ başlığından öncesi ZIRHTIR)
    ayrac1 = "# --- GÜNCEL ULTRA TEMİZ LİSTE"
    ayrac2 = "# --- BÜYÜK HAVUZDAN"
    
    kesim_noktasi = len(tum_icerik)
    if ayrac1 in tum_icerik: kesim_noktasi = tum_icerik.find(ayrac1)
    elif ayrac2 in tum_icerik: kesim_noktasi = tum_icerik.find(ayrac2)
    
    ana_kisi_metni = tum_icerik[:kesim_noktasi]

    # 1. ZIRH URL'LERİNİ HAFIZAYA AL (Yenileri eklerken çifte kanal olmasın diye)
    eklenen_urller = set()
    ana_liste_zirh = ["#EXTM3U\n"]
    bloklar = re.findall(r"(#EXTINF:.*?\n+https?.*?)(?=#EXTINF|$)", ana_kisi_metni, re.DOTALL | re.IGNORECASE)
    
    for blok in bloklar:
        satirlar = blok.strip().split('\n')
        if len(satirlar) >= 2:
            link = satirlar[-1].strip()
            if not any(yasak_ip in link for yasak_ip in YASAKLI_IP_LISTESI):
                ana_liste_zirh.append(blok.strip() + "\n")
                eklenen_urller.add(link)

    print(f"🟢 ZIRH ONAYI: Dosyandaki ana kanallar tam korumaya alındı, asla test edilmeyecek.")

    # 2. YEDEK KAYNAKLARI VE GITHUB'I TARA
    print("🔎 Yedek kaynaklar ve GitHub taze linkleri taranıp test ediliyor...")
    avlananlar = github_taze_link_avla()
    guncel_kaynak_listesi = list(set(YEDEK_KAYNAKLAR + avlananlar))
    
    ham_bulunanlar = []
    for kaynak in guncel_kaynak_listesi:
        try:
            r = session.get(kaynak, timeout=10, allow_redirects=True)
            if r.status_code in [200, 301, 302]:
                bulunan = re.findall(r"(#EXTINF:.*?\n+https?.*?)(?=#EXTINF|$)", r.text, re.DOTALL | re.IGNORECASE)
                ham_bulunanlar.extend((b, kaynak) for b in bulunan)
        except Exception: continue

    unique_adaylar = []
    gorulen_linkler = set()
    for k, kaynak_url in ham_bulunanlar:
        link = k.strip().split('\n')[-1].strip()
        # Zırhın içinde yoksa ve bu taramada daha önce görülmediyse aday yap
        if link not in eklenen_urller and link not in gorulen_linkler:
            unique_adaylar.append((k, kaynak_url))
            gorulen_linkler.add(link)

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        results = list(executor.map(lambda item: kanal_isleme(item[0], item[1], eklenen_urller), unique_adaylar))
        final_yedek_listesi = [r for r in results if r is not None]
        
    for r in final_yedek_listesi:
        link = r.strip().split('\n')[-1].strip()
        eklenen_urller.add(link) # Büyük havuz taraması için bunu da hafızaya al

    # 3. BÜYÜK HAVUZU ÇEK VE TEST ET
    havuz_son_metin = havuzdan_canli_kanallari_getir(eklenen_urller)

    # 4. DOSYAYA YAZDIRMA (SIRASIYLA: ZIRH -> YEDEKLER -> BÜYÜK HAVUZ)
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(ana_liste_zirh)
        
        if final_yedek_listesi:
            f.write(f"\n# --- GÜNCEL ULTRA TEMİZ LİSTE ({datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}) --- #\n")
            f.write("\n".join(final_yedek_listesi) + "\n")
            
        if havuz_son_metin.strip():
            f.write(f"\n# --- BÜYÜK HAVUZDAN %100 CANLI TÜRKÇE PANELLER ({datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}) --- #\n")
            f.write(havuz_son_metin.strip() + "\n")

    print(f"\n🏁 İŞLEM BİTTİ USTA! Yedek kaynaklar tarandı, Havuzdan taze paneller çekildi.")

if __name__ == "__main__":
    if sys.platform == "win32":
        try: sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError: pass
    main()
