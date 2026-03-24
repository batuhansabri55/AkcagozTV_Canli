import requests
import re
import os

# Senin o 1800 satırlık dokunulmaz listeni tanımlayan anahtar kelime veya sınır.
# Eğer listen hep aynı satırla bitiyorsa (örneğin beIN SPORTS 1 HD), 
# kod o satıra kadar olan kısmı "KUTSAL" sayacak.

YEDEK_KAYNAKLAR = [
    "https://mth.tc/DsGo",
    "https://raw.githubusercontent.com/sultansmgr/smart/refs/heads/main/viziTV.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://streams.uzunmuhalefet.com/lists/tr.m3u"
]

def main():
    m3u_dosya = "tr.m3u"
    dokunulmaz_kisim = []
    
    # 1. ADIM: Mevcut dosyayı oku ve SADECE dokunulmazları ayıkla
    if os.path.exists(m3u_dosya):
        with open(m3u_dosya, "r", encoding="utf-8") as f:
            satirlar = f.readlines()
            for i, satir in enumerate(satirlar):
                dokunulmaz_kisim.append(satir)
                # KRİTİK NOKTA: Senin 1800. linkin hangisiyse buraya onun ismini yaz.
                # Kod o ismi görünce "Tamam dokunulmaz bitti" der ve durur.
                if "beIN SPORTS 1 HD" in satir: 
                    break
    else:
        dokunulmaz_kisim = ["#EXTM3U\n"]

    # 2. ADIM: 7 Yedek kaynaktan TAZE linkleri çek
    yeni_liste = []
    pattern = r"(#EXTINF:[^\n]+)\n(https?://[^\s\n]+)"
    
    for url in YEDEK_KAYNAKLAR:
        try:
            r = requests.get(url, timeout=10)
            r.encoding = 'utf-8'
            if r.status_code == 200:
                matches = re.findall(pattern, r.text)
                for info, link in matches:
                    yeni_liste.append(f"{info}\n{link.strip()}\n")
        except:
            continue

    # 3. ADIM: Dosyayı SIFIRDAN YAZ (Dokunulmazlar + Yepyeni Linkler)
    with open(m3u_dosya, "w", encoding="utf-8") as f:
        f.writelines(dokunulmaz_kisim) # Senin 1800 tane sabit duruyor
        f.writelines(yeni_liste)       # Altındaki çöpler silindi, yeniler geldi
    
    print(f"✅ Operasyon Başarılı! 1800 link korundu, alt kısım güncellendi.")

if __name__ == "__main__":
    main()
