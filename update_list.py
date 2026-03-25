import streamlink
import os

def main():
    # Kanal Listen (Buraya istediğin kadar ekleme yapabilirsin)
    channels = [
        { "slug": "trt1", "name": "TRT 1", "url": "https://www.trtizle.com/canli/tv/trt-1" },
        { "slug": "showtv", "name": "Show TV", "url": "https://www.showtv.com.tr/canli-yayin" },
        { "slug": "tv8", "name": "TV8", "url": "https://www.tv8.com.tr/canli-yayin" },
        { "slug": "atv", "name": "ATV", "url": "https://www.atv.com.tr/canli-yayin" },
        { "slug": "kanald", "name": "Kanal D", "url": "https://www.kanald.com.tr/canli-yayin" },
        { "slug": "star", "name": "Star TV", "url": "https://www.startv.com.tr/canli-yayin" }
    ]

    os.makedirs("streams/best", exist_ok=True)
    
    # Ana liste içeriği (Başlangıç)
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
                
                # 1. Her kanalın kendi m3u8 dosyasını oluştur (Yedek olarak)
                with open(f"streams/best/{slug}.m3u8", "w") as f:
                    f.write(f"#EXTM3U\n#EXTINF:-1,{name}\n{best_url}")
                
                # 2. Ana listeye bu kanalı ekle
                logo = f"https://raw.githubusercontent.com/batuhansabri55/AkcagozTV_Canli/main/logos/logos/{slug}.png"
                m3u_content += f'#EXTINF:-1 tvg-id="{slug}" tvg-logo="{logo}",{name}\n{best_url}\n'
                
                print(f"✅ {name} eklendi.")
            else:
                print(f"⚠️ {name} bulunamadı.")
        except Exception as e:
            print(f"❌ {name} hatası: {e}")

    # 3. Tüm kanalları içeren ana dosyayı kaydet
    with open("canli.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("\n🚀 Ana liste 'canli.m3u' başarıyla oluşturuldu!")

if __name__ == "__main__":
    main()
