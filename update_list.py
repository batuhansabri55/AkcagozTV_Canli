import requests
import re
import time

def get_blogtv_links():
    print("🚀 Sadece BlogTV kanalları toplanıyor...")
    blog_m3u = ""
    ana_url = "https://www.blogtv.net.tr/p/turkiyenin-en-kapsaml-ulusal-kanallar.html"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        r = requests.get(ana_url, headers=headers, timeout=20)
        # Sadece ana kanalları yakala (Listeyi şişirmemek için)
        links = re.findall(r'href=[\"\'](https://www\.blogtv\.net\.tr/p/.*?\.html\?kanal=.*?)[\"\']', r.text)
        
        for link in list(set(links))[:30]: # En önemli ilk 30 kanalı al
            try:
                kanal_adi = link.split("kanal=")[1].replace("%20", " ").replace("+", " ").strip()
                res = requests.get(link, headers=headers, timeout=15)
                m3u8_find = re.search(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', res.text)
                
                if m3u8_find:
                    final_link = m3u8_find.group(1).replace("\\/", "/")
                    blog_m3u += f"#EXTINF:-1,{kanal_adi}\n{final_link}\n"
                    print(f"✅ Eklendi: {kanal_adi}")
                time.sleep(1)
            except: continue
    except Exception as e:
        print(f"❌ Hata: {e}")
    return blog_m3u

def main():
    # Sadece BlogTV'den gelen taze ve az sayıdaki linki dosyaya yazıyoruz
    final_content = "#EXTM3U\n"
    final_content += get_blogtv_links()

    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(final_content)
    print("✔️ tr.m3u hafifletildi ve güncellendi!")

if __name__ == "__main__":
    main()
