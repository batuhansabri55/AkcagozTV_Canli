import requests
import re
import os

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

# SENİN BELİRLEDİĞİN SIRALAMA [Hiyerarşik Tarama]
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

    # 1. DOSYAYI OKU VE İLK 2229 SATIRI AYIR (KUTSAL BÖLGE)
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        tum_satirlar = f.readlines()

    # İlk 2229 satır dokunulmazdır
    dokunulmaz_bolge = tum_satirlar[:2229]
    print(f"🛡️  İLK 2229 SATIR KORUMA ALTINA ALINDI. BU BÖLGEYE DOKUNULMAYACAK.")

    # Mükerrer kontrolü için mevcut tüm linkleri tara (ilk 2229 dahil)
    mevcut_icerik_full = "".join(tum_satirlar)
    eklenen_linkler = set(re.findall(r'https?://[^\s\n]+', mevcut_icerik_full))
    
    yeni_kanallar = []

    # 2. KAYNAKLARI SENİN SIRALAMANA GÖRE TARA
    for s_url in YEDEK_KAYNAKLAR:
        try:
            print(f"🌐 Kaynak taranıyor ({YEDEK_KAYNAKLAR.index(s_url)+1}/6): {s_url}")
            r = requests.get(s_url, headers=HEADERS, timeout=25)
            if r.status_code == 200:
                # M3U formatındaki kanal bloklarını (Info + Link) yakala
                matches = re.findall(r"(#EXTINF:[^\n]+\n+https?://[^\s\n]+)", r.text)
                count = 0
                for blok in matches:
                    # Linki ayıkla
                    link_match = re.search(r'https?://[^\s\n]+', blok)
                    if link_match:
                        link = link_match.group(0).strip()
                        # Eğer link ne dokunulmaz bölgede ne de yeni eklenenlerde yoksa ekle
                        if link not in eklenen_linkler:
                            yeni_kanallar.append(blok)
                            eklenen_linkler.add(link)
                            count += 1
                print(f"✅ {count} yeni benzersiz kanal sıraya eklendi.")
        except Exception as e:
            print(f"⚠️  Kaynak hatası: {s_url} -> {str(e)}")

    # 3. DOSYAYI BİRLEŞTİR VE YAZ
    # Önce dokunulmaz 2229 satır, sonra senin sıranla gelen yeni kanallar
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        # Dokunulmaz bölgeyi olduğu gibi yaz
        f.writelines(dokunulmaz_bolge)
        
        # Eğer dosya sonu boşlukla bitmiyorsa bir alt satıra geç
        if dokunulmaz_bolge and not dokunulmaz_bolge[-1].endswith('\n'):
            f.write('\n')
            
        # Yeni kanalları ekle
        for kanal in yeni_kanallar:
            f.write(kanal + "\n")

    print(f"🚀 İŞLEM TAMAM!")
    print(f"📦 Korunan Satır: 2229")
    print(f"➕ Yeni Eklenen: {len(yeni_kanallar)} kanal.")
    print(f"📂 Toplam satır sayısı güncellendi.")

if __name__ == "__main__":
    main()
