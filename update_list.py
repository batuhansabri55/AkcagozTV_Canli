import requests
import re
import os
import datetime

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
# USTA, İLK 3950 SATIR ASLA DEĞİŞMEZ, YENİLER SONRASINA GELİR
ZIRH_LIMIT = 3950
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
    """Gelen isimleri senin ALIASES formatına (YEDEK/YEDK) çevirir usta."""
    if "#EXTINF" in metin and "," in metin:
        parcalar = metin.rsplit(',', 1)
        ayarlar = parcalar[0]
        isim = parcalar[1].upper().replace(" ", "") # Boşlukları siler
        
        # Gereksiz takıları temizle
        isim = re.sub(r'\b(HEVC|RAW|PLUS|HD|FHD|SD|UHD|4K)\b', '', isim, flags=re.I)
        isim = re.sub(r'[^A-Z0-9]', '', isim) # Sadece harf ve rakam
        
        # --- SENİN ÖZEL ALIASES FORMATIN ---
        if "HABERTURK" in isim: isim = "HABERTURKYEDK"
        elif "CNNTURK" in isim: isim = "CNNTURKYEDEK"
        elif "TV24" in isim: isim = "TV24YEDEK"
        elif "24TV" in isim: isim = "TV24YEDEK"
        else: isim = f"{isim}YEDEK" # Örn: ATV -> ATVYEDEK
            
        return f"{ayarlar},{isim}"
    return metin

def main():
    eklenen_urller = set()
    ana_liste_zirh = [] 
    taze_kanal_listesi = []

    # 1. ADIM: ZIRHLI BÖLGEYİ MUHAFAZA ET
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_icerik = f.readlines()
            ana_liste_zirh = tum_icerik[:ZIRH_LIMIT]
            
            for satir in ana_liste_zirh:
                if satir.strip().startswith("http"):
                    eklenen_urller.add(satir.strip())

    # 2. ADIM: DIŞ KAYNAKLARDAN TAZE YEDEKLERİ ÇEK
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
                            
                            # Listeye ekle (Sıralama için kanal ismini de saklıyoruz)
                            taze_kanal_listesi.append(f"{temiz_ext}\n{link_satiri}")
                            eklenen_urller.add(link_satiri)
        except:
            continue

    # --- 3. ADIM: PEŞ PEŞE DİZİLİM (SIRALAMA) ---
    # Yeni gelen yedekleri isme göre alfabetik sıralarız (ATV'ler alt alta gelir)
    taze_kanal_listesi.sort()

    # 4. ADIM: KAYDETME (3950'DEN SONRASINA)
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        # Önce dokunulmaz zırhlı listeyi yaz
        f.writelines(ana_liste_zirh)
        
        # Zırhın hemen sonuna (3951. satır civarı) açıklamayı ve sıralı yedekleri yaz
        f.write(f"\n# --- {ZIRH_LIMIT} SATIRLIK ZIRH SONRASI SIRALI YEDEKLER ---\n")
        for k in taze_kanal_listesi:
            f.write(k + "\n")
            
        zaman = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n# SON GUNCELLEME: {zaman}\n")
    
    print(f"Usta işlem tamam! {len(taze_kanal_listesi)} yeni yedek kanal bloklar halinde eklendi.")

if __name__ == "__main__":
    main()
