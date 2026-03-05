import requests
import re
import time

def get_blogtv_links():
    print("🚀 BlogTV Canavar Bot Başlatıldı...")
    blog_m3u = ""
    ana_url = "https://www.blogtv.net.tr/p/turkiyenin-en-kapsaml-ulusal-kanallar.html"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3",
        "Referer": "https://www.google.com/"
    }

    try:
        session = requests.Session()
        r = session.get(ana_url, headers=headers, timeout=30)
        # Link yakalama sistemini daha basit ve geniş yaptık
        raw_links = re.findall(r'href=[\"\'](https://www\.blogtv\.net\.tr/p/.*?\.html\?kanal=.*?)[\"\']', r.text)
        
        unique_links = list(set(raw_links))
        print(f"📡 Toplam {len(unique_links)} kanal adayı bulundu. Taranıyor...")

        for link in unique_links[:40]: # İlk 40 kanalı tara
            try:
                kanal_adi = link.split("kanal=")[1].replace("%20", " ").replace("+", " ").strip()
                res = session.get(link, headers=headers, timeout=15)
                
                # m3u8 linklerini bulmak için 3 farklı taktik deniyoruz
                m3u8_match = re.search(r'[\"\'](https?://.*?\.m3u8.*?)[\"\']', res.text)
                if not m3u8_match:
                    m3u8_match = re.search(r'source:\s*[\"\'](https?://.*?\.m3u8.*?)[\"\']', res.text)
                
                if m3u8_match:
                    found_url = m3u8_match.group(1).replace("\\/", "/")
                    blog_m3u += f"#EXTINF:-1,{kanal_adi}\n{found_url}\n"
                    print(f"✅ Başarılı: {kanal_adi}")
                
                time.sleep(1.5) # Site kovmasın diye biraz yavaş git
            except: continue
            
    except Exception as e:
        print(f"❌ Ana hata: {e}")
    
    return blog_m3u

def main():
    final_m3u = "#EXTM3U\n"
    # Diğer hazır listeni de buraya ekliyoruz (iptv-org gibi)
    try:
        r_other = requests.get("https://iptv-org.github.io/iptv/countries/tr.m3u", timeout=15)
        if r_other.status_code == 200:
            final_m3u += "\n".join(r_other.text.split("\n")[1:]) + "\n"
    except: pass

    # BlogTV verilerini ekle
    final_m3u += get_blogtv_links()

    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(final_m3u)
    print("🚀 tr.m3u dosyası başarıyla dolduruldu!")

if __name__ == "__main__":
    main()
