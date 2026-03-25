import streamlink
import os

def main():
    # 1. Otomatik çekilecek kanallar
    auto_channels = [
        { "slug": "trt1", "name": "TRT 1", "url": "https://www.trtizle.com/canli/tv/trt-1" },
        { "slug": "showtv", "name": "Show TV", "url": "https://www.showtv.com.tr/canli-yayin" },
        { "slug": "tv8", "name": "TV8", "url": "https://www.tv8.com.tr/canli-yayin" },
        { "slug": "kanald", "name": "Kanal D", "url": "https://www.kanald.com.tr/canli-yayin" },
        { "slug": "now-tv", "name": "NOW TV", "url": "https://www.nowtv.com.tr/canli-yayin" },
        { "slug": "teve2", "name": "Teve2", "url": "https://www.teve2.com.tr/canli-yayin" }
    ]

    # 2. İnatçı kanallar için sabit yedek linkler (Seni kırmayacak olanlar)
    manual_channels = [
        { "slug": "atv", "name": "ATV", "m3u8": "https://turkuvaz-live.daioncdn.net/atv/atv.m3u8" },
        { "slug": "a-haber", "name": "A Haber", "m3u8": "https://turkuvaz-live.daioncdn.net/ahaber/ahaber.m3u8" },
        { "slug": "star", "name": "Star TV", "m3u8": "https://dogus-live.daioncdn.net/startv/startv.m3u8" }
    ]

    os.makedirs("streams/best", exist_ok=True)
    m3u_content = "#EXTM3U\n"
    session = streamlink.Streamlink()
    session.set_option("http-headers", "User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    print("--- Kanallar Hazırlanıyor ---")

    # Manuel kanalları listeye ekle
    for ch in manual_channels:
        logo = f"https://raw.githubusercontent.com/batuhansabri55/AkcagozTV_Canli/main/logos/logos/{ch['slug']}.png"
        m3u_content += f'#EXTINF:-1 tvg-id="{ch["slug"]}" tvg-logo="{logo}" group-title="ULUSAL",{ch["name"]}\n{ch["m3u8"]}\n'
        print(f"✅ {ch['name']} (Yedek Link) eklendi.")

    # Otomatik kanalları tara
    for ch in auto_channels:
        try:
            streams = session.streams(ch["url"])
            if streams and 'best' in streams:
                best_url = streams['best'].url
                logo = f"https://raw.githubusercontent.com/batuhansabri55/AkcagozTV_Canli/main/logos/logos/{ch['slug']}.png"
                m3u_content += f'#EXTINF:-1 tvg-id="{ch["slug"]}" tvg-logo="{logo}" group-title="ULUSAL",{ch["name"]}\n{best_url}\n'
                print(f"✅ {ch['name']} eklendi.")
        except:
            print(f"❌ {ch['name']} alınamadı.")

    with open("canli.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("\n🚀 Liste Tamamlandı!")

if __name__ == "__main__":
    main()
