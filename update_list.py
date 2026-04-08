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
        # Sayfa içindeki m3u8 linkini yakala
        match = re.search(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', response.text)
        if match:
            return match.group(1).replace('\\/', '/')
        return None
    except:
        return None

def tek_kanal_m3u_olustur():
    cnn_url = get_cnn_turk()
    
    if cnn_url:
        m3u_icerik = "#EXTM3U\n"
        m3u_icerik += '#EXTINF:-1 tvg-id="cnn-turk" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/c/c8/CNN_Turk_logo.png" group-title="HABER",CNN TURK\n'
        m3u_icerik += cnn_url + "\n"
        
        with open("tr.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_icerik)
        print("CNN Türk başarıyla güncellendi ve tr.m3u dosyasına yazıldı.")
    else:
        print("CNN Türk linki çekilemedi!")

if __name__ == "__main__":
    tek_kanal_m3u_olustur()
