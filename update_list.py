import requests
import re
import time

def get_links():
    print("🚀 Yeni hedef taranıyor: tv.canlitvvolo.com")
    m3u_content = "#EXTM3U\n"
    # Yeni ana sayfa
    base_url = "https://tv.canlitvvolo.com"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': base_url
    }

    try:
        # 1. Ana sayfadan kanal linklerini topla
        r = requests.get(base_url, headers=headers, timeout=20)
        # Sitedeki kanal sayfaları: /atv-izle-hd/ gibi biter
        channels = re.findall(r'href="(https://tv\.canlitvvolo\.com/[^"]+?-izle-hd/)"', r.text)
        channels = list(set(channels)) # Tekrarları sil
        
        print(f"📡 {len(channels)} adet kanal bulundu. Yayınlar ayıklanıyor...")

        for ch_url in channels[:40]: # İlk 40 tanesini dene
            try:
                # Kanal adını URL'den al (atv-izle-hd -> ATV)
                name = ch_url.split('/')[-2].replace('-izle-hd', '').replace('-', ' ').upper()
                
                # Kanal sayfasına gir
                res = requests.get(ch_url, headers=headers, timeout=15)
                
                # Sayfa içindeki .m3u8 linkini yakala
                m3u8_match = re.search(r'["\'](https?://[^"\'>\s]+?\.m3u8[^"\'>\s]*?)["\']', res.text)
                
                if m3u8_match:
                    final_url = m3u8_match.group(1).replace("\\/", "/")
                    m3u_content += f"#EXTINF:-1, {name}\n{final_url}\n"
                    print(f"✅ Eklendi: {name}")
                
                time.sleep(0.5) 
            except:
                continue

    except Exception as e:
        print(f"❌ Kritik Hata: {e}")
    
    return m3u_content

if __name__ == "__main__":
    final_m3u = get_links()
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(final_m3u)
    print("🏁 İşlem bitti. tr.m3u güncellendi.")
