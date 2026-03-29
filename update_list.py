import requests
import re
import os
import datetime

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

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
    """3964'TEN SONRASI İÇİN: Sayıları (TRT 1, TV 8) bozmadan kalite eklerini temizler."""
    if "#EXTINF" in metin and "," in metin:
        parcalar = metin.rsplit(',', 1)
        ayarlar = parcalar[0]
        isim = parcalar[1]

        # Eski usul temizlik (Sayılar kalır)
        isim = re.sub(r'\s*\([0-9]{3,4}[pP]?\)', '', isim) 
        isim = re.sub(r'\s*(-YT|\[.*?\]|\bHD\b|\bFHD\b|\bSD\b)\s*', ' ', isim, flags=re.I)
        isim = re.sub(r'^[\.\-\s]+', '', isim)
        
        isim = ' '.join(isim.split()).strip()
        return f"{ayarlar},{isim}"
    return metin

def main():
    # 1. ADIM: 3963. SATIRA KADAR SIFIR MÜDAHALE
    dokunulmaz_icerik = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_satirlar = f.readlines()
            # Senin kesin sınırın: 3963
            limit = min(3963, len(tum_satirlar))
            
            # BU DÖNGÜDE HİÇBİR İŞLEM YOK - OLDUĞU GİBİ ALIR
            for satir in tum_satirlar[:limit]:
                dokunulmaz_icerik.append(satir)

    # 2. ADIM: 3964'TEN SONRASI İÇİN YEDEKLERİ TEMİZLEYEREK EKLE
    print(f"🔄 3963 satıra zırh giydirildi. 3964'ten sonrası temizlenerek ekleniyor...")
    taze_kanal_listesi = []
    for url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            if r.status_code == 200:
                temiz_veri = re.sub(r'#EXTVLCOPT:.*?\n', '', r.text)
                bulunanlar = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", temiz_veri, re.DOTALL)
                for kanal in bulunanlar:
                    satir_grubu = kanal.strip().split('\n')
                    if len(satir_grubu) >= 2:
                        # Burada temizlik işlemi (Eski usul) devam ediyor
                        ext_satiri = yedek_kanali_temizle(satir_grubu[0])
                        link_satiri = satir_grubu[-1].strip()
                        
                        if 'group-title="' not in ext_satiri:
                            ext_satiri = ext_satiri.replace('#EXTINF:', '#EXTINF:-1 group-title="YEDEKLER",')
                        
                        taze_kanal_listesi.append(f"{ext_satiri}\n{link_satiri}")
        except: continue

    # 3. ADIM: DOSYAYI YAZ
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        # Senin emeğin olan ilk 3963 satır
        f.writelines(dokunulmaz_icerik)
        
        # 3964'ten itibaren başlayan temiz yedekler
        f.write("\n# --- 3964+ TEMIZ YEDEKLER ---\n")
        for k in taze_kanal_listesi:
            f.write(k + "\n")
        
        zaman = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n# SON GUNCELLEME: {zaman}\n")

    print(f"🚀 İşlem Tamam! İlk 3963 satıra dokunulmadı, kalanlar temizlendi.")

if __name__ == "__main__":
    main()
