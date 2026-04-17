import os
import datetime
import subprocess
import sys

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
ZIRH_LIMIT = 4750

YOUTUBE_KANALLARI = {
    "CNN TURK (YOUTUBE)": "https://www.youtube.com/watch?v=y3_beK6V_84",
    "HABER GLOBAL (YOUTUBE)": "https://www.youtube.com/watch?v=X_EWyemclKA"
}

def get_youtube_m3u8(url):
    try:
        # Modül olarak çağırmak PATH hatasını çözer
        cmd = [sys.executable, "-m", "yt_dlp", "-g", "-f", "best", url]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"YouTube Hatası ({url}): {result.stderr}")
    except Exception as e:
        print(f"Sistem Hatası: {e}")
    return None

def main():
    if not os.path.exists(FILE_PATH):
        print(f"Hata: {FILE_PATH} bulunamadı! Lütfen dosyanın script ile aynı klasörde olduğundan emin ol.")
        return

    # 1. ADIM: MEVCUT DOSYAYI OKU
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        tum_satirlar = f.readlines()
    
    zirhli_bolge = tum_satirlar[:ZIRH_LIMIT]
    print(f"Zırhlı bölge korundu: {len(zirhli_bolge)} satır.")

    # 2. ADIM: LİNKLERİ ÇEK
    yt_blok = []
    for isim, url in YOUTUBE_KANALLARI.items():
        print(f"{isim} linki çekiliyor...")
        m3u8_link = get_youtube_m3u8(url)
        if m3u8_link:
            yt_blok.append(f'#EXTINF:-1 group-title="YEDEKLER",{isim}\n{m3u8_link}')
            print(f"✓ Başarılı: {isim}")
        else:
            print(f"X Başarısız: {isim}")

    # 3. ADIM: DOSYAYI SIFIRDAN OLUŞTUR VE YAZ
    if yt_blok:
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            # Önce zırhı yaz
            f.writelines(zirhli_bolge)
            # Araya belirteç koy
            f.write("\n\n# ==========================================\n")
            f.write("# YOUTUBE CANLI YAYINLARI (OTOMATIK GUNCEL)\n")
            f.write("# ==========================================\n\n")
            # Linkleri yaz
            for kanal in yt_blok:
                f.write(kanal + "\n")
            
            simdi = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            f.write(f"\n# SON GUNCELLEME: {simdi}\n")
        print(f"\nUsta işlem tamam! {FILE_PATH} dosyasının en sonuna {len(yt_blok)} kanal eklendi.")
    else:
        print("\nHiç link çekilemediği için dosyaya dokunulmadı.")

if __name__ == "__main__":
    main()
