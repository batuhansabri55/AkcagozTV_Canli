import requests
import re
import os

# --- AYARLAR ---
FILE_PATH = "tr.m3u"

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
    "https://streams.uzunmuhalefet.com/lists/tr.m3u"
]

def isim_normalize(isim):
    if not isim: return ""
    isim = isim.lower()
    tr_map = str.maketrans("çığöşü", "cigosu")
    isim = isim.translate(tr_map)
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
    
    print(f"🔍 Toplam {len(matches)} kanal tarandı.")

    # 1. Sadece Dokunulmazları ayır
    for info, url in matches:
        link = url.strip()
        ch_name = info.split(',')[-1] if ',' in info else info
        temiz_isim = isim_normalize(ch_name)
        
        # SADECE Dokunulmaz listesinde olanları listeye alıyoruz
        if any(d in link.lower() for d in DOKUNULMAZLAR):
            yeni_liste.append(f"{info}\n{link}")
            eklenen_linkler.add(link)
        
        # Eski listedeki tüm kanal isimlerini hafızaya al (Yedeklerde aramak için)
        if temiz_isim:
            aranacak_kanallar[temiz_isim] = ch_name.strip()

    print(f"✅ {len(yeni_liste)-1} adet dokunulmaz link korundu. Diğerleri temizlendi.")

    # 2. Yedeklerden sadece listedeki kanalları çek
    for s_url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(s_url, timeout=15)
            y_matches = re.findall(pattern, r.text)
            for y_info, y_url in y_matches:
                yl = y_url.strip()
                yn = y_info.split(',')[-1] if ',' in y_info else y_info
                y_temiz = isim_normalize(yn)
                
                if y_temiz in aranacak_kanallar and yl not in eklenen_linkler:
                    yeni_liste.append(f"{y_info}\n{yl}")
                    eklenen_linkler.add(yl)
        except: continue

    # 3. Dosyayı tamamen boşaltıp yeni halini yaz
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(yeni_liste))
    
    print(f"🚀 Bitti! Dosyada şu an toplam {len(yeni_liste)-1} kanal var.")

if __name__ == "__main__":
    main()
