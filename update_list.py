import requests
import re
import os
import datetime

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

# SADECE BU GRUPLAR/KELİMELER GEÇİYORSA 3964'TEN SONRA EKLENECEK
FILTRE_KELIMELERI = [
    "TR FİLM", "ERLER FİLM", "ARZU FİLM", "YOUTUBE DIZI", 
    "YOUTUBE YABANCI FİLM", "YOUTUBE COCUK", "POLSKIEVTV", 
    "AZERBEYZAN", "SARKOR TV", "VIZI TV", "GLWIZ", 
    "PERSIAN", "Bulgaria", "GledaiTV", "Romania", 
    "RDS TV", "TouchTV", "Slovakia", "TURK", "TÜRK", "SPOR"
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
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://raw.githubusercontent.com/UzunMuhalefet/yayinlar/main/streams/best/all.m3u8",
    "https://raw.githubusercontent.com/UzunMuhalefet/Legal-IPTV/main/lists/turkey.m3u8"
]

def yedek_kanali_temizle(metin):
    """3964'TEN SONRASI İÇİN: İsimlerdeki gereksiz ekleri temizler."""
    if "#EXTINF" in metin and "," in metin:
        parcalar = metin.rsplit(',', 1)
        ayarlar = parcalar[0]
        isim = parcalar[1]
        
        # Temizlik regex işlemleri
        isim = re.sub(r'\s*\([0-9]{3,4}[pP]?\)', '', isim) 
        isim = re.sub(r'\s*(-YT|\[.*?\]|\bHD\b|\bFHD\b|\bSD\b)\s*', ' ', isim, flags=re.I)
        isim = re.sub(r'^[\.\-\s]+', '', isim)
        isim = ' '.join(isim.split()).strip()
        
        return f"{ayarlar},{isim}"
    return metin

def main():
    # 1. ADIM: 3963. SATIRA KADAR SIFIR MÜDAHALE (ZIRHLI KISIM)
    dokunulmaz_icerik = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_satirlar = f.readlines()
            limit = min(3963, len(tum_satirlar))
            for satir in tum_satirlar[:limit]:
                dokunulmaz_icerik.append(satir)

    print(f"🔄 3963 satır korumaya alındı. Kalanlar filtrelerle taranıyor...")

    # 2. ADIM: 3964'TEN SONRASI İÇİN FİLTRELİ YEDEKLER
    taze_kanal_listesi = []
    eklenen_urller = set()

    for url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            if r.status_code == 200:
                temiz_veri = re.sub(r'#EXTVLCOPT:.*?\n', '', r.text)
                bulunanlar = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", temiz_veri, re.DOTALL)
                
                for kanal in bulunanlar:
                    satir_grubu = kanal.strip().split('\n')
                    if len(satir_grubu) >= 2:
                        info_satiri = satir_grubu[0]
                        link_satiri = satir_grubu[-1].strip()

                        # FİLTRE KONTROLÜ: Sadece senin istediğin kelimeler varsa al
                        if any(k.upper() in info_satiri.upper() for k in FILTRE_KELIMELERI):
                            if link_satiri not in eklenen_urller:
                                temiz_info = yedek_kanali_temizle(info_satiri)
                                
                                # Grup başlığı yoksa "YEDEKLER" ekle
                                if 'group-title="' not in temiz_info:
                                    temiz_info = temiz_info.replace('#EXTINF:', '#EXTINF:-1 group-title="YEDEKLER",')
                                
                                taze_kanal_listesi.append(f"{temiz_info}\n{link_satiri}")
                                eklenen_urller.add(link_satiri)
            print(f"Bitti: {url}")
        except: continue

    # 3. ADIM: DOSYAYI YAZ
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        # Dokunulmaz ilk 3963 satır
        f.writelines(dokunulmaz_icerik)
        
        # 3964'ten sonrası
        f.write("\n# --- 3964+ FILTRELENMIS YEDEKLER ---\n")
        for k in taze_kanal_listesi:
            f.write(k + "\n")
        
        zaman = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n# SON GUNCELLEME: {zaman}\n")

    print(f"🚀 İşlem Tamam! 3963 satır korundu, üzerine {len(taze_kanal_listesi)} filtreli kanal eklendi.")

if __name__ == "__main__":
    main()
