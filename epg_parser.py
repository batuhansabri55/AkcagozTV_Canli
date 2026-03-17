name: EPG Otomatik Guncelle
on:
  schedule:
    - cron: '0 */6 * * *'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Python Kur
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Kutuphaneleri Yukle
        run: pip install requests
      - name: EPG Ayikla
        run: python epg_parser.py
      - name: Kaydet ve Yukle
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          # Dosya olustu mu kontrol et ve zorla ekle
          git add epg.json || echo "Dosya yok!"
          git commit -m "EPG Guncellendi" || exit 0
          git push
