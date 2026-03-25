import streamlink
import os
import requests

def main():
    # 1. ULUSAL KANALLAR (Özel Ayarlı)
    priority_channels = [
        { "slug": "trt1", "name": "TRT 1", "url": "https://www.trtizle.com/canli/tv/trt-1" },
        { "slug": "showtv", "name": "Show TV", "url": "https://www.showtv.com.tr/canli-yayin" },
        { "slug": "tv8", "name": "TV8", "url": "https://www.tv8.com.tr/canli-yayin" },
        # Kanal D için en stabil direkt link
        { "slug": "kanald", "name": "Kanal D", "url": "https://dogus-live.daioncdn.net/kanald/kanald.m3u8", "direct": True },
        { "slug": "now-tv", "name": "NOW TV", "url": "https://www.nowtv.com.tr/canli-yayin" },
        { "slug": "atv", "name": "ATV", "url": "https://atv-live.daioncdn.net/atv/atv.m3u8", "direct": True },
        { "slug": "star", "name": "Star TV", "url": "https://dogus-live.daioncdn.net/startv/startv.m3u8", "direct": True }
    ]

    os.makedirs("streams/best", exist_ok=True)
    m3u_content = "#EXTM3U\n"
    session = streamlink.Streamlink()
    
    # Tarayıcı taklidini en üst seviyeye çıkarıyoruz
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    session.set_option("http-headers", f"User-Agent={ua}")

    print("--- Kanallar Hazırlanıyor ---")
    for ch in priority_channels:
        try:
            if ch.get("direct"):
                final_url = ch["url"]
            else:
                streams = session.streams(ch["url"])
                final_url = streams['best'].url if streams and 'best' in streams else None
            
            if final_url:
                logo = f"https://raw.githubusercontent.com/batuhansabri55/AkcagozTV_Canli/main/logos/logos/{ch['slug']}.png"
                # TiviMate'e bu linkin Kanal D sitesinden geliyormuş gibi davranmasını söylüyoruz
                m3u_content += f'#EXTINF:-1 tvg-id="{ch["slug"]}" tvg-logo="{logo}" group-title="ULUSAL", {ch["name"]}\n'
                # Kanal D için kritik 'Referer' eklemesi
                if ch["slug"] == "kanald":
                    m3u_content += f'{final_url}|User-Agent={ua}&Referer=https://www.kanald.com.tr/\n'
                else:
                    m3u_content += f'{final_url}|User-Agent={ua}\n'
                print(f"✅ {ch['name']} hazır.")
        except: pass

    # 400+ Kanal Havuzu (Alt kısma eklenir)
    sources = ["https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr.m3u"]
    for src in sources:
        try:
            r = requests.get(src, timeout=10)
            if r.status_code == 200:
                m3u_content += "\n".join(r.text.splitlines()[1:]) + "\n"
        except: pass

    with open("canli.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("\n🚀 Kanal D zırhlı link eklendi! Actions'ı çalıştır.")

if __name__ == "__main__":
    main()
