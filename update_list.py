import requests
import re
import os
import datetime
import time
from concurrent.futures import ThreadPoolExecutor

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
ZIRH_LIMIT = 5047  # USTA: BURASI ARTIK KIRILMAZ BETON!
HEADERS = {'User-Agent': 'VLC/3.0.18 LibVLC/3.0.18'} # TiviMate ve Box dostu UA

YASAKLI_GRUPLAR = [
    "Webteizle", "TR FILM", "ARZU FILM", "ERLER FILM", "Taşacak Bu Deniz", 
    "EZEL", "FilmMedya", "Keloğlan", "PolskieTV", "MediabayTV", 
    "SarkorTV", "GLWIZ", "PERSIAN", "GledaiTV", "RDS TV", 
    "TouchTV", "Slovakia", "Bulgaria", "Romania", "Azerbeycan",
    "Superxfilm", "CINEMAMOD"
]

YEDEK_KAYNAKLAR = [
    "https://streams.uzunmuhalefet.com/lists/tr.m3u",
    "https://tinyurl.com/ytpatron",
    "https://urlz.fr/v1Xo",
    "https://raw.githubusercontent.com/smartgmr/cdn/refs/heads/main/Perfect.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://tinyurl.com/bdd2tz6h",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u"
]

def hiz_testi(kanal_verisi):
    """Linkin hızını ölçer, bozuksa eler."""
    try:
        ext_satiri, link = kanal_verisi
        start = time.time()
        # Sadece başlık bilgisini çek (Hızlı test için)
        response = requests.head(link, headers=HEADERS, timeout=1.5, allow_redirects=True)
        end = time.time()
        
        if response.status_code == 200:
            ms = int((end - start) * 1000)
            return (ms, ext_satiri, link)
    except:
        pass
    return None

def yedek_kanali_temizle(metin):
    if "#EXTINF" in metin and "," in metin:
        parcalar = metin.rsplit(',', 1)
        ayarlar = parcalar[0]
        isim = parcalar[1]
        isim = re.sub(r'\s*\|\s*[A-Z0-9+]+\b', '', isim)
        isim = re.sub(r'\b(HEVC|RAW|PLUS|HD|FHD|SD|UHD|4K)\b', '', isim, flags=re.I)
        isim = re.sub(r'\s*\([0-9]{3,4}[pP]?\)', '', isim)
        isim = re.sub(r'\s+', ' ', isim).strip()
        isim = re.sub(r'^[\.\-\s|]+', '', isim)
        return f"{ayarlar},{isim}"
    return metin

def main():
    eklenen_urller = set()
    ana_liste_zirh = [] 
    toplanan_yedekler = []

    # 1. ADIM: ZIRHLI BÖLGEYİ KORU
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_icerik = f.readlines()
            ana_liste_zirh = tum_icerik[:ZIRH_LIMIT]
            for satir in ana_liste_zirh:
                if satir.strip().startswith("http"):
                    eklenen_urller.add(satir.strip())

    # 2. ADIM: YEDEKLERİ TOPLA
    for url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                temiz_veri = re.sub(r'#EXTVLCOPT:.*?\n', '', r.text)
                bulunanlar = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", temiz_veri, re.DOTALL)
                for kanal in bulunanlar:
                    satir_grubu = kanal.strip().split('\n')
                    if len(satir_grubu) >= 2:
                        ext = satir_grubu[0]
                        link = satir_grubu[-1].strip()
                        if any(yasak.upper() in ext.upper() for yasak in YASAKLI_GRUPLAR): continue
                        if link not in eklenen_urller:
                            temiz_ext = yedek_kanali_temizle(ext)
                            if 'group-title="' not in temiz_ext:
                                temiz_ext = temiz_ext.replace('#EXTINF:', '#EXTINF:-1 group-title="YEDEKLER",')
                            toplanan_yedekler.append((temiz_ext, link))
                            eklenen_urller.add(link)
        except: continue

    # 3. ADIM: AKILLI SIRALAMA (Çoklu İşlem ile Hızlı Test)
    print(f"Usta, {len(toplanan_yedekler)} yedek link test ediliyor...")
    sirali_yedekler = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(hiz_testi, toplanan_yedekler))
        # Boş olmayan (çalışan) sonuçları hızlarına (ms) göre sırala
        sirali_yedekler = sorted([r for r in results if r is not None], key=lambda x: x[0])

    # 4. ADIM: KAYDETME
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(ana_liste_zirh) # Zırhlı bölge başa
        f.write(f"\n# --- SIRALI YEDEKLER (EN HIZLI EN USTE) ---\n")
        
        for ms, ext, link in sirali_yedekler:
            f.write(f"{ext}\n{link}\n")
            
        zaman = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n# SON GUNCELLEME: {zaman} | {len(sirali_yedekler)} ADET AKTIF YEDEK\n")
    print("Usta sistem mermi gibi güncellendi!")

if __name__ == "__main__":
    main()
