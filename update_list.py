import requests
import re
import time
import random

def get_links():
    print("🚀 Tarama başlatıldı: BlogTV üzerinden güncel liste çekiliyor...")
    m3u_header = "#EXTM3U\n"
    target_url = "https://www.blogtv.net.tr/p/turkiyenin-en-kapsaml-ulusal-kanallar.html"
    
    # Sitenin bot korumasını aşmak için gerçekçi bir tarayıcı profili
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://www.google.com/',
        'Origin': 'https://www.blogtv.net.tr',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    try:
        # Session kullanarak çerezleri ve bağlantıyı canlı tutalım
        session = requests.Session()
        response = session.get(target_url, headers=headers, timeout=30)
        
        # Regex: Tırnak işaretlerine bakmadan tüm kanal linklerini yakalar
        # Örnek: https://www.blogtv.net.tr/p/show-tv-izle.html?kanal=SHOW_TV
        pattern = r'https://www\.blogtv\.net\.tr/p/[^"\'>\s]+\.html\?kanal=[^"\'>\s]+'
        found_links = list(set(re.findall(pattern, response.text)))
        
        print(f"📡 Sitede {len(found_links)} adet kanal linki tespit edildi.")

        if not found_links:
            print("⚠️ KRİTİK: Hiç link bulunamadı! Site GitHub'ı tamamen bloklamış olabilir.")
            return m3u_header, 0

        m3u_body = ""
        success_count = 0

        for link in found_links[:40]: # İlk 40 kanalı tara
            try:
                # Kanal adını temizle ve güzelleştir
                raw_name = link.split("kanal=")[-1]
                name = raw_name.replace("%20", " ").replace("+", " ").replace("_", " ").upper()
                
                # Kanalın kendi sayfasına git
                ch_res = session.get(link, headers=headers, timeout=15)
                
                # Sayfa içindeki .m3u8 linkini her türlü yakalayan esnek arama
                m3u8_match = re.search(r'["\']?(https?://[^"\'>\s]+?\.m3u8[^"\'>\s]*?)["\']?', ch_res.text)
                
                if m3u8_match:
                    stream_url = m3u8_match.group(1).replace("\\/", "/")
                    m3u_body += f"#EXTINF:-1, {name}\n{stream_url}\n"
                    print(f"✅ Eklendi: {name}")
                    success_count += 1
                
                # Siteyi şüphelendirmemek için rastgele kısa beklemeler
                time.sleep(random.uniform(0.3, 0.8))
            except:
                continue
        
        return m3u_header + m3u_body, success_count

    except Exception as e:
        print(f"❌ Bir hata oluştu: {e}")
        return m3u_header, 0

if __name__ == "__main__":
    final_m3u, total = get_links()
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(final_m3u)
    
    import os
    file_size = os.path.getsize("tr.m3u")
    print(f"🏁 İşlem Bitti. Toplam: {total} kanal. Dosya Boyutu: {file_size} byte.")
