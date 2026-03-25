import requests
import re
import os

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Referer': 'https://giniko.smartiptvworld.workers.dev/',
}

# Dokunulmaz linkler - D1 veritabanı yapına göre
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
    "https://giniko.smartiptvworld.workers.dev" # Ana Hedef
]

def main():
    if not os.path.exists(FILE_PATH):
        print(f"❌ {FILE_PATH} bulunamadı!")
        return

    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        mevcut_icerik = f.read()

    yeni_liste = ["#EXTM3U"]
    eklenen_linkler = set()

    # 1. Dokunulmazları en başa ekle
    pattern = r"(#EXTINF:[^\n]+)\n+(https?://[^\s\n]+)"
    matches = re.findall(pattern, mevcut_icerik)
    for info, url in matches:
        link = url.strip()
        if any(d in link.lower() for d in DOKUNULMAZLAR):
            if link not in eklenen_linkler:
                yeni_liste.append(f"{info}\n{link}")
                eklenen_linkler.add(link)

    # 2. Kaynakları tara
    for s_url in YEDEK_KAYNAKLAR:
        try:
            print(f"🌐 Kaynak taranıyor: {s_url}")
            r = requests.get(s_url, headers=HEADERS, timeout=30)
            if r.status_code != 200: continue

            count = 0
            if "giniko" in s_url:
                # GINIKO ÖZEL: Sayfadaki TÜM .m3u8 içeren linkleri yakala
                # image_b3a327'deki mncdn yapısını ve token parametrelerini hedefler
                # Regex'i hem tırnaklı hem tırnaksız linkleri alacak şekilde genişlettim
                raw_links = re.findall(r'https?://[^\s\'"<>]+m3u8[^\s\'"<>]*', r.text)
                
                for yl in raw_links:
                    yl = yl.strip()
                    if yl not in eklenen_linkler:
                        # Linkin hemen öncesindeki 100 karakterde isim ara
                        pos = r.text.find(yl)
                        context = r.text[max(0, pos-100):pos]
                        
                        # İsimleri bulmak için yaygın HTML ve JS kalıplarını tara
                        name_match = re.findall(r'["\']([^"\']{3,30})["\']', context)
                        yn = name_match[-1] if name_match else "GINIKO KANAL"
                        
                        yeni_liste.append(f'#EXTINF:-1 group-title="GINIKO_ALL",{yn.strip()}\n{yl}')
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
    print(f"🚀 İŞLEM TAMAM! Toplam {len(yeni_liste)-1} kanal filtresiz kaydedildi.")

if __name__ == "__main__":
    main()
