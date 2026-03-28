import requests
import re
import os
import datetime
from concurrent.futures import ThreadPoolExecutor

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

# ALIAS SİSTEMİ (Tam Kelime Eşleşmesi İçin Hazır)
ALIAS_MAP = {
    "ATV": ["ATVHD 45", "ATVFHD 46"],
    "TV8": ["TV8HD 30", "TV8FHD 31"],
    "SHOW": ["SHOWTVHD 43", "SHOWTVFHD 42"],
    "KANAL D": ["KANALDHD 39", "KANALDFHD 40"],
    "STAR": ["STARTVHD 36", "STARTVFHD 37"],
    "NOW": ["NowTVHD 34", "NowTVFHD 33"],
    "TRT 1": ["TRT148", "TRT1337667"],
    "TV8.5": ["TV85HD 27", "TV85FHD 28"],
    "SZC": ["SZCTVHD 232355", "SZCTVFHD 144"]
}

global_counters = {k: 0 for k in ALIAS_MAP.keys()}

def alias_belirle(ham_isim):
    name = ham_isim.upper().strip()
    
    # TV8.5'u TV8'den önce kontrol etmeliyiz
    if "TV8.5" in name or "TV 8.5" in name:
        anahtar = "TV8.5"
        idx = global_counters[anahtar] % len(ALIAS_MAP[anahtar])
        yeni = ALIAS_MAP[anahtar][idx]
        global_counters[anahtar] += 1
        return yeni

    for anahtar, varyasyonlar in ALIAS_MAP.items():
        if anahtar == "TV8.5": continue # Yukarıda hallettik
        
        # Sadece TAM KELİME kontrolü (Sinema TV'yi korur)
        if re.search(rf'\b{re.escape(anahtar)}\b', name):
            idx = global_counters[anahtar] % len(varyasyonlar)
            yeni = varyasyonlar[idx]
            global_counters[anahtar] += 1
            return yeni
            
    return ham_isim # Hiçbiri tutmazsa ismi olduğu gibi bırak (Sinema TV vb.)

def link_kontrol_et(item):
    ext, link = item
    try:
        r = requests.head(link, headers=HEADERS, timeout=7, allow_redirects=True)
        if r.status_code == 200:
            return f"{ext}\n{link}"
    except: pass
    return None

def main():
    temiz_dokunulmaz = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            temiz_dokunulmaz = lines[:3963]

    kontrol_listesi = []
    print("🔄 Yedekler toplanıyor ve Akıllı Alias atanıyor...")
    for url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            if r.status_code == 200:
                blocks = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", r.text, re.DOTALL)
                for b in blocks:
                    parts = b.strip().split('\n')
                    if len(parts) >= 2:
                        ext_line = parts[0]
                        link_url = parts[1].strip()
                        
                        if "," in ext_line:
                            meta, old_name = ext_line.rsplit(',', 1)
                            new_name = alias_belirle(old_name.strip())
                            final_ext = f"{meta},{new_name}"
                            
                            if 'group-title' not in final_ext:
                                final_ext = final_ext.replace('#EXTINF:', '#EXTINF:-1 group-title="YEDEKLER",')
                            
                            kontrol_listesi.append((final_ext, link_url))
        except: continue

    print(f"⚡ {len(kontrol_listesi)} link kontrol ediliyor (Aynı anda 50 kanal)...")
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(link_kontrol_et, kontrol_listesi))
    
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(temiz_dokunulmaz)
        f.write("\n# --- AKILLI ALIAS YEDEKLERİ ---\n")
        for res in results:
            if res: f.write(res + "\n")

    print("🚀 Operasyon başarıyla bitti usta. Sinemalar kurtarıldı!")

if __name__ == "__main__":
    main()
