import requests
import re
import base64
import os

# --- AYARLAR ---
GITHUB_TOKEN = os.environ.get('GH_TOKEN') 
REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

# --- 1. DOKUNULMAZLAR ---
DOKUNULMAZ_BLOK = """#EXTINF:-1,--- PREMIUM STREAM ---
http://96587.premiumstream.in:80
#EXTINF:-1,--- MYWIRE STREAM ---
http://uro-levene-1012.mywire.org"""

# --- 2. KAYNAKLAR ---
YEDEK_KAYNAKLAR = [
    "https://mth.tc/DsGo",
    "https://raw.githubusercontent.com/sultansmgr/smart/refs/heads/main/viziTV.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://streams.uzunmuhalefet.com/lists/tr.m3u"
]

def update_m3u():
    print("🚀 İşlem başlatıldı...")
    
    # 1. Kaynaklardan veri çek
    final_liste = ["#EXTM3U", DOKUNULMAZ_BLOK]
    eklenen_linkler = set(["http://96587.premiumstream.in:80", "http://uro-levene-1012.mywire.org"])
    pattern = r"(#EXTINF:[^\n]*),([^\n]*)\n(https?://[^\n]*)"

    for s_url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(s_url, timeout=15)
            r.encoding = 'utf-8'
            matches = re.findall(pattern, r.text)
            for ext_info, ch_name, url in matches:
                link = url.strip()
                if link not in eklenen_linkler:
                    final_liste.append(f"{ext_info},{ch_name.strip()}\n{link}")
                    eklenen_linkler.add(link)
        except: continue

    yeni_icerik = "\n".join(final_liste)
    print(f"📦 Toplam {len(final_liste)} satır hazırlandı.")

    # 2. GitHub'a Yazma (ZORLAMA)
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    
    # Mevcut SHA'yı al
    get_r = requests.get(url, headers=headers)
    if get_r.status_code == 200:
        sha = get_r.json()['sha']
        print(f"🔑 Mevcut dosya SHA'sı alındı: {sha}")
        
        data = {
            "message": "🔥 KRİTİK GÜNCELLEME: SIFIR SÜZGEÇ TAM LİSTE",
            "content": base64.b64encode(yeni_icerik.encode("utf-8")).decode("utf-8"),
            "sha": sha
        }
        
        put_r = requests.put(url, json=data, headers=headers)
        if put_r.status_code == 200:
            print("✅ BAŞARILI: tr.m3u güncellendi!")
        else:
            print(f"❌ HATA: Yazma başarısız! Kod: {put_r.status_code}, Mesaj: {put_r.text}")
    else:
        print(f"❌ HATA: Dosya SHA alınamadı! Kod: {get_r.status_code}")

if __name__ == "__main__":
    update_m3u()
