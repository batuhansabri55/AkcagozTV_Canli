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
    """Kanal D, TV 8, Kanal 7 gibi isimleri ASLA bozmaz. Sadece -A, -B gibi takıları siler."""
    if "#EXTINF" in metin and "," in metin:
        parcalar = metin.rsplit(',', 1)
        ayarlar = parcalar[0]
        isim = parcalar[1]
        
        # 1. Baştaki gereksiz sayı/nokta temizliği
        isim = re.sub(r'^[0-9\.\-\s]+', '', isim)
        
        # 2. HEDEF: Sadece önünde TİRE olan tek harfli takılar (-A, -B, -C, -D)
        # "\s+\-[A-Z]\b" -> Boşluk + Tire + Tek Harf demektir. 
        # Bu kural "Kanal D" içindeki D'yi silmez çünkü D'nin önünde tire yok.
        isim = re.sub(r'\s+\-+[A-Z0-9]\b', '', isim, flags=re.I)
        
        # 3. İki tire arasındaki harfleri de siler (-A-, -B-)
        isim = re.sub(r'\s*\-+[A-Z0-9]\-+\s*', ' ', isim, flags=re.I)
        
        # 4. Standart etiket temizliği (HD, FHD, SD ve parantezli çözünürlükler)
        isim = re.sub(r'\s*\([0-9]{3,4}[pP]?\)', '', isim)
        isim = re.sub(r'\s*(-YT|\[.*?\]|\bHD\b|\bFHD\b|\bSD\b)\s*', ' ', isim, flags=re.I)
        
        # 5. Son toparlama
        isim = ' '.join(isim.split()).strip()
        
        # EMNİYET SİBİBİ: Eğer isim temizlik sonrası sadece "Kanal" kalmışsa orijinaline dön
        if isim.lower() == "kanal" and "D" in parcalar[1].upper():
            return f"{ayarlar},Kanal D"
            
        return f"{ayarlar},{isim}"
    return metin

def main():
    # 1. DOKUNULMAZ BÖLGEYİ KORU
    temiz_dokunulmaz = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            limit = min(3963, len(lines))
            for s in lines[:limit]:
                if s.startswith("#EXTINF"):
                    temiz_dokunulmaz.append(kanal_temizle(s) + "\n")
                else:
                    temiz_dokunulmaz.append(s)

    # 2. YEDEKLERİ TOPLA (HIZLI MOD)
    taze_list = []
    print("🔄 Kanal D koruma modu aktif. Yedekler çekiliyor...")
    for url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            if r.status_code == 200:
                blocks = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", r.text, re.DOTALL)
                for b in blocks:
                    s = b.strip().split('\n')
                    if len(s) >= 2:
                        ext = kanal_temizle(s[0])
                        if 'group-title="' not in ext:
                            ext = ext.replace('#EXTINF:', '#EXTINF:-1 group-title="YEDEKLER",')
                        taze_list.append(f"{ext}\n{s[1].strip()}")
        except: continue

    # 3. YAZMA
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(temiz_dokunulmaz)
        f.write("\n# --- KANAL D GARANTILI YEDEKLER ---\n")
        for k in taze_list:
            f.write(k + "\n")
        
        z = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n# SON GUNCELLEME: {z}\n")

    print(f"🚀 Tamamdır usta. Kanal D artık 'Kanal' değil, 'Kanal D'!")

if __name__ == "__main__":
    main()
