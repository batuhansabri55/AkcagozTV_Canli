import requests
import re
import time

def get_blogtv_links():
    print("🚀 Kanallar toplanıyor...")
    blog_m3u = "#EXTM3U\n"
    ana_url = "https://www.blogtv.net.tr/p/turkiyenin-en-kapsaml-ulusal-kanallar.html"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://www.blogtv.net.tr/"
    }

    try:
        r = requests.get(ana_url, headers=headers, timeout=30)
        # Tırnak işaretlerine bakmaksızın tüm kanal linklerini yakalayan esnek regex
        links = re.findall(r'https://www\.blogtv\.net\.tr/p/[^"\'>\s]+\.html\?kanal=[^"\'>\s]+', r.text)
        links = list(set(links)) # Tekrarları temizle
        
        print(f"✅ {len(links)} adet kanal linki bulundu.")

        for link in links[:40]: 
            try:
                # Kanal adını linkten çek ve temizle
                kanal_adi = link.split("kanal=")[-1].replace("%20", " ").replace("+", " ").strip().upper()
                
                res = requests.get(link, headers=headers, timeout=15)
                # m3u8 yakalama: Hem tek hem çift tırnağı hem de kaçış karakterlerini destekler
                m3u8_find = re.search(r'["\']?(https?://[^"\'>\s]+?\.m3u8[^"\'>\s]*?)["\']?', res.text)
                
                if m3u8_find:
                    final_link = m3u8_find.group(1).replace("\\/", "/")
                    blog_m3u += f"#EXTINF:-1, {kanal_adi}\n{final_link}\n"
                    print(f"➕ Eklendi: {kanal_adi}")
                
                time.sleep(0.5) 
            except:
                continue

    except Exception as e:
        print(f"❌ Hata: {e}")
    
    return blog_m3u

if __name__ == "__main__":
    liste = get_blogtv_links()
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(liste)
    print("✨ İşlem tamamlandı.")
