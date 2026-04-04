import requests
import re
import os
import datetime
import time
from concurrent.futures import ThreadPoolExecutor

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
ZIRH_LIMIT = 5047  # BU SATIR SAYISI ASLA DEĞİŞMEZ
HEADERS = {'User-Agent': 'VLC/3.0.18 LibVLC/3.0.18'}

YEDEK_KAYNAKLAR = [
    "https://streams.uzunmuhalefet.com/lists/tr.m3u",
    "https://tinyurl.com/ytpatron",
    "https://urlz.fr/v1Xo",
    "https://raw.githubusercontent.com/smartgmr/cdn/refs/heads/main/Perfect.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://tinyurl.com/bdd2tz6h",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u"
]

def hiz_testi(url):
    """Linkin hızını ölçer (ms)."""
    try:
        start = time.time()
        response = requests.head(url, headers=HEADERS, timeout=1.2, allow_redirects=True)
        if response.status_code == 200:
            return int((time.time() - start) * 1000)
    except:
        pass
    return 9999

def main():
    if not os.path.exists(FILE_PATH): return
    
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        tum_satirlar = f.readlines()
    
    zırh_bolumu = tum_satirlar[:ZIRH_LIMIT]
    mevcut_urller = set()
    link_havuzu = {} # Kanal ismi -> [Link listesi]

    # 1. ZIRHTAKİ LİNKLERİ ANALİZ ET
    for i in range(len(zırh_bolumu)):
        line = zırh_bolumu[i].strip()
        if line.startswith("http"):
            # Bir önceki satır EXTINF satırıdır
            kanal_adi = zırh_bolumu[i-1].split(',')[-1].strip()
            if kanal_adi not in link_havuzu: link_havuzu[kanal_adi] = []
            link_havuzu[kanal_adi].append(line)
            mevcut_urller.add(line)

    # 2. DIŞ KAYNAKLARDAN TAZE LİNKLERİ ÇEK (MÜKERRER OLMADAN)
    for y_url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(y_url, headers=HEADERS, timeout=10)
            bulunanlar = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", r.text, re.DOTALL)
            for kanal in bulunanlar:
                parca = kanal.strip().split('\n')
                k_adi = parca[0].split(',')[-1].strip()
                k_link = parca[-1].strip()
                if k_link not in mevcut_urller:
                    if k_adi not in link_havuzu: link_havuzu[k_adi] = []
                    link_havuzu[k_adi].append(k_link)
                    mevcut_urller.add(k_link)
        except: continue

    # 3. 9000 LİNKİ TOPLU TEST ET VE SIRALA
    print("Usta, bütün havuz (9000 link) tartılıyor...")
    for k_adi, linkler in link_havuzu.items():
        if len(linkler) > 1:
            with ThreadPoolExecutor(max_workers=10) as ex:
                sonuclar = list(ex.map(lambda u: (hiz_testi(u), u), linkler))
            # En hızlı (en düşük ms) olanı başa al
            link_havuzu[k_adi] = [item[1] for item in sorted(sonuclar)]

    # 4. YAZDIRMA (ZIRHIN SIRASINI BOZMADAN İÇİNİ GÜNCELLE)
    yeni_m3u = []
    zırh_index = 0
    while zırh_index < len(zırh_bolumu):
        satir = zırh_bolumu[zırh_index]
        if satir.startswith("http"):
            # Bu linkin ait olduğu kanalın EN HIZLISINI buraya yaz
            k_adi = zırh_bolumu[zırh_index-1].split(',')[-1].strip()
            en_hizli = link_havuzu[k_adi][0] 
            yeni_m3u.append(en_hizli + "\n")
            # En hızlıyı kullandık, havuzdan çıkar ki yedeklere de yazmasın
            link_havuzu[k_adi].pop(0)
        else:
            yeni_m3u.append(satir)
        zırh_index += 1

    # 5. GERİYE KALAN YEDEKLERİ ALTA EKLE
    yeni_m3u.append("\n# --- HIZ TESTİNDEN GEÇMİŞ SIRALI YEDEKLER ---\n")
    for k_adi, linkler in link_havuzu.items():
        for l in linkler:
            yeni_m3u.append(f'#EXTINF:-1 group-title="YEDEKLER",{k_adi}\n{l}\n')

    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(yeni_m3u)

if __name__ == "__main__":
    main()
