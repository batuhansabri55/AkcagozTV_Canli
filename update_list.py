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
    """Sadece virgülden sonraki kanal ismini temizler, linke veya logoya dokunmaz."""
    if "#EXTINF" in metin and "," in metin:
        # Satırı virgülden ikiye böl: [Ayarlar/Logo kısmı, Kanal İsmi kısmı]
        parcalar = metin.rsplit(',', 1)
        ayarlar = parcalar[0]
        isim = parcalar[1]
        
        # 1. İsmin başındaki sayıları sil (14. , 1. vb.)
        isim = re.sub(r'^[0-9\.\-\s]+', '', isim)
        
        # 2. Parantezli çözünürlükleri sil (576p, 720p, 1080p vb.)
        isim = re.sub(r'\s*\([0-9]{3,4}[pP]?\)', '', isim)
        
        # 3. Etiketleri sil (-YT, HD, FHD vb.) - Tam kelime eşleşmesiyle
        isim = re.sub(r'\s*(-YT|\[.*?\]|\bHD\b|\bFHD\b|\bSD\b)\s*', '', isim, flags=re.I)
        
        # Boşlukları onar
        isim = ' '.join(isim.split()).strip()
        
        return f"{ayarlar},{isim}"
    return metin

def main():
    # 1. ADIM: DOKUNULMAZ BÖLGEYİ OKU VE SADECE İSİMLERİ DÜZELT
    temiz_dokunulmaz = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_satirlar = f.readlines()
            limit = min(3963, len(tum_satirlar))
            for satir in tum_satirlar[:limit]:
                # Sadece EXTINF satırıysa temizle, link satırıysa olduğu gibi bırak
                if satir.startswith("#EXTINF"):
                    temiz_dokunulmaz.append(kanal_temizle(satir) + "\n")
                else:
                    temiz_dokunulmaz.append(satir)

    # 2. ADIM: YEDEKLERİ ÇEK
    taze_kanal_listesi = []
    for url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            if r.status_code == 200:
                # Blokları (EXTINF + Link) çek
                bulunanlar = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", r.text, re.DOTALL)
                for kanal in bulunanlar:
                    satirlar = kanal.strip().split('\n')
                    if len(satirlar) >= 2:
                        ext_satiri = kanal_temizle(satirlar[0])
                        link_satiri = satirlar[1]
                        
                        if 'group-title="' not in ext_satiri:
                            ext_satiri = ext_satiri.replace('#EXTINF:', '#EXTINF:-1 group-title="YEDEKLER",')
                        
                        taze_kanal_listesi.append(f"{ext_satiri}\n{link_satiri}")
        except: pass

    # 3. ADIM: YAZMA
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(temiz_dokunulmaz)
        f.write("\n# --- YEDEKLER BAŞLADI ---\n")
        for k in taze_kanal_listesi:
            f.write(k + "\n")
        
        zaman = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n# GUNCELLEME: {zaman}\n")

    print(f"🚀 İşlem bitti usta. {len(taze_kanal_listesi)} yedek eklendi.")

if __name__ == "__main__":
    main()
