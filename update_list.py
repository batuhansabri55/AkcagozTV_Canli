import requests
import re
import time

def get_blogtv_links():
    print("🚀 BlogTV kanalları toplanıyor...")
    blog_m3u = "#EXTM3U\n"
    ana_url = "https://www.blogtv.net.tr/p/turkiyenin-en-kapsaml-ulusal-kanallar.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.blogtv.net.tr/"
    }

    try:
        r = requests.get(ana_url, headers=headers, timeout=20)
        r.raise_for_status()
        
        # Regex'i daha esnek hale getirdik:
        links = re.findall(r'https://www\.blogtv\.net\.tr/p/[^"\']+\.html\?kanal=[^"\']+', r.text)
        links = list(set(links)) # Tekrar edenleri temizle
        
        print(f"✅ {len(links)} adet kanal linki bulundu.")

        for link in links[:40]: # İlk 40 kanalı dene
            try:
                # Kanal adını linkten çek ve temizle
                kanal_adi = link.split("kanal=")[-1].replace("%20", " ").replace("+", " ").strip().upper()
                
                res = requests.get(link, headers=headers, timeout=15)
                # m3u8 yakalama kısmını güçlendirdik
                m3u8_find = re.search(r'(https?://[^\s\'">]+\.m3u8[^\s\'">]*)', res.text)
                
                if m3u8_find:
                    final_link = m3u8_find.group(1).replace("\\/", "/")
                    blog_m3u += f"#EXTINF:-1, {kanal_adi}\n{final_link}\n"
                    print(f"➕ Eklendi: {kanal_adi}")
                
                time.sleep(1) # Siteyi yormamak ve ban yememek için
            except Exception as e:
                print(f"⚠️ Kanal hatası ({link}): {e}")
                continue

    except Exception as e:
        print(f"❌ Ana sayfa hatası: {e}")
    
    return blog_m3u

# Ana çalıştırma kısmı
if __name__ == "__main__":
    liste_icerigi = get_blogtv_links()
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(liste_icerigi)
    print("✨ İşlem tamamlandı, tr.m3u güncellendi.")
