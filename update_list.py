import requests
import re
import base64
import os

# --- AYARLAR ---
GITHUB_TOKEN = os.environ.get('GH_TOKEN') 
REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

# --- BURASI DOKUNULMAZ ALAN ---
# Bu linkler her zaman listenin en başında duracak
DOKUNULMAZ_LISTE = """
#EXTINF:-1,--- ÖZEL YAYIN 1 ---
http://96587.premiumstream.in:80
#EXTINF:-1,--- ÖZEL YAYIN 2 ---
http://uro-levene-1012.mywire.org
"""

# Yedeklerin çekileceği 7 kaynak
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
        "message": "🛡️ Dokunulmazlar El ile Eklendi + Yedekler Güncellendi",
        "content": base64.b64encode(icerik.encode("utf-8")).decode("utf-8"),
        "sha": sha
    }
    requests.put(url, json=data, headers=headers)

def update_m3u():
    _, sha = github_dosya_oku()
    
    # Listeyi Dokunulmazlarla başlatıyoruz
    final_liste = ["#EXTM3U", DOKUNULMAZ_LISTE.strip()]
    eklenen_linkler = set(["http://96587.premiumstream.in:80", "http://uro-levene-1012.mywire.org"])

    pattern = r"(#EXTINF:[^\n]*),([^\n]*)\n(https?://[^\n]*)"

    # 7 Kaynaktan yeni linkleri topla
    for s_url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(s_url, timeout=10)
            r.encoding = 'utf-8'
            matches = re.findall(pattern, r.text)
            for ext_info, ch_name, url in matches:
                link = url.strip()
                if link not in eklenen_linkler:
                    final_liste.append(f"{ext_info},{ch_name.strip()}\n{link}")
                    eklenen_linkler.add(link)
        except:
            continue

    # Dosyayı yaz
    github_dosya_yaz("\n".join(final_liste), sha)
    print("🚀 Dokunulmazlar çivi gibi çakıldı, yedekler altına eklendi!")

if __name__ == "__main__":
    update_m3u()
