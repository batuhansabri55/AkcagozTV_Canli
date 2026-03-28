import requests
import re
import os
import datetime
from concurrent.futures import ThreadPoolExecutor # Hızlandırıcı motor bu

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

def link_kontrol_et(kanal_blogu):
    """Tek bir kanal bloğunu (EXTINF + Link) kontrol eder."""
    satirlar = kanal_blogu.strip().split('\n')
    if len(satirlar) < 2: return None
    
    ext_satiri = satirlar[0]
    link_satiri = satirlar[1].strip()
    
    try:
        # Timeout 5 saniye, paralel çalıştığı için bekleme yapmaz
        r = requests.head(link_satiri, headers=HEADERS, timeout=5, allow_redirects=True)
        if r.status_code == 200:
            # İsim temizleme senin kodundaki mantıkla aynen devam
            temiz_ext = kanal_temizle(ext_satiri)
            if 'group-title="' not in temiz_ext:
                temiz_ext = temiz_ext.replace('#EXTINF:', '#EXTINF:-1 group-title="YEDEKLER",')
            return f"{temiz_ext}\n{link_satiri}"
    except:
        pass
    return None

def kanal_temizle(metin):
    """Senin kodundaki temizlik mantığının birebir aynısı."""
    if "#EXTINF" in metin and "," in metin:
        parcalar = metin.rsplit(',', 1)
        ayarlar = parcalar[0]
        isim = parcalar[1]
        isim = re.sub(r'^[0-9\.\-\s]+', '', isim)
        isim = re.sub(r'\s*\([0-9]{3,4}[pP]?\)', '', isim)
        isim = re.sub(r'\s*(-YT|\[.*?\]|\bHD\b|\bFHD\b|\bSD\b)\s*', '', isim, flags=re.I)
        isim = ' '.join(isim.split()).strip()
        return f"{ayarlar},{isim}"
    return metin

def main():
    # 1. DOKUNULMAZ BÖLGE
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

    # 2. YEDEKLERİ TOPLA
    ham_kanallar = []
    for url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            if r.status_code == 200:
                bulunanlar = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", r.text, re.DOTALL)
                ham_kanallar.extend(bulunanlar)
        except: continue

    # 3. HIZLI (PARALEL) KONTROL - BÜYÜ BURADA
    print(f"⚡ {len(ham_kanallar)} yedek 50 koldan taranıyor...")
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(link_kontrol_et, ham_kanallar))

    # 4. YAZMA
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(temiz_dokunulmaz)
        f.write("\n# --- HIZLI KONTROL EDİLMİŞ YEDEKLER ---\n")
        for res in results:
            if res: f.write(res + "\n")
        
        zaman = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n# SON GÜNCELLEME: {zaman}\n")

    print(f"🚀 İşlem bitti! Toplam sağlam yedek eklendi.")

if __name__ == "__main__":
    main()
