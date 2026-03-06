import requests
import re
import time

def get_volo_live():
    print("🚀 Volo Operasyonu Başladı: Derin tarama yapılıyor...")
    m3u_header = "#EXTM3U\n"
    base_url = "https://tv.canlitvvolo.com"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Referer': base_url,
        'Accept-Language': 'tr-TR,tr;q=0.9'
    }

    try:
        # 1. Ana sayfadan kanal kartlarını bul
        r = requests.get(base_url, headers=headers, timeout=20)
        # Sitenin link yapısı: /kanal-adi-izle-hd/
        channels = re.findall(r'href="(https://tv\.canlitvvolo\.com/[^"]+?)"', r.text)
        channels = list(set([c for c in channels if "-izle-hd" in c]))
        
        print(f"📡 {len(channels)} kanal bulundu. İçerikler süzülüyor...")

        body = ""
        for ch_url in channels[:40]:
            try:
                # İsim temizleme
                name = ch_url.split('/')[-2].replace('-izle-hd', '').replace('-', ' ').upper()
                
                # Sayfaya gir ve m3u8 ara
                res = requests.get(ch_url, headers=headers, timeout=15)
                
                # Sitenin kullandığı farklı m3u8 formatlarını yakala
                m3u8_pattern = r'["\'](https?://[^"\'>\s]+?\.m3u8[^"\'>\s]*?)["\']'
                match = re.search(m3u8_pattern, res.text)
                
                if match:
                    stream = match.group(1).replace("\\/", "/")
                    body += f"#EXTINF:-1, {name}\n{stream}\n"
                    print(f"✅ Eklendi: {name}")
                
                time.sleep(0.3)
            except: continue
            
        return m3u_header + body

    except Exception as e:
        print(f"❌ Hata: {e}")
        return m3u_header

if __name__ == "__main__":
    content = get_volo_live()
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(content)
    print("🏁 İşlem tamamlandı. GitHub Actions'ın bitmesini bekle.")
