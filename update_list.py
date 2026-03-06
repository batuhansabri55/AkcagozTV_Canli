import requests

def usta_worker_cek():
    # Senin Worker dashboard'unda çalışan M3U linki
    worker_liste_url = "https://giniko.smartiptvworld.workers.dev/liste.m3u"
    
    print(f"📡 Worker'dan liste çekiliyor: {worker_liste_url}")
    
    try:
        # Worker'ın bot kontrolünü aşmak için gerçekçi header
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36'
        }
        r = requests.get(worker_liste_url, headers=headers, timeout=30)
        
        if "#EXTM3U" in r.text:
            print(f"✅ Başarılı! {r.text.count('#EXTINF')} kanal bulundu.")
            return r.text
        else:
            print("⚠️ Worker M3U içeriği vermedi, boş sayfa döndü.")
            return "#EXTM3U\n"
    except Exception as e:
        print(f"❌ Hata: {e}")
        return "#EXTM3U\n"

if __name__ == "__main__":
    content = usta_worker_cek()
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(content)
