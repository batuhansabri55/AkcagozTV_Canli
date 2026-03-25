import requests
import re
import os

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'https://giniko.smartiptvworld.workers.dev/',
}

# Bu linkler asla silinmez, her zaman listenin en başında durur
DOKUNULMAZLAR = [
    "premiumstream.in", "workers.dev", "mywire.org", "token=DeaTHLesS", 
    "goldvod.site", "trt.com.tr", "turknet.ercdn.net", "daioncdn.net"
]

YEDEK_KAYNAKLAR = [
    "https://mth.tc/DsGo",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://streams.uzunmuhalefet.com/lists/tr.m3u",
    "https://giniko.smartiptvworld.workers.dev"
]

def main():
    if not os.path.exists(FILE_PATH):
        print(f"❌ {FILE_PATH} bulunamadı!")
        return

    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        mevcut_icerik = f.read()

    yeni_liste = ["#EXTM3U"]
    eklenen_linkler = set()

    # 1. Mevcut dokunulmazları koru
    pattern = r"(#EXTINF:[^\n]+)\n+(https?://[^\s\n]+)"
    matches = re.findall(pattern, mevcut_icerik)
    for info, url in matches:
        link = url.strip()
        if any(d in link.lower() for d in DOKUNULMAZLAR):
            if link not in eklenen_linkler:
                yeni_liste.append(f"{info}\n{link}")
                eklenen_linkler.add(link)

    # 2. Kaynakları süpür (Filtresiz)
    for s_url in YEDEK_KAYNAKLAR:
        try:
            print(f"🌐 Kaynak taranıyor: {s_url}")
            r = requests.get(s_url, headers=HEADERS, timeout=30)
            if r.status_code != 200: continue

            count = 0
            if "giniko" in s_url:
                # GINIKO ÖZEL: Sayfadaki her türlü m3u8 linkini ve çevresindeki metni yakala
                # playStream('link', 'isim') veya "link", "isim" fark etmez
                all_links = re.findall(r'(https?://[^\s\'"<>]+m3u8[^\s\'"<>]*).*?([A-Za-z0-9\s\-]{3,20})', r.text)
                
                for yl, yn in all_links:
                    yl = yl.strip()
                    if yl not in eklenen_linkler:
                        # Gereksiz karakterleri temizle
                        clean_name = re.sub(r'[^A-Za-z0-9\s\-]', '', yn).strip()
                        yeni_liste.append(f'#EXTINF:-1 group-title="GINIKO_ALL",{clean_name if clean_name else "KANAL"}\n{yl}')
                        eklenen_linkler.add(yl)
                        count += 1
            else:
                # Standart m3u tarama
                y_matches = re.findall(pattern, r.text)
                for y_info, y_url in y_matches:
                    yl = y_url.strip()
                    if yl not in eklenen_linkler:
                        yeni_liste.append(f"{y_info}\n{yl}")
                        eklenen_linkler.add(yl)
                        count += 1
            print(f"✅ {count} kanal eklendi.")
        except Exception as e:
            print(f"⚠️ Hata: {str(e)}")

    # 3. Kaydet
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(yeni_liste))
    print(f"🚀 İŞLEM TAMAM! Toplam {len(yeni_liste)-1} kanal filtresiz olarak kaydedildi.")

if __name__ == "__main__":
    main()
