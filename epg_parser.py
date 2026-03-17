import xml.etree.ElementTree as ET
import requests
import json
from datetime import datetime
import gzip
import os

# GitHub'daki en sağlam EPG kaynağı
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

    # SENİN PANELDEKİ (D1) İSİMLERLE %100 UYUMLU LİSTE
    channels_to_track = {
        "TRT1.tr": ["TRT 1 FHD", "TRT 1 HD"],
        "ATV.tr": ["ATV FHD", "ATV HD"],
        "KANALD.tr": ["KANAL D FHD", "KANAL D HD"],
        "STAR.tr": ["STAR TV FHD", "STAR TV HD"],
        "SHOW.tr": ["SHOW TV FHD", "SHOW TV HD"],
        "TV8.tr": ["TV 8 FHD", "TV 8 HD"],
        "FOX.tr": ["NOW TV FHD", "NOW TV HD"]
    }

    for programme in root.findall('programme'):
        channel_id = programme.get('channel')
        if channel_id in channels_to_track:
            start = programme.get('start')[:12]
            stop = programme.get('stop')[:12]
            
            if start <= now <= stop:
                title_elem = programme.find('title')
                if title_elem is not None:
                    # Bu kanala ait tüm isim varyasyonlarına aynı başlığı ekle
                    for ch_name in channels_to_track[channel_id]:
                        epg_data[ch_name] = {"title": title_elem.text}
                        print(f"Eklendi: {ch_name} -> {title_elem.text}")

    with open('epg.json', 'w', encoding='utf-8') as f:
        json.dump(epg_data, f, ensure_ascii=False)
    print("epg.json dosyası dolu şekilde hazır!")

if __name__ == "__main__":
    parse_epg()
