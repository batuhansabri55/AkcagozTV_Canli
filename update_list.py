import requests
import re
import os
import datetime

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

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
    """Kanal D'yi korur, sadece sonuna eklenmiş -A, -B, -C, -D gibi takıları siler."""
    if "#EXTINF" in metin and "," in metin:
        parcalar = metin.rsplit(',', 1)
        ayarlar = parcalar[0]
        isim = parcalar[1]
        
        # 1. Baştaki gereksiz sayı/nokta temizliği
        isim = re.sub(r'^[0-9\.\-\s]+', '', isim)
        
        # 2. KRİTİK AYAR: Sadece önünde TİRE olan tek harfli takıları sil (-A, -B, -C, -D)
        # Eğer "Kanal D" yazıyorsa (önünde tire yok), D harfi kalır.
        # Eğer "TRT 1 -A" yazıyorsa (önünde tire var), -A kısmı silinir.
        isim = re.sub(r'\s*\-\s*[A-Z0-9]\b', '', isim, flags=re.I)
        
        # 3. İsteğe bağlı: İki tire arasındakileri de sil (-A-)
        isim = re.sub(r'\s*\-\s*[A-Z0-9]\s*\-\s*', ' ', isim, flags=re.I)
        
        # 4. HD, FHD ve Çözünürlük parantezlerini temizle
        isim = re.sub(r'\s*\([0-9]{3,4}[pP]?\)', '', isim)
        isim = re.sub(r'\s*(-YT|\[.*?\]|\bHD\b|\bFHD\b|\bSD\b)\s*', ' ', isim, flags=re.I)
        
        # 5. Boşlukları toparla
        isim = ' '.join(isim.split()).strip()
        
        # Eğer temizlik sonrası isim boş kalırsa veya çok kısalırsa "Kanal" yazmasın diye 
        # orijinal isme (Kanal D gibi) geri dönme emniyeti:
        if len(isim) < 2 and "D" in parcalar[1].upper():
            return f"{ayarlar},{parcalar[1].strip()}"
            
        return f"{ayarlar},{isim}"
    return metin

def main():
    # 1. DOKUNULMAZ BÖLGE (3963 SATIR)
    temiz_dokunulmaz = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_satirlar = f.readlines()
            limit = min(3963, len(tum_satirlar))
            for satir in tum_satirlar[:limit]:
                if satir.startswith("#EXTINF"):
                    temiz_dokunulmaz.append(kanal_temizle(satir) + "\n")
                else:
                    temiz_dokunulmaz.append(satir)

    # 2. YEDEKLERİ HIZLICA TOPLA
    taze_kanal_listesi = []
    print("🔄 Kanallar temizleniyor... Kanal D korunuyor.")
    for url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            if r.status_code == 200:
                bulunanlar = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", r.text, re.DOTALL)
                for kanal in bulunanlar:
                    satir = kanal.strip().split('\n')
                    if len(satir) >= 2:
                        ext = kanal_temizle(satir[0])
                        link = satir[1].strip()
                        if 'group-title="' not in ext:
                            ext = ext.replace('#EXTINF:', '#EXTINF:-1 group-title="YEDEKLER",')
                        taze_kanal_listesi.append(f"{ext}\n{link}")
        except: continue

    # 3. YAZMA
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(temiz_dokunulmaz)
        f.write("\n# --- KANAL D KORUMALI YEDEKLER ---\n")
        for k in taze_kanal_listesi:
            f.write(k + "\n")
        
        zaman = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n# SON GUNCELLEME: {zaman}\n")

    print(f"🚀 İşlem bitti usta. Kanal D artık güvende!")

if __name__ == "__main__":
    main()
