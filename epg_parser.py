import xml.etree.ElementTree as ET
import requests
import json
from datetime import datetime
import gzip
import os

# SENİN VERDİĞİN ÇALIŞAN GOLDVOD ADRESİ
EPG_URL = "https://goldvod.site/xmltv.php?username=hpgdiscoo&password=123456"

def parse_epg():
    print("Goldvod EPG indiriliyor...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(EPG_URL, headers=headers, timeout=30)
        # Goldvod genelde sıkıştırılmamış XML gönderir, hata almamak için kontrol edelim
        try:
            content = gzip.decompress(r.content)
            print("Dosya GZIP olarak açıldı.")
        except:
            content = r.content
            print("Dosya düz XML olarak okundu.")
        
        root = ET.fromstring(content)
    except Exception as e:
        print(f"Bağlantı veya Okuma Hatası: {e}")
        return

    epg_data = {}
    now = datetime.now().strftime("%Y%m%d%H%M")

    # PANELDEKİ (D1) İSİMLERLE EŞLEŞTİRME
    mapping = {
        "trt1.tr": ["TRT 1 FHD", "TRT 1 HD"],
        "atv.tr": ["ATV FHD", "ATV HD"],
        "kanald.tr": ["KANAL D FHD", "KANAL D HD"],
        "star.tr": ["STAR TV FHD", "STAR TV HD"],
        "showtv.tr": ["SHOW TV FHD", "SHOW TV HD"],
        "tv8.tr": ["TV 8 FHD", "TV 8 HD"],
        "now.tr": ["NOW TV FHD", "NOW TV HD"]
    }

    found_count = 0
    for programme in root.findall('programme'):
        ch_id = programme.get('channel').lower()
        if ch_id in mapping:
            start = programme.get('start')[:12]
            stop = programme.get('stop')[:12]
            
            if start <= now <= stop:
                title_elem = programme.find('title')
                if title_elem is not None:
                    title = title_elem.text
                    for panel_name in mapping[ch_id]:
                        epg_data[panel_name] = {"title": title}
                        found_count += 1

    with open('epg.json', 'w', encoding='utf-8') as f:
        json.dump(epg_data, f, ensure_ascii=False)
    
    print(f"İşlem bitti! {found_count} kanal verisi epg.json dosyasına yazıldı.")

if __name__ == "__main__":
    parse_epg()
