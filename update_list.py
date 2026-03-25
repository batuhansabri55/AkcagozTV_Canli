import streamlink
import os

def main():
    # 2 Kanallı Test Listesi
    channels = [
        { "slug": "trt1", "url": "https://www.trtizle.com/canli/tv/trt-1" },
        { "slug": "showtv", "url": "https://www.showtv.com.tr/canli-yayin" }
    ]

    # Klasör oluştur
    os.makedirs("streams/best", exist_ok=True)

    for channel in channels:
        slug = channel["slug"]
        url = channel["url"]
        try:
            streams = streamlink.streams(url)
            if streams and 'best' in streams:
                best_url = streams['best'].url
                with open(f"streams/best/{slug}.m3u8", "w") as f:
                    f.write(f"#EXTM3U\n#EXTINF:-1,{slug}\n{best_url}")
                print(f"✅ {slug} Hazır!")
        except Exception as e:
            print(f"❌ {slug} Hatası: {e}")

if __name__ == "__main__":
    main()
