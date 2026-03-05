import requests
import re
import time

def get_blogtv_links():
    print("🚀 BlogTV taranıyor...")
    blog_m3u = ""
    ana_url = "https://www.blogtv.net.tr/p/turkiyenin-en-kapsaml-ulusal-kanallar.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        r = requests.get(ana_url, headers=headers, timeout=20)
        # Linkleri bulma kısmını daha esnek yaptık
        links = re.findall(r'href="(https://www\.blogtv\.net\.tr/p/[^"]+?\.html\?kanal=[^"]+?)"', r.text)
        
        for link in list(set(links)):
            try:
                # Kanal adını çek ve temizle
                kanal_adi = link.split("kanal=")[1].replace("%20", " ").replace("+", " ").strip()
                print(f"🔍 Kanal bulunuyor: {kanal_adi}")
                
                res = requests.get(link, headers=headers, timeout=15)
                # m3u8 linkini bulmak için daha güçlü bir arama
                m3u8_match = re.search(r'["\'](https?://[^"\']+?\.m3u8[^"\']*?)["\']', res.text)
                
                if m3u8_match:
                    ts_link = m3u8_match.group(1).replace("\\/", "/")
                    blog_m3u += f"#EXTINF:-1,{kanal_adi}\n{ts_link}\n"
                    print(f"✅ Link eklendi: {kanal_adi}")
                
                time.sleep(1) 
            except: continue
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")
    return blog_m3u

def main():
    final_m3u = "#EXTM3U\n"
    blog_data = get_blogtv_links()
    
    if len(blog_data) < 10:
        print("⚠️ Uyarı: Çok az link bulundu, liste boş olabilir!")
    
    final_m3u += blog_data
    
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(final_m3u)
    print("✔️ İşlem bitti.")

if __name__ == "__main__":
    main()
