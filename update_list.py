import requests
import re
import os

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

# SENİN BELİRLEDİĞİN 6 URL (SIRALAMA VE TAM İÇERİK GARANTİLİ)
YEDEK_KAYNAKLAR = [
    "https://streams.uzunmuhalefet.com/lists/tr.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://mth.tc/DsGo",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u"
]

def main():
    if not os.path.exists(FILE_PATH):
        print(f"❌ Hata: {FILE_PATH} dosyası dizinde bulunamadı!")
        return

    # 1. ADIM: İLK 3963 SATIRI KORUMAYA AL (KUTSAL BÖLGE)
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        tum_eski_satirlar = f.readlines()

    dokunulmaz_bolge = tum_eski_satirlar[:3963]
    print(f"🛡️  İLK 3963 SATIR MÜHÜRLENDİ. DEĞİŞİKLİK YAPILMAYACAK.")

    # 2. ADIM: 6 KAYNAKTAN TÜM KANALLARI SIRASIYLA TOPLA
    taze_kanal_listesi = []
    
    for url in YEDEK_KAYNAKLAR:
        try:
            print(f"🌐 Kaynak taranıyor: {url}")
            r = requests.get(url, headers=HEADERS, timeout=35)
            if r.status_code == 200:
                # M3U kanal bloklarını (Bilgi satırı + URL satırı) eksiksiz yakala
                # Not: Tırpanlama veya mükerrer kontrolü yapmadan NE VARSA ALIR.
                kanallar = re.findall(r"(#EXTINF:[^\n]+\n+https?://[^\s\n]+)", r.text)
                
                if kanallar:
                    taze_kanal_listesi.extend(kanallar)
                    print(f"✅ {len(kanallar)} kanalın tamamı sıraya eklendi.")
                else:
                    print(f"⚠️  Uyarı: {url} adresinde uygun formatta kanal bulunamadı.")
        except Exception as e:
            print(f"❌ Bağlantı hatası ({url}): {str(e)}")

    # 3. ADIM: GITHUB ÜZERİNDEKİ DOSYAYI GÜNCELLE (YAZMA)
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        # Önce mühürlü 3963 satırı olduğu gibi yaz (Eskisi neyse o)
        f.writelines(dokunulmaz_bolge)
        
        # Eğer dosyanın son satırı alt satıra geçmiyorsa geçiş ekle
        if dokunulmaz_bolge and not dokunulmaz_bolge[-1].endswith('\n'):
            f.write('\n')
            
        # 3963'ten sonrasını silmiştik, şimdi taze kanalları sırasıyla ekle
        for kanal_blogu in taze_kanal_listesi:
            f.write(kanal_blogu + "\n")

    print(f"🚀 İŞLEM BAŞARIYLA BİTTİ!")
    print(f"📦 Korunan Sabit Satır: 3963")
    print(f"➕ Eklenen Güncel Kanal: {len(taze_kanal_listesi)}")
    print(f"📝 Sonuç: 3963 satırdan sonrası tamamen yenilendi ve GitHub'a hazır.")

if __name__ == "__main__":
    main()
