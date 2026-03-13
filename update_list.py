import os
import re

# Senin GitHub Logo Klasörün
MY_LOGO_BASE = "https://raw.githubusercontent.com/batuhansabri55/AkcagozTV_Canli/main/logos/logos/"

# Eşleşecek kanallar
LOGO_MAP = {
    "atv": "atv.png",
    "kanal d": "kanald.png"
}

def update_m3u():
    file_name = "tr.m3u"
    if not os.path.exists(file_name):
        print(f"HATA: {file_name} dosyası bulunamadı!")
        return

    print("İşlem başlatıldı, lütfen bekleyin...")
    
    with open(file_name, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    degisim_sayisi = 0

    for line in lines:
        if line.startswith("#EXTINF"):
            line_lower = line.lower()
            for key, filename in LOGO_MAP.items():
                if key in line_lower:
                    new_url = MY_LOGO_BASE + filename
                    if 'tvg-logo="' in line:
                        line = re.sub(r'tvg-logo="[^"]*"', f'tvg-logo="{new_url}"', line)
                    else:
                        line = line.replace("#EXTINF:-1", f'#EXTINF:-1 tvg-logo="{new_url}"')
                    degisim_sayisi += 1
                    break
        new_lines.append(line)

    with open(file_name, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    
    print("-" * 30)
    print(f"BAŞARILI! {degisim_sayisi} kanalın logosu değiştirildi.")
    print("-" * 30)

if __name__ == "__main__":
    update_m3u()
