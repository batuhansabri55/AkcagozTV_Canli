import requests, re

# --- AYARLAR ---
# Senin o hiç silinmeyecek, en başta duracak 2 linkin
DOKUNULMAZLAR = """#EXTINF:-1,--- PREMIUM STREAM ---
http://96587.premiumstream.in:80
#EXTINF:-1,--- MYWIRE STREAM ---
http://uro-levene-1012.mywire.org"""

# Senin o meşhur 7-8 yedek kaynağın (Hepsini buraya ekledim)
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
    print("🚀 Kanallar toplanıyor (Süzgeçsiz)...")
    
    # Listeyi dokunulmazlarla başlatıyoruz
    final_liste = ["#EXTM3U", DOKUNULMAZLAR]
    
    # Link kopyalarını engellemek için set (Aynı kanal 5 kere gelmesin)
    eklenen_linkler = set(["http://96587.premiumstream.in:80", "http://uro-levene-1012.mywire.org"])
    
    # M3U satırlarını yakalayan kalıp
    pattern = r"(#EXTINF:[^\n]*),([^\n]*)\n(https?://[^\n]*)"

    # 7 kaynağın hepsini tek tek tara
    for url in YEDEK_KAYNAKLAR:
        try:
            print(f"🔗 Kaynak okunuyor: {url}")
            r = requests.get(url, timeout=15)
            r.encoding = 'utf-8'
            matches = re.findall(pattern, r.text)
            
            for ext_info, ch_name, ch_url in matches:
                link = ch_url.strip()
                # İSİM SÜZGECİ YOK! Sadece link daha önce eklenmediyse al.
                if link not in eklenen_linkler:
                    final_liste.append(f"{ext_info},{ch_name.strip()}\n{link}")
                    eklenen_linkler.add(link)
        except:
            print(f"⚠️ Kaynağa ulaşılamadı: {url}")
            continue

    # DOSYAYI YEREL OLARAK YAZ (Gerisini .yml halledecek)
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(final_liste))
    
    print(f"✅ İşlem Bitti! Toplam {len(eklenen_linkler)} kanal tr.m3u dosyasına yazıldı.")

if __name__ == "__main__":
    main()
