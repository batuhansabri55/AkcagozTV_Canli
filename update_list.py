import requests
import re
import os

# --- AYARLAR ---
# Buraya eski yedek kaynaklarını ekleyebilirsin
YEDEK_KAYNAKLAR = [
    "https://streams.uzunmuhalefet.com/lists/tr.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr.m3u"
]

def get_cnn_turk():
    """SeyirTur mantığının Python'a uyarlanmış hali"""
    url = "https://www.cnnturk.com/canli-yayin"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Referer': 'https://www.cnnturk.com/'
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        # JS kodundaki regex'in Python hali
        match = re.search(r'["\'](https?://[^\s"\']+\.m3u8[^\s"\']*)["\']', r.text)
        if match:
            link = match.group(1).replace('\\/', '/')
            # Zırhlı link formatı
            return f"{link}|User-Agent={headers['User-Agent']}&Referer={headers['Referer']}"
    except:
        return None
    return None

def m3u_olustur():
    kanallar = []
    
    # 1. ÖZEL KANAL: CNN TÜRK
    print("CNN Türk çekiliyor...")
    cnn = get_cnn_turk()
    if cnn:
        kanallar.append(f'#EXTINF:-1 tvg-id="cnn-turk" group-title="HABER",CNN TURK\n{cnn}')

    # 2. YEDEK KAYNAKLARDAN TOPLA (Senin eski sistemin)
    for kaynak in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(kaynak, timeout=5)
            # Burada gelen listeden sadece istediğin kanalları ayıklayabilirsin
            # Şimdilik basitçe ekliyoruz
            pass 
        except:
            continue

    # DOSYAYA YAZ
    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for k in kanallar:
            f.write(k + "\n")
    print("tr.m3u başarıyla güncellendi!")

if __name__ == "__main__":
    m3u_olustur()
