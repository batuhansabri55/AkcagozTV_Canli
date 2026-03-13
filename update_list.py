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
    if not os.path.exists("tr.m3u"):
        print("HATA: tr.m3u dosyası bulunamadı!")
        return

    with open("tr.m3u", "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    degisim_sayisi = 0

    for line in lines:
        if line.startswith("#EXTINF"):
            # Kanal adını bul (virgülden sonraki kısım)
            line_lower = line.lower()
            found = False
            for key, filename in LOGO_MAP.items():
                if key in line_lower:
                    new_url = MY_LOGO_BASE + filename
                    # Logo varsa değiştir, yoksa ekle
                    if 'tvg-logo="' in line:
                        line = re.sub(r'tvg-logo="[^"]*"', f'tvg-logo="{new_url}"', line)
                    else:
                        line = line.replace("#EXTINF:-1", f'#EXTINF:-1 tvg-logo="{new_url}"')
                    degisim_sayisi += 1
                    found = True
                    break
        new_lines.append(line)

    with open("tr.m3u", "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    
    print(f"BİTTİ! Toplam {degisim_sayisi} kanalın logosu güncellendi.")

if __name__ == "__main__":
    update_m3u()
