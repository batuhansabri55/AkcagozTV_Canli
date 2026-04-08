import requests
import re

def get_cnn_turk_professional():
    url = "https://www.cnnturk.com/canli-yayin"
    # Sunucuyu kandırmak için gerçek tarayıcı bilgileri şart
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Referer': 'https://www.cnnturk.com/'
    }

    try:
        # 1. Sayfa içeriğini çek
        response = requests.get(url, headers=headers, timeout=10)
        
        # 2. m3u8 linkini bul (Sadece playlist.m3u8 değil, tüm linki yakala)
        match = re.search(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', response.text)
        
        if match:
            # Linkteki ters slashları ve hatalı çift slashları temizle
            stream_url = match.group(1).replace('\\/', '/').replace('.tv//', '.tv/')
            
            # 3. VLC ve TiviMate'in anlayacağı 'Pipe' (|) yöntemini kullan
            # Bu yöntem, oynatıcıya "şu header bilgilerini kullanarak bağlan" talimatı verir.
            final_link = f"{stream_url}|User-Agent={headers['User-Agent']}&Referer={headers['Referer']}"
            return final_link
        
        return "Link bulunamadı."
    except Exception as e:
        return f"Hata: {str(e)}"

# Çalıştır ve sonucu gör
if __name__ == "__main__":
    print(get_cnn_turk_professional())
