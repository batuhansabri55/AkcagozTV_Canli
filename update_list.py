import yt_dlp

# Genişletilmiş Canlı Yayın Listesi
KANALLAR = {
    "A Haber": "https://www.youtube.com/@ahaber/live",
    "Sozcu TV": "https://www.youtube.com/@SozcuTelevizyonu/live",
    "CNN Turk": "https://www.youtube.com/@cnnturk/live",
    "HaberTurk": "https://www.youtube.com/@haberturk/live",
    "NTV": "https://www.youtube.com/@NTV/live",
    "Haber Global": "https://www.youtube.com/@HaberGlobal/live",
    "TV100": "https://www.youtube.com/@tv100/live",
    "TV NET": "https://www.youtube.com/@tvnet/live"
}

def canli_yayin_linki_al(url):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        # GitHub sunucularının YouTube bot barajına takılmasını engelleyen mobil yapay istemci ayarı
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios'],
                'skip': ['dash', 'hls']
            }
        }
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get('url')
    except Exception as e:
        print(f"   ❌ Link çözülürken hata oldu: {str(e)}")
        return None

def m3u_olustur(linkler):
    try:
        with open("youtube_canli.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for isim, link in linkler.items():
                if link:
                    f.write(f'#EXTINF:-1 tvg-name="{isim}" group-title="YouTube Canli",{isim}\n')
                    f.write(f"{link}\n")
        print("\n🚀 GENİŞLETİLMİŞ GÜNCEL M3U DOSYASI KLASÖRDE OLUŞTURULDU!")
    except Exception as e:
        print(f"❌ Dosya yazılırken hata: {str(e)}")

def ana_fonksiyon():
    yakalanan_linkler = {}
    
    print("🚀 Genişletilmiş Haber Paketi Linkleri Çekiliyor...\n")
    for isim, url in KANALLAR.items():
        print(f"-> {isim} için güncel akış çözülüyor...")
        canli_link = canli_yayin_linki_al(url)
        
        if canli_link:
            print(f"   🟢 Başarılı!")
            yakalanan_linkler[isim] = canli_link
        else:
            print(f"   ❌ {isim} linki alınamadı. (Yayında olmayabilir)")
            
    if yakalanan_linkler:
        print("\n======================= YAKALANAN TAM LİNKLER =======================")
        for isim, link in yakalanan_linkler.items():
            print(f"\n[{isim} - TAM LINK]:")
            print(link)
            print("-" * 70)
            
        m3u_olustur(yakalanan_linkler)
    else:
        print("\n❌ Maalesef hiçbir link çekilemedi.")

if __name__ == "__main__":
    ana_fonksiyon()
