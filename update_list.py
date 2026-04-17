import os
import datetime
import subprocess
import sys

# --- AYARLAR ---
FILE_PATH = "tr.m3u"

# ÖNEMLİ: Eğer m3u dosyan 4750 satırdan azsa, bu rakamı dosyanın mevcut satır sayısına 
# (mesela 4500) çekmelisin ki kod "zırhın bittiği yeri" anlasın.
ZIRH_LIMIT = 4500 

# YOUTUBE CANLI YAYIN LİSTESİ
YOUTUBE_KANALLARI = {
    "CNN TURK (YOUTUBE)": "https://www.youtube.com/watch?v=y3_beK6V_84",
    "HABER GLOBAL (YOUTUBE)": "https://www.youtube.com/watch?v=X_EWyemclKA",
    "24 TV (YOUTUBE)": "https://www.youtube.com/watch?v=fXHeid6Z_9I"
}

def get_youtube_m3u8(url):
    """YouTube engellerini aşmak için geliştirilmiş link çekici."""
    try:
        # --no-check-certificate ve --geo-bypass engelleri aşmak için eklendi
        cmd = [
            sys.executable, "-m", "yt_dlp", 
            "--quiet", "--no-warnings", 
            "--no-check-certificate",
            "--geo-bypass",
            "-g", "-f", "best[ext=mp4]/best", 
            url
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0 and result.stdout.strip().startswith("http"):
            return result.stdout.strip()
        else:
            print(f"!!! YouTube Veri Alınamadı ({url})")
    except Exception as e:
        print(f"!!! Sistem Hatası: {e}")
    return None

def main():
    print("\n--- YOUTUBE GUNCELLEME ISLEMI BASLADI ---")
    
    if not os.path.exists(FILE_PATH):
        print(f"HATA: {FILE_PATH} bulunamadı!")
        return

    # 1. DOSYAYI OKU VE ZIRHLI BÖLGEYİ AYIR
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        satirlar = f.readlines()
    
    mevcut_satir_sayisi = len(satirlar)
    print(f"Dosya okundu. Toplam satır: {mevcut_satir_sayisi}")

    # Eğer zırh limiti dosya boyutundan büyükse, limiti otomatik ayarla
    limit = min(ZIRH_LIMIT, mevcut_satir_sayisi)
    zirhli_bolge = satirlar[:limit]
    print(f"Zırhlı bölge (ilk {limit} satır) korumaya alındı.")

    # 2. YOUTUBE LİNKLERİNİ ÇEK
    yt_eklentileri = []
    for isim, url in YOUTUBE_KANALLARI.items():
        print(f"-> {isim} için taze link aranıyor...")
        link = get_youtube_m3u8(url)
        if link:
            yt_eklentileri.append(f'#EXTINF:-1 group-title="YEDEKLER",{isim}\n{link}\n')
            print(f"   [TAMAM] Link başarıyla alındı.")
        else:
            print(f"   [HATA] YouTube'dan link sökülemedi!")

    # 3. DOSYAYI YENİDEN OLUŞTUR (ZIRH + YOUTUBE LİNKLERİ)
    if yt_eklentileri:
        try:
            with open(FILE_PATH, 'w', encoding='utf-8') as f:
                # Önce dokunulmaz zırhlı bölge
                f.writelines(zirhli_bolge)
                
                # YouTube Başlığı ve Linkler
                f.write("\n# --- YOUTUBE CANLI YAYIN YEDEKLERİ ---\n")
                f.writelines(yt_eklentileri)
                
                simdi = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
                f.write(f"\n# SON GUNCELLEME: {simdi}\n")
            
            print(f"\n--- ISLEM BASARIYLA TAMAMLANDI ({simdi}) ---")
            print(f"{FILE_PATH} dosyasının en sonuna {len(yt_eklentileri)} kanal eklendi.")
        except Exception as e:
            print(f"Dosyaya yazarken hata oluştu: {e}")
    else:
        print("\n!!! KRİTİK: Hiç link alınamadı, dosya değiştirilmedi.")

if __name__ == "__main__":
    main()
