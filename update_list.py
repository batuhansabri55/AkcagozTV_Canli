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

def isim_normalize(isim):
    """Eşleşme için ismi en saf haline getirir."""
    if not isim: return ""
    isim = isim.lower()
    tr_map = str.maketrans("çığöşü", "cigosu")
    isim = isim.translate(tr_map)
    # Gereksiz tüm takıları ve karakterleri temizle
    isim = re.sub(r'\|tr\||hd|fhd|sd|4k|canli|tr:', '', isim)
    isim = re.sub(r'[^a-z0-9]', '', isim)
    return isim.strip()

def update_m3u():
    mevcut_icerik, sha = github_dosya_oku()
    if not sha: return

    yeni_liste = ["#EXTM3U"]
    eklenen_linkler = set()
    ana_kanallar = {} # Eşleşme için ana kanal isimlerini tutacağız

    pattern = r"(#EXTINF:[^\n]*),([^\n]*)\n(https?://[^\n]*)"

    # 1. ÖNCE ANA KANALLARI (DOKUNULMAZLARI) BELİRLE
    matches = re.findall(pattern, mevcut_icerik)
    for ext_info, ch_name, url in matches:
        link = url.strip()
        if any(d in link.lower() for d in DOKUNULMAZLAR):
            yeni_liste.append(f"{ext_info},{ch_name}\n{link}")
            eklenen_linkler.add(link)
            # Bu kanalın temizlenmiş ismini "aranacaklar" listesine ekle
            ana_kanallar[isim_normalize(ch_name)] = ch_name.strip()

    # 2. SADECE ANA KANALLARLA EŞLEŞEN YEDEKLERİ AL
    for s_url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(s_url, timeout=10)
            r.encoding = 'utf-8'
            y_matches = re.findall(pattern, r.text)
            for y_ext, y_name, y_url in y_matches:
                y_link = y_url.strip()
                y_temiz = isim_normalize(y_name)
                
                # EĞER bu yedek kanal bizim ana kanal listemizde Varsa ekle
                if y_temiz in ana_kanallar and y_link not in eklenen_linkler:
                    original_name = ana_kanallar[y_temiz]
                    yeni_liste.append(f"{y_ext},{original_name} (YEDEK)\n{y_link}")
                    eklenen_linkler.add(y_link)
        except: continue

    final_m3u = "\n".join(yeni_liste)
    github_dosya_yaz(final_m3u, sha)
    print(f"✅ Filtreleme Tamamlandı: {len(eklenen_linkler)} kanal/yedek dosyaya yazıldı.")
