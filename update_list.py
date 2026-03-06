import requests
import re
import time

def get_links():
    print("🚀 Volo taranıyor, bu sefer liste dolacak...")
    m3u_output = "#EXTM3U\n"
    # Hedef site artık Volo
    target = "https://tv.canlitvvolo.com"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': target
    }

    try:
        # 1. Ana sayfadan kanal linklerini topla
        r = requests.get(target, headers=headers, timeout=20)
        # Sitenin link yapısı: /show-tv-izle-hd/ gibi
        links = re.findall(r'href="(https://tv\.canlitvvolo\.com/[^"]+?)"', r.text)
        # Sadece kanal sayfalarını (hd takılı olanları) filtrele
        links = list(set([l for l in links if "-izle-hd" in l]))
        
        print(f"📡 {len(links)} adet kanal sayfası bulundu.")

        for url in links[:35]: # Hız için ilk 35 kanalı al
            try:
                # Kanal adını URL'den al (ör: atv-izle-hd -> ATV)
                name = url.split('/')[-2].replace('-izle-hd', '').replace('-', ' ').upper()
                
                # Kanal sayfasına gir ve asıl yayın (m3u8) linkini yakala
                res = requests.get(url, headers=headers, timeout=15)
                # m3u8 linkini her türlü tırnak yapısında bulur
                find_m3u8 = re.search(r'["\'](https?://[^"\'>\s]+?\.m3u8[^"\'>\s]*?)["\']', res.text)
                
                if find_m3u8:
                    stream = find_m3u8.group(1).replace("\\/", "/")
                    m3u_output += f"#EXTINF:-1, {name}\n{stream}\n"
                    print(f"✅ {name} eklendi.")
                
                time.sleep(0.5) # Siteyi yormayalım
            except: continue
            
        return m3u_output
    except Exception as e:
        print(f"❌ Kritik Hata: {e}")
        return "#EXTM3U\n"

if __name__ == "__main__":
    final_data = get_links()
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(final_data)
    print("🏁 İşlem tamam, tr.m3u güncellendi.")
