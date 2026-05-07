import requests
import re
import os
import datetime
import shutil
from concurrent.futures import ThreadPoolExecutor
import urllib3

# SSL Sertifika hatalarını görmezden gel (Bazı sağlam yayınlar için gerekli)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
ZIRH_LIMIT = 6210  # Bu satıra kadar olan kısma asla dokunulmaz ve linkleri yedeklere eklenmez
THREADS = 5        # Derin tarama için düşük hız (Sunucu engeline takılmamak için)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Icy-MetaData': '1'
}

# YASAKLI LİSTESİ (Grup adında bunlar geçiyorsa anında elenir)
YASAKLI_GRUPLAR = [
    "FreeShot", "Webteizle", "TR FILM", "ARZU FILM", "ERLER FILM", 
    "Taşacak Bu Deniz", "EZEL", "FilmMedya", "Keloğlan", "PolskieTV", 
    "MediabayTV", "SarkorTV", "GLWIZ", "PERSIAN", "GledaiTV", "RDS TV", 
    "TouchTV", "Slovakia", "Bulgaria", "Romania", "Azerbeycan",
    "Superxfilm", "CINEMAMOD", "Adult", "XXX"
]

YEDEK_KAYNAKLAR = [
    "https://streams.uzunmuhalefet.com/lists/tr.m3u",
    "https://tinyurl.com/ytpatron",
    "https://urlz.fr/v1Xo",
    "https://raw.githubusercontent.com/hayatiptv/iptv/master/index.m3u",
    "https://raw.githubusercontent.com/smartgmr/cdn/refs/heads/main/Perfect.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://tinyurl.com/bdd2tz6h",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u"
]

def link_saglam_mi(url):
    """VLC'DEKİ MRL HATALARINI SIFIRA İNDİREN DERİN KONTROL"""
    try:
        # stream=True ile sadece başlığı değil, veri akışını kontrol ediyoruz
        with requests.get(url, headers=HEADERS, timeout=12, stream=True, verify=False) as r:
            if r.status_code != 200:
                return False
            
            # Bağlantı kurulduktan sonra ilk veri paketini (chunk) çekmeye çalışıyoruz
            it = r.iter_content(chunk_size=1024)
            ilk_parca = next(it) 
            
            decoded_parca = ilk_parca.decode('utf-8', errors='ignore')
            
            # M3U8 ise içeriğinin dolu olduğunu (segment içerdiğini) doğrula
            if "#EXTM3U" in decoded_parca:
                valid_content = [".ts", ".m4s", "chunk", "mp4", "quality", "#EXT-X-STREAM-INF"]
                if not any(x in decoded_parca.lower() for x in valid_content):
                    return False
            
            return True
    except (StopIteration, Exception):
        return False

def kanal_isleme(kanal_metni, eklenen_urller):
    """Filtreleme, Temizleme ve Test İşlemi"""
    satir_grubu = kanal_metni.strip().split('\n')
    if len(satir_grubu) < 2: return None
    
    ext_satiri = satir_grubu[0]
    link_satiri = satir_grubu[-1].strip()
    
    # 1. MÜKERRER KONTROLÜ (Zırhlı listede varsa atla)
    if link_satiri in eklenen_urller:
        return None

    # 2. YASAKLI GRUP FİLTRESİ
    if any(yasak.lower() in ext_satiri.lower() for yasak in YASAKLI_GRUPLAR):
        return None

    # 3. DERİN CANLILIK TESTİ
    print(f"🔍 Analiz Ediliyor: {link_satiri[:50]}...")
    if link_saglam_mi(link_satiri):
        # Kanal İsim Temizliği
        isim_temiz = re.sub(r'\s*\|\s*[A-Z0-9+]+\b', '', ext_satiri)
        isim_temiz = re.sub(r'\b(HEVC|RAW|PLUS|HD|FHD|SD|UHD|4K)\b', '', isim_temiz, flags=re.I)
        
        if 'group-title="' not in isim_temiz:
            isim_temiz = isim_temiz.replace('#EXTINF:', '#EXTINF:-1 group-title="YEDEKLER",')
            
        print(f" ✅ TAMAM: {link_satiri[:40]}")
        return f"{isim_temiz}\n{link_satiri}"
    
    return None

def main():
    print(f"🚀 USTA SİSTEM BAŞLADI: {ZIRH_LIMIT} satır zırh altında.")
    
    # Mevcut m3u yedeğini al
    if os.path.exists(FILE_PATH):
        shutil.copyfile(FILE_PATH, FILE_PATH + ".bak")
        print(f"📦 Yedek Alındı: {FILE_PATH}.bak")

    eklenen_urller = set()
    ana_liste_zirh = []
    ham_bulunanlar = []

    # 1. ADIM: Zırhlı Bölgeyi Oku ve Hafızaya At (Mükerrer Engeli İçin)
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_lines = f.readlines()
            ana_liste_zirh = tum_lines[:ZIRH_LIMIT]
            for s in ana_liste_zirh:
                if s.strip().startswith("http"):
                    eklenen_urller.add(s.strip())
        print(f"🛡️  Zırhlı bölgedeki {len(eklenen_urller)} link muhafaza edildi, tekrar eklenmeyecek.")

    # 2. ADIM: Dış Kaynakları Tara
    for kaynak in YEDEK_KAYNAKLAR:
        try:
            print(f"📡 Kaynak taranıyor: {kaynak[:40]}...")
            r = requests.get(kaynak, headers=HEADERS, timeout=15, verify=False)
            if r.status_code == 200:
                bulunan = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", r.text, re.DOTALL)
                ham_bulunanlar.extend(bulunan)
        except: continue

    # 3. ADIM: Kendi İçinde Mükerrerleri Temizle
    unique_adaylar = []
    gorulen_linkler = set()
    for k in ham_bulunanlar:
        link = k.strip().split('\n')[-1].strip()
        if link not in eklenen_urller and link not in gorulen_linkler:
            unique_adaylar.append(k)
            gorulen_linkler.add(link)

    print(f"💎 {len(unique_adaylar)} yeni aday bulundu. Derin tarama başlıyor (Zaman alabilir)...")

    # 4. ADIM: Derin Tarama ve Filtreleme
    final_listesi = []
    # eklenen_urller setini fonksiyona iletiyoruz
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        # map fonksiyonuna eklenen_urller'i de dahil etmek için bir wrapper veya lambda kullanıyoruz
        results = list(executor.map(lambda k: kanal_isleme(k, eklenen_urller), unique_adaylar))
        final_listesi = [r for r in results if r is not None]

    # 5. ADIM: Dosyayı Yeniden Oluştur
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(ana_liste_zirh)
        f.write(f"\n# --- DERIN TARANMIS %100 CANLI YEDEKLER ({datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}) --- #\n")
        for k in final_listesi:
            f.write(k + "\n")

    print(f"\n🏁 İŞLEM BİTTİ USTA!")
    print(f"✅ Eklenen Yeni Sağlam Kanal: {len(final_listesi)}")
    print(f"⚠️ Mükerrer olduğu için veya ölü olduğu için elenen yüzlerce link oldu.")
    print(f"📄 Liste '{FILE_PATH}' dosyasına kaydedildi.")

if __name__ == "__main__":
    main()
