import streamlink
import os
import requests

def main():
    # 1. ÖNCELİKLİ ULUSAL KANALLAR
    # Bazıları otomatik çekilecek, bazıları en sağlam yedek linklerle gelecek
    priority_channels = [
        { "slug": "trt1", "name": "TRT 1", "url": "https://www.trtizle.com/canli/tv/trt-1" },
        { "slug": "showtv", "name": "Show TV", "url": "https://www.showtv.com.tr/canli-yayin" },
        { "slug": "tv8", "name": "TV8", "url": "https://www.tv8.com.tr/canli-yayin" },
        { "slug": "kanald", "name": "Kanal D", "url": "https://www.kanald.com.tr/canli-yayin" },
        { "slug": "now-tv", "name": "NOW TV", "url": "https://www.nowtv.com.tr/canli-yayin" },
        # ATV ve Star için en güncel yedek (CDN) linkleri
        { "slug": "atv", "name": "ATV", "url": "https://atv-live.daioncdn.net/atv/atv.m3u8", "direct": True },
        { "slug": "star", "name": "Star TV", "url": "https://dogus-live.daioncdn.net/startv/startv.m3u8", "direct": True },
        { "slug": "a-haber", "name": "A Haber", "url": "https://ahaber-live.daioncdn.net/ahaber/ahaber.m3u8", "direct": True }
    ]

    os.makedirs("streams/best", exist_ok=True)
    m3u_content = "#EXTM3U\n"
    session = streamlink.Streamlink()
    # TiviMate ile tam uyum için standart User-Agent
    session.set_option("http-headers", "User-Agent=Mozilla/5.0")

    print("--- Ulusal Kanallar Taranıyor ---")
    for ch in priority_channels:
        try:
            if ch.get("direct"):
                final_url = ch["url"]
            else:
                streams = session.streams(ch["url"])
                final_url = streams['best'].url if streams and 'best' in streams else None
            
            if final_url:
                logo = f"https://raw.githubusercontent.com/batuhansabri55/AkcagozTV_Canli/main/logos/logos/{ch['slug']}.png"
                m3u_content += f'#EXTINF:-1 tvg-id="{ch["slug"]}" tvg-logo="{logo}" group-title="ULUSAL KANALLAR",{ch["name"]}\n{final_url}\n'
                print(f"✅ {ch['name']} hazır.")
        except:
            print(f"❌ {ch['name']} çekilemedi.")

    print("\n--- 400+ Kanal Havuzu Ekleniyor ---")
    external_sources = [
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr.m3u",
        "https://raw.githubusercontent.com/Free-TV/IPTV/master/playlist/turkey.m3u"
    ]

    for src in external_sources:
        try:
            r = requests.get(src, timeout=10)
            if r.status_code == 200:
                lines = r.text.splitlines()
                m3u_content += "\n".join(lines[1:]) + "\n"
                print(f"✅ Kaynak eklendi: {src}")
        except: pass

    with open("canli.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("\n🚀 Liste güncellendi. TiviMate'i yenile usta!")

if __name__ == "__main__":
    main()
