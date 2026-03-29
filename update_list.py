import requests
import re
import os
import datetime

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

YEDEK_KAYNAKLAR = [
    "https://streams.uzunmuhalefet.com/lists/tr.m3u",
    "https://tinyurl.com/ytpatron",
    "https://urlz.fr/v1Xo",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://mth.tc/DsGo",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://raw.githubusercontent.com/UzunMuhalefet/yayinlar/main/streams/best/all.m3u8",
    "https://raw.githubusercontent.com/UzunMuhalefet/Legal-IPTV/main/lists/turkey.m3u8"
]

def karakter_duzelt(metin):
    """Türkçe karakterleri standartlaştırır."""
    tr_harfler = str.maketrans("İÜŞÇÖĞıüşçöğ", "IUSCOGiuscog")
    return metin.translate(tr_harfler)

def kanal_temizle(metin, yedek_mi=False):
    """Kanal isimlerini temizler; TRT 1, Kanal 7 gibi isimleri korur."""
    if "#EXTINF" in metin and "," in metin:
        parcalar = metin.rsplit(',', 1)
        ayarlar = parcalar[0]
        isim = parcalar[1].strip()

        # 1. Kalite eklerini temizle (HD, FHD vb.)
        isim = re.sub(r'\s*\b(FHD|HD|SD|UHD|4K|HEVC|1080p|720p)\b\s*', ' ', isim, flags=re.I)
        
        # 2. Gereksiz sembolleri temizle
        isim = re.sub(r'^[0-9\.\-\s]+', '', isim)
        isim = re.sub(r'\s*\([0-9]{3,4}[pP]?\)', '', isim)
        isim = re.sub(r'\s*(-YT|\[.*?\])\s*', '', isim, flags=re.I)

        # 3. AKILLI SAYI KORUMA (TRT 1, Kanal 7, A2, 24, 360 için)
        # Sadece 3 haneden büyük sayıları veya ismin en sonundaki 40+ sayıları siler
        def sayi_ayikla(match):
            s = match.group(0).strip()
            if s.isdigit() and int(s) > 40: return "" # 45, 46 gibi yedek nolarını sil
            return match.group(0) # 1, 7, 24 gibi isimleri koru

        isim = re.sub(r'\s*\d+\s*$', sayi_ayikla, isim)

        # 4. Standartlaştır
        isim = isim.upper()
        isim = karakter_duzelt(isim)
        isim = ' '.join(isim.split()).strip()

        # 5. YEDEK İBARESİ EKLE (İstenirse)
        if yedek_mi and "YEDEK" not in isim:
            isim = f"{isim} YEDEK"
        
        return f"{ayarlar},{isim}"
    return metin

def main():
    # 1. ADIM: DOKUNULMAZ BÖLGEYİ OKU
    temiz_dokunulmaz = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_satirlar = f.readlines()
            limit = min(3963, len(tum_satirlar))
            for satir in tum_satirlar[:limit]:
                if "#EXTVLCOPT" in satir: continue
                if satir.startswith("#EXTINF"):
                    # Ana listedekilere "YEDEK" yazmıyoruz
                    temiz_dokunulmaz.append(kanal_temizle(satir, yedek_mi=False) + "\n")
                else:
                    temiz_dokunulmaz.append(satir)

    # 2. ADIM: YEDEKLERİ TOPLA
    print("🔄 Yedekler toplanıyor ve isimlendiriliyor...")
    taze_kanal_listesi = []
    for url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            if r.status_code == 200:
                temiz_veri = re.sub(r'#EXTVLCOPT:.*?\n', '', r.text)
                bulunanlar = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", temiz_veri, re.DOTALL)
                for kanal in bulunanlar:
                    satirlar = kanal.strip().split('\n')
                    if len(satirlar) >= 2:
                        # İnternetten gelenlere "YEDEK" ekliyoruz
                        ext_satiri = kanal_temizle(satirlar[0], yedek_mi=True)
                        link_satiri = satirlar[-1].strip()
                        
                        if 'group-title="' not in ext_satiri:
                            ext_satiri = ext_satiri.replace('#EXTINF:', '#EXTINF:-1 group-title="YEDEKLER",')
                        taze_kanal_listesi.append(f"{ext_satiri}\n{link_satiri}")
        except: continue

    # 3. ADIM: DOSYAYI YAZ
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(temiz_dokunulmaz)
        f.write("\n# --- TUM YEDEKLER ---\n")
        for k in taze_kanal_listesi:
            f.write(k + "\n")
        
        zaman = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n# SON GUNCELLEME: {zaman}\n")

    print(f"🚀 İşlem bitti! TRT 1 vb. korundu, dış kaynaklara 'YEDEK' yazıldı.")

if __name__ == "__main__":
    main()
