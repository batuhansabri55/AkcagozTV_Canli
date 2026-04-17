import os
import datetime
import subprocess

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
ZIRH_LIMIT = 4750

# YOUTUBE CANLI YAYIN LİSTESİ
YOUTUBE_KANALLARI = {
    "CNN TURK (YOUTUBE)": "https://www.youtube.com/watch?v=y3_beK6V_84",
    "HABER GLOBAL (YOUTUBE)": "https://www.youtube.com/watch?v=X_EWyemclKA",
    "24 TV (YOUTUBE)": "https://www.youtube.com/watch?v=fXHeid6Z_9I",
    "TVNET (YOUTUBE)": "https://www.youtube.com/watch?v=7YpI6Z0pZf4"
}

def get_youtube_m3u8(url):
    """yt-dlp ile taze m3u8 linkini çekmeye çalışır."""
    try:
        # PATH sorunu yaşamamak için python -m yt_dlp kullanıyoruz
        cmd = ["python", "-m", "yt_dlp", "-g", "-f", "best", url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception as e:
        print(f"Hata ({url}): {e}")
    return None

def main():
    if not os.path.exists(FILE_PATH):
        print(f"Hata: {FILE_PATH} bulunamadı!")
        return

    # 1. ADIM: ZIRHLI BÖLGEYİ KORUMAYA AL
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        tum_satirlar = f.readlines()
        zirhli_bolge = tum_satirlar[:ZIRH_LIMIT]

    # 2. ADIM: YOUTUBE LİNKLERİNİ ÇÖZ
    yt_blok = []
    print("YouTube linkleri tazeleniyor...")
    for isim, url in YOUTUBE_KANALLARI.items():
        m3u8_link = get_youtube_m3u8(url)
        if m3u8_link:
            # Senin panel yapına uygun group-title ekliyoruz
            yt_blok.append(f'#EXTINF:-1 group-title="YEDEKLER",{isim}\n{m3u8_link}')
            print(f"✓ {isim} güncellendi.")

    # 3. ADIM: DOSYAYI YENİDEN OLUŞTUR
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        # Önce dokunulmaz 4750 satırı yaz
        f.writelines(zirhli_bolge)
        
        # Sonra YouTube yedeklerini ekle
        f.write("\n# --- YOUTUBE CANLI YAYIN YEDEKLERİ ---\n")
        for kanal in yt_blok:
            f.write(kanal + "\n")
        
        # En sona güncellenme tarihini bas
        simdi = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        f.write(f"\n# SON OTOMATİK GÜNCELLEME: {simdi}\n")

    print(f"\nİşlem Tamam! {len(yt_blok)} kanal 4750. satırdan sonrasına eklendi.")

if __name__ == "__main__":
    main()
