import requests
import re
import os
import datetime

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

YEDEK_KAYNAKLAR = [
    "https://streams.uzunmuhalefet.com/lists/tr.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://mth.tc/DsGo",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u"
]

# --- YENİ: LİNK TEST EDİCİ ---
def link_calisiyor_mu(url):
    try:
        # 3 saniye içinde cevap vermeyen link ölüdür
        r = requests.get(url, headers=HEADERS, timeout=3, stream=True)
        return r.status_code == 200
    except:
        return False

def main():
    # 1. ADIM: DOKUNULMAZ BÖLGEYİ KORU
    dokunulmaz_bolge = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_eski_satirlar = f.readlines()
            limit = min(3963, len(tum_eski_satirlar))
            dokunulmaz_bolge = tum_eski_satirlar[:limit]
            print(f"🛡️  {len(dokunulmaz_bolge)} SATIR KORUMAYA ALINDI.")

    # 2. ADIM: KAYNAKLARI TARA VE TEST ET
    taze_kanal_listesi = []
    for index, url in enumerate(YEDEK_KAYNAKLAR, 1):
        try:
            print(f"🌐 Kaynak taranıyor ({index}/6): {url}")
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code == 200:
                # Blokları yakala
                bloklar = re.findall(r"(#EXTINF:[^\n]+\n+https?://[^\s\n]+)", r.text)
                for blok in bloklar:
                    link = blok.split('\n')[-1].strip()
                    # KRİTİK: Sadece çalışan linkleri ekle!
                    if link_calisiyor_mu(link):
                        taze_kanal_listesi.append(blok)
                        print(f"✅ ÇALIŞIYOR: {link[:50]}...")
                    if len(taze_kanal_listesi) >= 100: break # GitHub'ı yormamak için sınır
        except Exception as e:
            print(f"❌ Hata ({url}): {str(e)}")

    # 3. ADIM: DOSYAYI YAZ
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(dokunulmaz_bolge)
        if dokunulmaz_bolge and not dokunulmaz_bolge[-1].endswith('\n'):
            f.write('\n')
        
        for kanal_blogu in taze_kanal_listesi:
            f.write(kanal_blogu + "\n")
            
        zaman = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n# Son Guncelleme: {zaman}\n")

    print(f"🚀 GÜNCELLEME TAMAMLANDI! Toplam Yeni (Çalışan): {len(taze_kanal_listesi)}")

if __name__ == "__main__":
    main()
