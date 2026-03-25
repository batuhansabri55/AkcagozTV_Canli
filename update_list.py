import requests
import re
import os

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
# Siteyi kandırmak için gerçek tarayıcı bilgisi
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'tr,en-US;q=0.7,en;q=0.3',
}

DOKUNULMAZLAR = [
    "premiumstream.in", "workers.dev", "mywire.org", "token=DeaTHLesS", 
    "goldvod.site", "trt.com.tr", "turknet.ercdn.net", "daioncdn.net"
]

YEDEK_KAYNAKLAR = [
    "https://streams.uzunmuhalefet.com/lists/tr.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://mth.tc/DsGo",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://raw.githubusercontent.com/sultansmgr/smart/refs/heads/main/viziTV.m3u"
    
]

def isim_normalize(isim):
    if not isim: return ""
    isim = isim.lower()
    tr_map = str.maketrans("çığöşü", "cigosu")
    isim = isim.translate(tr_map)
    isim = re.sub(r'\(.*?\)|\[.*?\]', '', isim)
    isim = re.sub(r'\|tr\||hd|fhd|sd|4k|canli|tr:|haber|ulusal|belgesel|fhd\+|fhd\+\+', '', isim)
    isim = re.sub(r'[^a-z0-9]', '', isim)
    return isim.strip()

def main():
    if not os.path.exists(FILE_PATH):
        print(f"❌ {FILE_PATH} bulunamadı!")
        return

    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        mevcut_icerik = f.read()

    yeni_liste = ["#EXTM3U"]
    eklenen_linkler = set()
    aranacak_kanallar = {}

    pattern = r"(#EXTINF:[^\n]+)\n+(https?://[^\s\n]+)"
    matches = re.findall(pattern, mevcut_icerik)
    
    print(f"📊 Başlıyoruz... Mevcut dosya: {len(matches)} kanal.")

    for info, url in matches:
        link = url.strip()
        ch_name = info.split(',')[-1] if ',' in info else info
        temiz_isim = isim_normalize(ch_name)
        
        if any(d in link.lower() for d in DOKUNULMAZLAR):
            if link not in eklenen_linkler:
                yeni_liste.append(f"{info}\n{link}")
                eklenen_linkler.add(link)
        
        if temiz_isim:
            aranacak_kanallar[temiz_isim] = ch_name.strip()

    for s_url in YEDEK_KAYNAKLAR:
        try:
            print(f"🌐 Bağlanıyor: {s_url}")
            # allow_redirects=True ekledik ki site yönlendirme yaparsa takip etsin
            r = requests.get(s_url, headers=HEADERS, timeout=25, allow_redirects=True)
            
            if r.status_code == 200:
                y_matches = re.findall(pattern, r.text)
                count = 0
                for y_info, y_url in y_matches:
                    yl = y_url.strip()
                    yn = y_info.split(',')[-1] if ',' in y_info else y_info
                    y_temiz = isim_normalize(yn)
                    
                    if y_temiz in aranacak_kanallar and yl not in eklenen_linkler:
                        yeni_liste.append(f"{y_info}\n{yl}")
                        eklenen_linkler.add(yl)
                        count += 1
                print(f"✅ {count} yeni link çekildi.")
            else:
                print(f"⚠️ Site hata verdi (Kod: {r.status_code})")
        except Exception as e:
            print(f"⚠️ Hata oluştu: {str(e)}")

    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(yeni_liste))
    
    print(f"🚀 İşlem Bitti! Toplam {len(yeni_liste)-1} kanal kaydedildi.")

if __name__ == "__main__":
    main()
