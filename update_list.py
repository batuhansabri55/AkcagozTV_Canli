import requests
import re
import os
import datetime

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
ZIRH_LIMIT = 6210  # Bu satıra kadar olan kısım dokunulmazdır
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

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

def link_saglam_mi(url):
    """Linkin gerçekten çalışıp çalışmadığını kontrol eder"""
    try:
        # HEAD isteği ile sadece başlığı kontrol eder, hızlıdır
        response = requests.head(url, headers=HEADERS, timeout=7, allow_redirects=True)
        return response.status_code == 200
    except:
        return False

def yedek_kanali_temizle(metin):
    """Kanal isimlerini temizleyip düzenler"""
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

    print(f"🚀 Operasyon Başladı: {ZIRH_LIMIT} satırlık zırh korunuyor...")

    # 1. ADIM: ZIRHLI BÖLGEYİ OKU VE KORU
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_icerik = f.readlines()
            ana_liste_zirh = tum_icerik[:ZIRH_LIMIT]
            
            for satir in ana_liste_zirh:
                satir_temiz = satir.strip()
                if satir_temiz.startswith("http"):
                    eklenen_urller.add(satir_temiz)
        print(f"✅ Zırhlı bölgedeki {len(eklenen_urller)} URL muhafaza edildi.")

    # 2. ADIM: DIŞ KAYNAKLARDAN ÇEK VE FİLTRELE
    for kaynak_url in YEDEK_KAYNAKLAR:
        print(f"\n📡 Kaynak taranıyor: {kaynak_url[:40]}...")
        try:
            r = requests.get(kaynak_url, headers=HEADERS, timeout=15)
            if r.status_code == 200:
                temiz_veri = re.sub(r'#EXTVLCOPT:.*?\n', '', r.text)
                bulunanlar = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", temiz_veri, re.DOTALL)
                
                for kanal in bulunanlar:
                    satir_grubu = kanal.strip().split('\n')
                    if len(satir_grubu) >= 2:
                        ext_satiri = satir_grubu[0]
                        link_satiri = satir_grubu[-1].strip()
                        
                        # Yasaklı grup kontrolü
                        if any(yasak.upper() in ext_satiri.upper() for yasak in YASAKLI_GRUPLAR):
                            continue
                            
                        # Mükerrer ve Canlılık kontrolü
                        if link_satiri not in eklenen_urller:
                            if link_saglam_mi(link_satiri):
                                temiz_ext = yedek_kanali_temizle(ext_satiri)
                                if 'group-title="' not in temiz_ext:
                                    temiz_ext = temiz_ext.replace('#EXTINF:', '#EXTINF:-1 group-title="YEDEKLER",')
                                
                                taze_kanal_listesi.append(f"{temiz_ext}\n{link_satiri}")
                                eklenen_urller.add(link_satiri)
                                print(f"  + Eklendi: {link_satiri[:40]}...")
                            else:
                                # Ölü linkleri depoya sokmuyoruz
                                pass 
        except Exception as e:
            print(f"  ⚠️ Kaynak hatası: {e}")
            continue

    # 3. ADIM: KAYDETME
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(ana_liste_zirh) # Zırhlı bölgeyi aynen yaz
        f.write(f"\n# --- DOKUNULMAZ BOLGE SONRASI CANLI YEDEKLER ---\n")
        for k in taze_kanal_listesi:
            f.write(k + "\n")
            
        zaman = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n# SON OTOMATIK GUNCELLEME: {zaman}\n")
    
    print(f"\n🏁 İşlem Bitti Usta! {len(taze_kanal_listesi)} adet taze ve çalışan yedek depoya eklendi.")

if __name__ == "__main__":
    main()
