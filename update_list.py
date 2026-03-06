import requests
import re
import time

def get_links():
    print("📡 Volo taranıyor, bu sefer olacak...")
    m3u_output = "#EXTM3U\n"
    target = "https://tv.canlitvvolo.com"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': target
    }

    try:
        # 1. Ana sayfadan kanal sayfalarını (URL'lerini) çek
        r = requests.get(target, headers=headers, timeout=20)
        # Sitenin link yapısı: /atv-izle-hd/ veya /show-tv-izle-hd/
        links = re.findall(r'href="(https://tv\.canlitvvolo\.com/[^"]+?)"', r.text)
        links = list(set([l for l in links if "-izle-hd" in l]))
        
        print(f"🔍 {len(links)} adet kanal sayfası bulundu.")

        for url in links[:35]: # İlk 35 kanalı dene
            try:
                name = url.split('/')[-2].replace('-izle-hd', '').replace('-', ' ').upper()
                res = requests.get(url, headers=headers, timeout=15)
                
                # En geniş kapsamlı m3u8 yakalayıcı
                find_m3u8 = re.search(r'["\'](https?://[^"\'>\s]+?\.m3u8[^"\'>\s]*?)["\']', res.text)
                
                if find_m3u8:
                    stream = find_m3u8.group(1).replace("\\/", "/")
                    m3u_output += f"#EXTINF:-1, {name}\n{stream}\n"
                    print(f"✅ {name} eklendi.")
                
                time.sleep(0.5)
            except: continue
            
        return m3u_output
    except Exception as e:
        print(f"❌ Hata: {e}")
        return "#EXTM3U\n"

if __name__ == "__main__":
    final_data = get_links()
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(final_data)
    print("🏁 Tamamlandı.")
