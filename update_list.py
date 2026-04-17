import requests
import re
import os
import datetime

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
# USTA, İLK 4750 SATIR DOKUNULMAZDIR. YENİLER BUNUN SONUNA EKLENİR.
ZIRH_LIMIT = 4750
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

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
    "https://raw.githubusercontent.com/hayatiptv/iptv/master/index.m3u",
    "https://raw.githubusercontent.com/smartgmr/cdn/refs/heads/main/Perfect.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://tinyurl.com/bdd2tz6h",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u"
]

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
    taze_kanal_listesi = []

    print("--- ZIRH KORUMALI ISLEM BASLADI ---")

    # 1. ADIM: ZIRHLI BÖLGEYİ OKU
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_icerik = f.readlines()
            ana_liste_zirh = tum_icerik[:ZIRH_LIMIT]
            
            for satir in ana_liste_zirh:
                satir_temiz = satir.strip()
                if satir_temiz.startswith("http"):
                    eklenen_urller.add(satir_temiz)
        print(f"-> {len(ana_liste_zirh)} satirlik zirh korundu.")

    # 2. ADIM: DIŞ KAYNAKLARDAN ÇEK
    for url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code == 200:
                temiz_veri = re.sub(r'#EXTVLCOPT:.*?\n', '', r.text)
                bulunanlar = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", temiz_veri, re.DOTALL)
                for kanal in bulunanlar:
                    satir_grubu = kanal.strip().split('\n')
                    if len(satir_grubu) >= 2:
                        ext_satiri = satir_grubu[0]
                        link_satiri = satir_grubu[-1].strip()
                        
                        if any(yasak.upper() in ext_satiri.upper() for yasak in YASAKLI_GRUPLAR):
                            continue
                            
                        if link_satiri not in eklenen_urller:
                            temiz_ext = yedek_kanali_temizle(ext_satiri)
                            if 'group-title="' not in temiz_ext:
                                temiz_ext = temiz_ext.replace('#EXTINF:', '#EXTINF:-1 group-title="YEDEKLER",')
                            
                            taze_kanal_listesi.append(f"{temiz_ext}\n{link_satiri}")
                            eklenen_urller.add(link_satiri)
        except:
            continue

    # 3. ADIM: KAYDETME
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(ana_liste_zirh)
        f.write(f"\n# --- {ZIRH_LIMIT} SATIRLIK DOKUNULMAZ BOLGE SONRASI YEDEKLER ---\n")
        for k in taze_kanal_listesi:
            f.write(k + "\n")
            
        zaman = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n# SON GUNCELLEME: {zaman}\n")
    print(f"--- ISLEM TAMAMLANDI: {len(taze_kanal_listesi)} yeni yedek eklendi. ---")

if __name__ == "__main__":
    main()
