import requests
import re
import time

def get_links():
    print("🚀 Volo Operasyonu: Derin tarama başlatılıyor...")
    m3u_header = "#EXTM3U\n"
    base_url = "https://tv.canlitvvolo.com"
    
    # Gerçek bir tarayıcı gibi davranmak için header bilgileri
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': base_url,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    }

    try:
        # 1. Ana sayfadan tüm kanal sayfalarını topla
        r = requests.get(base_url, headers=headers, timeout=20)
        # Sitenin link yapısı: /atv-izle-hd/ veya /show-tv-izle-hd/
        links = re.findall(r'href="(https://tv\.canlitvvolo\.com/[^"]+?-izle-hd/)"', r.text)
        links = list(set(links)) # Tekrarları sil
        
        print(f"📡 {len(links)} adet kanal sayfası tespit edildi.")

        content_body = ""
        for url in links[:40]: # İlk 40 kanal
            try:
                # Kanal ismini URL'den güzelleştir
                name = url.split('/')[-2].replace('-izle-hd', '').replace('-', ' ').upper()
                
                # Kanal sayfasına gir ve asıl yayın linkini (m3u8) ara
                res = requests.get(url, headers=headers, timeout=15)
                
                # Hem tek tırnak hem çift tırnak içindeki m3u8 linklerini yakalar
                m3u8_match = re.search(r'["\'](https?://[^"\'>\s]+?\.m3u8[^"\'>\s]*?)["\']', res.text)
                
                if m3u8_match:
                    stream_url = m3u8_match.group(1).replace("\\/", "/")
                    content_body += f"#EXTINF:-1, {name}\n{stream_url}\n"
                    print(f"✅ Eklendi: {name}")
                
                time.sleep(0.4) # Siteyi yormayalım
            except:
                continue
        
        return m3u_header + content_body

    except Exception as e:
        print(f"❌ Kritik Hata: {e}")
        return m3u_header

if __name__ == "__main__":
    final_m3u = get_links()
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(final_m3u)
    print("🏁 İşlem bitti, dosya kaydedildi.")
