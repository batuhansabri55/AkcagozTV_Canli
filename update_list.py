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

def yedek_kanali_temizle(metin):
    """SADECE YEDEKLER İÇİN: Sayıları (TRT 1, TV 8) bozmadan kalite eklerini temizler."""
    if "#EXTINF" in metin and "," in metin:
        parcalar = metin.rsplit(',', 1)
        ayarlar = parcalar[0]
        isim = parcalar[1]

        # Sadece yedeklerdeki gereksizleri temizle (Sayılar kalır)
        isim = re.sub(r'\s*\([0-9]{3,4}[pP]?\)', '', isim) # (1080p) gibi
        isim = re.sub(r'\s*(-YT|\[.*?\]|\bHD\b|\bFHD\b|\bSD\b)\s*', ' ', isim, flags=re.I)
        isim = re.sub(r'^[\.\-\s]+', '', isim) # Başındaki nokta/tire
        
        isim = ' '.join(isim.split()).strip()
        return f"{ayarlar},{isim}"
    return metin

def main():
    # 1. ADIM: İLK 5000 SATIRI DOKUNULMAZ OLARAK OKU
    dokunulmaz_icerik = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_satirlar = f.readlines()
            # Senin dokunulmaz sınırın (5000 satıra kadar)
            limit = min(5000, len(tum_satirlar))
            for satir in tum_satirlar[:limit]:
                # SIFIR MÜDAHALE: Virgülüne dokunmadan olduğu gibi al
                dokunulmaz_icerik.append(satir)

    # 2. ADIM: İNTERNETTEN GELEN YEDEKLERİ TOPLA VE TEMİZLE
    print("🔄 5000 satır korundu. Yedekler taranıyor ve temizleniyor...")
    taze_kanal_listesi = []
    for url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            if r.status_code == 200:
                # Verideki VLC satırlarını sil
                temiz_veri = re.sub(r'#EXTVLCOPT:.*?\n', '', r.text)
                
                bulunanlar = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", temiz_veri, re.DOTALL)
                for kanal in bulunanlar:
                    satir_grubu = kanal.strip().split('\n')
                    if len(satir_grubu) >= 2:
                        # BURADA TEMİZLİK DEVAM EDİYOR (Sayılar korunarak)
                        ext_satiri = yedek_kanali_temizle(satir_grubu[0])
                        link_satiri = satir_grubu[-1].strip()
                        
                        # TiviMate'de karışmasınlar diye grup etiketi ekle
                        if 'group-title="' not in ext_satiri:
                            ext_satiri = ext_satiri.replace('#EXTINF:', '#EXTINF:-1 group-title="YEDEKLER",')
                        
                        taze_kanal_listesi.append(f"{ext_satiri}\n{link_satiri}")
        except: continue

    # 3. ADIM: DOSYAYI YAZ
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        # Önce senin dokunulmaz 5000 satırın
        f.writelines(dokunulmaz_icerik)
        
        # Sonra altına temizlenmiş yedekler
        f.write("\n# --- TEMIZLENMIS YEDEKLER ---\n")
        for k in taze_kanal_listesi:
            f.write(k + "\n")
        
        zaman = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n# GUNCELLEME: {zaman}\n")

    print(f"🚀 İşlem bitti! İlk 5000 satırın zırh gibi korundu, sonrasına temizlik yapıldı.")

if __name__ == "__main__":
    main()
