import requests
import re

def get_cnn_turk():
    # CNN Türk'ün canlı yayın sayfası
    url = "https://www.cnnturk.com/canli-yayin"
    
    # Siteye tarayıcı gibi görünmek için gerekli headerlar
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Referer': 'https://www.cnnturk.com/'
    }

    try:
        # Sayfayı indir
        response = requests.get(url, headers=headers, timeout=10)
        
        # Sayfa içindeki m3u8 linkini regex ile cımbızla çek
        # CNN genellikle 'https://...playlist.m3u8' yapısını kullanır
        match = re.search(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', response.text)
        
        if match:
            # Linki bulduk, içindeki ters slashları (varsa) temizle
            stream_url = match.group(1).replace('\\/', '/')
            return stream_url
        else:
            return "Link bulunamadı."

    except Exception as e:
        return f"Hata oluştu: {str(e)}"

# --- Sadece CNN'i test et ---
if __name__ == "__main__":
    print("CNN Türk Linki Çekiliyor...")
    sonuc = get_cnn_turk()
    print(f"\nSONUÇ:\n{sonuc}")
