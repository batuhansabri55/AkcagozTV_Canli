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

# Bu linkler asla silinmez, listenin başında kalır
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
    "https://giniko.smartiptvworld.workers.dev" # Ana hedef burası
]

def main():
    if not os.path.exists(FILE_PATH):
        print(f"❌ {FILE_PATH} bulunamadı!")
        return

    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        mevcut_icerik = f.read()

    yeni_liste = ["#EXTM3U"]
    eklenen_linkler = set()

    # 1. Önce mevcut dosyandaki DOKUNULMAZ linkleri korumaya al
    pattern = r"(#EXTINF:[^\n]+)\n+(https?://[^\s\n]+)"
    matches = re.findall(pattern, mevcut_icerik)
    
    for info, url in matches:
        link = url.strip()
        if any(d in link.lower() for d in DOKUNULMAZLAR):
            if link not in eklenen_linkler:
                yeni_liste.append(f"{info}\n{link}")
                eklenen_linkler.add(link)

    # 2. Tüm kaynakları "filtresiz" tara
    for s_url in YEDEK_KAYNAKLAR:
        try:
            print(f"🌐 Kaynak taranıyor: {s_url}")
            r = requests.get(s_url, headers=HEADERS, timeout=25)
            if r.status_code != 200: continue

            count = 0
            if "giniko" in s_url:
                # Giniko'daki tüm m3u8 linklerini ve yanındaki isimleri filtrelemeden al
                # Regex: Hem linki hem de tırnak içindeki ismi yakalar
                g_matches = re.findall(r'["\'](https?://[^"\']+m3u8[^"\']*)["\'].*?["\']([^"\']+)["\']', r.text)
                
                # Eğer standart yapı yoksa onclick/playStream yapısını dene
                if not g_matches:
                    g_matches = re.findall(r"playStream\('([^']+)','([^']+)'\)", r.text)

                for yl, yn in g_matches:
                    yl = yl.strip()
                    if yl not in eklenen_linkler:
                        yeni_liste.append(f'#EXTINF:-1 group-title="GINIKO_FULL",{yn.strip()}\n{yl}')
                        eklenen_linkler.add(yl)
                        count += 1
            else:
                # Diğer yedek m3u dosyalarındaki her şeyi al
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

    # 3. Dosyayı tamamen güncelle
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(yeni_liste))
    
    print(f"🚀 İŞLEM TAMAM! Toplam {len(yeni_liste)-1} kanal filtresiz kaydedildi.")

if __name__ == "__main__":
    main()
