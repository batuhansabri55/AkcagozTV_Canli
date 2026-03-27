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
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://mth.tc/DsGo",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://raw.githubusercontent.com/UzunMuhalefet/yayinlar/main/streams/best/all.m3u8",
    "https://raw.githubusercontent.com/UzunMuhalefet/Legal-IPTV/main/lists/turkey.m3u8"
]

def main():
    # 1. ADIM: KUTSALI KORU
    dokunulmaz_bolge = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_satirlar = f.readlines()
            limit = min(3963, len(tum_satirlar))
            dokunulmaz_bolge = tum_satirlar[:limit]

    if not dokunulmaz_bolge: dokunulmaz_bolge = ["#EXTM3U\n"]

    # 2. ADIM: DAHA GÜÇLÜ ARAMA (REGEX GÜNCELLENDİ)
    taze_kanal_listesi = []
    for url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=35)
            if r.status_code == 200:
                # Yeni Regex: #EXTINF satırından başlayıp linkin sonuna kadar her şeyi alır
                kanallar = re.findall(r"(#EXTINF:[^\n]+\n+http[^\s\n]+)", r.text)
                taze_kanal_listesi.extend(kanallar)
        except: pass

    # 3. ADIM: YAZMA
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(dokunulmaz_bolge)
        if not dokunulmaz_bolge[-1].endswith('\n'): f.write('\n')
        
        f.write("\n# --- YENI YEDEKLER BASLADI ---\n")
        for kanal in taze_kanal_listesi:
            f.write(kanal + "\n")
            
        zaman = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n# Guncelleme: {zaman}\n")

    print(f"🚀 {len(taze_kanal_listesi)} Kanal Eklendi!")

if __name__ == "__main__":
    main()
