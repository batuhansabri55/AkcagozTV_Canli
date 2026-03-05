import requests
import re
import time

def get_blogtv_links():
    print("🚀 BlogTV Taraması Başladı...")
    blog_m3u = ""
    ana_url = "https://www.blogtv.net.tr/p/turkiyenin-en-kapsaml-ulusal-kanallar.html"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        r = requests.get(ana_url, headers=headers, timeout=20)
        # Sitedeki kanal sayfalarını bul (Örn: kanal=NOW TV TR)
        links = re.findall(r'href=[\"\'](https://www\.blogtv\.net\.tr/p/.*?\.html\?kanal=.*?)[\"\']', r.text)
        
        for link in list(set(links))[:20]: # Test için ilk 20 kanal
            try:
                kanal_adi = link.split("kanal=")[1].replace("%20", " ").replace("+", " ").strip()
                res = requests.get(link, headers=headers, timeout=15)
                
                # m3u8 linkini en yalın haliyle ara
                m3u8_find = re.search(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', res.text)
                
                if m3u8_find:
                    final_link = m3u8_find.group(1).replace("\\/", "/")
                    blog_m3u += f"#EXTINF:-1,{kanal_adi}\n{final_link}\n"
                    print(f"✅ Bulundu: {kanal_adi}")
                
                time.sleep(1) # Siteyi yormadan ilerle
            except: continue
    except Exception as e:
        print(f"❌ Hata: {e}")
    return blog_m3u

def main():
    final_content = "#EXTM3U\n"
    # Önce genel bir kaynak ekleyelim ki liste asla boş kalmasın
    try:
        r_genel = requests.get("https://iptv-org.github.io/iptv/countries/tr.m3u", timeout=10)
        final_content += "\n".join(r_genel.text.split("\n")[1:]) + "\n"
    except: pass

    # BlogTV'den gelenleri üzerine ekle
    final_content += get_blogtv_links()

    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(final_content)
    print("✔️ tr.m3u başarıyla güncellendi!")

if __name__ == "__main__":
    main()
