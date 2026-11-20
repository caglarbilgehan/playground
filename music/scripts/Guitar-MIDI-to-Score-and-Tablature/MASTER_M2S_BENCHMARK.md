# Master Benchmark: Guitar MIDI-to-Score and Tablature (M2S & FSA)

Bu belge, **Automatic Music Transcription (AMT)** aşamasından sonraki en kritik müzik mühendisliği problemi olan **Fret-String Assignment (FSA)** ve **MIDI-to-Score (M2S)** dönüşümünün kapsamlı bilimsel karşılaştırma raporudur.

---

## 🏆 Yönetici Özeti (Executive Summary)

* **Kontrol Grubu (FSA'sız Naif Dönüşüm):** Standart müzik yazılımlarının varsayılan açgözlü (en düşük perde) kuralı, insan gitaristin çaldığı tellerin **%72.1'ini yanlış** tahmin etmektedir (Doğruluk: **%27.9**, Hata: **4.14 perde**).
* **Kazanan Şampiyon Hat (`gtrsnipe` + `music21`):** Biyomekanik el hareket cezaları ve Viterbi optimizasyonu ile tel doğruluğunu **%61.0** seviyesine çıkarmış, perde hatasını **1.89 perdeye** indirmiştir.
* **Standart Uyumluluk:** Üretilen tüm dosyalar W3C MusicXML formatında olup, MuseScore, Guitar Pro ve Web tabanlı motorlarda hem **Standart Porte** hem de **6 Telli Tablature** olarak kusursuz açılmaktadır.

---

## 📊 Nihai Liderlik Matrisi

| Sıra | FSA Çözücüsü | Algoritma Tipi | Tel Doğruluğu (%) | Perde Hatası (MAE) | Çalınabilirlik Durumu |
| :---: | :--- | :--- | :---: | :---: | :---: |
| 🥇 | **gtrsnipe** | Biomechanical Viterbi DP | **%61.0** | **1.89 perde** | **İnsan Seviyesinde Akıcı & Ergonomik** |
| 🥈 | **GuitarArranger** | Fretboard Voicer (GA/Rule) | %50.7 | 3.05 perde | Akorlarda Başarılı, Sololarda Hantal |
| 🥉 | **tuttut** | HMM & Graph Theory | %28.2 | 4.12 perde | Açık Tellere Aşırı Yığılma |
| 4 | **Baseline** | Naive Greedy (Kontrol) | %27.9 | 4.14 perde | Çalınamaz / Fiziksel İhlaller |

---

## 🔬 Tamamlanan Deneyler:
1. [Deney 1: Kontrol Grubu (FSA Olmadan Dönüşüm)](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-MIDI-to-Score-and-Tablature/experiment_01_baseline_no_fsa/results/EXPERIMENT_01_REPORT.md)
2. [Deney 2: Açık Kaynak FSA Motorları Yarışması](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-MIDI-to-Score-and-Tablature/experiment_02_fsa_benchmark/results/EXPERIMENT_02_REPORT.md)
3. [Deney 3: Tam Faktöriyel M2S x FSA Matrisi](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-MIDI-to-Score-and-Tablature/experiment_03_m2s_fsa_matrix/results/EXPERIMENT_03_REPORT.md)
