import requests
import re

# Sadece bu kelimeyi içeren linkler sorgusuz sualsiz kabul edilir
DOKUNULMAZLAR = ["premiumstream.in"]

YEDEK_KAYNAKLAR = [
    "https://mth.tc/DsGo",
    "https://raw.githubusercontent.com/sultansmgr/smart/refs/heads/main/viziTV.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://streams.uzunmuhalefet.com/lists/tr.m3u"
]

def update_m3u():
    eklenen_linkler = set()
    final_list = []
    tum_metin = ""

    print("Kaynaklar internetten çekiliyor...")
    for s_url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(s_url, timeout=15)
            if r.status_code == 200:
                tum_metin += r.text + "\n"
        except: continue

    # Regex ile verileri ayıkla
    matches = re.findall(r"(#EXTINF:[^\n]*)\n(http[^\n]*)", tum_metin.replace('\r', ''))
    
    for info, url in matches:
        url_strip = url.strip()
        
        # TEKİLLEŞTİRME: Link set içinde yoksa listeye ekle
        if url_strip not in eklenen_linkler:
            final_list.append((info, url_strip))
            eklenen_linkler.add(url_strip)

    # DOSYAYI SIFIRDAN YAZ (W modu eski veriyi siler)
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for info, url in final_list:
            f.write(f"{info}\n{url}\n")
    
    print(f"İşlem bitti! Toplam {len(final_list)} benzersiz kanal kaydedildi.")
    print("Artık o 19 tane olan linklerden sadece 1 tane kaldı.")

if __name__ == "__main__":
    update_m3u()
