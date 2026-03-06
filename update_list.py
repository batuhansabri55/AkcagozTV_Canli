import requests
import re
import time

def get_links():
    print("🚀 Volo Operasyonu: Derin tarama başlatılıyor...")
    m3u_header = "#EXTM3U\n"
    # Sitenin ana adresi
    base_url = "https://tv.canlitvvolo.com"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': base_url
    }

    try:
        # 1. Ana sayfadan tüm kanal linklerini topla
        r = requests.get(base_url, headers=headers, timeout=20)
        # Sitenin link yapısı genellikle /kanal-adi-izle-hd/ şeklindedir
        links = re.findall(r'href="(https://tv\.canlitvvolo\.com/[^"]+?)"', r.text)
        # Sadece kanal sayfalarını al ve tekrarları sil
        links = list(set([l for l in links if "-izle-hd" in l]))
        
        print(f"📡 {len(links)} adet kanal sayfası tespit edildi.")

        content_body = ""
        for url in links[:40]: # İlk 40 kanalı tara (Hız için)
            try:
                # Kanal adını URL'den çıkar ve temizle
                name = url.split('/')[-2].replace('-izle-hd', '').replace('-', ' ').upper()
                
                # Kanal sayfasına git ve m3u8 linkini ara
                res = requests.get(url, headers=headers, timeout=15)
                
                # Bu regex hem tırnaklı hem tırnaksız linkleri yakalar
                m3u8_match = re.search(r'["\'](https?://[^"\'>\s]+?\.m3u8[^"\'>\s]*?)["\']', res.text)
                
                if m3u8_match:
                    stream_url = m3u8_match.group(1).replace("\\/", "/")
                    content_body += f"#EXTINF:-1, {name}\n{stream_url}\n"
                    print(f"✅ Eklendi: {name}")
                
                time.sleep(0.5) # Siteyi bloklamasın diye minik mola
            except:
                continue
        
        return m3u_header + content_body

    except Exception as e:
        print(f"❌ Kritik Hata: {e}")
        return m3u_header

if __name__ == "__main__":
    final_m3u = get_links()
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(final_m3u)
    
    import os
    size = os.path.getsize("tr.m3u")
    print(f"🏁 Bitti. Dosya boyutu: {size} byte.")
