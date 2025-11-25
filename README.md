# BIST Algo Scanner - Trend Breakout Detection 

BIST hisselerinde **"Hacimli Düşen Trend Kırılımı"** (Descending Trendline Breakout) formasyonunu matematiksel olarak tespit eden Python botu. 

`scipy` ile pivotları hesaplar, regresyon ile trendi çizer, `TA-Lib` ile mum teyidi (Engulfing/Marubozu) arar ve sonuçları grafik (`.png`) olarak kaydeder.

## Özellikler

- **Oto-Trend Çizimi:** `argrelextrema` ve `linregress` kullanarak matematiksel trend tespiti.
- **Filtreler:**
  - Düşen Trend (Negatif Eğim)
  - Hacim Patlaması (>1.5x Ort)
  - Mum Teyidi (Opsiyonel)
- **Risk Yönetimi:** ATR bazlı dinamik Stop-Loss, TP1 ve TP2 hesaplaması.
- **Görsel Çıktı:** Sinyal gelen hisselerin grafiklerini trend çizgileriyle beraber `Sinyal_Grafikleri` klasörüne kaydeder.

# Gerekli kütüphaneler
pip install yfinance pandas numpy scipy mplfinance ta-lib

<img width="800" height="575" alt="CELHA IS_20251125" src="https://github.com/user-attachments/assets/c024350e-9294-46a0-8079-5ebb40809e0e" />
<img width="800" height="575" alt="OZRDN IS_20251125" src="https://github.com/user-attachments/assets/b052a088-4410-4e58-b091-9b20183654c1" />
