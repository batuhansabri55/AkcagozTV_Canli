import requests
import os
import re
from concurrent.futures import ThreadPoolExecutor

# VIP: Bu kelimeleri içeren linkler ASLA silinmez ve TEST EDİLMEDEN kabul edilir
DOKUNULMAZLAR = ["hpgdiscoo", "premiumstream.in", "workers.dev", "cdn-vizi", "viziTV"]

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
    
    # VIP Kontrol: Dokunulmaz kelime geçiyorsa testi atla, direkt kabul et
    if any(ozel in url_clean for ozel in DOKUNULMAZLAR):
        return (info, url)

    try:
        # Hızlı test için stream=True kullanıyoruz
        r = requests.get(url, timeout=4, stream=True, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            # Sadece ilk bir kaç byte'ı kontrol edip bağlantıyı kapatıyoruz
            content = next(r.iter_content(chunk_size=64), None)
            r.close()
            if content: return (info, url)
    except: pass
    return None

def update_m3u():
    aday_listesi = []
    korunanlar = []  # Manuel/Zırhlı linkler
    eklenen_linkler = set()

    # 1. Mevcut tr.m3u varsa oku ve DOKUNULMAZ olanları ayır
    if os.path.exists("tr.m3u"):
        with open("tr.m3u", "r", encoding="utf-8") as f:
            content = f.read()
            matches = re.findall(r"(#EXTINF:.*)\n(http.*)", content)
            for info, url in matches:
                if any(ozel in url.lower() for ozel in DOKUNULMAZLAR):
                    if url not in eklenen_linkler:
                        korunanlar.append((info, url))
                        eklenen_linkler.add(url)
                else:
                    aday_listesi.append((info, url))

    # 2. Dış kaynaklardaki yeni linkleri topla
    print(f"[*] {len(YEDEK_KAYNAKLAR)} kaynak taranıyor...")
    for s_url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(s_url, timeout=10)
            if r.status_code == 200:
                matches = re.findall(r"(#EXTINF:.*)\n(http.*)", r.text)
                for info, url in matches:
                    if url not in eklenen_linkler:
                        aday_listesi.append((info, url))
        except: continue

    # 3. Çoklu işlemle (Thread) linkleri test et
    print(f"[*] {len(aday_listesi)} link test ediliyor (Dokunulmazlar hariç)...")
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(link_test_et, aday_listesi))
        
    # 4. Sonuçları birleştir (Önce korunanlar, sonra sağlamlar)
    final_liste = korunanlar
    for res in results:
        if res and res[1] not in eklenen_linkler:
            final_liste.append(res)
            eklenen_linkler.add(res[1])

    # 5. Dosyayı tertemiz yaz
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for info, url in final_liste:
            f.write(f"{info}\n{url}\n")
    
    print(f"[+] BİTTİ! Toplam {len(final_liste)} sağlam kanal 'tr.m3u' dosyasına yazıldı.")

if __name__ == "__main__":
    update_m3u()
