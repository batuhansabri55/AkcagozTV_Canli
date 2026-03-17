import xml.etree.ElementTree as ET
import requests
import json
from datetime import datetime, timedelta

EPG_URL = "https://goldvod.site/xmltv.php?username=hpgdiscoo&password=123456"

def parse_epg():
    print("Goldvod verisi taranıyor...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(EPG_URL, headers=headers, timeout=45)
        root = ET.fromstring(r.content)
    except Exception as e:
        print(f"Hata: {e}")
        return

    # TEŞHİS: Goldvod içinde hangi kanal ID'leri var?
    print("--- GOLDVOD KANAL LİSTESİ (İLK 20) ---")
    channels = root.findall('channel')
    for ch in channels[:20]:
        print(f"ID: {ch.get('id')} | İsim: {ch.find('display-name').text if ch.find('display-name') is not None else 'Yok'}")
    print("---------------------------------------")

    epg_data = {}
    tr_now = (datetime.utcnow() + timedelta(hours=3)).strftime("%Y%m%d%H%M")

    # Senin m3u listendeki tvg-id değerleri
    mapping = {
        "trt1.tr": ["TRT 1 FHD", "TRT 1 HD", "TRT 1 4K"],
        "kanald.tr": ["KANAL D FHD", "KANAL D HD", "KANAL D 4K"],
        "atv.tr": ["ATV FHD", "ATV HD", "ATV 4K"],
        "startv.tr": ["STAR TV FHD", "STAR TV HD", "STAR TV 4K"],
        "now.tr": ["NOW TV FHD", "NOW TV HD"],
        "showtv.tr": ["SHOW TV FHD", "SHOW TV HD", "SHOW TV 4K", "SHOW TV FHD (O)"],
        "tv8.tr": ["TV 8 FHD", "TV 8 HD"],
        "showtürk.tr": ["SHOW TÜRK"]
    }

    count = 0
    for programme in root.findall('programme'):
        ch_id = programme.get('channel')
        if not ch_id: continue
        
        # Küçük-büyük harf duyarlılığını kaldırarak kontrol et
        found_match = False
        for m_id, panel_names in mapping.items():
            if ch_id.lower() == m_id.lower():
                found_match = True
                start = programme.get('start')[:12]
                stop = programme.get('stop')[:12]
                if start <= tr_now <= stop:
                    title_elem = programme.find('title')
                    if title_elem is not None:
                        for panel_name in panel_names:
                            epg_data[panel_name] = {"title": title_elem.text}
                            count += 1
    
    with open('epg.json', 'w', encoding='utf-8') as f:
        json.dump(epg_data, f, ensure_ascii=False)
    
    print(f"İşlem Tamam! {count} kanal epg.json dosyasına yazıldı.")

if __name__ == "__main__":
    parse_epg()
