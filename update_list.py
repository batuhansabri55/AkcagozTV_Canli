import requests
import re
import base64
import os

# --- AYARLAR ---
GITHUB_TOKEN = os.environ.get('GH_TOKEN') 
REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

DOKUNULMAZLAR = [
    "premiumstream.in", "workers.dev", "mywire.org", "token=DeaTHLesS", 
    "goldvod.site", "trt.com.tr", "turknet.ercdn.net", "daioncdn.net"
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

def isim_temizle(isim):
    """Kanal isimlerini Worker'ın anlayacağı hale getirir."""
    if not isim: return ""
    isim = isim.lower()
    # Türkçe karakterleri çevir
    tr_map = str.maketrans("çığöşü", "cigosu")
    isim = isim.translate(tr_map)
    # Gereksiz ekleri temizle (Worker eşleşmesi için kritik)
    isim = re.sub(r'\b(fhd|hd|sd|4k|hevc|turkiye|tr|canli)\b', '', isim)
    # Sadece harf ve rakam bırak
    isim = re.sub(r'[^a-z0-9]', '', isim)
    return isim.strip()

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
        "message": "🔄 İsim Standardizasyonu & Yedekler Güncellendi",
        "content": base64.b64encode(icerik.encode("utf-8")).decode("utf-8"),
        "sha": sha
    }
    requests.put(url, json=data, headers=headers)

def update_m3u():
    mevcut_icerik, sha = github_dosya_oku()
    if not sha: return

    yeni_liste = ["#EXTM3U"]
    eklenen_linkler = set()
    # Daha esnek regex: #EXTINF ve URL arasındaki her şeyi yakalar
    pattern = r"(#EXTINF:[^\n]*),([^\n]*)\n(https?://[^\n]*)"

    # 1. Dokunulmazları Koru
    matches = re.findall(pattern, mevcut_icerik)
    for ext_info, ch_name, url in matches:
        link = url.strip()
        if any(d in link.lower() for d in DOKUNULMAZLAR):
            yeni_liste.append(f"{ext_info},{ch_name}\n{link}")
            eklenen_linkler.add(link)

    # 2. Yedekleri Temizleyerek Ekle
    for s_url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(s_url, timeout=15)
            r.encoding = 'utf-8' # Karakter bozulmasını önle
            matches = re.findall(pattern, r.text)
            for ext_info, ch_name, url in matches:
                link = url.strip()
                if link not in eklenen_linkler:
                    # İsimdeki karmaşayı temizle ki Worker tanısın
                    temiz_isim = ch_name.strip().upper() 
                    yeni_liste.append(f"{ext_info},{temiz_isim}\n{link}")
                    eklenen_linkler.add(link)
        except: continue

    final_m3u = "\n".join(yeni_liste)
    github_dosya_yaz(final_m3u, sha)
    print(f"🚀 {len(eklenen_linkler)} benzersiz yedek işlendi.")

if __name__ == "__main__":
    update_m3u()
