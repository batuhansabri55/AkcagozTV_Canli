import requests
import re
import time

def get_links():
    print("🚀 Tarama başlatılıyor: BlogTV...")
    m3u_header = "#EXTM3U\n"
    # Hedef site
    target_url = "https://www.blogtv.net.tr/p/turkiyenin-en-kapsaml-ulusal-kanallar.html"
    
    # Gerçek kullanıcı gibi görünmek için detaylı headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Referer': 'https://www.google.com/',
        'Accept-Language': 'tr,en-US;q=0.7,en;q=0.3'
    }

    try:
        # 1. Ana sayfayı çek
        response = requests.get(target_url, headers=headers, timeout=30)
        
        # Regex'i süper esnek yaptık: tırnak olsun olmasın, ne varsa yakalar
        # Örnek: https://www.blogtv.net.tr/p/atv-izle.html?kanal=ATV
        pattern = r'https://www\.blogtv\.net\.tr/p/[^"\'>\s]+\.html\?kanal=[^"\'>\s]+'
        found_links = re.findall(pattern, response.text)
        found_links = list(dict.fromkeys(found_links)) # Tekrarları sıralı sil
        
        print(f"📡 {len(found_links)} adet potansiyel kanal bulundu.")

        m3u_body = ""
        count = 0

        for link in found_links[:45]: # İlk 45 kanalı işle
            try:
                # Kanal adını temizle
                name = link.split("kanal=")[-1].replace("%20", " ").replace("+", " ").upper()
                
                # Kanal sayfasına gir
                ch_res = requests.get(link, headers=headers, timeout=15)
                
                # Sayfa içindeki .m3u8 linkini her türlü bulur
                m3u8_match = re.search(r'["\']?(https?://[^"\'>\s]+?\.m3u8[^"\'>\s]*?)["\']?', ch_res.text)
                
                if m3u8_match:
                    final_url = m3u8_match.group(1).replace("\\/", "/")
                    m3u_body += f"#EXTINF:-1, {name}\n{final_url}\n"
                    print(f"✅ Eklendi: {name}")
                    count += 1
                
                time.sleep(0.5) # Ban yememek için minik mola
            except:
                continue
        
        return m3u_header + m3u_body, count

    except Exception as e:
        print(f"❌ Kritik Hata: {e}")
        return m3u_header, 0

if __name__ == "__main__":
    content, total = get_links()
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(content)
    
    import os
    size = os.path.getsize("tr.m3u")
    print(f"🏁 Bitti. Toplam {total} kanal. Dosya boyutu: {size} byte.")
