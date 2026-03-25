import streamlink
import os

def main():
    # ATV ve A Haber için YouTube linklerini, diğerleri için web linklerini koyduk
    channels = [
        { "slug": "trt1", "name": "TRT 1", "url": "https://www.trtizle.com/canli/tv/trt-1" },
        { "slug": "showtv", "name": "Show TV", "url": "https://www.showtv.com.tr/canli-yayin" },
        { "slug": "tv8", "name": "TV8", "url": "https://www.tv8.com.tr/canli-yayin" },
        { "slug": "atv", "name": "ATV", "url": "https://www.youtube.com/@atv/live" }, # YouTube'a çevirdik
        { "slug": "a-haber", "name": "A Haber", "url": "https://www.youtube.com/@ahaber/live" }, # YouTube'a çevirdik
        { "slug": "kanald", "name": "Kanal D", "url": "https://www.kanald.com.tr/canli-yayin" },
        { "slug": "now-tv", "name": "NOW TV", "url": "https://www.nowtv.com.tr/canli-yayin" },
        { "slug": "star", "name": "Star TV", "url": "https://www.startv.com.tr/canli-yayin" },
        { "slug": "teve2", "name": "Teve2", "url": "https://www.teve2.com.tr/canli-yayin" }
    ]

    os.makedirs("streams/best", exist_ok=True)
    m3u_content = "#EXTM3U\n"
    
    session = streamlink.Streamlink()
    # En güçlü tarayıcı taklidi
    session.set_option("http-headers", "User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    print(f"--- {len(channels)} Kanal İşleniyor ---")

    for channel in channels:
        slug, name, url = channel["slug"], channel["name"], channel["url"]
        try:
            streams = session.streams(url)
            if streams and 'best' in streams:
                best_url = streams['best'].url
                
                # Tekil dosya
                with open(f"streams/best/{slug}.m3u8", "w") as f:
                    f.write(f"#EXTM3U\n#EXTINF:-1,{name}\n{best_url}")
                
                # Ana listeye ekle
                logo = f"https://raw.githubusercontent.com/batuhansabri55/AkcagozTV_Canli/main/logos/logos/{slug}.png"
                m3u_content += f'#EXTINF:-1 tvg-id="{slug}" tvg-logo="{logo}" group-title="ULUSAL",{name}\n{best_url}\n'
                print(f"✅ {name} eklendi.")
            else:
                print(f"⚠️ {name} link alınamadı.")
        except Exception as e:
            print(f"❌ {name} Hatası: {str(e)[:50]}")

    with open("canli.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("\n🚀 Liste güncellendi. YouTube takviyesi yapıldı!")

if __name__ == "__main__":
    main()
