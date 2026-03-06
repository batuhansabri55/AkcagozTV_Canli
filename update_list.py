import requests
import re

def get_giniko_data():
    print("📡 Giniko Workers kaynağına bağlanılıyor...")
    # Ekranında açık olan kaynak adres
    target_url = "https://giniko.smartiptvworld.workers.dev/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(target_url, headers=headers, timeout=30)
        
        # Eğer sayfa doğrudan bir M3U dosyasıysa
        if "#EXTM3U" in response.text:
            print("✅ Hazır M3U listesi bulundu!")
            return response.text
            
        # Eğer sayfa JSON veya HTML ise içindeki isim ve m3u8 linklerini ayıkla
        print("🔍 Kanal linkleri ayıklanıyor...")
        # Örn: "name":"TRT 1", "url":"https://..." yapısını yakalar
        matches = re.findall(r'["\']?name["\']?:\s*["\']([^"\']+)["\'].*?["\']?url["\']?:\s*["\']([^"\']+\.m3u8[^"\']*)["\']', response.text, re.IGNORECASE)
        
        if matches:
            m3u_output = "#EXTM3U\n"
            for name, url in matches:
                # Gereksiz kaçış karakterlerini temizle
                clean_url = url.replace("\\/", "/")
                m3u_output += f"#EXTINF:-1, {name.strip()}\n{clean_url}\n"
            print(f"✅ {len(matches)} adet kanal listeye eklendi.")
            return m3u_output
        else:
            # Düz metin taraması (Her ihtimale karşı)
            simple_links = re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', response.text)
            if simple_links:
                m3u_output = "#EXTM3U\n"
                for i, link in enumerate(simple_links):
                    m3u_output += f"#EXTINF:-1, Kanal {i+1}\n{link}\n"
                return m3u_output

        print("⚠️ Uyarı: Kaynakta işlenebilir link bulunamadı.")
        return "#EXTM3U\n"

    except Exception as e:
        print(f"❌ Hata: {e}")
        return "#EXTM3U\n"

if __name__ == "__main__":
    final_list = get_giniko_data()
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(final_list)
    print("🏁 İşlem tamamlandı. tr.m3u güncellendi.")
