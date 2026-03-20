import requests
import re
import base64
import os

# --- AYARLAR ---
GITHUB_TOKEN = os.environ.get('GH_TOKEN') 
REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

# --- DOKUNULMAZLAR (Bu kelimeleri içeren linkler asla silinmez) ---
# Buraya TRT ve Kanal D linklerinde geçen "turknet" ve "trt" kelimelerini de ekledim.
DOKUNULMAZLAR = [
    "premiumstream.in", "workers.dev", "mywire.org", "token=DeaTHLesS", "goldvod.site",
    "trt.com.tr", "turknet.ercdn.net", "daioncdn.net"
]

YEDEK_KAYNAKLAR = [
    "https://mth.tc/DsGo",
    "https://raw.githubusercontent.com/sultansmgr/smart/refs/heads/main/viziTV.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://streams.uzunmuhalefet.com/lists/tr.m3u"
]

def github_dosya_oku():
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        content = base64.b64decode(r.json()['content']).decode('utf-8')
        return content, r.json()['sha']
    return "", None

def github_dosya_yaz(icerik, sha):
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    data = {
        "message": "🔄 Dokunulmazlar Sabitlendi & Yedekler Güncellendi",
        "content": base64.b64encode(icerik.encode("utf-8")).decode("utf-8"),
        "sha": sha
    }
    requests.put(url, json=data, headers=headers)

def update_m3u():
    mevcut_icerik, sha = github_dosya_oku()
    if not sha:
        print("❌ Dosya okunamadı!")
        return

    yeni_liste = ["#EXTM3U"]
    eklenen_linkler = set()

    # --- ÖNEMLİ DÜZELTME: Hem http hem https linkleri yakalar ---
    # Regex pattern: (http ve https destekli)
    pattern = r"(#EXTINF:[^\n]*)\n(https?://[^\n]*)"

    # 1. Önce Dokunulmazları Koru
    blocks = re.findall(pattern, mevcut_icerik)
    for info, url in blocks:
        link = url.strip()
        if any(d in link.lower() for d in DOKUNULMAZLAR):
            yeni_liste.append(f"{info}\n{link}")
            eklenen_linkler.add(link)

    # 2. Sonra Yedekleri Ekle
    for s_url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(s_url, timeout=10)
            matches = re.findall(pattern, r.text.replace('\r', ''))
            for info, url in matches:
                link = url.strip()
                if link not in eklenen_linkler:
                    yeni_liste.append(f"{info}\n{link}")
                    eklenen_linkler.add(link)
        except: continue

    # 3. GitHub'a Yaz
    final_m3u = "\n".join(yeni_liste)
    github_dosya_yaz(final_m3u, sha)
    print(f"🚀 İşlem tamam! {len(yeni_liste)-1} kanal dosyaya yazıldı.")

if __name__ == "__main__":
    update_m3u()
