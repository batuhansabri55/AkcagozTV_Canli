import requests
import re
import time
import random

def get_links():
    print("🚀 Tarama başlatıldı...")
    m3u_content = "#EXTM3U\n"
    target_url = "https://www.blogtv.net.tr/p/turkiyenin-en-kapsaml-ulusal-kanallar.html"
    
    # Siteyi kandırmak için daha detaylı browser bilgileri
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'tr,en-US;q=0.7,en;q=0.3',
        'Referer': 'https://www.google.com/', # Google'dan geliyormuş gibi yapalım
        'Connection': 'keep-alive',
    }

    try:
        session = requests.Session() # Session kullanarak çerezleri tutalım
        response = session.get(target_url, headers=headers, timeout=30)
        
        # Sitedeki TÜM blogtv linklerini yakala (ne olur ne olmaz)
        links = re.findall(r'https?://www\.blogtv\.net\.tr/p/[^"\'>\s]+', response.text)
        # Sadece içinde "kanal=" olanları süz
        channel_links = [l for l in links if "kanal=" in l]
        channel_links = list(set(channel_links)) # Tekrarları sil

        print(f"📡 Toplam {len(channel_links)} kanal linki yakalandı.")

        if not channel_links:
            print("❗ Uyarı: Hiç link bulunamadı. Kaynak kodunu bir loglayalım:")
            print(response.text[:500]) # Hata analizi için ilk 500 karakteri yazdır

        for link in channel_links[:45]:
            try:
                # İsmi linkten çıkar
                name = link.split("kanal=")[-1].replace("-", " ").replace("_", " ").upper()
                
                # Kanal sayfasına git
                res = session.get(link, headers=headers, timeout=15)
                
                # En geniş m3u8 arama deseni
                m3u8 = re.search(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*?)', res.text)
                
                if m3u8:
                    stream_url = m3u8.group(1).replace("\\/", "/")
                    m3u_content += f"#EXTINF:-1, {name}\n{stream_url}\n"
                    print(f"✅ Eklendi: {name}")
                
                time.sleep(random.uniform(0.5, 1.5)) # Rastgele bekleme (bot koruması için)
            except:
                continue

    except Exception as e:
        print(f"💥 Ana hata: {e}")
    
    return m3u_content

if __name__ == "__main__":
    result = get_links()
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(result)
    print("🏁 Bitti. tr.m3u güncellendi.")
