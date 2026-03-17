import xml.etree.ElementTree as ET
import requests
import json
from datetime import datetime, timedelta

EPG_URL = "https://goldvod.site/xmltv.php?username=hpgdiscoo&password=123456"

def parse_epg():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(EPG_URL, headers=headers, timeout=45)
        root = ET.fromstring(r.content)
    except Exception as e:
        print(f"Hata: {e}")
        return

    epg_data = {}
    # Türkiye saati (UTC+3)
    tr_now = (datetime.utcnow() + timedelta(hours=3)).strftime("%Y%m%d%H%M")

    # M3U VE D1 TABLANDAKİ tvg_id DEĞERLERİNE GÖRE EŞLEŞTİRME
    mapping = {
        "trt1.tr": ["TRT 1 FHD", "TRT 1 HD", "TRT 1 4K"],
        "kanald.tr": ["KANAL D FHD", "KANAL D HD", "KANAL D 4K"],
        "atv.tr": ["ATV FHD", "ATV HD", "ATV 4K"],
        "STARTV.tr": ["STAR TV FHD", "STAR TV HD", "STAR TV 4K"],
        "Now.tr": ["NOW TV FHD", "NOW TV HD"],
        "showtv.tr": ["SHOW TV FHD", "SHOW TV HD", "SHOW TV 4K", "SHOW TV FHD (O)"],
        "tv8.tr": ["TV 8 FHD"],
        "showtürk.tr": ["SHOW TÜRK"]
    }

    count = 0
    for programme in root.findall('programme'):
        raw_id = programme.get('channel')
        if not raw_id: continue
        
        # Goldvod ID'sini senin listenle eşleştir
        for target_id, panel_names in mapping.items():
            if raw_id.lower() == target_id.lower():
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
    
    print(f"Bitti! {count} kanal epg.json dosyasına başarıyla işlendi.")

if __name__ == "__main__":
    parse_epg()
