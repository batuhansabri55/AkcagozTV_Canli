import requests

def get_giniko_m3u():
    print("🚀 Giniko veri havuzuna sızılıyor...")
    # Giniko'nun asıl veri sağlayan ham ucu
    url = "https://giniko.smartiptvworld.workers.dev/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36'
    }

    try:
        # Siteye doğrudan istek atıyoruz
        r = requests.get(url, headers=headers, timeout=30)
        
        # Eğer site bize M3U formatında veri gönderirse doğrudan al
        if "#EXTM3U" in r.text:
            print("✅ M3U Listesi başarıyla yakalandı!")
            return r.text
        else:
            print("⚠️ Sayfa içeriği M3U değil, ham veri işlenemedi.")
            return "#EXTM3U\n# Veri çekilemedi."
            
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        return "#EXTM3U\n"

if __name__ == "__main__":
    content = get_giniko_m3u()
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(content)
    print("🏁 tr.m3u dosyası güncellendi. Actions bitince kontrol et!")
