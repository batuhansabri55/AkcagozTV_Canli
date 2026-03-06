import requests
import re
import time

def get_blogtv_links():
    print("🚀 Sistem başlatıldı, kanallar taranıyor...")
    blog_m3u = "#EXTM3U\n"
    ana_url = "https://www.blogtv.net.tr/p/turkiyenin-en-kapsaml-ulusal-kanallar.html"
    
    # Gerçek bir tarayıcı gibi davranalım
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": "https://www.blogtv.net.tr/"
    }

    try:
        r = requests.get(ana_url, headers=headers, timeout=30)
        # YENİ REGEX: Sadece blogtv linklerine odaklan, tırnak işaretlerini umursama
        # Bu regex, href içindeki veya dışındaki tüm kanal linklerini yakalar
        links = re.findall(r'https://www\.blogtv\.net\.tr/p/[^\s"\'<>]+?\.html\?kanal=[^\s"\'<>]+', r.text)
        links = list(dict.fromkeys(links)) # Sıralamayı bozmadan tekrarları sil
        
        if not links:
            print("❌ HATA: Hiç kanal linki bulunamadı! Site yapısı değişmiş olabilir.")
            return blog_m3u

        print(f"✅ {len(links)} adet potansiyel kanal bulundu. İşleniyor...")

        for link in links[:40]: # İlk 40 tanesini işle
            try:
                # Kanal adını linkten çek (örneğin: kanal=show_tv -> SHOW TV)
                kanal_adi = link.split("kanal=")[-1].replace("_", " ").replace("%20", " ").upper()
                
                res = requests.get(link, headers=headers, timeout=15)
                # m3u8 linkini yakala (en esnek haliyle)
                m3u8_find = re.search(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*?)', res.text)
                
                if m3u8_find:
                    m3u8_url = m3u8_find.group(1).replace("\\/", "/")
                    blog_m3u += f"#EXTINF:-1, {kanal_adi}\n{m3u8_url}\n"
                    print(f"➕ Eklendi: {kanal_adi}")
                
                time.sleep(0.5) # Siteyi yormayalım
            except Exception as e:
                continue

    except Exception as e:
        print(f"❌ Ana sayfa çekilemedi: {e}")
    
    return blog_m3u

if __name__ == "__main__":
    liste_icerigi = get_blogtv_links()
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(liste_icerigi)
    
    # Dosya boyutunu kontrol et
    import os
    size = os.path.getsize("tr.m3u")
    print(f"🏁 İşlem bitti. Dosya boyutu: {size} byte.")
