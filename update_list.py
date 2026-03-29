import requests
import re
import os
import datetime

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
ZIRH_LIMIT = 3963  # BU SATIRA KADAR NOKTASINA DOKUNULMAZ
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

YASAKLI_GRUPLAR = ["Webteizle", "TR FILM", "ARZU FILM", "ERLER FILM", "EZEL", "FilmMedya", "CINEMAMOD"]

YEDEK_KAYNAKLAR = [
    "https://streams.uzunmuhalefet.com/lists/tr.m3u",
    "https://tinyurl.com/ytpatron",
    "https://urlz.fr/v1Xo",
    "https://raw.githubusercontent.com/smartgmr/cdn/refs/heads/main/Perfect.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://tinyurl.com/bdd2tz6h",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://raw.githubusercontent.com/UzunMuhalefet/yayinlar/main/streams/best/all.m3u8",
    "https://raw.githubusercontent.com/UzunMuhalefet/Legal-IPTV/main/lists/turkey.m3u8"
]

def yedek_kanali_temizle(metin):
    """Sadece 3964+ sonrası gelen yedeklerin isimlerini temizler."""
    if "#EXTINF" in metin and "," in metin:
        parcalar = metin.rsplit(',', 1)
        ayarlar, isim = parcalar[0], parcalar[1]
        isim = re.sub(r'\s*\|\s*[A-Z0-9+]+\b', '', isim)
        isim = re.sub(r'\b(HEVC|RAW|PLUS|HD|FHD|SD|UHD|4K)\b', '', isim, flags=re.I)
        isim = re.sub(r'\s*\([0-9]{3,4}[pP]?\)', '', isim)
        isim = re.sub(r'\s+', ' ', isim).strip()
        return f"{ayarlar},{isim}"
    return metin

def main():
    eklenen_urller = set()
    dokunulmaz_icerik = []
    taze_kanal_listesi = []

    # 1. ADIM: 3963 SATIRI OLDUĞU GİBİ OKU VE LİNKLERİ HAFIZAYA AL
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_satirlar = f.readlines()
            limit = min(ZIRH_LIMIT, len(tum_satirlar))
            
            for i in range(limit):
                satir = tum_satirlar[i]
                dokunulmaz_icerik.append(satir)
                
                # Zırhlı bölgedeki linkleri hafızaya ekle ki aşağıda tekrar etmesin
                link_adresi = satir.strip()
                if link_adresi.startswith("http"):
                    eklenen_urller.add(link_adresi)

    print(f"🛡️ {ZIRH_LIMIT} satır zırhlandı. Hafızaya alınan orijinal link sayısı: {len(eklenen_urller)}")

    # 2. ADIM: YEDEKLERİ ÇEK (ZIRHTA VARSA EKLEME)
    for url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            if r.status_code == 200:
                temiz_veri = re.sub(r'#EXTVLCOPT:.*?\n', '', r.text)
                bulunanlar = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", temiz_veri, re.DOTALL)
                
                for kanal in bulunanlar:
                    satir_grubu = kanal.strip().split('\n')
                    if len(satir_grubu) >= 2:
                        ext_satiri = satir_grubu[0]
                        link_satiri = satir_grubu[-1].strip()

                        # Yasaklı kontrolü
                        if any(yasak.upper() in ext_satiri.upper() for yasak in YASAKLI_GRUPLAR):
                            continue

                        # EĞER BU LİNK ZIRHLI BÖLGEDE VEYA ÖNCEKİ YEDEKLERDE VARSA EKLEME
                        if link_satiri not in eklenen_urller:
                            temiz_ext = yedek_kanali_temizle(ext_satiri)
                            if 'group-title="' not in temiz_ext:
                                temiz_ext = temiz_ext.replace('#EXTINF:', '#EXTINF:-1 group-title="YEDEKLER",')
                            
                            taze_kanal_listesi.append(f"{temiz_ext}\n{link_satiri}")
                            eklenen_urller.add(link_satiri)
            print(f"Kaynak tarandı: {url}")
        except: continue

    # 3. ADIM: YAZMA
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        # Zırhlı bölge (Aynen kopyalandı, noktasına dokunulmadı)
        f.writelines(dokunulmaz_icerik)
        
        # Sadece zırhta olmayan benzersiz yedekler
        f.write("\n# --- 3964+ TEMIZ VE BENZERSIZ YEDEKLER ---\n")
        for k in taze_kanal_listesi:
            f.write(k + "\n")
        
        zaman = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n# SON GUNCELLEME: {zaman}\n")

    print(f"🚀 İşlem Tamam! Zırh korundu ve mükerrer yedekler engellendi.")

if __name__ == "__main__":
    main()
