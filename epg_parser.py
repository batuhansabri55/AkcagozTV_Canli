import xml.etree.ElementTree as ET
import requests
import json
from datetime import datetime
import os

# SENİN ÇALIŞAN GOLDVOD ADRESİN
EPG_URL = "https://goldvod.site/xmltv.php?username=hpgdiscoo&password=123456"

def parse_epg():
    print("Goldvod EPG verisi çekiliyor...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(EPG_URL, headers=headers, timeout=30)
        # Goldvod XML formatında veri gönderir
        root = ET.fromstring(r.content)
    except Exception as e:
        print(f"Hata: {e}")
        return

    epg_data = {}
    # Şu anki zamanı EPG formatında al (YılAyGünSaatDakika)
    now = datetime.now().strftime("%Y%m%d%H%M")

    # GOLDVOD KANAL ID'LERİNİ SENİN PANELDEKİ İSİMLERLE EŞLEŞTİRİYORUZ
    # Goldvod'dan gelen ID'leri küçük harfe çevirerek kontrol eder
    mapping = {
        "trt1.tr": ["TRT 1 FHD", "TRT 1 HD"],
        "atv.tr": ["ATV FHD", "ATV HD"],
        "kanald.tr": ["KANAL D FHD", "KANAL D HD"],
        "startv.tr": ["STAR TV FHD", "STAR TV HD"],
        "showtv.tr": ["SHOW TV FHD", "SHOW TV HD"],
        "tv8.tr": ["TV 8 FHD", "TV 8 HD"],
        "fox.tr": ["NOW TV FHD", "NOW TV HD"]
    }

    count = 0
    for programme in root.findall('programme'):
        ch_id = programme.get('channel').lower()
        if ch_id in mapping:
            start = programme.get('start')[:12]
            stop = programme.get('stop')[:12]
            
            # Eğer şu anki zaman yayın saati arasındaysa başlığı al
            if start <= now <= stop:
                title_elem = programme.find('title')
                if title_elem is not None:
                    title = title_elem.text
                    for panel_name in mapping[ch_id]:
                        epg_data[panel_name] = {"title": title}
                        count += 1

    # Dosyayı oluştur (Boş kalmaması için en az bir kayıt olmalı)
    with open('epg.json', 'w', encoding='utf-8') as f:
        json.dump(epg_data, f, ensure_ascii=False)
    
    print(f"Başarılı! {count} adet yayın akışı epg.json dosyasına işlendi.")

if __name__ == "__main__":
    parse_epg()
