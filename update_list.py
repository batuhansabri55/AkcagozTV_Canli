import requests
import re
import base64
import os

# --- AYARLAR ---
# Eğer GH_TOKEN yoksa GitHub'ın kendi otomatik tokenını kullanır
GITHUB_TOKEN = os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')
REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

# Senin asla silinmeyecek kutsal linklerin
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

def isim_normalize(isim):
    if not isim: return ""
    isim = isim.lower()
    tr_map = str.maketrans("çığöşü", "cigosu")
    isim = isim.translate(tr_map)
    # Gereksiz her şeyi temizle
    isim = re.sub(r'\|tr\||hd|fhd|sd|4k|canli|tr:|haber|ulusal|belgesel', '', isim)
    isim = re.sub(r'[^a-z0-9]', '', isim)
    return isim.strip()

def github_dosya_oku():
    if not GITHUB_TOKEN:
        print("❌ HATA: Token bulunamadı!")
        return "", None
    
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            content = base64.b64decode(r.json()['content']).decode('utf-8')
            return content, r.json()['sha']
        else:
            print(f"❌ GitHub API Hatası: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"❌ Bağlantı Hatası: {e}")
    return "", None

def github_dosya_yaz(icerik, sha):
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    data = {
        "message": "♻️ Liste Guncellendi (Dokunulmazlar Korundu)",
        "content": base64.b64encode(icerik.encode("utf-8")).decode("utf-8"),
        "sha": sha
    }
    r = requests.put(url, json=data, headers=headers)
    return r.status_code

def update_m3u():
    mevcut_icerik, sha = github_dosya_oku()
    if not sha: return

    yeni_liste = ["#EXTM3U"]
    eklenen_linkler = set()
    aranacak_kanallar = {}

    # ESNEK REGEX: Hem virgüllü hem virgülsüz #EXTINF satırlarını yakalar
    # (#EXTINF:-1,Kanal Adı) veya (#EXTINF:-1 tvg-id="..." , Kanal Adı) fark etmez
    pattern = r"(#EXTINF:[^\n,]+(?:,[^\n]+)?)\n+(https?://[^\s\n]+)"

    # 1. ADIM: Mevcut 1800 linki tara, dokunulmazları ayır
    matches = re.findall(pattern, mevcut_icerik)
    for ext_info, url in matches:
        link = url.strip()
        if any(d in link.lower() for d in DOKUNULMAZLAR):
            yeni_liste.append(f"{ext_info}\n{link}")
            eklenen_linkler.add(link)
            
            # İsim kısmını yedek aramak için ayıkla (Virgülden sonrasını alır)
            ch_name = ext_info.split(',')[-1] if ',' in ext_info else ext_info
            temiz = isim_normalize(ch_name)
            if temiz:
                aranacak_kanallar[temiz] = ch_name.strip()

    print(f"💎 {len(eklenen_linkler)} dokunulmaz link zırhlandı.")

    # 2. ADIM: Yedeklerden taze linkleri çek (Sadece senin listendekileri)
    for s_url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(s_url, timeout=10)
            y_matches = re.findall(pattern, r.text)
            for y_info, y_url in y_matches:
                yl = y_url.strip()
                y_name = y_info.split(',')[-1] if ',' in y_info else y_info
                y_temiz = isim_normalize(y_name)
                
                if y_temiz in aranacak_kanallar and yl not in eklenen_linkler:
                    yeni_liste.append(f"{y_info}\n{yl}")
                    eklenen_linkler.add(yl)
        except: continue

    # 3. ADIM: GitHub'a Bas
    final_m3u = "\n".join(yeni_liste)
    durum = github_dosya_yaz(final_m3u, sha)
    
    if durum in [200, 201]:
        print("🚀 İşlem Tamam! Liste güncellendi.")
    else:
        print(f"⚠️ Hata Kodu: {durum}")

if __name__ == "__main__":
    update_m3u()
