import streamlink
import os

def main():
    # Güncellenmiş Kanal Listesi
    channels = [
        { "slug": "trt1", "url": "https://www.trtizle.com/canli/tv/trt-1" },
        { "slug": "showtv", "url": "https://www.showtv.com.tr/canli-yayin" },
        { "slug": "tv8", "url": "https://www.tv8.com.tr/canli-yayin" }, # TV8 eklendi
        { "slug": "atv", "url": "https://www.atv.com.tr/canli-yayin" },
        { "slug": "kanald", "url": "https://www.kanald.com.tr/canli-yayin" },
        { "slug": "star", "url": "https://www.startv.com.tr/canli-yayin" }
    ]

    # Klasörü hazırla
    os.makedirs("streams/best", exist_ok=True)

    print(f"--- {len(channels)} Kanal İşleniyor ---")

    for channel in channels:
        slug = channel["slug"]
        url = channel["url"]
        try:
            # Streamlink ile en iyi kaliteyi yakala
            streams = streamlink.streams(url)
            if streams and 'best' in streams:
                best_url = streams['best'].url
                
                # Her kanal için ayrı m3u8 oluştur
                with open(f"streams/best/{slug}.m3u8", "w") as f:
                    f.write(f"#EXTM3U\n#EXTINF:-1,{slug}\n{best_url}")
                print(f"✅ {slug} güncellendi.")
            else:
                print(f"⚠️ {slug} için yayın bulunamadı.")
        except Exception as e:
            print(f"❌ {slug} Hatası: {str(e)}")

if __name__ == "__main__":
    main()
