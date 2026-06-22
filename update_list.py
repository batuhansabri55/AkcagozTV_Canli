import requests
import re
import os
import datetime
import shutil
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib3
from urllib.parse import urljoin

# SSL hatalarını tamamen sustur
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
ZIRH_LIMIT = 4200
THREADS = 64         # 5600 link için tam güç hız ayarı!

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}

# --- YASAKLI VE YEDEK LİSTELERI ---
YASAKLI_GRUPLAR = [
    "FreeShot", "Webteizle", "TR FILM", "ARZU FILM", "ERLER FILM", 
    "Taşacak Bu Deniz", "EZEL", "FilmMedya", "Keloğlan", "PolskieTV", 
    "MediabayTV", "SarkorTV", "GLWIZ", "PERSIAN", "GledaiTV", "RDS TV", 
    "TouchTV", "Slovakia", "Bulgaria", "Romania", "Azerbeycan",
    "Superxfilm", "CINEMAMOD", "Adult", "XXX"
]

YASAKLI_IP_LISTESI = [
    "87.121.104.29",
    "87.121.104.29:1071"
]

YEDEK_KAYNAKLAR = [
    "https://streams.uzunmuhalefet.com/lists/tr.m3u",
    "https://raw.githubusercontent.com/hayatiptv/iptv/master/index.m3u",
    "https://link.testworkery0.workers.dev/patron.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://www.dropbox.com/scl/fi/p58t5o980tah2hz3234a5/SmartGO.m3u?rlkey=w44w0ycaa83uyn21uph77pp6v&st=mj0n6byr&raw=1",
    "https://raw.githubusercontent.com/hydrokin/M3U/e4e9ba44d54d360ff3e6388220a4dc1019bf34e/tvando.m3u",
    "https://raw.githubusercontent.com/kadirsener1/avva/537423d13dd489dd9ec1627c5b5b2bad765e25a5/playlist.m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u"
]

# --- 🎯 BÜYÜK HAVUZ AYARI ---
BUYUK_HAVUZ_URL = "https://raw.githubusercontent.com/batuhansabri55/AkcagozTV_Canli/refs/heads/main/paneller.txt"

# ==============================================================================
# 🆕 İSİM TEMİZLEME VE STANDARTLAŞTIRMA ROBOTU (EPG & ALIASES İÇİN)
# ==============================================================================
def havuz_kanal_ismini_temizle(extinf_satiri):
    """Havuzdan gelen kanal isimlerini tırpanlayıp TiviMate'in tanıyacağı saf hale getirir."""
    if "," in extinf_satiri:
        prefix, kanal_adi = extinf_satiri.split(",", 1)
    else:
        prefix = '#EXTINF:-1 tvg-id="" group-title="HAVUZ CANLI"'
        kanal_adi = extinf_satiri

    # İsimdeki tüm gereksiz takıları temizle
    kanal_adi = re.sub(r'(?i)\b(TR:|TR\s*\||TR\s*-|TURKISH|TÜRKÇE|TURKCE|TÜRK)\b', '', kanal_adi)
    kanal_adi = re.sub(r'(?i)\b(FHD|HD|SD|UHD|4K|HEVC|RAW|PLUS|1080P|720P|30FPS|60FPS)\b', '', kanal_adi)
    kanal_adi = re.sub(r'(?i)\b(YEDEK|BACKUP|ALT|TEST)\b', '', kanal_adi)
    
    # Özel sembolleri ve gereksiz boşlukları temizle
    kanal_adi = kanal_adi.replace("::", "").replace("-", "").replace("|", "").strip()
    
    # Çift boşlukları tek boşluğa düşür ve tamamen büyük harf yap (TiviMate Aliases daha rahat eşleşsin)
    kanal_adi = " ".join(kanal_adi.split()).upper()
    
    if not kanal_adi:
        return extinf_satiri
        
    return f'{prefix},{kanal_adi}'

# ==============================================================================
# BÜYÜK HAVUZDAN %100 CANLI TÜRKÇE PANEL BULMA MEKANİZMASI
# ==============================================================================
def havuzu_indir():
    print("📥 Büyük havuz listesi indiriliyor...")
    try:
        response = requests.get(BUYUK_HAVUZ_URL, headers=HEADERS, timeout=15, verify=False)
        if response.status_code == 200:
            linkler = re.findall(r'(http://[^\s"\']+get\.php\?[^\s"\']+)', response.text)
            return list(dict.fromkeys(linkler))
        return []
    except Exception:
        return []

def havuz_yayin_canli_mi(test_url):
    try:
        with requests.get(test_url, headers=HEADERS, timeout=5, stream=True, verify=False, allow_redirects=True) as r:
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
        pass
    return False

def havuz_paneli_test_et(url):
    test_url = url.replace("type=m3u_plus", "type=m3u").replace("type=m3u", "type=m3u_plus")
    tr_isaretleri = ["TR:", "TR|", "TR -", "TURKISH", "TÜRKÇE", "TURKCE", 'GROUP-TITLE="TR', "TÜRK"]
    try:
        response = requests.get(test_url, headers=HEADERS, timeout=10, verify=False)
        if response.status_code == 200 and "#EXTM3U" in response.text:
            satirlar = response.text.splitlines()
            bulunan_tr_kanallari = []
            sadece_tr_linkleri = []
            
            for i in range(len(satirlar)):
                satir = satirlar[i]
                if satir.startswith("#EXTINF"):
                    if any(isaret in satir.upper() for isaret in tr_isaretleri):
                        if i + 1 < len(satirlar) and satirlar[i+1].startswith("http"):
                            kanal_linki = satirlar[i+1]
                            temiz_link = kanal_linki.replace("type=m3u_plus", "output=ts").replace("type=m3u", "output=ts")
                            
                            # 🎯 URL PARAMETRE VE QUERY STRING DOĞRULAMA (Eksik Soru İşareti Hata Tamiri)
                            if "output=ts" not in temiz_link:
                                if "?" in temiz_link:
                                    temiz_link += "&output=ts"
                                else:
                                    if not any(temiz_link.lower().split('?')[0].endswith(ext) for ext in [".ts", ".m3u8", ".mkv", ".mp4"]):
                                        temiz_link += "?output=ts"
                            
                            temiz_satir = havuz_kanal_ismini_temizle(satir)
                            bulunan_tr_kanallari.append(f"{temiz_satir}\n{temiz_link}")
                            sadece_tr_linkleri.append(temiz_link)
            
            if len(sadece_tr_linkleri) >= 30:
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
    print("⚡ Canlı ve aktif Türkçe panel aranıyor, lütfen bekleyin...")
    with ThreadPoolExecutor(max_workers=30) as executor:
        gorevler = {executor.submit(havuz_paneli_test_et, url): url for url in link_listesi}
        for gosterge in as_completed(gorevler):
            sonuc = gosterge.result()
            if sonuc:
                return sonuc
    return ""

# ==============================================================================
# 🛡️ MEVCUT ORİJİNAL FONKSİYONLARINIZ
# ==============================================================================
def github_taze_link_avla():
    yeni_kaynaklar = []
    tarih = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
    arama_terimleri = ["trt1", "documentary", "belgesel"]
    
    # GitHub Actions'da istek kısıtlamasına takılmamak için dahili güvenli başlık oluşturuyoruz
    github_headers = HEADERS.copy()
    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        github_headers["Authorization"] = f"token {github_token}"
    
    for terim in arama_terimleri:
        search_url = f"https://api.github.com/search/code?q=extension:m3u+{terim}+pushed:>{tarih}&sort=indexed"
        try:
            r = requests.get(search_url, headers=github_headers, timeout=10)
            if r.status_code == 200:
                items = r.json().get('items', [])
                for item in items:
                    raw = item['html_url'].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
                    if raw not in yeni_kaynaklar:
                        yeni_kaynaklar.append(raw)
                    if len(yeni_kaynaklar) >= 15: break
        except:
            continue
            
    return yeni_kaynaklar[:12]

def link_saglam_mi(url):
    if "atv-switch" in url.lower() or "vizitv" in url.lower():
        return True

    try:
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
            
            if "#extm3u" in content_text_lower or "#extinf" in content_text_lower or "media-sequence" in content_text_lower:
                lines = content_text.split('\n')
                video_segment_url = None
                
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        if "http" in line or ".ts" in line or ".m3u8" in line or "stream" in line or "channel" in line:
                            if not line.startswith("http"):
                                video_segment_url = urljoin(url, line)
                            else:
                                video_segment_url = line
                            break
                
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
    
    if "tvando.m3u" in kaynak_url.lower() or "testworkery0" in kaynak_url.lower() or "patron.m3u" in kaynak_url.lower():
        if link_satiri in eklenen_urller: return None
        isim_temiz = re.sub(r'\s*\|\s*[A-Z0-9+]+\b', '', ext_satiri)
        isim_temiz = re.sub(r'\b(HEVC|RAW|PLUS|HD|FHD|SD|UHD|4K)\b', '', isim_temiz, flags=re.I)
        return f"{isim_temiz}\n{link_satiri}"

    if any(yasak_ip in link_satiri for yasak_ip in YASAKLI_IP_LISTESI):
        return None
        
    if link_satiri in eklenen_urller: return None
    if any(yasak.lower() in ext_satiri.lower() for yasak in YASAKLI_GRUPLAR): return None

    link_onayli = link_saglam_mi(link_satiri)

    if link_onayli:
        isim_temiz = re.sub(r'\s*\|\s*[A-Z0-9+]+\b', '', ext_satiri)
        isim_temiz = re.sub(r'\b(HEVC|RAW|PLUS|HD|FHD|SD|UHD|4K)\b', '', isim_temiz, flags=re.I)
        isim_temiz = re.sub(r'\s+YEDEK', 'YEDEK', isim_temiz, flags=re.IGNORECASE)
        return f"{isim_temiz}\n{link_satiri}"
    
    return None

# ==============================================================================
# 🚀 ANA MAIN FONKSİYONU (YENİLENMİŞ AKILLI ÖNBELLEKLİ SÜRÜM)
# ==============================================================================
def main():
    print("🛡️ USTA SİSTEM V10.0: Akıllı Havuz Korumalı Sürdürülebilir Kararlı Sürüm!")
    
    if os.path.exists(FILE_PATH):
        shutil.copyfile(FILE_PATH, FILE_PATH + ".bak")

    avlananlar = github_taze_link_avla()
    guncel_kaynak_listesi = list(set(YEDEK_KAYNAKLAR + avlananlar))
    
    eklenen_urller = set()
    ana_liste_zirh = []
    ham_bulunanlar = []

    # 🛡️ 4000 SATIR DOKUNULMAZ ZIRH KORUMASI VE ESKİ HAVUZ KONTROL MEKANİZMASI
    eski_havuz_metni = ""
    eski_havuz_canli_mi = False

    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_lines = f.readlines()
            ana_liste_zirh = tum_lines[:ZIRH_LIMIT]  # İlk 4000 satırı asla kaybetmemek üzere ayırır.
            for s in ana_liste_zirh:
                if s.strip().startswith("http"):
                    eklenen_urller.add(s.strip())
            
            # 🔍 --- AKILLI HAVUZ ANALİZ ROBOTU ---
            alt_lines = tum_lines[ZIRH_LIMIT:]
            havuz_header_index = -1
            for idx, line in enumerate(alt_lines):
                if "# --- BÜYÜK HAVUZDAN" in line:
                    havuz_header_index = idx
                    break
            
            # Eğer dosyada daha önce eklenmiş bir havuz bölümü varsa analiz et
            if havuz_header_index != -1:
                eski_havuz_satirlari = alt_lines[havuz_header_index+1:]
                eski_havuz_linkleri = [s.strip() for s in eski_havuz_satirlari if s.strip().startswith("http")]
                
                if eski_havuz_linkleri:
                    print("🕵️ Eski havuz paneli bulundu, canlılığı test ediliyor...")
                    # Mevcut panelden rastgele 3 kanalı cımbızla seçip test ediyoruz
                    test_edilecekler = random.sample(eski_havuz_linkleri, min(3, len(eski_havuz_linkleri)))
                    if sum(1 for link in test_edilecekler if havuz_yayin_canli_mi(link)) >= 2:
                        print("\n🟢 ESKİ HAVUZ PANELİ HALA CANLI VE AKTİF! Kod yorulmayacak, aynen korunuyor.")
                        eski_havuz_metni = "".join(eski_havuz_satirlari)
                        eski_havuz_canli_mi = True
                    else:
                        print("\n🔴 ESKİ HAVUZ PANELİ ÖLMÜŞ VEYA PATLAMIŞ! Büyük havuzdan taze panel aranacak...")

    for kaynak in guncel_kaynak_listesi:
        try:
            r = requests.get(kaynak, headers=HEADERS, timeout=15, verify=False, allow_redirects=True)
            if r.status_code in [200, 301, 302]:
                bulunan = re.findall(r"(#EXTINF:.*?\n+https?.*?)(?=#EXTINF|$)", r.text, re.DOTALL | re.IGNORECASE)
                for b in bulunan:
                    ham_bulunanlar.append((b, kaynak))
        except: 
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

    # 🔮 ADIM 3: AKILLI KARAR VERME AŞAMASI
    if eski_havuz_canli_mi:
        print("\n🔮 Adım 3: Mevcut havuz canlı olduğu için büyük havuz taraması atlandı, eski listeye sadık kalındı.")
        havuz_canli_metni = eski_havuz_metni
    else:
        print("\n🔮 Adım 3: Büyük havuz taranıyor ve isimler TiviMate için sabitleniyor...")
        havuz_canli_metni = havuzdan_canli_kanallari_getir()

    # 🛡️ YENİDEN YAZMA AŞAMASINDA ZIRH KORUMASI VE DİNAMİK ALAN GÜNCELLEMESİ
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(ana_liste_zirh)  # İlk 4000 dokunulmaz satırı başa aynen yazar.
        
        f.write(f"\n# --- GÜNCEL ULTRA TEMİZ LİSTE ({datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}) --- #\n")
        for k in final_listesi:
            f.write(k + "\n")
            
        if havuz_canli_metni.strip():
            f.write("\n# --- BÜYÜK HAVUZDAN %100 CANLI TÜRKÇE PANELLER (SABİT İSİMLİ) --- #\n")
            f.write(havuz_canli_metni.strip() + "\n")

    print(f"\n🏁 İŞLEM BİTTİ USTA! İlk {ZIRH_LIMIT} satıra dokunulmadı, altına sadece yeni çalışanlar eklendi.")

if __name__ == "__main__":
    main()
