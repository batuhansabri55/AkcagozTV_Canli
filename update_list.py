import streamlink
import os

def main():
    channels = [
        { "slug": "trt1", "name": "TRT 1", "url": "https://www.trtizle.com/canli/tv/trt-1" },
        { "slug": "showtv", "name": "Show TV", "url": "https://www.showtv.com.tr/canli-yayin" },
        { "slug": "tv8", "name": "TV8", "url": "https://www.tv8.com.tr/canli-yayin" },
        { "slug": "atv", "name": "ATV", "url": "https://www.atv.com.tr/canli-yayin" }, # İnatçı kanal 1
        { "slug": "a-haber", "name": "A Haber", "url": "https://www.ahaber.com.tr/video/canli-yayin" }, # İnatçı kanal 2
        { "slug": "kanald", "name": "Kanal D", "url": "https://www.kanald.com.tr/canli-yayin" },
        { "slug": "now-tv", "name": "NOW TV", "url": "https://www.nowtv.com.tr/canli-yayin" },
        { "slug": "star", "name": "Star TV", "url": "https://www.startv.com.tr/canli-yayin" },
        { "slug": "teve2", "name": "Teve2", "url": "https://www.teve2.com.tr/canli-yayin" }
    ]

    os.makedirs("streams/best", exist_ok=True)
    m3u_content = "#EXTM3U\n"
    
    # Streamlink oturumunu ve ayarlarını güçlendiriyoruz
    session = streamlink.Streamlink()
    session.set_option("http-headers", "User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    session.set_option("hls-live-edge", 3)
    session.set_option("hls-segment-threads", 2)

    print(f"--- {len(channels)} Kanal Taranıyor ---")

    for channel in channels:
        slug, name, url = channel["slug"], channel["name"], channel["url"]
        try:
            # Streamlink ile en kaliteli yayını bulmayı dene
            streams = session.streams(url)
            if streams and 'best' in streams:
                best_url = streams['best'].url
                
                # Tekil dosya oluştur
                with open(f"streams/best/{slug}.m3u8", "w") as f:
                    f.write(f"#EXTM3U\n#EXTINF:-1,{name}\n{best_url}")
                
                # Ana listeye ekle
                logo = f"https://raw.githubusercontent.com/batuhansabri55/AkcagozTV_Canli/main/logos/logos/{slug}.png"
                m3u_content += f'#EXTINF:-1 tvg-id="{slug}" tvg-logo="{logo}" group-title="ULUSAL KANALLAR",{name}\n{best_url}\n'
                print(f"✅ {name} eklendi.")
            else:
                print(f"⚠️ {name} linki alınamadı, streamlink bu siteyi o an çözemedi.")
        except Exception as e:
            print(f"❌ {name} hatası: {str(e)[:100]}")

    with open("canli.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("\n🚀 Güncelleme bitti. TiviMate'te listeyi yenile!")

if __name__ == "__main__":
    main()
