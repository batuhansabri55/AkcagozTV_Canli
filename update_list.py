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
    """İsimdeki -A-, [B], (C), D gibi tüm tek harfli takıları ve etiketleri temizler."""
    if "#EXTINF" in metin and "," in metin:
        parcalar = metin.rsplit(',', 1)
        ayarlar = parcalar[0]
        isim = parcalar[1]
        
        # 1. Baştaki sayıları ve gereksiz noktaları temizle
        isim = re.sub(r'^[0-9\.\-\s]+', '', isim)
        
        # 2. KRİTİK: Tek harfli (A-Z) tüm takıları temizle
        # -D-, [D], (D), " D ", "- D" gibi her varyasyonu yakalar
        isim = re.sub(r'\s*[\-\(\[]?\s*\b[A-Z]\b\s*[\-\)\]]?\s*', ' ', isim, flags=re.I)
        
        # 3. Bilinen diğer kalabalıkları temizle
        isim = re.sub(r'\s*\([0-9]{3,4}[pP]?\)', '', isim)
        isim = re.sub(r'\s*(-YT|\[.*?\]|\bHD\b|\bFHD\b|\bSD\b)\s*', ' ', isim, flags=re.I)
        
        # 4. Temizliği bitir
        isim = ' '.join(isim.split()).strip()
        return f"{ayarlar},{isim}"
    return metin

def main():
    # 1. ADIM: DOKUNULMAZ BÖLGEYİ KORU (3963 SATIR)
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

    # 2. ADIM: YEDEKLERİ HIZLICA ÇEK VE TEMİZLE
    print("🔄 Yedekler toplanıyor, -D- gibi takılar ayıklanıyor...")
    taze_kanal_listesi = []
    for url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            if r.status_code == 200:
                bulunanlar = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", r.text, re.DOTALL)
                for kanal in bulunanlar:
                    satirlar = kanal.strip().split('\n')
                    if len(satirlar) >= 2:
                        ext_satiri = kanal_temizle(satirlar[0])
                        link_satiri = satirlar[1].strip()
                        
                        if 'group-title="' not in ext_satiri:
                            ext_satiri = ext_satiri.replace('#EXTINF:', '#EXTINF:-1 group-title="YEDEKLER",')
                        
                        taze_kanal_listesi.append(f"{ext_satiri}\n{link_satiri}")
        except: continue

    # 3. ADIM: YAZMA İŞLEMİ
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(temiz_dokunulmaz)
        f.write("\n# --- HARF TAKILARINDAN ARINDIRILMIS YEDEKLER ---\n")
        for k in taze_kanal_listesi:
            f.write(k + "\n")
        
        zaman = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n# SON GUNCELLEME: {zaman}\n")

    print(f"🚀 Tamamdır usta. -D- dahil tüm harfler temizlendi, toplam {len(taze_kanal_listesi)} yedek hazır.")

if __name__ == "__main__":
    main()
