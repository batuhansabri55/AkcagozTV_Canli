import xml.etree.ElementTree as ET
import requests
import json
from datetime import datetime
import gzip

EPG_URL = "https://raw.githubusercontent.com/fokus-itv/epg/main/guide.xml.gz"

def parse_epg():
    print("EPG indiriliyor...")
    r = requests.get(EPG_URL)
    try:
        content = gzip.decompress(r.content)
        root = ET.fromstring(content)
    except Exception as e:
        print(f"Hata: {e}")
        return

    epg_data = {}
    now = datetime.now().strftime("%Y%m%d%H%M")

    # PANEL İSİMLERİ (Senin paneldekilerle birebir aynı olmalı)
    channels_to_track = {
        "TRT1.tr": "TRT 1 FHD",
        "ATV.tr": "ATV",
        "KANALD.tr": "KANAL D",
        "STAR.tr": "STAR TV",
        "SHOW.tr": "SHOW TV",
        "TV8.tr": "TV8",
        "FOX.tr": "NOW TV"
    }

    for programme in root.findall('programme'):
        channel_id = programme.get('channel')
        if channel_id in channels_to_track:
            start = programme.get('start')[:12]
            stop = programme.get('stop')[:12]
            if start <= now <= stop:
                title_elem = programme.find('title')
                if title_elem is not None:
                    ch_name = channels_to_track[channel_id]
                    epg_data[ch_name] = {"title": title_elem.text}

    with open('epg.json', 'w', encoding='utf-8') as f:
        json.dump(epg_data, f, ensure_ascii=False)
    print("epg.json hazır!")

if __name__ == "__main__":
    parse_epg()
