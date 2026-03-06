import requests
import re
import time

def get_links():
    print("🚀 Volo üzerinden kanallar toplanıyor...")
    m3u_header = "#EXTM3U\n"
    # Yeni Hedef Site (Diğer sekmende açık olan site)
    base_url = "https://tv.canlitvvolo.com"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': base_url
    }

    try:
        r = requests.get(base_url, headers=headers, timeout=20)
        # Sitedeki kanal sayfalarını bulur (-izle-hd/ yapısı)
        channels = re.findall(r'href="(https://tv\.canlitvvolo\.com/[^"]+?-izle-hd/)"', r.text)
        channels = list(set(channels)) 
        
        print(f"📡 {len(channels)} kanal bulundu. Linkler ayıklanıyor...")

        content = m3u_header
        for ch_url in channels[:30]: # İlk 30 kanalı tara
            try:
                name = ch_url.split('/')[-2].replace('-izle-hd', '').replace('-', ' ').upper()
                res = requests.get(ch_url, headers=headers, timeout=15)
                # Sayfa içindeki gizli m3u8 yayın linkini bulur
                m3u8 = re.search(r'["\'](https?://[^"\'>\s]+?\.m3u8[^"\'>\s]*?)["\']', res.text)
                
                if m3u8:
                    stream = m3u8.group(1).replace("\\/", "/")
                    content += f"#EXTINF:-1, {name}\n{stream}\n"
                    print(f"✅ {name} eklendi.")
                time.sleep(0.5)
            except: continue
        return content
    except: return m3u_header

if __name__ == "__main__":
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(get_links())
    print("🏁 tr.m3u güncellendi.")
