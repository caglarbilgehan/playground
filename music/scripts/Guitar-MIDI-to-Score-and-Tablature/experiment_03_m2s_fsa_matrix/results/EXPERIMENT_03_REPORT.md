# Deney 3: M2S x FSA Faktöriyel Matris Raporu

**Tarih:** 2026-11-20  
**Amaç:** M2S notasyon motoru (`music21`) ile farklı FSA algoritmalarının kombinasyonunu; hem referans (kusursuz) MIDI girdisi hem de AMT (YourMT3+) transkripsiyon girdisi altında karşılaştırmak.

---

## 📊 Faktöriyel Performans Matrisi (Ortalama Değerler)

| Girdi Hattı (Pipeline) | FSA Motoru | Notasyon Motoru | Tel Doğruluğu (%) | Perde Doğruluğu (%) | Perde Hatası (MAE) | Standart Çıktı |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| Pipeline A (Referans MIDI) | **gtrsnipe** (🥇 **Şampiyon**) | music21 | **%61.0** | %61.0 | **1.89 perde** | W3C MusicXML |
| Pipeline A (Referans MIDI) | **GuitarArranger** (🥈) | music21 | **%50.7** | %50.7 | **3.05 perde** | W3C MusicXML |
| Pipeline A (Referans MIDI) | **tuttut** (🥉) | music21 | **%28.2** | %28.2 | **4.12 perde** | W3C MusicXML |
| Pipeline A (Referans MIDI) | **Baseline** (Kontrol) | music21 | **%27.9** | %27.9 | **4.14 perde** | W3C MusicXML |
| Pipeline B (YourMT3+ AMT) | **gtrsnipe** (🥇 **Şampiyon**) | music21 | **%61.5** | %61.5 | **1.88 perde** | W3C MusicXML |
| Pipeline B (YourMT3+ AMT) | **GuitarArranger** (🥈) | music21 | **%53.2** | %53.2 | **2.63 perde** | W3C MusicXML |
| Pipeline B (YourMT3+ AMT) | **tuttut** (🥉) | music21 | **%29.3** | %29.3 | **4.06 perde** | W3C MusicXML |
| Pipeline B (YourMT3+ AMT) | **Baseline** (Kontrol) | music21 | **%27.4** | %27.4 | **4.19 perde** | W3C MusicXML |

---

## 🎼 Üretilen Nihai Skorlar (Generated Scores)

Tüm 10 test parçası için W3C standartlarında MusicXML dosyaları üretilmiştir:
* **Şampiyon Skorlar (`*_gtrsnipe.musicxml`):** Biyomekanik Viterbi ile sol elin en ergonomik perdelerine dizilmiş nota ve TAB partitürleri.
* **Kontrol Skorları (`*_baseline.musicxml`):** Naif açgözlü algoritmayla üretilmiş ham partitürler.
* **Uçtan Uca Skorlar (`*_yourmt3_gtrsnipe.musicxml`):** Ham WAV sesinden başlayıp doğrudan nihai partitüre kadar uzanan tam otonom yapay zeka hattı.
