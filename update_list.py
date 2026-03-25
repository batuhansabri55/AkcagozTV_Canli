import streamlink
import os

def main():
    # BURASI KANAL LİSTESİ - Buraya istediğin kadar ekleme yapabilirsin
    channels = [
        { "slug": "trt1", "name": "TRT 1", "url": "https://www.trtizle.com/canli/tv/trt-1" },
        { "slug": "trt-haber", "name": "TRT Haber", "url": "https://www.trtizle.com/canli/tv/trt-haber" },
        { "slug": "trt-spor", "name": "TRT Spor", "url": "https://www.trtizle.com/canli/tv/trt-spor" },
        { "slug": "trt-belgesel", "name": "TRT Belgesel", "url": "https://www.trtizle.com/canli/tv/trt-belgesel" },
        { "slug": "showtv", "name": "Show TV", "url": "https://www.showtv.com.tr/canli-yayin" },
        { "slug": "tv8", "name": "TV8", "url": "https://www.tv8.com.tr/canli-yayin" },
        { "slug": "tv8-5", "name": "TV8.5", "url": "https://www.tv8.com.tr/tv8-5-canli-yayin" },
        { "slug": "atv", "name": "ATV", "url": "https://www.atv.com.tr/canli-yayin" },
        { "slug": "a-haber", "name": "A Haber", "url": "https://www.ahaber.com.tr/video/canli-yayin" },
        { "slug": "kanald", "name": "Kanal D", "url": "https://www.kanald.com.tr/canli-yayin" },
        { "slug": "teve2", "name": "Teve2", "url": "https://www.teve2.com.tr/canli-yayin" },
        { "slug": "star", "name": "Star TV", "url": "https://www.startv.com.tr/canli-yayin" },
        { "slug": "now-tv", "name": "NOW TV", "url": "https://www.nowtv.com.tr/canli-yayin" },
        { "slug": "haberturk", "name": "Habertürk", "url": "https://www.haberturk.com/canli-yayin" },
        { "slug": "bloomberg-ht", "name": "Bloomberg HT", "url": "https://www.bloomberght.com/canli-yayin" },
        { "slug": "halk-tv", "name": "Halk TV", "url": "https://halktv.com.tr/canli-yayin" },
        { "slug": "sozcu-tv", "name": "Sözcü TV", "url": "https://www.szctv.com.tr/canli-yayin" }
    ]

    os.makedirs("streams/best", exist_ok=True)
    m3u_content = "#EXTM3U\n"

    print(f"--- {len(channels)} Kanal İşleniyor ---")

    for channel in channels:
        slug = channel["slug"]
        name = channel["name"]
        url = channel["url"]
        try:
            streams = streamlink.streams(url)
            if streams and 'best' in streams:
                best_url = streams['best'].url
                
                # Tekil dosya oluşturma
                with open(f"streams/best/{slug}.m3u8", "w") as f:
                    f.write(f"#EXTM3U\n#EXTINF:-1,{name}\n{best_url}")
                
                # Ana listeye ekleme
                logo = f"https://raw.githubusercontent.com/batuhansabri55/AkcagozTV_Canli/main/logos/logos/{slug}.png"
                m3u_content += f'#EXTINF:-1 tvg-id="{slug}" tvg-logo="{logo}",{name}\n{best_url}\n'
                print(f"✅ {name} eklendi.")
            else:
                print(f"⚠️ {name} bulunamadı.")
        except Exception as e:
            print(f"❌ {name} hatası: {e}")

    # canli.m3u dosyasını yaz
    with open("canli.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("\n🚀 İşlem tamam! 'canli.m3u' güncellendi.")

if __name__ == "__main__":
    main()
