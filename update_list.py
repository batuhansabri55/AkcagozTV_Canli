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

# --- 2. SIKI SÜZGEÇ (Sadece bu anahtar kelimeler geçebilir) ---
# Listeyi daraltmak için sadece en önemli kanalları buraya aldım
KUTSAL_ISIMLER = [
    "TRT 1", "ATV", "TV8", "SHOW TV", "KANAL D", "STAR TV", "NOW", "BEYAZ TV", 
    "KANAL 7", "TEVE2", "A2", "360", "FLASH", "A HABER", "CNN TURK", "HABER TURK", 
    "NTV", "HABER GLOBAL", "TRT HABER", "SÖZCÜ TV", "HALK TV", "TELE1", "KRT", 
    "BEIN", "SPORT", "SSPORT", "TIVIBU", "EXXEN", "NAT GEO", "DISCOVERY", "TLC", 
    "DMAX", "SINEMA", "MOVIES", "TRT COCUK", "MINIKA", "CARTOON"
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
    return r.json()['sha'] if r.status_code == 200 else None

def github_dosya_yaz(icerik, sha):
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    data = {"message": "🧹 Sıkı Süzgeç Uygulandı", "content": base64.b64encode(icerik.encode("utf-8")).decode("utf-8"), "sha": sha}
    requests.put(url, json=data, headers=headers)

def update_m3u():
    sha = github_dosya_oku()
    final_liste = ["#EXTM3U", DOKUNULMAZ_BLOK]
    eklenen_linkler = {"96587.premiumstream.in", "uro-levene-1012.mywire.org"}
    pattern = r"(#EXTINF:[^\n]*),([^\n]*)\n(https?://[^\n]*)"

    for s_url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(s_url, timeout=10)
            matches = re.findall(pattern, r.text)
            for ext_info, ch_name, url in matches:
                isim = ch_name.strip().upper()
                link = url.strip()
                # Sadece süzgeçteki kelimelerden biri varsa ekle
                if any(hedef in isim for hedef in KUTSAL_ISIMLER):
                    if link not in eklenen_linkler:
                        # Link set'ine sadece hostname'i ekleyerek aynı kanalın farklı linklerini de süzebiliriz
                        final_liste.append(f"{ext_info},{ch_name.strip()}\n{link}")
                        eklenen_linkler.add(link)
        except: continue

    github_dosya_yaz("\n".join(final_liste), sha)

if __name__ == "__main__":
    update_m3u()
