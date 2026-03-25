import requests
import re
import os

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

# SENİN ATTIĞIN TAM SIRALAMA
YEDEK_KAYNAKLAR = [
    "https://streams.uzunmuhalefet.com/lists/tr.m3u",             # 1. Sırada
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u", # 2. Sırada
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8", # 3. Sırada
    "https://mth.tc/DsGo",                                       # 4. Sırada
    "https://publiciptv.com/countries/tr/m3u",                   # 5. Sırada
    "https://iptv-org.github.io/iptv/countries/tr.m3u"           # 6. Sırada
]

def main():
    if not os.path.exists(FILE_PATH):
        print(f"❌ {FILE_PATH} bulunamadı!")
        return

    # 1. DOSYAYI OKU VE İLK 2229 SATIRI KESİP AYIR
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        satirlar = f.readlines()

    # İlk 2229 satır dokunulmaz "Kutsal Bölge"
    dokunulmaz_bolge = satirlar[:2229]
    print(f"🛡️  İlk 2229 satır ayrıldı ve koruma altına alındı.")

    # Mükerrer (çift) kanal olmaması için mevcut tüm linkleri bir hafızaya alalım
    mevcut_metin = "".join(satirlar)
    eklenen_linkler = set(re.findall(r'https?://[^\s\n]+', mevcut_metin))
    
    yeni_eklenecekler = []

    # 2. KAYNAKLARI SIRASIYLA TARA
    for url in YEDEK_KAYNAKLAR:
        try:
            print(f"🌐 Kaynak taranıyor: {url}")
            r = requests.get(url, headers=HEADERS, timeout=20)
            if r.status_code == 200:
                # Kanal bloğunu (EXTINF ve URL) beraber yakala
                matches = re.findall(r"(#EXTINF:[^\n]+\n+https?://[^\s\n]+)", r.text)
                sayac = 0
                for blok in matches:
                    # Blok içindeki linki bul
                    link = re.search(r'https?://[^\s\n]+', blok).group(0).strip()
                    # Eğer bu link listede (özellikle ilk 2229'da) yoksa listeye ekle
                    if link not in eklenen_linkler:
                        yeni_eklenecekler.append(blok)
                        eklenen_linkler.add(link)
                        sayac += 1
                print(f"✅ {sayac} yeni kanal alındı.")
        except:
            print(f"⚠️  Bağlantı hatası: {url}")

    # 3. YAZMA AŞAMASI (KARIŞIKLIK OLMADAN)
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        # ÖNCE DOKUNULMAZ 2229 SATIR
        f.writelines(dokunulmaz_bolge)
        
        # Eğer dosya sonu alt satıra geçmemişse geç
        if dokunulmaz_bolge and not dokunulmaz_bolge[-1].endswith('\n'):
            f.write('\n')
            
        # SONRA YENİ KANALLAR
        for kanal in yeni_eklenecekler:
            f.write(kanal + "\n")

    print(f"🚀 BİTTİ! 2229 satır korundu, üzerine {len(yeni_eklenecekler)} yeni kanal eklendi.")

if __name__ == "__main__":
    main()
