# EN BASİT VERSİYON
lines = open("tr.m3u", "r", encoding="utf-8").readlines()
new_lines = []
count = 0

for line in lines:
    if "#EXTINF" in line:
        l = line.lower()
        if "atv" in l:
            line = '#EXTINF:-1 tvg-logo="https://raw.githubusercontent.com/batuhansabri55/AkcagozTV_Canli/main/logos/logos/atv.png",ATV\n'
            count += 1
        elif "kanal d" in l:
            line = '#EXTINF:-1 tvg-logo="https://raw.githubusercontent.com/batuhansabri55/AkcagozTV_Canli/main/logos/logos/kanald.png",Kanal D\n'
            count += 1
    new_lines.append(line)

with open("tr.m3u", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print(f"Bitti! {count} kanal değişti.")
input("Kapatmak için Enter'a bas...")
