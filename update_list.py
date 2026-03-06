import requests
import os

# Online yedek kaynaklar
YEDEK_KAYNAKLAR = [
    "https://raw.githubusercontent.com/sultansmgr/smart/refs/heads/main/viziTV.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://streams.uzunmuhalefet.com/lists/tr.m3u"
]

def update_m3u():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    
    # 1. ADIM: Senin mevcut tr.m3u dosyanı oku (Manuel linklerini korumak için)
    manuel_icerik = ""
    if os.path.exists("tr.m3u"):
        with open("tr.m3u", "r", encoding="utf-8") as f:
            lines = f.readlines()
            # Sadece senin manuel eklediğin kısımları al (Örn: ilk 100 satır veya özel işaret arası)
            # Şimdilik dosyanın tamamını "temel" kabul ediyoruz:
            manuel_icerik = "".join(lines)
            if not manuel_icerik.startswith("#EXTM3U"):
                manuel_icerik = "#EXTM3U\n" + manuel_icerik
    else:
        manuel_icerik = "#EXTM3U\n"

    added_links = set()
    # Mevcut linkleri 'set'e ekle ki kopyası gelmesin
    for line in manuel_icerik.splitlines():
        if line.startswith("http"):
            added_links.add(line.strip())

    # 2. ADIM: Online yedekleri tara ve senin içeriğinin altına ekle
    online_yedekler = "\n# --- OTOMATIK BESLEME YEDEKLERI --- #\n"
    
    for url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code == 200:
                lines = r.text.splitlines()
                current_info = ""
                for line in lines:
                    line = line.strip()
                    if line.startswith("#EXTINF"):
                        current_info = line
                    elif line.startswith("http") and current_info:
                        if line not in added_links:
                            online_yedekler += f"{current_info}\n{line}\n"
                            added_links.add(line)
                        current_info = ""
        except: continue

    # 3. ADIM: Manuel + Online birleştir ve tek dosya yap
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(manuel_icerik.strip() + "\n" + online_yedekler)
    
    print("✅ Manuel linklerin korundu ve yedekler altına eklendi!")

if __name__ == "__main__":
    update_m3u()
