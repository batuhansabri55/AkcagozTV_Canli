import requests
import re
import os

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

# SENİN BELİRLEDİĞİN 6'LI SIRALAMA
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

    # 1. DOSYAYI OKU VE İLK 3963 SATIRI KİLİTLE
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        satirlar = f.readlines()

    # Artık dokunulmaz sınırımız: 3963
    dokunulmaz_bolge = satirlar[:3963]
    print(f"🛡️  İLK 3963 SATIR MÜHÜRLENDİ. GOLD VOD VE ÖZEL LİSTEN GÜVENDE.")

    # Mükerrer kontrolü için mevcut tüm linkleri tara (3963 satır dahil)
    mevcut_metin = "".join(satirlar)
    eklenen_linkler = set(re.findall(r'https?://[^\s\n]+', mevcut_metin))
    
    yeni_eklenecekler = []

    # 2. KAYNAKLARI SIRASIYLA TARA (1'DEN 6'YA)
    for url in YEDEK_KAYNAKLAR:
        try:
            print(f"🌐 Kaynak taranıyor ({YEDEK_KAYNAKLAR.index(url)+1}/6): {url}")
            r = requests.get(url, headers=HEADERS, timeout=25)
            if r.status_code == 200:
                # Kanal bloklarını (EXTINF + URL) yakala
                matches = re.findall(r"(#EXTINF:[^\n]+\n+https?://[^\s\n]+)", r.text)
                sayac = 0
                for blok in matches:
                    link_match = re.search(r'https?://[^\s\n]+', blok)
                    if link_match:
                        link = link_match.group(0).strip()
                        # Link senin 3963 satırlık kilitli bölgende yoksa ekle
                        if link not in eklenen_linkler:
                            yeni_eklenecekler.append(blok)
                            eklenen_linkler.add(link)
                            sayac += 1
                print(f"✅ {sayac} yeni kanal sıraya alındı.")
        except Exception as e:
            print(f"⚠️  Bağlantı hatası: {url} -> {str(e)}")

    # 3. YAZMA AŞAMASI (DÜZENLİ VE SIRALI)
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        # ÖNCE KİLİTLİ 3963 SATIRI YAZ
        f.writelines(dokunulmaz_bolge)
        
        # Satır sonu kontrolü
        if dokunulmaz_bolge and not dokunulmaz_bolge[-1].endswith('\n'):
            f.write('\n')
            
        # SONRA YENİ KANALLARI EKLE
        for kanal in yeni_eklenecekler:
            f.write(kanal + "\n")

    print(f"🚀 İŞLEM BAŞARIYLA TAMAMLANDI!")
    print(f"📦 Korunan Satır Sayısı: 3963")
    print(f"➕ Eklenen Yeni Kanal: {len(yeni_eklenecekler)}")

if __name__ == "__main__":
    main()
