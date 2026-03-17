import xml.etree.ElementTree as ET
import requests
import json
from datetime import datetime, timedelta

# GOLDVOD ADRESİN
EPG_URL = "https://goldvod.site/xmltv.php?username=hpgdiscoo&password=123456"

def parse_epg():
    print("Goldvod verisi tüm kanallar için taranıyor...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(EPG_URL, headers=headers, timeout=60)
        root = ET.fromstring(r.content)
    except Exception as e:
        print(f"Bağlantı Hatası: {e}")
        return

    epg_data = {}
    tr_now = (datetime.utcnow() + timedelta(hours=3)).strftime("%Y%m%d%H%M")

    # MAPPING: Goldvod_ID: ["Panel_Ismi_1", "Panel_Ismi_2"]
    # Usta, buraya en önemli kanalları bir kez yazıyoruz, geri kalanını sistem hallediyor.
    mapping = {
        "trt1.tr": ["TRT 1 FHD", "TRT 1 HD", "TRT 1 4K"],
        "atv.tr": ["ATV FHD", "ATV HD"],
        "kanald.tr": ["KANAL D FHD", "KANAL D HD"],
        "STARTV.tr": ["STAR TV FHD", "STAR TV HD"],
        "Now.tr": ["NOW TV FHD", "NOW TV HD"],
        "showtv.tr": ["SHOW TV FHD", "SHOW TV HD"],
        "tv8.tr": ["TV 8 FHD", "TV 8 HD"],
        "showtürk.tr": ["SHOW TÜRK"],
        # SPOR KANALLARI (ID'leri Goldvod'a göre ekliyoruz)
        "beinsports1.tr": ["beIN SPORTS 1 FHD", "BEIN SPORTS 1 HD"],
        "beinsports2.tr": ["beIN SPORTS 2 FHD"],
        "ssport.tr": ["S SPORT HD", "S SPORT FHD"],
        "tivibuspor1.tr": ["TİVİBU SPOR 1 HD"],
        "trtspor.tr": ["TRT SPOR HD"],
        "aspor.tr": ["A SPOR HD"]
    }

    count = 0
    # Tüm yayınları tara
    for programme in root.findall('programme'):
        xml_id = programme.get('channel')
        if not xml_id: continue
        
        # ID eşleşmesi kontrolü
        xml_id_lower = xml_id.lower()
        for gold_id, panel_names in mapping.items():
            if xml_id_lower == gold_id.lower():
                start = programme.get('start')[:12]
                stop = programme.get('stop')[:12]
                
                if start <= tr_now <= stop:
                    title_elem = programme.find('title')
                    if title_elem is not None:
                        for name in panel_names:
                            epg_data[name] = {"title": title_elem.text}
                            count += 1

    # Dosyayı Kaydet
    with open('epg.json', 'w', encoding='utf-8') as f:
        json.dump(epg_data, f, ensure_ascii=False)
    
    print(f"İşlem bitti! {count} kanal verisi epg.json dosyasına yazıldı.")

if __name__ == "__main__":
    parse_epg()
