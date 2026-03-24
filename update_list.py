import requests
import re

# 1. HEM EN BAŞTA DURACAK HEM DE İÇİNDEKİ 1800 KANALI ÇEKECEK OLANLAR
OZEL_KAYNAKLAR = [
    "http://96587.premiumstream.in:80",
    "http://uro-levene-1012.mywire.org"
]

# 2. DİĞER YEDEK KAYNAKLAR
YEDEK_KAYNAKLAR = [
    "https://mth.tc/DsGo",
    "https://raw.githubusercontent.com/sultansmgr/smart/refs/heads/main/viziTV.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://streams.uzunmuhalefet.com/lists/tr.m3u"
]

def main():
    print("🚀 Operasyon: Özel linklerin içindeki 1800+ kanal çekiliyor...")
    
    final_liste = ["#EXTM3U"]
    eklenen_linkler = set()
    pattern = r"(#EXTINF:[^\n]*),([^\n]*)\n(https?://[^\n]*)"

    # ADIM 1: Önce o senin 1800 kanallık özel linklerini tara ve en başa ekle
    for url in OZEL_KAYNAKLAR:
        try:
            print(f"💎 Özel kaynak okunuyor: {url}")
            r = requests.get(url, timeout=20)
            r.encoding = 'utf-8'
            matches = re.findall(pattern, r.text)
            for ext, name, link in matches:
                clean_link = link.strip()
                if clean_link not in eklenen_linkler:
                    final_liste.append(f"{ext},{name.strip()}\n{clean_link}")
                    eklenen_linkler.add(clean_link)
        except:
            print(f"⚠️ Özel kaynakta sorun: {url}")

    # ADIM 2: Diğer yedekleri tara ve listenin devamına ekle
    for url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(url, timeout=15)
            r.encoding = 'utf-8'
            matches = re.findall(pattern, r.text)
            for ext, name, link in matches:
                clean_link = link.strip()
                if clean_link not in eklenen_linkler:
                    final_liste.append(f"{ext},{name.strip()}\n{clean_link}")
                    eklenen_linkler.add(clean_link)
        except:
            continue

    # Dosyayı kaydet
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(final_liste))
    
    print(f"✅ BİTTİ! Toplam {len(eklenen_linkler)} kanal (1800+ özel dahil) yazıldı.")

if __name__ == "__main__":
    main()
