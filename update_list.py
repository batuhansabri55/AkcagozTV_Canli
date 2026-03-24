import requests
import re
import base64
import os

# --- AYARLAR ---
GITHUB_TOKEN = os.environ.get('GH_TOKEN') 
REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

# --- 1. DOKUNULMAZLAR (Hic degismez) ---
DOKUNULMAZ_BLOK = """#EXTINF:-1,--- PREMIUM STREAM ---
http://96587.premiumstream.in:80
#EXTINF:-1,--- MYWIRE STREAM ---
http://uro-levene-1012.mywire.org"""

# --- 2. KUTSAL ISIMLER (Sadece bunlar gecebilir) ---
KUTSAL_ISIMLER = """
TRT1,ATV,TV8,SHOW TV,KANAL D,STAR TV,NowTV,BEYAZ TV,KANAL 7,TEVE 2,A2,360 TV,TV8.5,FLASH TV,TRT 2,A HABER,CNN TURK,HABER TURK,NTV,HABER GLOBAL,TRT HABER,ULKE TV,KRT TV,HALK TV,TV100,SÖZCÜ TV,24 TV,TVNET,EKOL TV,BLOOMBERGHT,TGRT HABER,TELE 1,APARA,NATIONAL GEOGRAPHIC,NAT GEO WILD,DMAX,TLC,BEIN GURME,BEIN IZ,DISCOVERY,TRT BELGESEL,BBC Earth,SINEMA TV,FILMBOX,beIN Movies,FX,Dizismart,TRT COCUK,MINIKA,CARTOON NETWORK,NICKELODEON,beIN SPORTS,S Sport,TIVIBUSPORT,SPORSMART,Eurosport,TRT SPOR,Tabii Spor,EXXEN,FBTV
"""
arama_listesi = [n.strip().upper() for n in KUTSAL_ISIMLER.split(",") if n.strip()]

# --- 3. KAYNAKLAR ---
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
    data = {"message": "🧹 Liste Temizlendi ve Suzuldu", "content": base64.b64encode(icerik.encode("utf-8")).decode("utf-8"), "sha": sha}
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
                # HEM isim listede olacak HEM DE link yeni olacak
                if any(hedef in isim for hedef in arama_listesi):
                    if link not in eklenen_linkler:
                        final_liste.append(f"{ext_info},{ch_name.strip()}\n{link}")
                        eklenen_linkler.add(link)
        except: continue

    github_dosya_yaz("\n".join(final_liste), sha)

if __name__ == "__main__":
    update_m3u()
