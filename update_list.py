import requests
import re

# 1. Kaynaklar: 7 Yedek URL'nin tamamı (Süzgeç yok, ne bulursa alacak)
YEDEK_KAYNAKLAR = [
    "https://mth.tc/DsGo",
    "https://raw.githubusercontent.com/sultansmgr/smart/refs/heads/main/viziTV.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://streams.uzunmuhalefet.com/lists/tr.m3u"
]

# 2. Dokunulmazlar: En tepede kalacak senin özel 2 linkin
DOKUNULMAZLAR = """#EXTINF:-1,--- PREMIUM STREAM ---
http://96587.premiumstream.in:80
#EXTINF:-1,--- MYWIRE STREAM ---
http://uro-levene-1012.mywire.org"""

def main():
    print("🚀 Operasyon Başladı: 400+ kanal toplanıyor...")
    
    # Listeyi dokunulmazlarla başlatıyoruz
    final_liste = ["#EXTM3U", DOKUNULMAZLAR]
    
    # Aynı linkin tekrarlanmaması için kontrol kümesi
    eklenen_linkler = set([
        "http://96587.premiumstream.in:80", 
        "http://uro-levene-1012.mywire.org"
    ])
    
    # M3U satırlarını yakalayan gelişmiş kalıp
    pattern = r"(#EXTINF:[^\n]*),([^\n]*)\n(https?://[^\n]*)"

    for url in YEDEK_KAYNAKLAR:
        try:
            print(f"🔗 Kaynak taranıyor: {url}")
            r = requests.get(url, timeout=15)
            r.encoding = 'utf-8'
            
            # Kaynaktaki tüm eşleşmeleri bul
            matches = re.findall(pattern, r.text)
            
            for ext_info, ch_name, ch_url in matches:
                link = ch_url.strip()
                # SÜZGEÇ YOK: İsim ne olursa olsun, link yeniyse listeye ekle
                if link not in eklenen_linkler:
                    final_liste.append(f"{ext_info},{ch_name.strip()}\n{link}")
                    eklenen_linkler.add(link)
        except:
            print(f"⚠️ Kaynak atlandı (Hata): {url}")
            continue

    # 3. Dosyayı Yaz: GitHub Actions bu dosyayı buradan alıp internete basacak
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(final_liste))
    
    print(f"✅ İŞLEM TAMAM! Toplam {len(eklenen_linkler)} kanal tr.m3u dosyasına kaydedildi.")

if __name__ == "__main__":
    main()
