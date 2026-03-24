import requests
import re

# 1. DOKUNULMAZLAR: Bu linkler asla silinmez ve en üstte durur
# Format: (Kanal Bilgisi, Kanal İsmi, Link)
DOKUNULMAZ_LISTE = [
    ("#EXTINF:-1", "--- PREMIUM STREAM ---", "http://96587.premiumstream.in:80"),
    ("#EXTINF:-1", "--- MYWIRE STREAM ---", "http://uro-levene-1012.mywire.org")
]

# 2. YEDEK KAYNAKLAR: 400+ kanalın geleceği yerler
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
    print("🚀 Operasyon Başladı: Dokunulmazlar korunuyor, yedekler toplanıyor...")
    
    final_liste = ["#EXTM3U"]
    eklenen_linkler = set()

    # Önce dokunulmazları en başa ekle
    for ext, name, link in DOKUNULMAZ_LISTE:
        final_liste.append(f"{ext},{name}\n{link}")
        eklenen_linkler.add(link.strip())

    # M3U satır yakalayıcı
    pattern = r"(#EXTINF:[^\n]*),([^\n]*)\n(https?://[^\n]*)"

    # Yedekleri tara
    for url in YEDEK_KAYNAKLAR:
        try:
            print(f"🔗 Kaynak taranıyor: {url}")
            r = requests.get(url, timeout=15)
            r.encoding = 'utf-8'
            matches = re.findall(pattern, r.text)
            
            for ext_info, ch_name, ch_url in matches:
                link = ch_url.strip()
                # Eğer link dokunulmazlarda yoksa ve yeni bir linkse ekle
                if link not in eklenen_linkler:
                    final_liste.append(f"{ext_info},{ch_name.strip()}\n{link}")
                    eklenen_linkler.add(link)
        except:
            continue

    # Dosyayı kaydet
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(final_liste))
    
    print(f"✅ Bitti! {len(eklenen_linkler)} kanal (dokunulmazlar dahil) başarıyla yazıldı.")

if __name__ == "__main__":
    main()
