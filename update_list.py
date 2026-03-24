import requests
import re
import base64
import os

# --- AYARLAR ---
GITHUB_TOKEN = os.environ.get('GH_TOKEN') 
REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

# Senin korumak istediğin kelimeler
DOKUNULMAZLAR = ["premiumstream.in", "workers.dev", "mywire.org", "token=DeaTHLesS", "goldvod.site", "trt.com.tr", "turknet.ercdn.net", "daioncdn.net"]

# Yedek kaynaklar
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
    # 1. GitHub'dan Güncel Dosyayı ve SHA Değerini Al (En kritik adım)
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print(f"❌ Dosya okunamadı! Hata Kodu: {r.status_code}")
        return

    mevcut_icerik = base64.b64decode(r.json()['content']).decode('utf-8')
    guncel_sha = r.json()['sha']

    # 2. Kanal Bloklarını Ayıkla (Regex: #EXTINF ve altındaki linki paket yapar)
    # Satır sonu karakterlerini (\r\n) temizlemek için daha esnek bir yapı kullandım
    pattern = r"(#EXTINF:[^\n]+)\n+(https?://[^\s\n]+)"
    matches = re.findall(pattern, mevcut_icerik)
    
    final_liste = ["#EXTM3U"]
    eklenen_linkler = set()

    # Dokunulmazları koru
    for info, link in matches:
        clean_link = link.strip()
        if any(d in clean_link.lower() for d in DOKUNULMAZLAR):
            final_liste.append(f"{info}\n{clean_link}")
            eklenen_linkler.add(clean_link)

    print(f"🛡️ {len(final_liste)-1} dokunulmaz link ayrıldı.")

    # 3. Yedekleri Çek ve Ekle
    for s_url in YEDEK_KAYNAKLAR:
        try:
            res = requests.get(s_url, timeout=10)
            y_matches = re.findall(pattern, res.text)
            for y_info, y_link in y_matches:
                yl = y_link.strip()
                if yl not in eklenen_linkler:
                    final_liste.append(f"{y_info}\n{yl}")
                    eklenen_linkler.add(yl)
        except: continue

    # 4. GitHub'a Geri Yaz (Güncel SHA ile)
    yeni_m3u = "\n".join(final_liste)
    data = {
        "message": "♻️ Otomatik VIP Koruma Guncellemesi",
        "content": base64.b64encode(yeni_m3u.encode("utf-8")).decode("utf-8"),
        "sha": guncel_sha
    }
    
    update_r = requests.put(url, json=data, headers=headers)
    
    if update_r.status_code in [200, 201]:
        print("✅ Başarılı: Dosya güncellendi!")
    else:
        print(f"❌ Güncelleme Başarısız! Hata: {update_r.text}")

if __name__ == "__main__":
    main()
