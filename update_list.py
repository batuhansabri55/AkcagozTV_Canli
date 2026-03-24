import requests
import re
import base64
import os

# --- AYARLAR ---
GITHUB_TOKEN = os.environ.get('GH_TOKEN') 
REPO_NAME = "batuhansabri55/AkcagozTV_Canli"
FILE_PATH = "tr.m3u"

# BU LİSTE SENİN 2995 KANALLIK ÖZEL FİLTREN (Dokunulmazlar)
# Sadece bu isimleri içeren kanallar içeri alınır, gerisi kapı dışı!
KUTSAL_ISIMLER = """
TRT1 FHD,TRT1 HD,ATV FHD,ATV HD,TV8 FHD,TV8 HD,SHOW TV FHD,SHOW TV HD,KANAL D FHD,KANAL D HD,STAR TV FHD,STAR TV HD,NowTV HD,NowTV,BEYAZ TV FHD,BEYAZ TV HD,TYT TURK,CNBC-E,KANAL 7 FHD,KANAL 7 HD,TEVE 2 FHD,TEVE 2 HD,A2 HD,360 TV HD,TV8.5 FHD,TV8.5 HD,FLASH TV HD,TRT 2 HD,BI TV,TRT GENC,TVSHOWMAX HD,Meltem TV,A HABER FHD,A HABER HD,CNN TURK FHD,CNN TURK HD,HABER TURK HD,HABER TURK,NTV FHD,NTV HD,HABER GLOBAL HD,HABER GLOBAL,TRT HABER FHD,TRT HABER HD,ULKE TV FHD,ULKE TV HD,KRT TV FHD,KRT TV HD,HALK TV FHD,HALK TV HD,TV100 FHD,TV100 HD,SÖZCÜ TV FHD,SÖZCÜ TV HD,24 TV FHD,24 TV HD,TVNET FHD,EKOL TV,TVNET HD,BLOOMBERGHT HD,BLOOMBERGHT,TGRT HABER FHD,TGRT HABER HD,TELE 1 HD,ULUSAL KANAL,APARA HD,Bengu Turk,EKO TURK,NATIONAL GEOGRAPHIC HD,NAT GEO WILD HD,HABITAT TV,DMAX FHD,TLC HD,BEIN GURME HD,BEIN IZ HD,LOVE NATURE,DISCOVERY CHANNEL,DISCOVERY ID,XYABAN TV HD,TARIH TV,TRT BELGESEL HD,BBC Earth HD,Da Vinci,VIASAT HISTORY,VIASAT EXPLORER,UNIVERSAL BELGESEL,UNIVERSAL DISCOVERY,SINEMA TV,SINEMA TV 2,SINEMA TV KOMEDI,SINEMA TV KOMEDI 2,SINEMA TV AKSIYON,SINEMA TV AKSIYON 2,SINEMA TV AILE,SINEMA TV AILE 2,SINEMA TV YERLI,SINEMA TV YERLI 2,SINEMA TV 1001,SINEMA TV 1002,SONVIZYON,CHOICE,KEMAL SUNAL,FANTEZI,BILIMKURGU,DRAM,WESTERN,TURK,TURK KOMEDI,YESILCAM,YESILCAM KOMEDI,AKSIYON,BEST PICTURES,KORKU,KOMEDI,MARVEL,CINE BOX HD 1,CINE BOX HD 2,CINE BOX HD 3,CINE BOX HD 4,CINE BOX HD 5,CINE BOX HD 6,CINE BOX HD 7,CINE BOX HD 8,LOCA 1,LOCA 2,LOCA 3,CINE VISION 1,CINE VISION 2,CINE VISION 3,CINE VISION 4,CINE VISION 5,CINE VISION 6,FILM SCREEN,MOVIESMART Classic HD,MOVIESMART TURK,Filmbox HD,beIN Movies Premiere HD,BEIN MOVIES PREMIER 2,beIN Movies Stars HD,beIN Movies Turk HD,BeIN Box Office,beIN Series 1,beIN Series 2,beIN Series 3,beIN Series 4,Dizismart Max,EPIC DRAMA,FX FHD,Dizismart Premium HD,TRT Diyanet Cocuk,NICK JR,BABY TV,DUCK TV,DISNEY JR HD,CARTOONITO,SMART ÇOCUK,TRT COCUK FHD,MINIKA COCUK FHD,MINIKA GO FHD,CARTOON NETWORK HD,NICKTOONS,NICKELODEON,UNIVERSAL COCUK,UNIVERSAL DISNEY,PEMBE PANTER,REDKIT,SIRINLER,ASLAN,BIZ IKIMIZ,BULMACA KULESI,CILLE,DORU,EGE ILE GAGA,ELIFIN DUSLERI,ELIF VE ARKADASLARI,EMIRAY,KUCUK HAZERFANI,BIKAPTAN PENGU,KARE,KOSTEBEKGILLER,LEYLEK KARDES,MAYSA VE BULUT,MUTLU OYUNCAKLAR,NASREDDIN HOCA,PIRIL,TAVSAN MOMO,YADE,TOM AND JERRY,RAFADAN TAYFA,PEPE,SEVIMLI DOSTLAR,NILOYA,MASHA ILE KOCA AYI,LIMON ILE ZEYTIN,KUZUCUK,KUKULI,PIJAMASKELILER,KRAL SAKIR,CANIM KARDESIM,KELOGLAN,BARBIE,GRIZY VE LEMINGLER,KONUSAN TOM,DAMAR TV,Roman TV,TURK POP MÜZİK,Sezen Aksu,Universal Muslum Gurses,KRALPOP,TRT MUZIK HD,POWER TURK HD,POWER TV HD,NR1 TURK,NR1,DREAM TURK HD,HIT MUZIK SANAT,Vav TV,REHBER,DOST TV,Semerkand TV,Lalegul,DIYANET TV,KUDUS TV,BURSA LINE TV,TRT AVAZ,ADA TV,AKSU TV,ALANYA POSTA TV,ARTI,ASTV,ORDU TV HABER 61,KANAL 58,VANGOLU TV,EDESSA TV,Anadolu Dernek,BR TV,BRT 1,ÇAY TV,DEHA TV 1,DENIZPOSTASI TV,DIM TV,ER TV,KANAL FIRAT,KANAL 3,KANAL 15,KANAL 23,KANAL 26,KANAL Z,URFA FANATİKKIBRIS GENC TV,LIFE TV,MERCAN TV,OLAY TURK,SAT 7 TURK,RUMELİ TV,TON TV,TV 6,TV 41,VUSLAT TV,YOL TV,Turkiye,Sahiller,Sonbahar,Suyun Sesi,Kar,Sahil ve Dalgalar,Kış,Güne Uyanış,Dron Dünyası,Fire,Yağmur,Akvaryum,Tropikal Sahil,Kamp Atesi,Noel,Dünya,Norway,Austria,MAXSPORTS 1,MAXSPORTS 2,MAXSPORTS 3,MAXSPORTS 4 Formula 1,MAXSPORTS 5 Formula 1,MAXSPORTS 6 UFC,beIN SPORTS 1 SD,beIN SPORTS 1 HD,beIN SPORTS 1 FHD,Bein Sports 1,beIN SPORTS 4K PLUS 1 FHD,PLUS 2 HD,Bein Xtra,BEIN SPORTS 2 SD,BEIN SPORTS 2 HD,beIN SPORTS 2 FHD,Bein Sports 2,BEIN SPORTS 3 SD,BEIN SPORTS 3 HD,beIN SPORTS 3 FHD,Bein Sports 3,BEIN SPORTS 4 SD,BEIN SPORTS 4 HD,Bein Sports 4,beIN SPORTS 5 HD,Bein Sports 5,beIN SPORTS MAX 1 HD,beIN SPORTS MAX 1 FHD,beIN SPORTS MAX 2 HD,beIN SPORTS MAX 2 FHD,beIN SPORTS HABER HD,ASPOR FHD,ASPOR HD,EKOL SPORTS,S Sport HD,S Sport FHD,S Sport 2 HD,S Sport 2 FHD,TIVIBUSPORT,TIVIBUSPORT 1 HD,TIVIBUSPORT 2 HD,TIVIBUSPORT 3 HD,TIVIBUSPORT 4 HD,SPORSMART HD,SPORSMART FHD,SPORSMART 2 FHD,Eurosport 1 HD,Eurosport 2 HD,TRT SPOR FHD,TRT SPOR HD,Tabii Spor,Tabii Spor 1,Tabii Spor 2,Tabii Spor 3,Tabii Spor 4,Tabii Spor 5,Tabii Spor 6,Tabii Spor 7,Tabii Spor 8,Tabii Spor 9,Tabii Spor 10,HT SPOR,TRT SPOR YILDI,SIFIR TV,FBTV HD,NBA TV HD,TJK TV,SPORTS TV HD,EXXEN 1 SD,EXXEN 1 HD,EXXEN 1 FHD,EXXEN 2,EXXEN 3,EXXEN 4,EXXEN 5,EXXEN 6,EXXEN 7,EXXEN 8,S Sport+ 1,S Sport+ 2,S Sport+ 3,S Sport+ 4,S Sport+ 5,S Sport+ 6,S Sport+ 7,S Sport+ 8,S Sport+ 9,S Sport+ 10,ÇİFTÇİ TV,CAN SUYU,4TÜRK POPMÜZİK,TRT MÜZİK,SLOW KARADENİZ,ARABESK,ASRİ SAADET TV,VAAZ TV,GZT TV,4FİNANS,TÜRK,İKRA TV,AKİT TV
"""

# Akıllı Arama için isimleri hazırla
arama_listesi = [n.strip().lower().replace(" ", "") for n in KUTSAL_ISIMLER.split(",") if n.strip()]

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
        "message": "♻️ Dokunulmaz Filtre Aktif: Liste Süzüldü",
        "content": base64.b64encode(icerik.encode("utf-8")).decode("utf-8"),
        "sha": sha
    }
    requests.put(url, json=data, headers=headers)

def update_m3u():
    _, sha = github_dosya_oku() # Mevcut içeriği okumaya gerek yok, sıfırdan süzerek kuracağız
    
    yeni_liste = ["#EXTM3U"]
    eklenen_linkler = set()

    # M3U satırlarını yakalayan regex
    pattern = r"(#EXTINF:[^\n]*),([^\n]*)\n(https?://[^\n]*)"

    for s_url in YEDEK_KAYNAKLAR:
        try:
            print(f"🔗 Taranıyor: {s_url}")
            r = requests.get(s_url, timeout=15)
            r.encoding = 'utf-8'
            matches = re.findall(pattern, r.text)
            
            for ext_info, ch_name, url in matches:
                link = url.strip()
                temiz_isim = ch_name.lower().replace(" ", "")
                
                # FİLTRE: Eğer kanal ismi bizim "Dokunulmaz" listemizde geçiyorsa ekle
                if any(hedef in temiz_isim for hedef in arama_listesi):
                    if link not in eklenen_linkler:
                        # Orijinal satırı bozmadan ekle
                        yeni_liste.append(f"{ext_info},{ch_name.strip()}\n{link}")
                        eklenen_linkler.add(link)
                        
        except Exception as e:
            print(f"⚠️ Hata oluştu: {s_url}")
            continue

    final_m3u = "\n".join(yeni_liste)
    github_dosya_yaz(final_m3u, sha)
    print(f"🚀 İşlem Başarılı! Toplam {len(eklenen_linkler)} dokunulmaz kanal/yedek yazıldı.")

if __name__ == "__main__":
    update_m3u()
