import requests
import re
import os
import datetime

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

# GÜNCEL 6'LI KAYNAK LİSTEN
YEDEK_KAYNAKLAR = [
    "https://streams.uzunmuhalefet.com/lists/tr.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://mth.tc/DsGo",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u"
]

def main():
    # 1. ADIM: DOKUNULMAZ BÖLGEYİ (İLK 3963 SATIR) AL
    dokunulmaz_bolge = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_eski_satirlar = f.readlines()
            # 3963 satır senin kutsal bölgendir
            limit = min(3963, len(tum_eski_satirlar))
            dokunulmaz_bolge = tum_eski_satirlar[:limit]
            print(f"🛡️  {len(dokunulmaz_bolge)} SATIR KORUMAYA ALINDI.")
    
    # Dosya yoksa veya bozuksa başlığı ekle
    if not dokunulmaz_bolge or not dokunulmaz_bolge[0].startswith("#EXTM3U"):
        dokunulmaz_bolge = ["#EXTM3U\n"]
        print("⚠️ tr.m3u baştan oluşturuldu.")

    # 2. ADIM: KAYNAKLARDAN TAZE KANALLARI ÇEK
    taze_kanal_listesi = []
    for index, url in enumerate(YEDEK_KAYNAKLAR, 1):
        try:
            print(f"🌐 Kaynak taranıyor ({index}/6): {url}")
            r = requests.get(url, headers=HEADERS, timeout=35)
            if r.status_code == 200:
                # INFO ve URL bloklarını yakala
                kanallar = re.findall(r"(#EXTINF:[^\n]+\n+https?://[^\s\n]+)", r.text)
                if kanallar:
                    taze_kanal_listesi.extend(kanallar)
                    print(f"✅ {len(kanallar)} kanal eklendi.")
        except Exception as e:
            print(f"❌ Hata ({url}): {str(e)}")

    # 3. ADIM: DOSYAYI YAZ
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        # Önce sabit satırları yaz
        f.writelines(dokunulmaz_bolge)
        
        # Satır sonu kontrolü
        if dokunulmaz_bolge and not dokunulmaz_bolge[-1].endswith('\n'):
            f.write('\n')
            
        # Taze kanalları altına ekle
        for kanal_blogu in taze_kanal_listesi:
            f.write(kanal_blogu + "\n")
            
        # GÜNCELLEME İMZASI (GitHub'ın uyumamasını sağlar)
        zaman = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n# Son Guncelleme: {zaman}\n")

    # Temizlik
    if os.path.exists("canli.m3u"):
        os.remove("canli.m3u")

    print(f"🚀 GÜNCELLEME TAMAMLANDI! Toplam Yeni: {len(taze_kanal_listesi)}")

if __name__ == "__main__":
    main()
