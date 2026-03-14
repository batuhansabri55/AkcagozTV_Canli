import requests
import os
import re
from concurrent.futures import ThreadPoolExecutor

# TEST EDİLMEYECEK / SİLİNMEYECEK DOMAINLER
DOKUNULMAZLAR = [
    "premiumstream",
    "workers.dev",
    "cdn-vizi",
    "vizitv",
    "goldvod"
]

# YEDEK IPTV KAYNAKLARI
YEDEK_KAYNAKLAR = [
    "https://mth.tc/DsGo",
    "https://raw.githubusercontent.com/sultansmgr/smart/refs/heads/main/viziTV.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/yasarfalkan/m3u-dosyam/refs/heads/main/YMBK.m3u8",
    "https://publiciptv.com/countries/tr/m3u",
    "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "https://streams.uzunmuhalefet.com/lists/tr.m3u"
]

MAX_LINK_PER_CHANNEL = 3

def normalize_name(name):
    return re.sub(r'[^a-z0-9]', '', name.lower())

def parse_m3u(text):
    return re.findall(r"(#EXTINF:.*?,(.*))\n(https?:\/\/.*)", text)

def link_test_et(item):

    info, name, url = item
    url_clean = url.lower()

    if any(vip in url_clean for vip in DOKUNULMAZLAR):
        return (info, name, url)

    try:
        r = requests.get(
            url,
            timeout=3,
            stream=True,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        if r.status_code == 200:
            data = next(r.iter_content(128), None)
            r.close()
            if data:
                return (info, name, url)

    except:
        pass

    return None


def update_m3u():

    adaylar = []
    korunanlar = []
    eklenen = set()

    if os.path.exists("tr.m3u"):

        with open("tr.m3u", "r", encoding="utf-8") as f:

            matches = parse_m3u(f.read())

            for info, name, url in matches:

                if any(vip in url.lower() for vip in DOKUNULMAZLAR):

                    korunanlar.append((info, name, url))
                    eklenen.add(url)

                else:

                    adaylar.append((info, name, url))

    for kaynak in YEDEK_KAYNAKLAR:

        try:

            r = requests.get(kaynak, timeout=10)

            if r.status_code == 200:

                adaylar.extend(parse_m3u(r.text))

        except:
            continue

    with ThreadPoolExecutor(max_workers=30) as exe:

        results = list(exe.map(link_test_et, adaylar))

    kanal_map = {}

    for res in results:

        if not res:
            continue

        info, name, url = res

        if url in eklenen:
            continue

        key = normalize_name(name)

        if key not in kanal_map:
            kanal_map[key] = []

        if len(kanal_map[key]) < MAX_LINK_PER_CHANNEL:

            kanal_map[key].append((info, name, url))
            eklenen.add(url)

    final_list = []

    final_list.extend(korunanlar)

    for kanal in kanal_map.values():
        final_list.extend(kanal)

    with open("tr.m3u", "w", encoding="utf-8") as f:

        f.write("#EXTM3U\n")

        for info, name, url in final_list:

            f.write(f"{info}\n{url}\n")

    print("TEMİZLENDİ")
    print("Toplam kanal:", len(final_list))


if __name__ == "__main__":
    update_m3u()
