import requests
import time

# Devamlı güncellenen güvenilir kaynaklar
YEDEK_KAYNAKLAR = [
    "https://raw.githubusercontent.com/sultansmgr/smart/refs/heads/main/viziTV.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://streams.uzunmuhalefet.com/lists/tr.m3u"
]

def update_m3u():
    print("🚀 Liste guncelleme baslatildi...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    
    # M3U Baslangici
    final_content = "#EXTM3U\n"
    added_links = set()

    for url in YEDEK_KAYNAKLAR:
        print(f"📡 Kaynak okunuyor: {url}")
        try:
            # 403 hatasini asmak icin headers ile istek atiyoruz
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code == 200:
                lines = r.text.splitlines()
                current_info = ""
                
                for line in lines:
                    line = line.strip()
                    if line.startswith("#EXTINF"):
                        current_info = line
                    elif line.startswith("http") and current_info:
                        # Tekrar eden linkleri engelle
                        if line not in added_links:
                            final_content += f"{current_info}\n{line}\n"
                            added_links.add(line)
                        current_info = ""
            else:
                print(f"⚠️ Hata: {url} (Kod: {r.status_code})")
        except Exception as e:
            print(f"❌ Baglanti hatasi: {url} -> {e}")

    # tr.m3u dosyasina kaydet
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(final_content)
    
    print(f"✅ Islem tamam! Toplam {len(added_links)} taze link toplandi.")

if __name__ == "__main__":
    update_m3u()
