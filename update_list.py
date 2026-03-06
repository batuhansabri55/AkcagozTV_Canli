import requests
import re
import time

def get_links():
    print("🚀 Yeni hedef taranıyor: tv.canlitvvolo.com")
    m3u_content = "#EXTM3U\n"
    base_url = "https://tv.canlitvvolo.com"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': base_url
    }

    try:
        # 1. Ana sayfayı çek ve kanal sayfalarını bul
        r = requests.get(base_url, headers=headers, timeout=20)
        # Sitedeki kanal sayfaları /kanal-adi-izle-hd/ şeklinde biter
        channels = re.findall(r'href="(https://tv\.canlitvvolo\.com/[^"]+?-izle-hd/)"', r.text)
        channels = list(set(channels)) 
        
        print(f"📡 {len(channels)} adet kanal sayfası bulundu. M3U8 aranıyor...")

        for ch_url in channels[:35]: # İlk 35 kanalı tara
            try:
                # Kanal ismini URL'den güzelleştir
                name = ch_url.split('/')[-2].replace('-izle-hd', '').replace('-', ' ').upper()
                
                # Kanal sayfasına gir ve yayın linkini yakala
                res = requests.get(ch_url, headers=headers, timeout=15)
                m3u8 = re.search(r'["\'](https?://[^"\'>\s]+?\.m3u8[^"\'>\s]*?)["\']', res.text)
                
                if m3u8:
                    stream_url = m3u8.group(1).replace("\\/", "/")
                    m3u_content += f"#EXTINF:-1, {name}\n{stream_url}\n"
                    print(f"✅ Eklendi: {name}")
                
                time.sleep(0.5) 
            except: continue

    except Exception as e:
        print(f"❌ Hata: {e}")
    
    return m3u_content

if __name__ == "__main__":
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(get_links())
    print("🏁 İşlem bitti.")
