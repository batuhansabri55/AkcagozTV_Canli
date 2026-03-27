import requests
import re
import os
import datetime

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

# SENİN 6'LI ANA KAYNAĞIN + YENİ ONLİNE REPOLAR (HİÇBİRİSİNİ YEMEDİK USTA)
YEDEK_KAYNAKLAR = [
    "https://streams.uzunmuhalefet.com/lists/tr.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://mth.tc/DsGo",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    # --- YENİ TAZE YEDEKLER BURADAN GELİYOR ---
    "https://raw.githubusercontent.com/UzunMuhalefet/yayinlar/main/streams/best/all.m3u8",
    "https://raw.githubusercontent.com/UzunMuhalefet/Legal-IPTV/main/lists/turkey.m3u8"
]

def main():
    # 1. ADIM: DOKUNULMAZ BÖLGEYİ (İLK 3963 SATIR) MUHAFAZA ET
    dokunulmaz_bolge = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_eski_satirlar = f.readlines()
            # Senin el emeği göz nuru 3963 satırın burada kilitleniyor
            limit = min(3963, len(tum_eski_satirlar))
            dokunulmaz_bolge = tum_eski_satirlar[:limit]
            print(f"🛡️  TAM {len(dokunulmaz_bolge)} SATIR KORUMA ALTINA ALINDI. ASLA DEĞİŞMEZ.")

    # Dosya yoksa veya bozuksa başlığı ekle
    if not dokunulmaz_bolge or not dokunulmaz_bolge[0].startswith("#EXTM3U"):
        dokunulmaz_bolge = ["#EXTM3U\n"]
        print("⚠️ tr.m3u mevcut değildi, sıfırdan başlık atıldı.")

    # 2. ADIM: TÜM KAYNAKLARDAN (6+2) TAZE KANALLARI TOPLA
    taze_kanal_listesi = []
    for index, url in enumerate(YEDEK_KAYNAKLAR, 1):
        try:
            print(f"🌐 Kaynak taranıyor ({index}/{len(YEDEK_KAYNAKLAR)}): {url}")
            r = requests.get(url, headers=HEADERS, timeout=35)
            if r.status_code == 200:
                # INFO ve URL bloklarını hatasız yakala
                kanallar = re.findall(r"(#EXTINF:[^\n]+\n+https?://[^\s\n]+)", r.text)
                if kanallar:
                    taze_kanal_listesi.extend(kanallar)
                    print(f"✅ {len(kanallar)} kanal çekildi.")
        except Exception as e:
            print(f"❌ Hata oluştu ({url}): {str(e)}")

    # 3. ADIM: DOSYAYI YENİDEN İNŞA ET
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        # Önce senin o dokunulmaz 3963 satırını yazıyoruz
        f.writelines(dokunulmaz_bolge)
        
        # Satır sonu temizliği (Boşluk kalmasın)
        if dokunulmaz_bolge and not dokunulmaz_bolge[-1].endswith('\n'):
            f.write('\n')
        
        # Ardından tüm online yedekleri (Seninkiler + Yeniler) altına diziyoruz
        f.write("\n# --- OTOMATİK GÜNCEL YEDEKLER START ---\n")
        for kanal_blogu in taze_kanal_listesi:
            f.write(kanal_blogu + "\n")
            
        # GÜNCELLEME İMZASI
        zaman = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n# Son Sistem Guncellemesi: {zaman}\n")

    # Geçici dosyaları temizle
    if os.path.exists("canli.m3u"):
        os.remove("canli.m3u")

    print(f"🚀 İŞLEM TAMAM USTA! {len(taze_kanal_listesi)} Taze Yedek Listenin Altına Eklendi.")

if __name__ == "__main__":
    main()
