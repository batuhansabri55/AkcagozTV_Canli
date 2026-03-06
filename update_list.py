import requests
import re

def get_direct_list():
    print("🚀 Engel tanımayan son deneme başlatılıyor...")
    # Giniko panelinin ana veri ucu
    url = "https://giniko.smartiptvworld.workers.dev/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36',
        'Accept': '*/*'
    }

    try:
        r = requests.get(url, headers=headers, timeout=30)
        # Sayfada m3u8 linki veya kanal ismi var mı bak
        if "m3u8" in r.text or "#EXTM3U" in r.text:
            print("✅ Veri yakalandı!")
            return r.text
        else:
            print("⚠️ Site yine boş döndü. Bot koruması aktif.")
            return "#EXTM3U\n# Site robotu engelledi."
    except:
        return "#EXTM3U\n"

if __name__ == "__main__":
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(get_direct_list())
