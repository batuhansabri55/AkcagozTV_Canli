import requests
import re
import os
import datetime
from concurrent.futures import ThreadPoolExecutor

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

# GENİŞLETİLMİŞ VE DAHA HASSAS ALIAS SİSTEMİ
ALIAS_MAP = {
    "TV8.5": ["TV85HD 27", "TV85FHD 28"], # TV8'den önce gelmeli ki karışmasın
    "TV8": ["TV8HD 30", "TV8FHD 31"],
    "ATV": ["ATVHD 45", "ATVFHD 46"],
    "TRT 1": ["TRT148", "TRT1337667"],
    "SHOW": ["SHOWTVHD 43", "SHOWTVFHD 42"],
    "KANAL D": ["KANALDHD 39", "KANALDFHD 40"],
    "STAR": ["STARTVHD 36", "STARTVFHD 37"],
    "NOW": ["NowTVHD 34", "NowTVFHD 33"],
    "A HABER": ["A HABERHD 140", "A HABERFHD 139"],
    "CNN TURK": ["CNNTURKHD 150", "CNNTURKFHD 149"],
    "HABERTURK": ["HABERTURKHD 148", "HABERTURKFHD 147"],
    "NTV": ["NTVHD 152", "NTVFHD 151"],
    "SZC": ["SZCTVHD 232355", "SZCTVFHD 144"]
}

# Dağıtım sayacı (Kaldığı yerden devam etmesi için global)
global_counters = {k: 0 for k in ALIAS_MAP.keys()}

def alias_belirle(ham_isim):
    name = ham_isim.upper().replace(" ", "")
    for anahtar, varyasyonlar in ALIAS_MAP.items():
        key_clean = anahtar.upper().replace(" ", "")
        if key_clean in name:
            # TV8 ve TV8.5 karışıklığını önlemek için ek kontrol
            if key_clean == "TV8" and "TV8.5" in name:
                continue
            
            idx = global_counters[anahtar] % len(varyasyonlar)
            yeni = varyasyonlar[idx]
            global_counters[anahtar] += 1
            return yeni
    return ham_isim

def link_kontrol_et(item):
    ext, link = item
    try:
        # Timeout'u 7 yaptık, daha garantici
        r = requests.head(link, headers=HEADERS, timeout=7, allow_redirects=True)
        if r.status_code == 200:
            return f"{ext}\n{link}"
    except:
        pass
    return None

def main():
    # 1. DOKUNULMAZ BÖLGE
    temiz_dokunulmaz = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            temiz_dokunulmaz = lines[:3963]

    # 2. YEDEKLERİ TOPLA
    kontrol_listesi = []
    for url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(url, timeout=20)
            if r.status_code == 200:
                # Blokları ayır
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

    # 3. PARALEL TARAMA
    print(f"⚡ {len(kontrol_listesi)} link derinlemesine taranıyor...")
    with ThreadPoolExecutor(max_workers=40) as executor:
        results = list(executor.map(link_kontrol_et, kontrol_listesi))
    
    # 4. YAZMA
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(temiz_dokunulmaz)
        f.write("\n# --- TUM SAGLAM YEDEKLER ---\n")
        for res in results:
            if res: f.write(res + "\n")

    print("🚀 Usta şimdi bitti. Sayılar şimdi gerçekçi çıkacak.")

if __name__ == "__main__":
    main()
