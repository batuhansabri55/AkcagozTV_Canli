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
    # Gereksiz ekleri temizle
    isim = re.sub(r'\|tr\||hd|fhd|sd|4k|canli|tr:|haber|ulusal|belgesel|fhd\+|fhd\+\+', '', isim)
    isim = re.sub(r'[^a-z0-9]', '', isim)
    return isim.strip()

def main():
    if not os.path.exists(FILE_PATH):
        print("❌ tr.m3u bulunamadı!")
        return

    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        mevcut_icerik = f.read()

    yeni_liste = ["#EXTM3U"]
    eklenen_linkler = set()
    korunacak_kanal_isimleri = {}

    # Regex: M3U formatını yakalamak için
    pattern = r"(#EXTINF:[^\n]+)\n+(https?://[^\s\n]+)"

    # 1. ADIM: Dokunulmazları ayır ve koru
    matches = re.findall(pattern, mevcut_icerik)
    for info, url in matches:
        link = url.strip()
        # Kanal ismini çek (virgülden sonrası)
        ch_name = info.split(',')[-1] if ',' in info else info
        temiz_isim = isim_normalize(ch_name)
        
        if any(d in link.lower() for d in DOKUNULMAZLAR):
            yeni_liste.append(f"{info}\n{link}")
            eklenen_linkler.add(link)
        
        # Dokunulmaz olsun olmasın, elimizdeki tüm kanal isimlerini yedeklerde aramak için listeye alıyoruz
        if temiz_isim:
            korunacak_kanal_isimleri[temiz_isim] = ch_name.strip()

    print(f"✅ {len(yeni_liste)-1} adet dokunulmaz link korundu.")

    # 2. ADIM: Yedeklerden güncel linkleri çek
    for s_url in YEDEK_KAYNAKLAR:
        try:
            print(f"🌐 Kaynak taranıyor: {s_url}")
            r = requests.get(s_url, timeout=10)
            if r.status_code != 200: continue
            
            for y_info, y_url in re.findall(pattern, r.text):
                yl = y_url.strip()
                yn = y_info.split(',')[-1] if ',' in y_info else y_info
                y_temiz = isim_normalize(yn)
                
                # Eğer bu kanal bizim listemizde varsa ve link daha önce eklenmemişse ekle
                if y_temiz in korunacak_kanal_isimleri and yl not in eklenen_linkler:
                    # Orijinal isim bilgisini veya yedektekini kullanabilirsin
                    yeni_liste.append(f"{y_info}\n{yl}")
                    eklenen_linkler.add(yl)
        except Exception as e:
            print(f"⚠️ Hata: {s_url} çekilemedi.")
            continue

    # 3. ADIM: Dosyayı tamamen temizleyip yeni haliyle yaz
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(yeni_liste))
    
    print(f"🚀 İşlem Tamam! Toplam {len(eklenen_linkler)} link ile dosya güncellendi.")

if __name__ == "__main__":
    main()
