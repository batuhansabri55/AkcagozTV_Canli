import requests
import re
import base64
import os

# --- AYARLAR ---
GITHUB_TOKEN = os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')
REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

# Senin asıl kanallarını (D1/Dokunulmaz) tanıyan zırhlı liste
DOKUNULMAZLAR = ["premiumstream.in", "workers.dev", "mywire.org", "token=DeaTHLesS", "goldvod.site", "trt.com.tr", "turknet.ercdn.net", "daioncdn.net"]

# 5300 LİNKİN GELDİĞİ 7 ANA KAYNAK (YEDEKLER)
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
    # Gereksiz her şeyi temizle (Kanal D HD -> kanald)
    isim = re.sub(r'\|tr\||hd|fhd|sd|4k|canli|tr:|haber|ulusal|belgesel', '', isim)
    isim = re.sub(r'[^a-z0-9]', '', isim)
    return isim.strip()

def main():
    if not GITHUB_TOKEN:
        print("❌ HATA: Token bulunamadı! GitHub Secrets ayarını kontrol et.")
        return

    # 1. GitHub'daki Mevcut Dosyayı Oku (SHA ve Mevcut Linkler İçin)
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print(f"❌ Dosya Çekilemedi! Hata: {r.status_code}")
        return

    mevcut_icerik = base64.b64decode(r.json()['content']).decode('utf-8')
    sha = r.json()['sha']

    yeni_liste = ["#EXTM3U"]
    eklenen_linkler = set()
    aranacak_kanallar = set()

    # Regex: Hem virgüllü hem virgülsüz satırları yakalar
    pattern = r"(#EXTINF:[^\n]+)\n+(https?://[^\s\n]+)"
    
    # 2. ÖNCE: Senin mevcut listendeki dokunulmazları (1800+) zırhla
    matches = re.findall(pattern, mevcut_icerik)
    for info, link in matches:
        l_strip = link.strip()
        if any(d in l_strip.lower() for d in DOKUNULMAZLAR):
            yeni_liste.append(f"{info}\n{l_strip}")
            eklenen_linkler.add(l_strip)
            # Bu kanalın ismini "rehber" olarak kaydet
            ch_name = info.split(',')[-1] if ',' in info else info
            aranacak_kanallar.add(isim_normalize(ch_name))

    print(f"📌 {len(aranacak_kanallar)} asıl kanal korundu. Yedeklerden süzme yapılıyor...")

    # 3. SONRA: 7 Yedek Kaynağı Tara (Sadece senin listendekileri içeri al)
    for s_url in YEDEK_KAYNAKLAR:
        try:
            res = requests.get(s_url, timeout=12)
            y_matches = re.findall(pattern, res.text)
            for y_info, y_url in y_matches:
                yl = y_url.strip()
                yn = y_info.split(',')[-1] if ',' in y_info else y_info
                # EĞER bu kanal senin asıl listende varsa ve link yeniyse ekle
                if isim_normalize(yn) in aranacak_kanallar and yl not in eklenen_linkler:
                    yeni_liste.append(f"{y_info}\n{yl}")
                    eklenen_linkler.add(yl)
        except: continue

    # 4. GITHUB'A GERİ YÜKLE
    final_m3u = "\n".join(yeni_liste)
    data = {
        "message": "♻️ Akıllı Filtreleme: 5300 -> 2500 (Eksiksiz Yedekli)",
        "content": base64.b64encode(final_m3u.encode("utf-8")).decode("utf-8"),
        "sha": sha
    }
    
    update_r = requests.put(url, json=data, headers=headers)
    if update_r.status_code in [200, 201]:
        print(f"✅ İŞLEM BAŞARILI! Toplam {len(eklenen_linkler)} kanal/yedek m3u dosyasına yazıldı.")
    else:
        print(f"❌ YAZMA HATASI: {update_r.text}")

if __name__ == "__main__":
    main()
