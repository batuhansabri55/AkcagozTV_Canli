import requests
import re

def get_cnn_turk():
    url = "https://www.cnnturk.com/canli-yayin"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Referer': 'https://www.cnnturk.com/'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # m3u8 linkini bul
        match = re.search(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', response.text)
        if match:
            raw_url = match.group(1).replace('\\/', '/')
            # Çift slash hatasını temizle (https://live.duhnet.tv//S2 -> /S2)
            raw_url = raw_url.replace('.tv//', '.tv/')
            
            # TiviMate ve VLC için header bilgilerini linke yapıştırıyoruz
            # Bu format oynatıcıya "bu linki açarken şu User-Agent'ı kullan" der.
            final_url = f"{raw_url}|User-Agent={headers['User-Agent']}&Referer={headers['Referer']}"
            return final_url
        return None
    except:
        return None

# Test çıktısını alalım
print(get_cnn_turk())
