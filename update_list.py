import requests
import re
import os
import datetime
import shutil
import urllib3
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin

# SSL UYARILARINI KAPAT
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# =========================
# AYARLAR
# =========================

FILE_PATH = "tr.m3u"

# İlk kaç satır korunacak
ZIRH_LIMIT = 3350

# Thread sayısı
THREADS = 4

# Timeout
CONNECT_TIMEOUT = 8
READ_TIMEOUT = 15

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Connection": "keep-alive"
}

YASAKLI_GRUPLAR = [
    "FreeShot",
    "Webteizle",
    "TR FILM",
    "ARZU FILM",
    "ERLER FILM",
    "Taşacak Bu Deniz",
    "EZEL",
    "FilmMedya",
    "Keloğlan",
    "PolskieTV",
    "MediabayTV",
    "SarkorTV",
    "GLWIZ",
    "PERSIAN",
    "GledaiTV",
    "RDS TV",
    "TouchTV",
    "Slovakia",
    "Bulgaria",
    "Romania",
    "Azerbeycan",
    "Superxfilm",
    "CINEMAMOD",
    "Adult",
    "XXX"
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

# =========================
# SESSION
# =========================

session = requests.Session()
session.headers.update(HEADERS)

# =========================
# LINK TEST
# =========================

def link_saglam_mi(url):
    """
    GERÇEK IPTV TESTİ:
    - URL açılıyor mu
    - M3U8 geçerli mi
    - TS segment geliyor mu
    - Veri akışı var mı
    """

    try:
        with session.get(
            url,
            timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            stream=True,
            verify=False,
            allow_redirects=True
        ) as r:

            if r.status_code != 200:
                return False

            content_type = r.headers.get("Content-Type", "").lower()

            # =========================
            # M3U8 TESTİ
            # =========================

            if (
                "mpegurl" in content_type
                or "m3u8" in url.lower()
            ):

                text = ""

                for chunk in r.iter_content(chunk_size=2048):

                    if chunk:
                        try:
                            text += chunk.decode("utf-8", errors="ignore")
                        except:
                            pass

                    if len(text) > 12000:
                        break

                if "#EXTM3U" not in text:
                    return False

                lines = []

                for line in text.splitlines():

                    line = line.strip()

                    if not line:
                        continue

                    if line.startswith("#"):
                        continue

                    lines.append(line)

                if not lines:
                    return False

                ilk_segment = lines[0]

                # Relative URL düzelt
                if not ilk_segment.startswith("http"):
                    ilk_segment = urljoin(url, ilk_segment)

                # =========================
                # TS SEGMENT TESTİ
                # =========================

                with session.get(
                    ilk_segment,
                    timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
                    stream=True,
                    verify=False,
                    allow_redirects=True
                ) as ts:

                    if ts.status_code != 200:
                        return False

                    veri = next(ts.iter_content(4096), None)

                    if not veri:
                        return False

                    # Çok küçük veri sahte olabilir
                    if len(veri) < 1000:
                        return False

                return True

            # =========================
            # DIRECT VIDEO TESTİ
            # =========================

            veri = next(r.iter_content(4096), None)

            if not veri:
                return False

            if len(veri) < 1000:
                return False

            return True

    except:
        return False

# =========================
# KANAL İŞLEME
# =========================

def kanal_isleme(kanal_metni, mevcut_linkler):

    try:

        satirlar = kanal_metni.strip().splitlines()

        if len(satirlar) < 2:
            return None

        extinf = satirlar[0].strip()
        url = satirlar[-1].strip()

        # URL geçersiz
        if not url.startswith("http"):
            return None

        # Mükerrer
        if url in mevcut_linkler:
            return None

        # Yasaklı grup
        if any(y.lower() in extinf.lower() for y in YASAKLI_GRUPLAR):
            return None

        # Test
        if not link_saglam_mi(url):
            print(f" ❌ ÖLÜ: {url[:60]}")
            return None

        # İsim temizleme
        temiz = re.sub(
            r'\s*\|\s*[A-Z0-9+]+\b',
            '',
            extinf
        )

        temiz = re.sub(
            r'\b(HEVC|RAW|PLUS|HD|FHD|SD|UHD|4K)\b',
            '',
            temiz,
            flags=re.I
        )

        if 'group-title="' not in temiz:
            temiz = temiz.replace(
                '#EXTINF:',
                '#EXTINF:-1 group-title="YEDEKLER",'
            )

        print(f" ✅ CANLI: {url[:60]}")

        return f"{temiz}\n{url}"

    except:
        return None

# =========================
# M3U PARSER
# =========================

def m3u_parse(text):

    pattern = r'(#EXTINF:.*?\n.*?http[^\n\r]+)'

    return re.findall(
        pattern,
        text,
        re.DOTALL | re.IGNORECASE
    )

# =========================
# ANA SİSTEM
# =========================

def main():

    print("\n🛡️ IPTV DERİN TEMİZLİK BAŞLADI\n")

    # YEDEK OLUŞTUR
    if os.path.exists(FILE_PATH):

        backup_name = (
            FILE_PATH +
            "." +
            datetime.datetime.now().strftime("%Y%m%d_%H%M%S") +
            ".bak"
        )

        shutil.copyfile(FILE_PATH, backup_name)

        print(f"📦 YEDEK ALINDI: {backup_name}")

    mevcut_linkler = set()
    ana_zirh = []

    # =========================
    # MEVCUT DOSYA OKU
    # =========================

    if os.path.exists(FILE_PATH):

        with open(FILE_PATH, "r", encoding="utf-8", errors="ignore") as f:

            lines = f.readlines()

            ana_zirh = lines[:ZIRH_LIMIT]

            for line in lines:

                line = line.strip()

                if line.startswith("http"):
                    mevcut_linkler.add(line)

    print(f"🧱 ZIRH LINK SAYISI: {len(mevcut_linkler)}")

    # =========================
    # KAYNAKLARI TARA
    # =========================

    bulunanlar = []

    for kaynak in YEDEK_KAYNAKLAR:

        try:

            print(f"\n📡 Taranıyor: {kaynak}")

            r = session.get(
                kaynak,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
                verify=False,
                allow_redirects=True
            )

            if r.status_code != 200:
                print(" ❌ Kaynak erişilemedi")
                continue

            data = r.text

            bulunan = m3u_parse(data)

            print(f" 🔍 Bulunan: {len(bulunan)}")

            bulunanlar.extend(bulunan)

        except Exception as e:

            print(f" ❌ HATA: {e}")

    # =========================
    # MÜKERRER TEMİZLE
    # =========================

    unique_kanallar = []
    gorulenler = set()

    for kanal in bulunanlar:

        try:

            link = kanal.strip().splitlines()[-1].strip()

            if link in mevcut_linkler:
                continue

            if link in gorulenler:
                continue

            gorulenler.add(link)

            unique_kanallar.append(kanal)

        except:
            pass

    print(f"\n🧪 TEST EDİLECEK YENİ KANAL: {len(unique_kanallar)}")

    # =========================
    # THREAD TEST
    # =========================

    final_liste = []

    with ThreadPoolExecutor(max_workers=THREADS) as executor:

        results = list(
            executor.map(
                lambda x: kanal_isleme(x, mevcut_linkler),
                unique_kanallar
            )
        )

        final_liste = [
            r for r in results
            if r is not None
        ]

    # =========================
    # DOSYAYA YAZ
    # =========================

    with open(FILE_PATH, "w", encoding="utf-8") as f:

        f.writelines(ana_zirh)

        f.write(
            f"\n# ===== CANLI YEDEKLER ===== {datetime.datetime.now().strftime('%d-%m-%Y %H:%M')} ===== #\n\n"
        )

        for kanal in final_liste:

            f.write(kanal + "\n\n")

    print("\n===================================")
    print(f"✅ EKLENEN GERÇEK CANLI KANAL: {len(final_liste)}")
    print("🏁 TEMİZLİK TAMAMLANDI")
    print("===================================\n")

# =========================
# START
# =========================

if __name__ == "__main__":
    main()
