import requests
import re
import os

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
}

DOKUNULMAZLAR = [
    "premiumstream.in", "workers.dev", "mywire.org", "token=DeaTHLesS", 
    "goldvod.site", "trt.com.tr", "turknet.ercdn.net", "daioncdn.net"
]

YEDEK_KAYNAKLAR = [
    "https://mth.tc/DsGo",
    "https://raw.githubusercontent.com/sultansmgr/smart/refs/heads/main/viziTV.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://streams.uzunmuhalefet.com/lists/tr.m3u",
    "https://giniko.smartiptvworld.workers.dev"  # ÖZEL KAYNAK EKLENDİ
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
    
    print(f"📊 Mevcut dosya: {len(matches)} kanal inceleniyor.")

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
            print(f"🌐 Kaynak taranıyor: {s_url}")
            r = requests.get(s_url, headers=HEADERS, timeout=25, allow_redirects=True)
            
            if r.status_code == 200:
                # Eğer site giniko ise özel regex kullan, değilse standart m3u regexi kullan
                if "giniko" in s_url:
                    # Giniko'nun HTML yapısından isim ve linki söken özel regex
                    y_matches = re.findall(r'onclick="playStream\(\'([^\']+)\',\'([^\']+)\'\)"', r.text)
                    # Not: matches (link, name) şeklinde döner
                    count = 0
                    for yl, yn in y_matches:
                        y_temiz = isim_normalize(yn)
                        if y_temiz in aranacak_kanallar and yl not in eklenen_linkler:
                            yeni_liste.append(f'#EXTINF:-1 group-title="YEDEK",{yn}\n{yl}')
                            eklenen_linkler.add(yl)
                            count += 1
                else:
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
                print(f"✅ {count} yeni link alındı.")
            else:
                print(f"⚠️ Bağlanılamadı: {r.status_code}")
        except Exception as e:
            print(f"⚠️ Hata: {str(e)}")

    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(yeni_liste))
    
    print(f"🚀 İŞLEM TAMAM! Toplam {len(yeni_liste)-1} kanal kaydedildi.")

if __name__ == "__main__":
    main()
