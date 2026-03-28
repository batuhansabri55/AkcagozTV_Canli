import requests
import re
import os
import datetime

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

# SENİN 6'LI ANA LİSTEN + TAZE REPOLAR
YEDEK_KAYNAKLAR = [
    "https://streams.uzunmuhalefet.com/lists/tr.m3u",
    "https://tinyurl.com/ytpatron",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://mth.tc/DsGo",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://raw.githubusercontent.com/UzunMuhalefet/yayinlar/main/streams/best/all.m3u8",
    "https://raw.githubusercontent.com/UzunMuhalefet/Legal-IPTV/main/lists/turkey.m3u8"
]

def main():
    # 1. ADIM: KUTSAL 3963 SATIRI KORU
    dokunulmaz_bolge = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_satirlar = f.readlines()
            limit = min(3963, len(tum_satirlar))
            dokunulmaz_bolge = tum_satirlar[:limit]
            print(f"🛡️  {len(dokunulmaz_bolge)} SATIR KİLİTLENDİ.")

    if not dokunulmaz_bolge:
        dokunulmaz_bolge = ["#EXTM3U\n"]

    # 2. ADIM: ONLİNE KAYNAKLARI SÜZEREK ÇEK
    taze_kanal_listesi = []
    for url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            if r.status_code == 200:
                # Regex'i genişlettik: Satır aralarındaki boşluklara takılmaz
                bulunanlar = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", r.text, re.DOTALL)
                for kanal in bulunanlar:
                    # Sadece Türkiye kanallarını veya senin yedekleri içerenleri al
                    kanal_temiz = kanal.strip()
                    # Eğer kanal zaten senin dokunulmaz bölgede yoksa ekle (opsiyonel)
                    taze_kanal_listesi.append(kanal_temiz)
        except:
            print(f"❌ {url} kaynağına ulaşılamadı.")

    # 3. ADIM: YAZMA (YEDEKLERİ GRUPLAYARAK)
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(dokunulmaz_bolge)
        
        if not dokunulmaz_bolge[-1].endswith('\n'):
            f.write('\n')
        
        # AYIRICI BAŞLIK VE GRUP ETİKETİ
        f.write("\n# --- ONLİNE OTOMATİK YEDEKLER BAŞLADI ---\n")
        
        for kanal in taze_kanal_listesi:
            # Gelen kanalları TiviMate'te kolay bulman için "YEDEK" grubuna sokuyoruz
            if 'group-title="' not in kanal:
                kanal = kanal.replace('#EXTINF:', '#EXTINF:-1 group-title="YEDEKLER",')
            f.write(kanal + "\n")
            
        zaman = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n# SON GUNCELLEME: {zaman}\n")

    print(f"🚀 TOPLAM {len(taze_kanal_listesi)} YEDEK KANAL EKLENDİ USTA!")

if __name__ == "__main__":
    main()
