import requests
import re

def get_giniko_list():
    print("🚀 Giniko/Workers üzerinden liste çekiliyor...")
    # Senin ekranında açık olan kaynak adres
    target_url = "https://giniko.smartiptvworld.workers.dev/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    try:
        r = requests.get(target_url, headers=headers, timeout=25)
        # Sayfa içindeki kanal isimlerini ve m3u8 linklerini avla
        # Genellikle "name":"KANAL", "url":"http..." şeklinde olur
        matches = re.findall(r'["\']?name["\']?:\s*["\']([^"\']+)["\'].*?["\']?url["\']?:\s*["\']([^"\']+\.m3u8[^"\']*)["\']', r.text, re.IGNORECASE)
        
        if not matches:
            # Alternatif: Düz metin içinde m3u8 arama
            matches = re.findall(r'#EXTINF:-1,\s*(.*?)\n(https?://.*?\.m3u8.*)', r.text)

        if matches:
            m3u_content = "#EXTM3U\n"
            for name, url in matches:
                m3u_content += f"#EXTINF:-1, {name.strip()}\n{url.strip()}\n"
            print(f"✅ {len(matches)} kanal başarıyla eklendi!")
            return m3u_content
        else:
            print("⚠️ Link bulunamadı, ham veri çekiliyor...")
            return r.text if "#EXTM3U" in r.text else "#EXTM3U\n"

    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        return "#EXTM3U\n"

if __name__ == "__main__":
    result = get_giniko_list()
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(result)
    print("🏁 Bitti. tr.m3u güncellendi.")
