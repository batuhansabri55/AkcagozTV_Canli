import requests
import re
import base64
import os

# --- AYARLAR ---
GITHUB_TOKEN = os.environ.get('GH_TOKEN') 
REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

DOKUNULMAZLAR = ["premiumstream.in", "workers.dev", "mywire.org", "token=DeaTHLesS", "goldvod.site", "trt.com.tr", "turknet.ercdn.net", "daioncdn.net"]
YEDEK_KAYNAKLAR = ["https://mth.tc/DsGo", "https://raw.githubusercontent.com/sultansmgr/smart/refs/heads/main/viziTV.m3u", "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u", "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8", "https://publiciptv.com/countries/tr/m3u", "https://iptv-org.github.io/iptv/countries/tr.m3u", "https://streams.uzunmuhalefet.com/lists/tr.m3u"]

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
    data = {"message": "♻️ Liste Guncellendi", "content": base64.b64encode(icerik.encode("utf-8")).decode("utf-8"), "sha": sha}
    r = requests.put(url, json=data, headers=headers)
    return r.status_code

def update_m3u():
    mevcut_icerik, sha = github_dosya_oku()
    if not sha: return

    # YENİ REGEX: #EXTINF ile başlayan satırı ve altındaki linki paket yapar. 
    # Virgül olsa da olmasa da yakalar.
    pattern = r"(#EXTINF:[^\n]+)\n+(https?://[^\s\n]+)"
    
    final_liste = ["#EXTM3U"]
    eklenen_linkler = set()

    # 1. Mevcut Dokunulmazları Ayıkla
    matches = re.findall(pattern, mevcut_icerik)
    for info, url in matches:
        link = url.strip()
        if any(d in link.lower() for d in DOKUNULMAZLAR):
            final_liste.append(f"{info}\n{link}")
            eklenen_linkler.add(link)

    # 2. Yedekleri Ekle
    for s_url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(s_url, timeout=10)
            y_matches = re.findall(pattern, r.text)
            for y_info, y_url in y_matches:
                y_link = y_url.strip()
                if y_link not in eklenen_linkler:
                    final_liste.append(f"{y_info}\n{y_link}")
                    eklenen_linkler.add(y_link)
        except: continue

    # 3. GitHub'a Bas
    final_m3u = "\n".join(final_liste)
    github_dosya_yaz(final_m3u, sha)

if __name__ == "__main__":
    update_m3u()
