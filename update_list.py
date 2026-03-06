import requests
import re
import time

def get_links():
    print("🛰️ Bağlantı kuruluyor...")
    m3u_header = "#EXTM3U\n"
    # Hedef URL
    target = "https://www.blogtv.net.tr/p/turkiyenin-en-kapsaml-ulusal-kanallar.html"
    
    # Çok daha güçlü ve gerçekçi tarayıcı başlıkları
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'tr,en-US;q=0.7,en;q=0.3',
        'Referer': 'https://www.google.com/',
        'Cache-Control': 'no-cache'
    }

    try:
        # 1. Ana sayfayı çek
        r = requests.get(target, headers=headers, timeout=30)
        
        # Sitedeki tüm kanal linklerini yakala (regex'i en esnek hale getirdim)
        # Tırnaklı, tırnaksız veya farklı parametreli her şeyi deneyecek
        found_links = re.findall(r'https://www\.blogtv\.net\.tr/p/[^"\'>\s]+\.html\?kanal=[^"\'>\s]+', r.text)
        found_links = list(set(found_links)) # Tekrarları sil
        
        print(f"🔍 Sitede {len(found_links)} adet link tespit edildi.")

        content = m3u_header
        count = 0

        for link in found_links[:50]:
            try:
                # Kanal ismini ayıkla
                name = link.split("kanal=")[-1].replace("%20", " ").replace("+", " ").upper()
                
                # Kanal sayfasını çek
                res = requests.get(link, headers=headers, timeout=15)
                
                # m3u8 linkini ara (vjs-source, script veya düz metin içinde)
                m3u8_match = re.search(r'["\'](https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*?)["\']', res.text)
                
                if m3u8_match:
                    final_url = m3u8_match.group(1).replace("\\/", "/")
                    content += f"#EXTINF:-1, {name}\n{final_url}\n"
                    print(f"✅ Eklendi: {name}")
                    count += 1
                
                time.sleep(0.3) # Çok hızlı gidip ban yemeyelim
            except:
                continue
        
        return content, count

    except Exception as e:
        print(f"❌ Kritik Hata: {e}")
        return m3u_header, 0

if __name__ == "__main__":
    final_m3u, total = get_links()
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(final_m3u)
    
    print(f"🏁 İşlem bitti. Toplam {total} kanal dosyaya yazıldı.")
