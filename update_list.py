import requests
import re
import os

def get_cnn_turk():
    url = "https://www.cnnturk.com/canli-yayin"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Referer': 'https://www.cnnturk.com/'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        # m3u8 linkini ayıkla
        match = re.search(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', response.text)
        if match:
            raw_url = match.group(1).replace('\\/', '/')
            # Çift slash hatasını temizle
            clean_url = raw_url.replace('.tv//', '.tv/')
            # VLC ve TiviMate için sihirli dokunuş: Header ekle
            final_url = f"{clean_url}|User-Agent={headers['User-Agent']}&Referer={headers['Referer']}"
            return final_url
        return None
    except:
        return None

# Ana çalıştırma
cnn_link = get_cnn_turk()

if cnn_link:
    m3u_content = f"#EXTM3U\n#EXTINF:-1 tvg-logo=\"https://upload.wikimedia.org/wikipedia/commons/c/c8/CNN_Turk_logo.png\",CNN TURK\n{cnn_link}"
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("Link başarıyla alındı ve tr.m3u oluşturuldu!")
else:
    print("HATA: Link çekilemedi!")
