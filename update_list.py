import requests
import re
import base64
import os

# --- AYARLAR ---
GITHUB_TOKEN = os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')
REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

# Senin asıl kanallarını tanıyan anahtar kelimeler (Zırhlı Liste)
DOKUNULMAZLAR = ["premiumstream.in", "workers.dev", "mywire.org", "token=DeaTHLesS", "goldvod.site", "trt.com.tr", "turknet.ercdn.net", "daioncdn.net"]

# 5300 LİNKİN GELDİĞİ 7 KAYNAK BURASI (YEDEKLER)
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

def main():
    # 1. GitHub'daki Mevcut Dosyayı Al (Rehber olarak kullanacağız)
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print("❌ Dosya okunamadı!")
        return

    mevcut_icerik = base64.b64decode(r.json()['content']).decode('utf-8')
    sha = r.json()['sha']

    yeni_liste = ["#EXTM3U"]
    eklenen_linkler = set()
    aranacak_kanallar = set()

    pattern = r"(#EXTINF:[^\n]+)\n+(https?://[^\s\n]+)"
    
    # 2. ÖNCE: Senin mevcut listendeki dokunulmazları ayıkla ve isimlerini hafızaya al
    matches = re.findall(pattern, mevcut_icerik)
    for info, link in matches:
        if any(d in link.lower() for d in DOKUNULMAZLAR):
            yeni_liste.append(f"{info}\n{link}")
            eklenen_linkler.add(link.strip())
            # İsim normalize edip "aranacaklar" listesine ekle
            name = info.split(',')[-1] if ',' in info else info
            aranacak_kanallar.add(isim_normalize(name))

    print(f"📌 {len(aranacak_kanallar)} asıl kanal için yedekler taranıyor...")

    # 3. SONRA: 7 Yedek Kaynağı Tara (Sadece senin listendekileri al)
    for s_url in YEDEK_KAYNAKLAR:
        try:
            res = requests.get(s_url, timeout=10)
            y_matches = re.findall(pattern, res.text)
            for y_info, y_link in y_matches:
                yl = y_link.strip()
                y_name = y_info.split(',')[-1] if ',' in y_info else y_info
                # Eğer bu kanal senin asıl listende varsa ve link yeniyse ekle
                if isim_normalize(y_name) in aranacak_kanallar and yl not in eklenen_linkler:
                    yeni_liste.append(f"{y_info}\n{yl}")
                    eklenen_linkler.add(yl)
        except: continue

    # 4. GitHub'a Geri Bas
    final_m3u = "\n".join(yeni_liste)
    data = {"message": "♻️ Liste Güncellendi (5300 -> 2500 Filtreli)", "content": base64.b64encode(final_m3u.encode("utf-8")).decode("utf-8"), "sha": sha}
    
    update_r = requests.put(url, json=data, headers=headers)
    if update_r.status_code in [200, 201]:
        print(f"✅ Başarılı! Toplam {len(eklenen_linkler)} kanal/yedek yazıldı.")
    else:
        print(f"❌ Yazma hatası: {update_r.text}")

if __name__ == "__main__":
    main()
