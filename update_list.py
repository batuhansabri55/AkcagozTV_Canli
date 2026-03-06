import requests

def worker_verisini_kurtar():
    # Senin Worker dashboard'unda M3U üreten asıl link
    url = "https://giniko.smartiptvworld.workers.dev/liste.m3u"
    
    print(f"📡 Worker'dan liste çekiliyor: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36'
    }

    try:
        # Worker'a doğrudan istek atıyoruz
        r = requests.get(url, headers=headers, timeout=30)
        
        # Eğer Worker içeriği M3U olarak veriyorsa alıyoruz
        if "#EXTM3U" in r.text:
            kanal_sayisi = r.text.count("#EXTINF")
            print(f"✅ Başarılı! {kanal_sayisi} kanal yakalandı.")
            return r.text
        else:
            print("⚠️ Worker M3U formatında veri göndermedi.")
            return "#EXTM3U\n# Veri formatı hatalı."
            
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        return "#EXTM3U\n"

if __name__ == "__main__":
    content = worker_verisini_kurtar()
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(content)
