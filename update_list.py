import requests
import re
import os
import datetime
from concurrent.futures import ThreadPoolExecutor

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

# YEDEK KAYNAKLAR (Aynı kalıyor)
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

# --- GENİŞLETİLMİŞ ALIAS SİSTEMİ ---
# Senin paylaştığın listeye göre güncellendi
ALIAS_MAP = {
    "ATV": ["ATVHD 45", "ATVFHD 46"],
    "TRT 1": ["TRT148", "TRT1337667"],
    "SHOW": ["SHOWTVHD 43", "SHOWTVFHD 42"],
    "KANAL D": ["KANALDHD 39", "KANALDFHD 40"],
    "STAR": ["STARTVHD 36", "STARTVFHD 37"],
    "TV8": ["TV8HD 30", "TV8FHD 31"],
    "NOW": ["NowTVHD 34", "NowTVFHD 33"],
    "A HABER": ["A HABERHD 140", "A HABERFHD 139"],
    "CNN TURK": ["CNNTURKHD 150", "CNNTURKFHD 149"],
    "HABERTURK": ["HABERTURKHD 148", "HABERTURKFHD 147"],
    "NTV": ["NTVHD 152", "NTVFHD 151"],
    "HABER GLOBAL": ["HABERGLOBALHD 232359", "HABERGLOBALFHD 40495"],
    "TRT HABER": ["TRTHABERHD 146", "TRTHABERFHD 145"],
    "ULKE TV": ["ULKETVHD 133", "ULKETVFHD 132"],
    "TV100": ["TV100HD 232356", "TV100FHD 50939"],
    "SZC": ["SZCTVHD 232355", "SZCTVFHD 144"],
    "HALK TV": ["HALK TV 232357", "HALK TV 5"],
    "KRT": ["KRT TV 232358", "KRT TV 15281"],
    "TGRT": ["TGRT HABER 222870", "TGRT HABER 232352"],
    "TELE 1": ["TELE 1 121"],
    "BEYAZ": ["BEYAZ TV 24", "BEYAZ TV 25"],
    "KANAL 7": ["KANAL 7 50845", "KANAL 7 22"],
    "TEVE 2": ["TEVE 2 18", "TEVE 2 19"],
    "A2": ["A2 9"],
    "TV8.5": ["TV85HD 27", "TV85FHD 28"],
    "TRT 2": ["TRT 2 40980"],
    "EKOL": ["EKOL TV 255109"],
    "BLOOMBERG": ["BLOOMBERGHT 137", "BLOOMBERGHT 50842"],
    "BEIN SERIES": ["beIN Series 1 222", "beIN Series 2 220", "beIN Series 3 219", "beIN Series 4 103134"]
}

sayaclar = {k: 0 for k in ALIAS_MAP.keys()}

def alias_yap(isim):
    upper_isim = isim.upper()
    for anahtar, varyasyonlar in ALIAS_MAP.items():
        if anahtar in upper_isim:
            idx = sayaclar[anahtar] % len(varyasyonlar)
            yeni = varyasyonlar[idx]
            sayaclar[anahtar] += 1
            return yeni
    return isim # Eşleşmezse orijinali bırak

def link_canli_mi(item):
    ext, link = item
    try:
        r = requests.head(link, headers=HEADERS, timeout=3, allow_redirects=True)
        if r.status_code == 200:
            return f"{ext}\n{link}"
    except: pass
    return None

def main():
    # 1. DOKUNULMAZ BÖLGE
    temiz_dokunulmaz = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            temiz_dokunulmaz = lines[:3963]

    # 2. YEDEKLERİ ÇEK
    kontrol_listesi = []
    print("🔄 Yedekler çekiliyor ve Alias atanıyor...")
    for url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                # Regex ile blokları çek
                bulunanlar = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", r.text, re.DOTALL)
                for kanal in bulunanlar:
                    satir = kanal.strip().split('\n')
                    if len(satir) >= 2:
                        ext_part = satir[0]
                        link_part = satir[1].strip()
                        
                        # İsim kısmını bul ve Alias'a sok
                        if "," in ext_part:
                            bas, isim = ext_part.rsplit(',', 1)
                            yeni_isim = alias_yap(isim.strip())
                            yeni_ext = f"{bas},{yeni_isim}"
                            
                            # Group-title ekle
                            if 'group-title' not in yeni_ext:
                                yeni_ext = yeni_ext.replace('#EXTINF:', '#EXTINF:-1 group-title="YEDEKLER",')
                            
                            kontrol_listesi.append((yeni_ext, link_part))
        except: continue

    # 3. PARALEL HIZLI TARAMA
    print(f"⚡ {len(kontrol_listesi)} yedek kontrol ediliyor (Aynı anda 50 link)...")
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(link_canli_mi, kontrol_listesi))
    
    # 4. DOSYAYA YAZ
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(temiz_dokunulmaz)
        f.write("\n# --- PROFESYONEL ALIAS YEDEKLERİ ---\n")
        for res in results:
            if res: f.write(res + "\n")
        
        f.write(f"\n# SON GUNCELLEME: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"🚀 Usta işlem tamam! Sağlam linkler senin numaralı sistemine göre dizildi.")

if __name__ == "__main__":
    main()
