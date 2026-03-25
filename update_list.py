import requests
import re
import os

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

# GÜNCEL KAYNAKLARIN
YEDEK_KAYNAKLAR = [
    "https://streams.uzunmuhalefet.com/lists/tr.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://mth.tc/DsGo",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u"
]

def main():
    # 1. ADIM: İLK 3963 SATIRI OKU (DOSYA YOKSA BİLE HATA VERME)
    dokunulmaz_bolge = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_eski_satirlar = f.readlines()
            dokunulmaz_bolge = tum_eski_satirlar[:3963]
            print(f"🛡️  İLK {len(dokunulmaz_bolge)} SATIR KORUMAYA ALINDI.")
    else:
        # Dosya yoksa en azından başlık koyalım ki bozulmasın
        dokunulmaz_bolge = ["#EXTM3U\n"]
        print("⚠️  tr.m3u bulunamadı, yeni başlık oluşturuldu.")

    # 2. ADIM: KAYNAKLARDAN KANALLARI ÇEK
    taze_kanal_listesi = []
    for url in YEDEK_KAYNAKLAR:
        try:
            print(f"🌐 Kaynak taranıyor ({YEDEK_KAYNAKLAR.index(url)+1}/{len(YEDEK_KAYNAKLAR)}): {url}")
            r = requests.get(url, headers=HEADERS, timeout=35)
            if r.status_code == 200:
                # Kanalları bul (INFO + URL)
                kanallar = re.findall(r"(#EXTINF:[^\n]+\n+https?://[^\s\n]+)", r.text)
                if kanallar:
                    taze_kanal_listesi.extend(kanallar)
                    print(f"✅ {len(kanallar)} kanal alındı.")
        except Exception as e:
            print(f"❌ Hata ({url}): {str(e)}")

    # 3. ADIM: DOSYAYI YAZ VE CANLI.M3U VARSA SİL
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(dokunulmaz_bolge)
        if dokunulmaz_bolge and not dokunulmaz_bolge[-1].endswith('\n'):
            f.write('\n')
        for kanal_blogu in taze_kanal_listesi:
            f.write(kanal_blogu + "\n")

    # Temizlik: Kod yanlışlıkla canli.m3u üretirse onu burada yok edelim
    if os.path.exists("canli.m3u"):
        os.remove("canli.m3u")

    print(f"🚀 GÜNCELLEME TAMAMLANDI!")
    print(f"➕ Toplam Yeni Kanal: {len(taze_kanal_listesi)}")

if __name__ == "__main__":
    main()
