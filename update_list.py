import requests
import re
import time

def get_blogtv_links():
    print("🚀 BlogTV taranıyor...")
    blog_m3u = ""
    ana_url = "https://www.blogtv.net.tr/p/turkiyenin-en-kapsaml-ulusal-kanallar.html"
    # Daha gerçekçi bir tarayıcı kimliği
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.google.com/"
    }
    
    try:
        session = requests.Session()
        r = session.get(ana_url, headers=headers, timeout=20)
        links = re.findall(r'href="(https://www\.blogtv\.net\.tr/p/.*?\.html\?kanal=.*?)"', r.text)
        
        for link in list(set(links))[:15]: # İlk etapta test için 15 kanal
            try:
                kanal_adi = link.split("kanal=")[1].replace("%20", " ").replace("+", " ")
                print(f"🔍 Kanal: {kanal_adi}")
                
                res = session.get(link, headers=headers, timeout=15)
                # m3u8 linkini daha geniş bir aramayla bul
                m3u8_match = re.search(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', res.text)
                
                if m3u8_match:
                    link_url = m3u8_match.group(1).replace("\\", "")
                    blog_m3u += f"#EXTINF:-1,{kanal_adi}\n{link_url}\n"
                    print(f"✅ Başarılı")
                
                time.sleep(2) # Engellenmemek için bekleme süresini artırdık
            except: continue
    except Exception as e:
        print(f"❌ Hata: {e}")
    return blog_m3u

def main():
    final_m3u = "#EXTM3U\n"
    final_m3u += get_blogtv_links()
    
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(final_m3u)
    print("✔️ tr.m3u güncellendi!")

if __name__ == "__main__":
    main()
