import requests
import re
import base64
import os
from concurrent.futures import ThreadPoolExecutor

# --- AYARLAR ---
# GitHub Settings -> Secrets -> Actions kısmındaki GH_TOKEN'ı çeker
# ÖNEMLİ: workflow dosyasında (main.yml) bu değişkenin env olarak tanımlanması gerekir.
GITHUB_TOKEN = os.environ.get('GH_TOKEN') 
REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

# Bu linkler test edilmeden direkt listeye eklenir.
DOKUNULMAZLAR = ["premiumstream.in", "workers.dev", "mywire.org", "token=DeaTHLesS"]

# Kaynak listesi.
YEDEK_KAYNAKLAR = [
    "https://mth.tc/DsGo",
    "https://raw.githubusercontent.com/sultansmgr/smart/refs/heads/main/viziTV.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://streams.uzunmuhalefet.com/lists/tr.m3u"
]

def github_yukle(icerik):
    """Bulunan kanalları GitHub deposuna yükler."""
    if not GITHUB_TOKEN:
        print("❌ HATA: GH_TOKEN bulunamadı! Settings -> Secrets kısmını kontrol et.")
        return

    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}", 
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Mevcut dosyanın SHA bilgisini al (Güncelleme yapabilmek için şart)
    r = requests.get(url, headers=headers)
    sha = r.json().get('sha') if r.status_code == 200 else None

    data = {
        "message": "Otomatik Liste Guncelleme",
        "content": base64.b64encode(icerik.encode("utf-8")).decode("utf-8")
    }
    if sha: 
        data["sha"] = sha

    r = requests.put(url, json=data, headers=headers)
    if r.status_code in [200, 201]: 
        print(f"✅ GITHUB TAMAM! {FILE_PATH} dosyası başarıyla güncellendi.")
    else: 
        print(f"❌ YUKLEME HATASI: {r.status_code} - {r.text}")

def link_test_et(item):
    """Linklerin aktif olup olmadığını hızlıca kontrol eder."""
    info, url = item
    if any(ozel in url.lower() for ozel in DOKUNULMAZLAR): 
        return (info, url)
    try:
        # Hızlı test için 5 saniye zaman aşımı
        with requests.get(url, timeout=5, stream=True) as r:
            if r.status_code == 200: 
                return (info, url)
    except: 
        pass
    return None

def update_m3u():
    """Ana işleyiş: Kaynakları tara, test et ve yükle."""
    adaylar = []
    eklenen_linkler = set()
    
    print("🔄 Kaynaklar taranıyor...")
    for s_url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(s_url, timeout=10)
            if r.status_code == 200:
                # M3U formatındaki info ve url kısımlarını ayıkla
                matches = re.findall(r"(#EXTINF:[^\n]*)\n(http[^\n]*)", r.text.replace('\r', ''))
                for info, url in matches:
                    u = url.strip()
                    if u not in eklenen_linkler:
                        adaylar.append((info, u))
                        eklenen_linkler.add(u)
        except: 
            continue

    print(f"📡 Toplam {len(adaylar)} kanal bulundu. Test ediliyor...")
    
    # 30 koldan hızlıca test et (Multi-threading)
    with ThreadPoolExecutor(max_workers=30) as executor:
        sonuclar = list(filter(None, executor.map(link_test_et, adaylar)))

    print(f"✅ {len(sonuclar)} aktif kanal GitHub'a gönderiliyor...")
    
    output = "#EXTM3U\n" + "\n".join([f"{i}\n{u}" for i, u in sonuclar])
    github_yukle(output)

if __name__ == "__main__":
    update_m3u()
