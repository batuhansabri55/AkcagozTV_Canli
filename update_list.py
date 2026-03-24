import requests
import re
import base64
import os

# --- AYARLAR ---
GITHUB_TOKEN = os.environ.get('GH_TOKEN') 
REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

# Bu linkler asla silinmez, listenin en başında durur
DOKUNULMAZLAR = [
    "premiumstream.in", "workers.dev", "mywire.org", "token=DeaTHLesS", 
    "goldvod.site", "trt.com.tr", "turknet.ercdn.net", "daioncdn.net"
]

# Yedeklerin çekileceği ham listeler
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
    """Eşleşme için ismi en sade hale getirir (Örn: '|TR| KANAL D HD' -> 'kanald')"""
    if not isim: return ""
    isim = isim.lower()
    tr_map = str.maketrans("çığöşü", "cigosu")
    isim = isim.translate(tr_map)
    # Gereksiz ekleri ve karakterleri temizle
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
        "message": "♻️ Akıllı Filtreleme: Gereksiz kanallar temizlendi",
        "content": base64.b64encode(icerik.encode("utf-8")).decode("utf-8"),
        "sha": sha
    }
    requests.put(url, json=data, headers=headers)

def update_m3u():
    mevcut_icerik, sha = github_dosya_oku()
    if not sha: 
        print("❌ Dosya GitHub'dan okunamadı!")
        return

    yeni_liste = ["#EXTM3U"]
    eklenen_linkler = set()
    aranacak_kanallar = {} # Temiz isim -> Orijinal İsim eşleşmesi

    # M3U satırlarını yakalayan regex
    pattern = r"(#EXTINF:[^\n]*),([^\n]*)\n(https?://[^\n]*)"

    # 1. ADIM: Senin asıl listendeki (Dokunulmaz) kanalları belirle
    matches = re.findall(pattern, mevcut_icerik)
    for ext_info, ch_name, url in matches:
        link = url.strip()
        if any(d in link.lower() for d in DOKUNULMAZLAR):
            yeni_liste.append(f"{ext_info},{ch_name.strip()}\n{link}")
            eklenen_linkler.add(link)
            # Bu kanalın ismini temizleyip hafızaya al (Yedek ararken kullanacağız)
            temiz = isim_normalize(ch_name)
            if temiz:
                aranacak_kanallar[temiz] = ch_name.strip()

    print(f"📌 {len(aranacak_kanallar)} ana kanal için yedek aranıyor...")

    # 2. ADIM: Yedek kaynaklardan SADECE bizim listemizde olanları çek
    for s_url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(s_url, timeout=10)
            r.encoding = 'utf-8'
            y_matches = re.findall(pattern, r.text)
            for y_ext, y_name, y_url in y_matches:
                y_link = y_url.strip()
                y_temiz = isim_normalize(y_name)
                
                # EĞER yedek kanal bizim ana listemizde varsa ekle
                if y_temiz in aranacak_kanallar and y_link not in eklenen_linkler:
                    ana_isim = aranacak_kanallar[y_temiz]
                    # Worker'ın tanıması için ismi senin veritabanındakiyle aynı yapıyoruz
                    yeni_liste.append(f"{y_ext},{ana_isim}\n{y_link}")
                    eklenen_linkler.add(y_link)
        except Exception as e:
            continue

    final_m3u = "\n".join(yeni_liste)
    github_dosya_yaz(final_m3u, sha)
    print(f"🚀 İşlem Başarılı! Toplam {len(eklenen_linkler)} kanal/yedek m3u dosyasına yazıldı.")

if __name__ == "__main__":
    update_m3u()
