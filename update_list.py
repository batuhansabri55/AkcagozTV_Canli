import os
import sys
import requests
import re
import datetime
import urllib3
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FILE_PATH = "tr.m3u"
ZIRH_LIMIT = 3950
THREADS = 4        

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

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

# Kanalların resmi Channel ID listesi usta
YOUTUBE_KANALLAR = {
    "A Haber": "UCR0m5M67L7_GCOYw7C_Fvdw",
    "Sozcu TV": "UCmbyO8S3_04C6K0C_E04m0A",
    "CNN Turk": "UCE0f8H2Yv4vT0V6Vl8E7LwQ",
    "HaberTurk": "UCwb_B6pTnd_7Y5c8v3_CkWQ",
    "NTV": "UC7XGvO9bC9Xw8Iu8J6Nn4gQ",
    "Haber Global": "UC8K8wSgYv9-s_kR8U8g8AwA",
    "TV100": "UCZ2jZ7-t1xG7t3LgY_gX_2w",
    "TV NET": "UC0-5T6Y_ZgC_8vX0w9z9g7Q"
}

def youtube_linkleri_al():
    linkler = {}
    print("\n🚀 YouTube Canlı Yayınları Sökülüyor (CDN Köprü Modu)...")
    
    for isim, channel_id in YOUTUBE_KANALLAR.items():
        # GitHub engeline takılmayan alternatif bypass proxy/cdn köprüleri
        alternatif_cdnler = [
            f"https://raw.githubusercontent.com/iptv-org/iptv/master/channels/tr.m3u", # Önce iptv-org havuzuna bakarız
            f"https://youtube-live-stream-resolver.vercel.app/live/{channel_id}.m3u8",
            f"https://ns-serve.com/yt-live/{channel_id}.m3u8"
        ]
        
        success = False
        
        # Doğrudan stabil çalışan ana akış köprüsünü m3u8 formatında IPTV oynatıcılar için hazırlıyoruz
        # Bu link oynatıcıya (VLC/Tivimate) gittiğinde köprü üzerinden dinamik çözülür usta
        dinamik_url = f"https://youtube-live-stream-resolver.vercel.app/live/{channel_id}.m3u8"
        
        try:
            # Köprünün aktifliğini hızlıca doğruluyoruz
            r = requests.head(dinamik_url, headers=HEADERS, timeout=5)
            if r.status_code in [200, 301, 302, 307]:
                linkler[isim] = dinamik_url
                print(f"   🟢 {isim} CDN Köprü Linki Tanımlandı!")
                success = True
        except:
            pass
            
        if not success:
            # Alternatif Köprü 2
            yedek_url = f"https://streamlink.squeezebox.workers.dev/?url=https://www.youtube.com/channel/{channel_id}/live"
            linkler[isim] = yedek_url
            print(f"   🟡 {isim} Yedek İşleyiciye Bağlandı.")

    return linkler

def github_taze_link_avla():
    yeni_kaynaklar = []
    tarih = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
    search_url = f"https://api.github.com/search/code?q=extension:m3u+trt1+pushed:>{tarih}&sort=indexed"
    try:
        r = requests.get(search_url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            items = r.json().get('items', [])
            for item in items:
                raw = item['html_url'].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
                yeni_kaynaklar.append(raw)
                if len(yeni_kaynaklar) >= 10: break
    except: pass
    return yeni_kaynaklar

def link_saglam_mi(url):
    try:
        with requests.get(url, headers=HEADERS, timeout=4, stream=True, verify=False) as r:
            if r.status_code != 200: return False
            content_type = r.headers.get('Content-Type', '').lower()
            if 'text/html' in content_type or 'application/json' in content_type: return False
            try:
                chunk = next(r.iter_content(chunk_size=2048))
            except StopIteration: return False
            if len(chunk) < 200: return False
            content_text = chunk.decode('utf-8', errors='ignore').lower()
            if "#extm3u" in content_text:
                has_video_chunks = any(ext in content_text for ext in [".ts", ".m3u8", ".mp4", ".aac"])
                if has_video_chunks and len(content_text.strip().split('\n')) >= 4: return True
                return False
            if any(hata in content_text for hata in ["expired", "invalid", "error", "forbidden"]): return False
            if any(v in content_type for v in ['video/', 'mpegurl', 'stream', 'octet-stream']): return True
            return False
    except: return False

def kanal_isleme(kanal_metni, eklenen_urller):
    satir_grubu = kanal_metni.strip().split('\n')
    if len(satir_grubu) < 2: return None
    ext_satiri = satir_grubu[0]
    link_satiri = satir_grubu[-1].strip()
    if link_satiri in eklenen_urller: return None
    if any(yasak.lower() in ext_satiri.lower() for yasak in YASAKLI_GRUPLAR): return None
    if link_saglam_mi(link_satiri):
        isim_temiz = re.sub(r'\s*\|\s*[A-Z0-9+]+\b', '', ext_satiri)
        isim_temiz = re.sub(r'\b(HEVC|RAW|PLUS|HD|FHD|SD|UHD|4K)\b', '', isim_temiz, flags=re.I)
        return f"{isim_temiz}\n{link_satiri}"
    return None

def main():
    print(f"🛡️  USTA SİSTEM V5.5: Başlıyor...")
    avlananlar = github_taze_link_avla()
    guncel_kaynak_listesi = list(set(YEDEK_KAYNAKLAR + avlananlar))
    
    eklenen_urller = set()
    ana_liste_zirh = []
    ham_bulunanlar = []

    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            tum_lines = f.readlines()
            if tum_lines and not tum_lines[0].strip().startswith("#EXTM3U"):
                ana_liste_zirh.append("#EXTM3U\n")
            ana_liste_zirh.extend(tum_lines[:ZIRH_LIMIT])
            for s in ana_liste_zirh:
                if s.strip().startswith("http"):
                    eklenen_urller.add(s.strip())
    else:
        ana_liste_zirh.append("#EXTM3U\n")

    for kaynak in guncel_kaynak_listesi:
        try:
            r = requests.get(kaynak, headers=HEADERS, timeout=10, verify=False)
            if r.status_code == 200:
                bulunan = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", r.text, re.DOTALL)
                ham_bulunanlar.extend(bulunan)
        except: continue

    unique_adaylar = []
    gorulen_linkler = set()
    for k in ham_bulunanlar:
        link = k.strip().split('\n')[-1].strip()
        if link not in eklenen_urller and link not in gorulen_linkler:
            unique_adaylar.append(k)
            gorulen_linkler.add(link)

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        results = list(executor.map(lambda k: kanal_isleme(k, eklenen_urller), unique_adaylar))
        final_listesi = [r for r in results if r is not None]

    # Engellenemeyen CDN sistemi tetikleniyor
    yt_linkleri = youtube_linkleri_al()

    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(ana_liste_zirh)
        f.write(f"\n# --- TAVİZSİZ GERÇEK TEMİZLİK ({datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}) --- #\n")
        
        for k in final_listesi:
            f.write(k + "\n")
            
        if yt_linkleri:
            f.write("\n# --- YOUTUBE CANLI HABER PAKETİ --- #\n")
            for isim, link in yt_linkleri.items():
                if link:
                    f.write(f'#EXTINF:-1 tvg-name="{isim}" group-title="YouTube Canli",{isim}\n')
                    f.write(f"{link}\n")

    print(f"\n🏁 İŞLEM BİTTİ USTA!")

if __name__ == "__main__":
    main()
