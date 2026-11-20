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
| 🥇 **1** | **gtrsnipe (Biomechanical Viterbi)** | Biomechanical Viterbi | **%61.5** | %61.5 | **1.88 perde** | 1.33 |
| 🥈 **2** | **GuitarArranger (Fretboard Voicer)** | Fretboard Voicing | **%53.2** | %53.2 | **2.63 perde** | 1.24 |
| 🥉 **3** | **tuttut (HMM & Graph Viterbi)** | HMM & Graph Theory | **%29.3** | %29.3 | **4.06 perde** | 1.38 |
|    **4** | **Baseline (Naive Greedy)** | Naive Greedy (Kontrol) | **%27.4** | %27.4 | **4.19 perde** | 1.40 |

---

## 📋 Parça Bazlı Ayrıntılı Karşılaştırma (Tel Doğruluğu %)

| Parça Adı | Tür / Stil | Baseline (Naive) | tuttut | gtrsnipe | GuitarArranger |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `05_BN3-119-G_solo` | Bossa Nova (Solo) | %6.7 | %6.7 | %48.3 | **%55.0** |
| `03_Funk1-97-C_solo` | Funk (Solo) | %24.2 | %24.2 | %35.2 | **%37.4** |
| `04_Jazz1-200-B_solo` | Jazz (Solo) | %7.1 | %7.1 | **%51.8** | %28.6 |
| `00_Rock2-142-D_solo` | Rock (Solo) | %59.6 | %61.5 | **%79.8** | %27.9 |
| `02_SS1-100-C#_solo` | Singer-Songwriter (Solo) | %23.6 | %23.6 | **%72.7** | %43.6 |
| `04_BN2-131-B_comp` | Bossa Nova (Comping) | %55.4 | %61.5 | %64.1 | **%88.7** |
| `02_Funk1-97-C_comp` | Funk (Comping) | %71.9 | %71.9 | %73.9 | **%81.0** |
| `01_Jazz3-150-C_comp` | Jazz (Comping) | %3.1 | %3.9 | **%60.9** | %18.8 |
| `05_Rock3-117-Bb_comp` | Rock (Comping) | %11.9 | %13.8 | **%72.8** | %72.2 |
| `00_SS3-84-Bb_comp` | Singer-Songwriter (Comping) | %10.7 | %18.6 | %55.7 | **%79.3** |

---

## 💡 Bilimsel Değerlendirme ve Analiz

1. **Viterbi vs. Naive:** Biomechanical Viterbi optimizasyonu kullanan sistemler, kontrol grubuna (%27.9) kıyasla açık ara üstünlük sergilemektedir.
2. **Klavye Pozisyonu:** Özellikle sololarda elin belirli bir pozisyonda kalmasını sağlayan el kaydırma cezaları (movement penalty) ve tel değiştirme cezaları (string-switch penalty), transkripsiyonun çalınabilirliğini dramatik olarak artırmaktadır.

---

## 🎯 Sonraki Adım: Deney 3 (Tam Faktöriyel M2S x FSA Matrisi)
FSA yarışmasının lideri ve diğer alternatifler, M2S motorları (`music21`, `MuseScore CLI`) ile birleştirilerek nihai W3C MusicXML ve profesyonel TAB skorlarına dönüştürülecektir.
