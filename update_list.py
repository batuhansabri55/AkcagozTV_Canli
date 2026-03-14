import requests
import os
import re
from concurrent.futures import ThreadPoolExecutor

# VIP: Bu kelimeleri içeren linkler ASLA silinmez ve TEST EDİLMEDEN kabul edilir
DOKUNULMAZLAR = ["hpgdiscoo", "premiumstream.in", "workers.dev", "cdn-vizi", "viziTV"]

# Bilgisayarındaki dev Goldvod dosyasının adı (Aynı klasörde olmalı)
GOLDVOD_DOSYA_ADI = "playlist_hpgdiscoo(2).m3u"

YEDEK_KAYNAKLAR = [
    "https://mth.tc/DsGo",
    "https://raw.githubusercontent.com/sultansmgr/smart/refs/heads/main/viziTV.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://streams.uzunmuhalefet.com/lists/tr.m3u"
]

def link_test_et(item):
    info, url = item
    url_clean = url.lower()
    if any(ozel in url_clean for ozel in DOKUNULMAZLAR):
        return (info, url)
    try:
        r = requests.get(url, timeout=4, stream=True, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            content = next(r.iter_content(chunk_size=64), None)
            r.close()
            if content: return (info, url)
    except: pass
    return None

def update_m3u():
    aday_listesi = []
    korunanlar = [] 
    eklenen_linkler = set()

    # 1. YEREL GOLDVOD DOSYASINI OKU (19.500 Satırlık Dosya)
    if os.path.exists(GOLDVOD_DOSYA_ADI):
        print(f"[*] Yerel dosya okunuyor: {GOLDVOD_DOSYA_ADI}")
        with open(GOLDVOD_DOSYA_ADI, "r", encoding="utf-8") as f:
            content = f.read()
            matches = re.findall(r"(#EXTINF:.*)\n(http.*)", content)
            for info, url in matches:
                # Sadece senin kullanıcı adını içeren linkleri alıyoruz
                if "hpgdiscoo" in url.lower() and url not in eklenen_linkler:
                    korunanlar.append((info, url))
                    eklenen_linkler.add(url)
    else:
        print(f"[!] UYARI: {GOLDVOD_DOSYA_ADI} bulunamadı! Sadece dış kaynaklar taranacak.")

    # 2. MEVCUT tr.m3u İÇİNDEKİ DOKUNULMAZLARI KORU
    if os.path.exists("tr.m3u"):
        with open("tr.m3u", "r", encoding="utf-8") as f:
            matches = re.findall(r"(#EXTINF:.*)\n(http.*)", f.read())
            for info, url in matches:
                if any(ozel in url.lower() for ozel in DOKUNULMAZLAR) and url not in eklenen_linkler:
                    korunanlar.append((info, url))
                    eklenen_linkler.add(url)

    # 3. DIŞ KAYNAKLARI TARA
    print(f"[*] {len(YEDEK_KAYNAKLAR)} dış kaynak taranıyor...")
    for s_url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(s_url, timeout=8)
            if r.status_code == 200:
                matches = re.findall(r"(#EXTINF:.*)\n(http.*)", r.text)
                for info, url in matches:
                    if url not in eklenen_linkler:
                        aday_listesi.append((info, url))
        except: continue

    # 4. TEST İŞLEMİ
    print(f"[*] {len(aday_listesi)} link test ediliyor...")
    with ThreadPoolExecutor(max_workers=25) as executor:
        results = list(executor.map(link_test_et, aday_listesi))
        
    # 5. BİRLEŞTİR VE YAZ
    final_liste = korunanlar # Önce zırhlı Goldvod ve diğer VIP linkler
    for res in results:
        if res and res[1] not in eklenen_linkler:
            final_liste.append(res)
            eklenen_linkler.add(res[1])

    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for info, url in final_liste:
            f.write(f"{info}\n{url}\n")
    
    print(f"[+] İŞLEM TAMAM! Toplam {len(final_liste)} kanal hazır.")

if __name__ == "__main__":
    update_m3u()
