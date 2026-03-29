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
    """Türkçe karakterleri standartlaştırır (CNN TÜRK -> CNN TURK)."""
    tr_harfler = str.maketrans("İÜŞÇÖĞıüşçöğ", "IUSCOGiuscog")
    return metin.translate(tr_harfler)

def kanal_temizle(metin):
    """Kanal isimlerini temizler; TRT 1, Kanal 7 gibi isimleri korur, yedek sayılarını siler."""
    if "#EXTINF" in metin and "," in metin:
        parcalar = metin.rsplit(',', 1)
        ayarlar = parcalar[0]
        isim = parcalar[1].strip()

        # 1. Regex Temizlikleri
        isim = re.sub(r'^[0-9\.\-\s]+', '', isim)
        isim = re.sub(r'\s*\([0-9]{3,4}[pP]?\)', '', isim)
        isim = re.sub(r'\s*(-YT|\[.*?\])\s*', '', isim, flags=re.I)

        # 2. Kalite eklerini temizle (HD, FHD vb.)
        isim = re.sub(r'\s*\b(FHD|HD|SD|UHD|4K|HEVC|1080p|720p)\b\s*', ' ', isim, flags=re.I)

        # 3. AKILLI SAYI SÜZGECİ: Sadece 40'tan büyük yedek numaralarını siler
        def sayi_kontrol(match):
            gelen_sayi = match.group(0).strip()
            if gelen_sayi.isdigit():
                if int(gelen_sayi) > 40:
                    return ""
            return match.group(0)

        isim = re.sub(r'\s*\d+\s*$', sayi_kontrol, isim)

        # 4. Karakter ve Boşluk Düzenleme
        isim = isim.upper()
        isim = karakter_duzelt(isim)
        isim = ' '.join(isim.split()).strip()
        
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
                if "#EXTVLCOPT" in satir:
                    continue
                if satir.startswith("#EXTINF"):
                    temiz_dokunulmaz.append(kanal_temizle(satir) + "\n")
                else:
                    temiz_dokunulmaz.append(satir)

    # 2. ADIM: YEDEKLERİ TOPLA
    print("🔄 Kanallar standart hale getiriliyor (TRT 1, Kanal 7 vb. korunuyor)...")
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
                        ext_satiri = kanal_temizle(satirlar[0])
                        link_satiri = satirlar[-1].strip()
                        
                        if 'group-title="' not in ext_satiri:
                            ext_satiri = ext_satiri.replace('#EXTINF:', '#EXTINF:-1 group-title="YEDEKLER",')
                        taze_kanal_listesi.append(f"{ext_satiri}\n{link_satiri}")
        except: continue

    # 3. ADIM: DOSYAYI YAZ
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(temiz_dokunulmaz)
        f.write("\n# --- TUM YEDEKLER (AKILLI LISTE) ---\n")
        for k in taze_kanal_listesi:
            f.write(k + "\n")
        
        zaman = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n# SON GUNCELLEME: {zaman}\n")

    print(f"🚀 İşlem bitti! Kanal isimleri korundu, yedek numaraları ve OPT satırları temizlendi.")

if __name__ == "__main__":
    main()
