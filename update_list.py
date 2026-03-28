import requests
import re
import os
import datetime

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

YEDEK_KAYNAKLAR = [
    "https://streams.uzunmuhalefet.com/lists/tr.m3u",
    "https://tinyurl.com/ytpatron",
    "https://urlz.fr/v1Xo",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://mth.tc/DsGo",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://raw.githubusercontent.com/UzunMuhalefet/yayinlar/main/streams/best/all.m3u8",
    "https://raw.githubusercontent.com/UzunMuhalefet/Legal-IPTV/main/lists/turkey.m3u8"
]

def kanal_temizle(metin):
    """Kanal ismindeki sayıları, çözünürlükleri ve gereksiz etiketleri siler."""
    if "#EXTINF" in metin:
        parcalar = metin.rsplit(',', 1)
        if len(parcalar) > 1:
            bilgi = parcalar[0]
            isim = parcalar[1]
            
            # 1. Başındaki "14. ", "1. " gibi sayıları siler
            isim = re.sub(r'^[0-9]+\.?[ ]*', '', isim)
            
            # 2. Sonundaki (1080p), -YT, [FHD], HD, SD gibi takıları siler
            # Büyük/küçük harf duyarsız (flags=re.I)
            temizlik_reg = r'\s*(\([0-9]+[pP]?\)|-YT|\[.*?\]|\bHD\b|\bFHD\b|\bSD\b|\bUHD\b|\b4K\b)\s*$'
            isim = re.sub(temizlik_reg, '', isim, flags=re.I)
            
            # 3. Çift boşlukları tek yapar ve kenarları kırpar
            isim = ' '.join(isim.split()).strip()
            
            return f"{bilgi},{isim}"
    return metin

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

    # 2. ADIM: ONLİNE KAYNAKLARI SÜZEREK ÇEK VE TEMİZLE
    taze_kanal_listesi = []
    for url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            if r.status_code == 200:
                bulunanlar = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", r.text, re.DOTALL)
                for kanal in bulunanlar:
                    kanal_satirlari = kanal.strip().split('\n')
                    if len(kanal_satirlari) >= 2:
                        # İlk satırı (EXTINF) temizliyoruz
                        temiz_extinf = kanal_temizle(kanal_satirlari[0])
                        link = kanal_satirlari[1]
                        
                        # TiviMate Grubu ekle (YEDEKLER)
                        if 'group-title="' not in temiz_extinf:
                            temiz_extinf = temiz_extinf.replace('#EXTINF:', '#EXTINF:-1 group-title="YEDEKLER",')
                        
                        taze_kanal_listesi.append(f"{temiz_extinf}\n{link}")
        except:
            print(f"❌ {url} kaynağına ulaşılamadı.")

    # 3. ADIM: YAZMA
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(dokunulmaz_bolge)
        
        if not dokunulmaz_bolge[-1].endswith('\n'):
            f.write('\n')
        
        f.write("\n# --- ONLİNE OTOMATİK YEDEKLER BAŞLADI (TEMİZLENDİ) ---\n")
        
        for kanal in taze_kanal_listesi:
            f.write(kanal + "\n")
            
        zaman = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n# SON GUNCELLEME: {zaman}\n")

    print(f"🚀 TOPLAM {len(taze_kanal_listesi)} YEDEK KANAL JİLET GİBİ EKLENDİ USTA!")

if __name__ == "__main__":
    main()
