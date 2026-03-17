import xml.etree.ElementTree as ET
import requests
import json
from datetime import datetime

# Daha stabil ve açık bir XML kaynağı
EPG_URL = "https://itv.unidgn.com/epg/guide.xml"

def parse_epg():
    print("EPG indiriliyor...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(EPG_URL, headers=headers)
    
    if r.status_code != 200:
        print(f"Hata: Sunucu cevap vermedi. Kod: {r.status_code}")
        return

    # XML verisini işle
    try:
        root = ET.fromstring(r.content)
    except Exception as e:
        print(f"XML Okuma Hatası: {e}")
        return

    epg_data = {}
    # Şu anki zamanı EPG formatında al (YılAyGünSaatDakika)
    now = datetime.now().strftime("%Y%m%d%H%M")

    # PANELDEKİ KANAL İSİMLERİNLE EŞLEŞTİRME
    # Sol taraf XML'deki ID, sağ taraf senin paneldeki adın
    channels_to_track = {
        "TRT 1": "TRT 1 FHD",
        "ATV": "ATV",
        "Kanal D": "KANAL D",
        "Star TV": "STAR TV",
        "Show TV": "SHOW TV",
        "TV8": "TV8",
        "FOX": "NOW TV"
    }

    for programme in root.findall('programme'):
        channel_id = programme.get('channel')
        if channel_id in channels_to_track:
            start = programme.get('start')[:12]
            stop = programme.get('stop')[:12]
            
            # Eğer şu an bu program yayınlanıyorsa al
            if start <= now <= stop:
                title_elem = programme.find('title')
                if title_elem is not None:
                    title = title_elem.text
                    ch_name = channels_to_track[channel_id]
                    epg_data[ch_name] = {"title": title}
                    print(f"Bulundu: {ch_name} -> {title}")

    with open('epg.json', 'w', encoding='utf-8') as f:
        json.dump(epg_data, f, ensure_ascii=False)
    print("epg.json başarıyla güncellendi!")

if __name__ == "__main__":
    parse_epg()
