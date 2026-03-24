import requests
import re
import base64
import os

# --- AYARLAR ---
GITHUB_TOKEN = os.environ.get('GH_TOKEN') 
REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

# ASLA DOKUNULMAYACAK ANA KAYNAKLARIN (Bunlar her zaman en üstte kalacak)
DOKUNULMAZ_URL_1 = "96587.premiumstream.in"
DOKUNULMAZ_URL_2 = "uro-levene-1012.mywire.org"

# 7 Güncel Kaynak (Yeni linkler buralardan gelecek)
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
        "message": "🛡️ Özel Listeler Başa Alındı + Yedek Linkler Eklendi",
        "content": base64.b64encode(icerik.encode("utf-8")).decode("utf-8"),
        "sha": sha
    }
    requests.put(url, json=data, headers=headers)

def update_m3u():
    mevcut_icerik, sha = github_dosya_oku()
    if not mevcut_icerik: return

    dokunulmaz_kanallar = []
    eklenen_linkler = set()
    final_liste = ["#EXTM3U"]

    # 1. ADIM: Mevcut dosyadaki dokunulmaz adresleri ayıkla
    # (Senin özel linklerini kaybetmemek için hafızaya alıyoruz)
    pattern = r"(#EXTINF:[^\n]*),([^\n]*)\n(https?://[^\n]*)"
    mevcut_matches = re.findall(pattern, mevcut_icerik)
    
    for ext_info, ch_name, url in mevcut_matches:
        link = url.strip()
        if DOKUNULMAZ_URL_1 in link or DOKUNULMAZ_URL_2 in link:
            dokunulmaz_kanallar.append(f"{ext_info},{ch_name.strip()}\n{link}")
            eklenen_linkler.add(link)

    # Dokunulmazları listenin en başına ekle
    final_liste.extend(dokunulmaz_kanallar)
    print(f"💎 {len(dokunulmaz_kanallar)} adet özel kanal korumaya alındı.")

    # 2. ADIM: 7 Kaynaktan yeni ne varsa topla ve altına ekle
    yeni_eklenen = 0
    for s_url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(s_url, timeout=10)
            matches = re.findall(pattern, r.text)
            for ext_info, ch_name, url in matches:
                link = url.strip()
                if link not in eklenen_linkler:
                    final_liste.append(f"{ext_info},{ch_name.strip()}\n{link}")
                    eklenen_linkler.add(link)
                    yeni_eklenen += 1
        except: continue

    # 3. ADIM: Dosyayı GitHub'a gönder
    github_dosya_yaz("\n".join(final_liste), sha)
    print(f"🚀 İşlem bitti! Dokunulmazlar yerinde, {yeni_eklenen} yeni link eklendi.")

if __name__ == "__main__":
    update_m3u()
