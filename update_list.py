import requests
import re

# 1. ÖZEL KAYNAKLAR (İçindeki binlerce kanalı söküp alacağımız yerler)
# Bu linklerin her biri aslında birer dev liste
OZEL_KAYNAKLAR = [
    "http://96587.premiumstream.in:80",
    "http://uro-levene-1012.mywire.org"
]

# 2. DİĞER YEDEK KAYNAKLAR (Listenin devamına eklenecekler)
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
    print("🚀 Operasyon: Dev listeler parçalanıyor ve kanallar çekiliyor...")
    
    final_liste = ["#EXTM3U"]
    eklenen_linkler = set()
    
    # Kanal yakalama kalıbı (Kanal Bilgisi, Kanal İsmi, Link)
    pattern = r"(#EXTINF:[^\n]*),([^\n]*)\n(https?://[^\n]*|http://[^\n]*)"

    # ADIM 1: Senin o Premium ve Mywire listelerini komple tara
    for url in OZEL_KAYNAKLAR:
        try:
            print(f"💎 Özel dev liste okunuyor: {url}")
            r = requests.get(url, timeout=25) # Büyük liste olduğu için süreyi uzun tuttuk
            r.encoding = 'utf-8'
            matches = re.findall(pattern, r.text)
            
            for ext, name, link in matches:
                clean_link = link.strip()
                if clean_link not in eklenen_linkler:
                    final_liste.append(f"{ext},{name.strip()}\n{clean_link}")
                    eklenen_linkler.add(clean_link)
        except Exception as e:
            print(f"⚠️ Özel kaynakta hata: {e}")

    # ADIM 2: Diğer 7 yedek kaynağı tara
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

    # DOSYAYI YAZ (GitHub Actions bunu senin tr.m3u dosyana basacak)
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(final_liste))
    
    print(f"✅ İşlem Tamam! Toplam {len(eklenen_linkler)} kanal süzüldü ve eklendi.")

if __name__ == "__main__":
    main()
