import requests
import os

YEDEK_KAYNAKLAR = [
    "https://raw.githubusercontent.com/sultansmgr/smart/refs/heads/main/viziTV.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://streams.uzunmuhalefet.com/lists/tr.m3u"
]

def link_test_et(url):
    """Link aktif mi değil mi kontrol eder."""
    try:
        r = requests.head(url, timeout=3, allow_redirects=True)
        return r.status_code < 400
    except:
        return False

def update_m3u():
    headers = {"User-Agent": "Mozilla/5.0"}
    temiz_liste = []
    eklenen_linkler = set()

    # 1. MEVCUT DOSYADAKİ HER ŞEYİ TEST ET VE AYIKLA
    if os.path.exists("tr.m3u"):
        with open("tr.m3u", "r", encoding="utf-8") as f:
            lines = f.readlines()
            info = ""
            for line in lines:
                line = line.strip()
                if line.startswith("#EXTINF"): info = line
                elif line.startswith("http"):
                    # Dosyadaki linki test et, çalışıyorsa listeye geri al
                    if link_test_et(line):
                        if info: temiz_liste.append(info)
                        temiz_liste.append(line)
                        eklenen_linkler.add(line)
                    info = ""

    # 2. DIŞ KAYNAKLARDAN YENİ ÇALIŞAN LİNKLERİ EKLE
    for url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                lines = r.text.splitlines()
                info = ""
                for l in lines:
                    if l.startswith("#EXTINF"): info = l
                    elif l.startswith("http") and info:
                        link = l.strip()
                        if link not in eklenen_linkler and link_test_et(link):
                            temiz_liste.append(info)
                            temiz_liste.append(link)
                            eklenen_linkler.add(link)
                        info = ""
        except: continue

    # 3. SADECE ÇALIŞANLARLA DOSYAYI SIFIRDAN YAZ
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n" + "\n".join(temiz_liste))

if __name__ == "__main__":
    update_m3u()
