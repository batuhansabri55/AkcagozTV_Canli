import requests
import re
import time

# Taramak istediğin diğer sabit kaynaklar
SOURCES = [
    "https://iptv-org.github.io/iptv/countries/tr.m3u"
]

def get_blogtv_links():
    print("🚀 BlogTV kanalları taranıyor...")
    blog_m3u = ""
    ana_url = "https://www.blogtv.net.tr/p/turkiyenin-en-kapsaml-ulusal-kanallar.html"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        r = requests.get(ana_url, headers=headers, timeout=15)
        # Sitedeki kanal sayfalarının linklerini bulur
        links = re.findall(r'href="(https://www\.blogtv\.net\.tr/p/.*?\.html\?kanal=.*?)"', r.text)
        
        for link in set(links):
            try:
                kanal_adi = link.split("kanal=")[1].replace("%20", " ").replace("+", " ")
                print(f"🔍 Kanal aranıyor: {kanal_adi}")
                
                res = requests.get(link, headers=headers, timeout=10)
                m3u8_match = re.search(r'(https?://.*?\.m3u8.*?)"', res.text)
                
                if m3u8_match:
                    blog_m3u += f"#EXTINF:-1,{kanal_adi}\n{m3u8_match.group(1)}\n"
                    print(f"✅ Link bulundu: {kanal_adi}")
                
                time.sleep(1) # Site engellemesin diye bekleme
            except:
                continue
    except Exception as e:
        print(f"❌ BlogTV hatası: {e}")
    return blog_m3u

def main():
    final_m3u = "#EXTM3U\n"
    final_m3u += get_blogtv_links()

    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10)
            final_m3u += "\n" + "\n".join(r.text.split('\n')[1:])
        except:
            continue

    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(final_m3u)
    print("✔️ tr.m3u dosyası başarıyla güncellendi!")

if __name__ == "__main__":
    main()
