import requests
import re
import base64
import os

# --- AYARLAR ---
# GitHub'da secret ismin neyse onu buraya yaz (Genelde GH_TOKEN kullanılır)
GITHUB_TOKEN = os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')
REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

# Bu linkler asla silinmez, her zaman listenin en başında kalır
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
    isim = re.sub(r'\|tr\||hd|fhd|sd|4k|canli|tr:|haber|ulusal|belgesel', '', isim)
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
        "message": "♻️ VIP Koruma & Akıllı Yedekleme",
        "content": base64.b64encode(icerik.encode("utf-8")).decode("utf-8"),
        "sha": sha
    }
    r = requests.put(url, json=data, headers=headers)
    return r.status_code

def update_m3u():
    mevcut_icerik, sha = github_dosya_oku()
    if not sha: 
        print("❌ Dosya GitHub'dan okunamadı! Token veya Repo hatası.")
        return

    yeni_liste = ["#EXTM3U"]
    eklenen_linkler = set()
    aranacak_kanallar = {} 

    # Regex: #EXTINF satırını ve altındaki linki blok olarak yakalar
    pattern = r"(#EXTINF:[^\n]*),([^\n]*)\n(https?://[^\n]*)"

    # 1. ADIM: Mevcut dosyadaki DOKUNULMAZ kanalları (1800+ link) ayıkla ve koru
    matches = re.findall(pattern, mevcut_icerik)
    for ext_info, ch_name, url in matches:
        link = url.strip()
        if any(d in link.lower() for d in DOKUNULMAZLAR):
            yeni_liste.append(f"{ext_info},{ch_name.strip()}\n{link}")
            eklenen_linkler.add(link)
            
            # Eski koddaki mantık: Bu kanalın ismini yedek araması için hafızaya al
            temiz = isim_normalize(ch_name)
            if temiz:
                aranacak_kanallar[temiz] = ch_name.strip()

    print(f"📌 {len(eklenen_linkler)} dokunulmaz link korundu. Yedekler aranıyor...")

    # 2. ADIM: Yedek kaynaklardan SADECE senin listende olan isimleri çek
    for s_url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(s_url, timeout=12)
            r.encoding = 'utf-8'
            if r.status_code == 200:
                y_matches = re.findall(pattern, r.text)
                for y_ext, y_name, y_url in y_matches:
                    y_link = y_url.strip()
                    y_temiz = isim_normalize(y_name)
                    
                    # EĞER yedek kanal bizim ana listemizde varsa ve link yeniyse ekle
                    if y_temiz in aranacak_kanallar and y_link not in eklenen_linkler:
                        ana_isim = aranacak_kanallar[y_temiz]
                        yeni_liste.append(f"{y_ext},{ana_isim}\n{y_link}")
                        eklenen_linkler.add(y_link)
        except:
            continue

    # 3. ADIM: GitHub'a Yaz
    final_m3u = "\n".join(yeni_liste)
    durum = github_dosya_yaz(final_m3u, sha)
    
    if durum in [200, 201]:
        print(f"🚀 Başarılı! Toplam {len(eklenen_linkler)} kanal/yedek dosyaya yazıldı.")
    else:
        print(f"❌ Yazma hatası! GitHub Hata Kodu: {durum}")

if __name__ == "__main__":
    update_m3u()
