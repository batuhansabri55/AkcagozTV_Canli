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
    # Temizliği derinleştiriyoruz
    isim = re.sub(r'\(.*?\)|\[.*?\]', '', isim) # Parantez içlerini sil
    isim = re.sub(r'\|tr\||hd|fhd|sd|4k|canli|tr:|haber|ulusal|belgesel|fhd\+|fhd\+\+', '', isim)
    isim = re.sub(r'[^a-z0-9]', '', isim)
    return isim.strip()

def main():
    if not os.path.exists(FILE_PATH):
        print("❌ HATA: tr.m3u dosyası bulunamadı!")
        return

    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        mevcut_icerik = f.read()

    yeni_liste = ["#EXTM3U"]
    eklenen_linkler = set()
    aranacak_kanallar = {}

    # Regex: Daha esnek bir yapı
    pattern = r"(#EXTINF:[^\n]+)\n+(https?://[^\s\n]+)"
    matches = re.findall(pattern, mevcut_icerik)
    
    print(f"📊 Mevcut dosyada {len(matches)} kanal bulundu.")

    # 1. Dokunulmazları Koru
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

    print(f"🛡️  {len(yeni_liste)-1} adet dokunulmaz link sisteme eklendi.")

    # 2. Yedeklerden Çek
    for s_url in YEDEK_KAYNAKLAR:
        try:
            print(f"🌐 Kaynak taranıyor: {s_url}")
            r = requests.get(s_url, timeout=15)
            y_matches = re.findall(pattern, r.text)
            
            eklenen_bu_kaynak = 0
            for y_info, y_url in y_matches:
                yl = y_url.strip()
                yn = y_info.split(',')[-1] if ',' in y_info else y_info
                y_temiz = isim_normalize(yn)
                
                # İsim eşleşiyorsa veya yedek link senin dokunulmazlarından biriyse ekle
                if y_temiz in aranacak_kanallar and yl not in eklenen_linkler:
                    yeni_liste.append(f"{y_info}\n{yl}")
                    eklenen_linkler.add(yl)
                    eklenen_bu_kaynak += 1
            print(f"✅ Bu kaynaktan {eklenen_bu_kaynak} yeni link alındı.")
        except:
            print(f"⚠️ Kaynağa ulaşılamadı: {s_url}")
            continue

    # 3. Yazma İşlemi (Zorunlu Güncelleme İçin Dosyayı Yeniden Yaz)
    son_icerik = "\n".join(yeni_liste)
    
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(son_icerik)
    
    print(f"🚀 İŞLEM TAMAM! Toplam {len(yeni_liste)-1} kanal kaydedildi.")

if __name__ == "__main__":
    main()
