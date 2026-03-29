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

def main():
    # 1. ADIM: SENİN DOSYANI OKU VE OLDUĞU GİBİ KORU
    orijinal_icerik = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            # Dosyanın tamamını satır satır oku
            tum_satirlar = f.readlines()
            # Senin dokunulmaz sınırın (3963 satır)
            limit = min(3963, len(tum_satirlar))
            for satir in tum_satirlar[:limit]:
                # BURADA HİÇBİR TEMİZLEME FONKSİYONU YOK! 
                # Ne yazıyorsa o; boşluksa boşluk, noktaysa nokta.
                orijinal_icerik.append(satir)

    # 2. ADIM: YEDEKLERİ TOPLA
    print("🔄 Yedekler toplanıyor (Senin listene dokunulmuyor)...")
    taze_kanal_listesi = []
    for url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            if r.status_code == 200:
                # Sadece gelen verideki VLC satırlarını siliyoruz (Liste kirlenmesin diye)
                temiz_veri = re.sub(r'#EXTVLCOPT:.*?\n', '', r.text)
                
                # Kanal bloklarını (EXTINF + Link) ayır
                bulunanlar = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", temiz_veri, re.DOTALL)
                for kanal in bulunanlar:
                    satirlar = kanal.strip().split('\n')
                    if len(satirlar) >= 2:
                        ext_satiri = satirlar[0]
                        link_satiri = satirlar[-1].strip()
                        
                        # İnternetten gelenlere karışmasınlar diye grup etiketi ekle
                        if 'group-title="' not in ext_satiri:
                            ext_satiri = ext_satiri.replace('#EXTINF:', '#EXTINF:-1 group-title="YEDEKLER",')
                        
                        taze_kanal_listesi.append(f"{ext_satiri}\n{link_satiri}")
        except: continue

    # 3. ADIM: DOSYAYI YAZ
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        # Önce senin 3963 satırlık orijinal içeriğini yaz
        f.writelines(orijinal_icerik)
        
        # Sonra altına internetten gelenleri ekle
        f.write("\n# --- INTERNETTEN GELEN YEDEKLER ---\n")
        for k in taze_kanal_listesi:
            f.write(k + "\n")
        
        zaman = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n# SON GUNCELLEME: {zaman}\n")

    print(f"🚀 İşlem bitti usta! Senin 5000 satırın (ilk 3963'ü) tek bir virgülü değişmeden korundu.")

if __name__ == "__main__":
    main()
