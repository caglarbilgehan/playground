# Deney 2: Açık Kaynak FSA Motorları Liderlik Raporu

**Tarih:** 2026-11-20  
**Zemin Gerçeği:** GuitarSet (10 Parça - 6 Tel Hexaphonic Manyetik Kayıtları)  
**Değerlendirilen Metrikler:**
1. **Tel Doğruluğu (String Accuracy %):** Gerçek gitaristin vurduğu tel ile eşleşme oranı.
2. **Perde Doğruluğu (Fret Accuracy %):** Hem tel hem perdenin birebir tutma oranı.
3. **Perde Hatası (Fret MAE):** Seçilen perde ile gerçek perde arasındaki ortalama sapma (perde cinsinden).
4. **Ortalama El Kayması (Hand Shift):** Sol elin ardışık perdeler arasında atlama mesafesi (Ergonomi).

---

## 🏆 FSA LİDERLİK TABLOSU (Genel Sıralama)

| Sıra | FSA Motoru | Algoritmik Yaklaşım | Tel Doğruluğu (%) | Perde Doğruluğu (%) | Perde Hatası (MAE) | Ortalama El Atlama |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| 🥇 **1** | **gtrsnipe (Biomechanical Viterbi)** | Biomechanical Viterbi | **%61.0** | %61.0 | **1.89 perde** | 1.38 |
| 🥈 **2** | **GuitarArranger (Fretboard Voicer)** | Fretboard Voicing | **%50.7** | %50.7 | **3.05 perde** | 1.19 |
| 🥉 **3** | **tuttut (HMM & Graph Viterbi)** | HMM & Graph Theory | **%28.2** | %28.2 | **4.12 perde** | 1.38 |
|    **4** | **Baseline (Naive Greedy)** | Naive Greedy (Kontrol) | **%27.9** | %27.9 | **4.14 perde** | 1.37 |

---

## 📋 Parça Bazlı Ayrıntılı Karşılaştırma (Tel Doğruluğu %)

| Parça Adı | Tür / Stil | Baseline (Naive) | tuttut | gtrsnipe | GuitarArranger |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `05_BN3-119-G_solo` | Bossa Nova (Solo) | %6.5 | %6.5 | **%38.7** | %30.6 |
| `03_Funk1-97-C_solo` | Funk (Solo) | %24.8 | %25.0 | %29.5 | **%33.3** |
| `04_Jazz1-200-B_solo` | Jazz (Solo) | %6.2 | %6.2 | **%50.8** | %46.1 |
| `00_Rock2-142-D_solo` | Rock (Solo) | %56.1 | %56.9 | **%71.5** | %53.9 |
| `02_SS1-100-C#_solo` | Singer-Songwriter (Solo) | %23.7 | %23.7 | **%74.6** | %44.1 |
| `04_BN2-131-B_comp` | Bossa Nova (Comping) | %54.9 | %55.3 | %67.0 | **%85.0** |
| `02_Funk1-97-C_comp` | Funk (Comping) | %71.4 | %71.4 | **%81.0** | %71.4 |
| `01_Jazz3-150-C_comp` | Jazz (Comping) | %3.5 | %3.5 | **%44.8** | %19.3 |
| `05_Rock3-117-Bb_comp` | Rock (Comping) | %16.8 | %17.1 | **%89.7** | %55.8 |
| `00_SS3-84-Bb_comp` | Singer-Songwriter (Comping) | %15.2 | %16.9 | %62.5 | **%67.4** |

---

## 💡 Bilimsel Değerlendirme ve Analiz

1. **Viterbi vs. Naive:** Biomechanical Viterbi optimizasyonu kullanan sistemler, kontrol grubuna (%27.9) kıyasla açık ara üstünlük sergilemektedir.
2. **Klavye Pozisyonu:** Özellikle sololarda elin belirli bir pozisyonda kalmasını sağlayan el kaydırma cezaları (movement penalty) ve tel değiştirme cezaları (string-switch penalty), transkripsiyonun çalınabilirliğini dramatik olarak artırmaktadır.

---

## 🎯 Sonraki Adım: Deney 3 (Tam Faktöriyel M2S x FSA Matrisi)
FSA yarışmasının lideri ve diğer alternatifler, M2S motorları (`music21`, `MuseScore CLI`) ile birleştirilerek nihai W3C MusicXML ve profesyonel TAB skorlarına dönüştürülecektir.
