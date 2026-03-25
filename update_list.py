import streamlink
import os
import json

def main():
    # Kanal Listen (Gelecekte burayı config.json'dan okutabiliriz)
    channels = [
        { "slug": "trt1", "url": "https://www.trtizle.com/canli/tv/trt-1" },
        { "slug": "showtv", "url": "https://www.showtv.com.tr/canli-yayin" }
    ]

    # Çıktı klasörlerini oluştur (Senin repoda 'streams' yoksa otomatik açar)
    output_dir = "streams/best"
    os.makedirs(output_dir, exist_ok=True)

    for channel in channels:
        slug = channel["slug"]
        url = channel["url"]
        
        try:
            streams = streamlink.streams(url)
            if streams and 'best' in streams:
                best_url = streams['best'].url
                
                # Her kanal için ayrı bir m3u8 dosyası oluşturuyoruz
                file_path = os.path.join(output_dir, f"{slug}.m3u8")
                with open(file_path, "w") as f:
                    # TiviMate ve diğerleri için standart format
                    f.write(f"#EXTM3U\n#EXTINF:-1 tvg-id=\"{slug}\" tvg-logo=\"https://raw.githubusercontent.com/batuhansabri55/AkcagozTV_Canli/main/logos/logos/{slug}.png\",{slug}\n{best_url}")
                
                print(f"✅ Güncellendi: {slug}")
        except Exception as e:
            print(f"❌ Hata ({slug}): {e}")

if __name__ == "__main__":
    main()
