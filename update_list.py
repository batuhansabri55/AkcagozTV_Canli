import os
import datetime
import subprocess
import sys

# --- AYARLAR ---
FILE_PATH = "tr.m3u"
ZIRH_LIMIT = 4750

# YOUTUBE CANLI YAYIN LİSTESİ
YOUTUBE_KANALLARI = {
    "CNN TURK (YOUTUBE)": "https://www.youtube.com/watch?v=y3_beK6V_84",
    "HABER GLOBAL (YOUTUBE)": "https://www.youtube.com/watch?v=X_EWyemclKA"
}

def get_youtube_m3u8(url):
    """yt-dlp ile linki çekmeyi dener, hata varsa ekrana basar."""
    try:
        # PATH sorununu aşmak için tam executable yolunu kullanıyoruz
        cmd = [sys.executable, "-m", "yt_dlp", "-g", "-f", "best", url]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        else:
            print(f"!!! YouTube Hatası ({url}): {result.stderr}")
    except Exception as e:
        print(f"!!! Sistem Hatası: {e}")
    return None

def main():
    print("--- ISLEM BASLADI ---")
    
    if not os.path.exists(FILE_PATH):
        print(f"HATA: {FILE_PATH} bulunamadı. Lütfen dosya ismini kontrol et.")
        return

    # 1. DOSYAYI OKU
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        satirlar = f.readlines()
    
    print(f"Dosya okundu. Toplam satır: {len(satirlar)}")
    zirhli_bolge = satirlar[:ZIRH_LIMIT]

    # 2. YOUTUBE LİNKLERİNİ AL
    yt_eklentileri = []
    for isim, url in YOUTUBE_KANALLARI.items():
        print(f"-> {isim} aranıyor...")
        link = get_youtube_m3u8(url)
        if link:
            # Senin panelindeki grup yapısına sadık kalarak ekliyoruz
            yt_eklentileri.append(f'#EXTINF:-1 group-title="YEDEKLER",{isim}\n{link}\n')
            print(f"   [OK] Link alındı.")
        else:
            print(f"   [HATA] Link çekilemedi!")

    # 3. DOSYAYA YAZ (ZIRH + YENİLER)
    if yt_eklentileri:
        try:
            with open(FILE_PATH, 'w', encoding='utf-8') as f:
                # Dokunulmaz 4750 satır
                f.writelines(zirhli_bolge)
                
                # Ayırıcı ve yeni linkler
                f.write("\n# --- OTOMATIK YOUTUBE YEDEKLERI ---\n")
                f.writelines(yt_eklentileri)
                
                simdi = datetime.datetime.now().strftime('%H:%M:%S')
                f.write(f"# Guncelleme: {simdi}\n")
            
            print(f"--- ISLEM BASARIYLA TAMAMLANDI (Saat: {simdi}) ---")
            print(f"Lütfen {FILE_PATH} dosyasını açıp en sona (4750. satır civarı) bak.")
        except Exception as e:
            print(f"Dosyaya yazarken hata oluştu: {e}")
    else:
        print("!!! KRİTİK: Hiçbir YouTube linki alınamadığı için dosyada değişiklik yapılmadı.")

if __name__ == "__main__":
    main()
