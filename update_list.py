import requests
import re
import os

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

# SENİN GÜNCEL 7'Lİ SIRALAMAN (HİÇBİRİNDE KOTA YOK)
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
        print(f"❌ Hata: {FILE_PATH} bulunamadı!")
        return

    # 1. ADIM: İLK 3963 SATIRI AYIR VE KORU
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        tum_eski_satirlar = f.readlines()

    # 3963 satır senin özel "Kutsal Bölgen"
    dokunulmaz_bolge = tum_eski_satirlar[:3963]
    print(f"🛡️  İLK 3963 SATIR MÜHÜRLENDİ. BU KISIM ASLA DEĞİŞMEZ.")

    # 2. ADIM: 7 KAYNAKTAN TÜM KANALLARI SIRASIYLA ÇEK
    taze_kanal_listesi = []
    
    for url in YEDEK_KAYNAKLAR:
        try:
            print(f"🌐 Kaynak taranıyor ({YEDEK_KAYNAKLAR.index(url)+1}/7): {url}")
            r = requests.get(url, headers=HEADERS, timeout=35)
            if r.status_code == 200:
                # Kanalları (INFO + URL) tırpanlamadan çek
                kanallar = re.findall(r"(#EXTINF:[^\n]+\n+https?://[^\s\n]+)", r.text)
                
                if kanallar:
                    taze_kanal_listesi.extend(kanallar)
                    print(f"✅ {len(kanallar)} kanalın tamamı alındı.")
                else:
                    print(f"⚠️  Uyarı: {url} adresinde kanal bulunamadı.")
        except Exception as e:
            print(f"❌ Bağlantı hatası ({url}): {str(e)}")

    # 3. ADIM: 3963'TEN SONRASINI SİL VE YENİLERİ YAZ
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        # Önce dokunulmaz kısmı yaz
        f.writelines(dokunulmaz_bolge)
        
        # Satır sonu kontrolü
        if dokunulmaz_bolge and not dokunulmaz_bolge[-1].endswith('\n'):
            f.write('\n')
            
        # Sonra 7 URL'den gelen tüm kanalları altına ekle
        for kanal_blogu in taze_kanal_listesi:
            f.write(kanal_blogu + "\n")

    print(f"🚀 GÜNCELLEME TAMAMLANDI!")
    print(f"📦 Korunan Sabit Satır: 3963")
    print(f"➕ Toplam Yeni Kanal: {len(taze_kanal_listesi)}")
    print(f"✅ Not: 2. sıraya onureroz.com eklendi.")

if __name__ == "__main__":
    main()

