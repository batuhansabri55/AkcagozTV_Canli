import requests
import re
import base64
import os

# --- AYARLAR ---
GITHUB_TOKEN = os.environ.get('GH_TOKEN') 
REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

# --- DOKUNULMAZ KELİMELER (Bu linkler asla silinmez/değişmez) ---
DOKUNULMAZLAR = ["premiumstream.in", "workers.dev", "mywire.org", "token=DeaTHLesS", "goldvod.site"]

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
        "message": "🔄 Yedekler Güncellendi (Dokunulmazlar Korundu)",
        "content": base64.b64encode(icerik.encode("utf-8")).decode("utf-8"),
        "sha": sha
    }
    requests.put(url, json=data, headers=headers)

def update_m3u():
    # 1. Mevcut tr.m3u dosyasını GitHub'dan oku
    mevcut_icerik, sha = github_dosya_oku()
    if not sha:
        print("❌ Dosya okunamadı!")
        return

    yeni_liste = ["#EXTM3U"]
    eklenen_linkler = set()

    # 2. ÖNCE DOKUNULMAZLARI AYIKLA VE KORU
    # Mevcut dosyadaki her bloğu tara, eğer dokunulmaz kelime geçiyorsa listeye ekle
    blocks = re.findall(r"(#EXTINF:[^\n]*)\n(http[^\n]*)", mevcut_icerik)
    for info, url in blocks:
        link = url.strip()
        if any(d in link.lower() for d in DOKUNULMAZLAR):
            yeni_liste.append(f"{info}\n{link}")
            eklenen_linkler.add(link)

    # 3. YEDEK KAYNAKLARDAN YENİ LİNKLERİ TOPLA
    for s_url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(s_url, timeout=10)
            matches = re.findall(r"(#EXTINF:[^\n]*)\n(http[^\n]*)", r.text.replace('\r', ''))
            for info, url in matches:
                link = url.strip()
                # Eğer link yeni ise ve dokunulmazlar arasında değilse ekle
                if link not in eklenen_linkler:
                    yeni_liste.append(f"{info}\n{link}")
                    eklenen_linkler.add(link)
        except: continue

    # 4. GÜNCEL LİSTEYİ GİTHUB'A GERİ YÜKLE
    final_m3u = "\n".join(yeni_liste)
    github_dosya_yaz(final_m3u, sha)
    print("🚀 İşlem tamam! D1 kullanılmadı, yedekler güncellendi.")

if __name__ == "__main__":
    update_m3u()
