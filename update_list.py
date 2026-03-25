import requests
import re
import os

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
# Giniko sitesinin veriyi çektiği gizli API adresi
GINIKO_API = "https://giniko.smartiptvworld.workers.dev/api/data" 

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://giniko.smartiptvworld.workers.dev/',
}

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
    "https://streams.uzunmuhalefet.com/lists/tr.m3u"
]

def isim_normalize(isim):
    if not isim: return ""
    isim = isim.lower()
    tr_map = str.maketrans("çığöşü", "cigosu")
    isim = isim.translate(tr_map)
    # Temizlik: Gereksiz her şeyi at (Regex ile)
    isim = re.sub(r'\(.*?\)|\[.*?\]', '', isim)
    isim = re.sub(r'\|tr\||hd|fhd|sd|4k|canli|tr:|haber|ulusal|belgesel|fhd\+|fhd\+\+|tv|\-|\.|\:', '', isim)
    return "".join(isim.split()) # Tüm boşlukları siler

def main():
    if not os.path.exists(FILE_PATH):
        print(f"❌ {FILE_PATH} bulunamadı!")
        return

    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        mevcut_icerik = f.read()

    yeni_liste = ["#EXTM3U"]
    eklenen_linkler = set()
    aranacak_kanallar = {}

    # 1. Mevcut kanalları oku ve dokunulmazları koru
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

    # 2. GINIKO ÖZEL TARAMA (Arka Kapı)
    print("🌐 Giniko Gizli Veri Kanalı (API) taranıyor...")
    try:
        # Önce ana sayfadan token veya session kontrolü yapalım
        session = requests.Session()
        session.get("https://giniko.smartiptvworld.workers.dev/", headers=HEADERS, timeout=10)
        
        # Şimdi asıl veri kaynağını deneyelim
        g_resp = session.get(GINIKO_API, headers=HEADERS, timeout=15)
        count = 0
        if g_resp.status_code == 200:
            # Sitenin veriyi basma şekline göre regex (Link ve İsim yakalama)
            g_matches = re.findall(r'["\'](https?://[^"\']+m3u8[^"\']*)["\'].*?["\']([^"\']+)["\']', g_resp.text)
            for yl, yn in g_matches:
                y_temiz = isim_normalize(yn)
                if y_temiz in aranacak_kanallar and yl not in eklenen_linkler:
                    yeni_liste.append(f'#EXTINF:-1 group-title="YEDEK_GINIKO",{yn.strip()}\n{yl}')
                    eklenen_linkler.add(yl)
                    count += 1
        print(f"✅ Giniko API üzerinden {count} link alındı.")
    except Exception as e:
        print(f"⚠️ Giniko API Hatası: {str(e)}")

    # 3. DİĞER YEDEK KAYNAKLAR
    for s_url in YEDEK_KAYNAKLAR:
        try:
            print(f"🌐 Kaynak taranıyor: {s_url}")
            r = requests.get(s_url, headers=HEADERS, timeout=20)
            if r.status_code == 200:
                y_matches = re.findall(pattern, r.text)
                c = 0
                for y_info, y_url in y_matches:
                    yl = y_url.strip()
                    yn = y_info.split(',')[-1] if ',' in y_info else y_info
                    y_temiz = isim_normalize(yn)
                    if y_temiz in aranacak_kanallar and yl not in eklenen_linkler:
                        yeni_liste.append(f"{y_info}\n{yl}")
                        eklenen_linkler.add(yl)
                        c += 1
                print(f"✅ {c} yeni link alındı.")
        except: pass

    # 4. Kaydet
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(yeni_liste))
    print(f"🚀 İŞLEM TAMAM! Toplam {len(yeni_liste)-1} kanal güncellendi.")

if __name__ == "__main__":
    main()
