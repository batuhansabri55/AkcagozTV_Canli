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

# BU KANALLARA DOKUNMAK YASAK!
KORUNACAKLAR = ["KANAL D", "TV 8,5", "TV 8.5", "TV 8", "KANAL 7"]

def kanal_temizle(metin):
    """Kanal D ve TV 8,5'u korur, -A-, -B- gibi takıları kökten siler."""
    if "#EXTINF" in metin and "," in metin:
        parcalar = metin.rsplit(',', 1)
        ayarlar = parcalar[0]
        isim = parcalar[1].strip()
        
        # 1. Koruma Kontrolü
        ust_isim = isim.upper()
        if any(k in ust_isim for k in KORUNACAKLAR):
            return f"{ayarlar},{isim}"

        # 2. Takı Temizliği (-A-, -B-, -C-, -D- gibi)
        # Sadece iki tire arasındaki tek harf/rakamı hedef alır
        isim = re.sub(r'\s*\-+[A-Z0-9]\-+\s*', ' ', isim, flags=re.I)
        # Sonundaki tireli harfi siler (-A, -D gibi)
        isim = re.sub(r'\s+\-+[A-Z0-9]$', '', isim, flags=re.I)
        
        # 3. Klasik Çöpler (HD, FHD, SD ve parantez içindekiler)
        isim = re.sub(r'\s*\([0-9]{3,4}[pP]?\)', '', isim)
        isim = re.sub(r'\s*(-YT|\[.*?\]|\bHD\b|\bFHD\b|\bSD\b)\s*', ' ', isim, flags=re.I)
        
        isim = ' '.join(isim.split()).strip()
        return f"{ayarlar},{isim}"
    return metin

def main():
    # 1. DOKUNULMAZ BÖLGEYİ OKU
    temiz_dokunulmaz = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Sadece ilk 3963 satırı al (Kod bulaşmışsa onları da temizler)
            for s in lines[:3963]:
                if s.startswith("#EXTINF"):
                    temiz_dokunulmaz.append(kanal_temizle(s) + "\n")
                elif s.startswith("http"):
                    temiz_dokunulmaz.append(s.strip() + "\n")
                elif s.startswith("#EXTM3U"):
                    temiz_dokunulmaz.append(s)

    # 2. YEDEKLERİ TOPLA
    taze_kanal_listesi = []
    for url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code == 200:
                blocks = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", r.text, re.DOTALL)
                for b in blocks:
                    s = b.strip().split('\n')
                    if len(s) >= 2:
                        ext = kanal_temizle(s[0])
                        link = s[1].strip()
                        if 'group-title="' not in ext:
                            ext = ext.replace('#EXTINF:', '#EXTINF:-1 group-title="YEDEKLER",')
                        taze_kanal_listesi.append(f"{ext}\n{link}")
        except: continue

    # 3. YAZMA (BURASI KRİTİK, KOD SIZMASINI ÖNLER)
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        # Başlangıç etiketi yoksa ekle
        if not any(x.startswith("#EXTM3U") for x in temiz_dokunulmaz):
            f.write("#EXTM3U\n")
            
        f.writelines(temiz_dokunulmaz)
        f.write("\n# --- TEMIZ YEDEKLER ---\n")
        for k in taze_kanal_listesi:
            f.write(k + "\n")
        
        z = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n# GUNCELLEME: {z}\n")

    print("🚀 İşlem bitti usta. Liste tertemiz.")

if __name__ == "__main__":
    main()
