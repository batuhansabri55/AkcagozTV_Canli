import xml.etree.ElementTree as ET
import requests
import json
from datetime import datetime

EPG_URL = "https://goldvod.site/xmltv.php?username=hpgdiscoo&password=123456"

def parse_epg():
    print("Goldvod verisi ayıklanıyor...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(EPG_URL, headers=headers, timeout=40)
        root = ET.fromstring(r.content)
    except Exception as e:
        print(f"Hata: {e}")
        return

    epg_data = {}
    now = datetime.now().strftime("%Y%m%d%H%M")

    # PANELİNDEKİ tvg_id DEĞERLERİNE GÖRE EŞLEŞTİRME
    mapping = {
        "trt1.tr": ["TRT 1 FHD", "TRT 1 HD"],
        "atv.tr": ["ATV FHD", "ATV HD"],
        "kanald.tr": ["KANAL D FHD", "KANAL D HD"],
        "startv.tr": ["STAR TV FHD", "STAR TV HD"],
        "showtv.tr": ["SHOW TV FHD", "SHOW TV HD"],
        "tv8.tr": ["TV 8 FHD", "TV 8 HD"],
        "fox.tr": ["NOW TV FHD", "NOW TV HD"],
        "now.tr": ["NOW TV FHD", "NOW TV HD"]
    }

    count = 0
    for programme in root.findall('programme'):
        raw_id = programme.get('channel')
        if not raw_id: continue
        
        ch_id = raw_id.lower()
        # Kanal ismi mapping listemizde var mı kontrol et
        if ch_id in mapping:
            start = programme.get('start')[:12]
            stop = programme.get('stop')[:12]
            
            if start <= now <= stop:
                title_elem = programme.find('title')
                if title_elem is not None:
                    title_text = title_elem.text
                    for panel_name in mapping[ch_id]:
                        epg_data[panel_name] = {"title": title_text}
                        count += 1

    with open('epg.json', 'w', encoding='utf-8') as f:
        json.dump(epg_data, f, ensure_ascii=False)
    
    print(f"Başarılı! {count} kanal için yayın bilgisi epg.json dosyasına yazıldı.")

if __name__ == "__main__":
    parse_epg()
