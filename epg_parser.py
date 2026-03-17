import xml.etree.ElementTree as ET
import requests
import json
import gzip
from datetime import datetime

# Yayın akışı kaynağı
EPG_URL = "https://raw.githubusercontent.com/fokus-itv/epg/main/guide.xml.gz"

def parse_epg():
    r = requests.get(EPG_URL)
    with open("guide.xml.gz", "wb") as f:
        f.write(r.content)
    
    with gzip.open("guide.xml.gz", 'rb') as f:
        tree = ET.parse(f)
        root = tree.getroot()

    epg_data = {}
    now = datetime.now().strftime("%Y%m%d%H%M%S")

    # Burası önemli: Sol taraf EPG'deki ID, Sağ taraf senin paneldeki kanal adın.
    # Eğer isimler tutmazsa EPG görünmez.
    channels_to_track = {
        "TRT1.tr": "TRT 1 FHD",
        "ATV.tr": "ATV",
        "KANALD.tr": "KANAL D",
        "STAR.tr": "STAR TV",
        "SHOW.tr": "SHOW TV",
        "TV8.tr": "TV8"
    }

    for programme in root.findall('programme'):
        channel_id = programme.get('channel')
        if channel_id in channels_to_track:
            start = programme.get('start')[:14]
            stop = programme.get('stop')[:14]
            
            if start <= now <= stop:
                title = programme.find('title').text
                ch_name = channels_to_track[channel_id]
                epg_data[ch_name] = {"title": title}

    with open('epg.json', 'w', encoding='utf-8') as f:
        json.dump(epg_data, f, ensure_ascii=False)

if __name__ == "__main__":
    parse_epg()
