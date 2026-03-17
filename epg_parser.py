import xml.etree.ElementTree as ET
import requests
import json
from datetime import datetime
import io
import gzip

# Sağlam bir XMLTV kaynağı
EPG_URL = "https://raw.githubusercontent.com/fokus-itv/epg/main/guide.xml"

def parse_epg():
    print("EPG indiriliyor...")
    r = requests.get(EPG_URL)
    
    # Dosya içeriğini belirle (Gzip mi yoksa düz metin mi?)
    content = r.content
    if content.startswith(b'\x1f\x8b'):
        print("Sıkıştırılmış dosya açılıyor...")
        content = gzip.decompress(content)
    
    root = ET.fromstring(content)
    epg_data = {}
    now = datetime.now().strftime("%Y%m%d%H%M%S")

    # Senin paneldeki kanal isimlerinle tam eşleşmeli usta!
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
                title_elem = programme.find('title')
                if title_elem is not None:
                    title = title_elem.text
                    ch_name = channels_to_track[channel_id]
                    epg_data[ch_name] = {"title": title}

    with open('epg.json', 'w', encoding='utf-8') as f:
        json.dump(epg_data, f, ensure_ascii=False)
    print("epg.json başarıyla oluşturuldu!")

if __name__ == "__main__":
    parse_epg()
