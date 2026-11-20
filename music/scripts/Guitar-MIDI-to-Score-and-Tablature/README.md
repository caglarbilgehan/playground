# MIDI-to-Score (M2S) ve Fret-String Assignment (FSA) Kıyaslama Laboratuvarı

Bu laboratuvar, Automatic Music Transcription (AMT) aşamasından elde edilen polifonik gitar MIDI dosyalarını insan eliyle çalınabilir, ergonomik ve standart W3C MusicXML / Tablature notalarına dönüştürme sürecini bilimsel olarak test eder.

---

## 🎯 Araştırma Soruları ve Hipotezler

1. **Deney 1 (Kontrol Grubu - FSA Olmadan Dönüşüm):**
   * *Soru:* Standart bir MIDI dosyasını doğrudan bir notasyon motoruna (`music21`, `MuseScore`) verdiğimizde ne olur?
   * *Hipotez:* Gitara özel perde ve tel ataması yapılmadığında çıkan TAB'lar insan eliyle çalınamaz derecede ergonomik kural ihlali (imkansız el atlamaları, aynı tele birden fazla nota basma) içerir.

2. **Deney 2 (Açık Kaynak FSA Motorlarının Yarışması):**
   * *Soru:* Açık kaynak ekosistemindeki farklı yaklaşımlar (HMM/Viterbi: `tuttut`, Sezgisel: `gtrsnipe`, Genetik Algoritma: `GuitarArranger`) gitaristin gerçek çalışını ne kadar isabetle tahmin eder?
   * *Hipotez:* Çizge teorisi ve Viterbi optimizasyonu (HMM), lokal sezgisel kurallara kıyasla daha yüksek Tel Doğruluğu (% String Accuracy) ve daha düşük Perde Hatası (MAE) sağlar.

3. **Deney 3 (Faktöriyel Matris Kıyaslaması - M2S x FSA):**
   * *Soru:* Hangi FSA motoru hangi M2S notasyon aracıyla birleştiğinde en yüksek standart uyumluluğu ve görsel okunabilirliği sunar?
   * *Çıktı:* Nihai üretim hattı için şampiyon kombinasyonun belirlenmesi.

---

## 📂 Klasör Mimarisi

```text
playground/music/scripts/Guitar-MIDI-to-Score-and-Tablature/
│
├── README.md                                  # Deneylerin amacını açıklayan teknik kılavuz (Türkçe)
* `fsa_engines/`: Test edilecek açık kaynak FSA adaptörleri (`tuttut`, `gtrsnipe`, `guitar_arranger`).
* `m2s_engines/`: Notasyon üreticileri (`music21`, `musescore`).
* `evaluation/`: JAMS okuyucu ve metrik hesaplama motorları (Tel Doğruluğu, Perde Hatası, Ergonomi).
* `experiment_01_baseline_no_fsa/`: 1. Deney çalıştırma ve çıktı klasörü.
* `experiment_02_fsa_benchmark/`: 2. Deney çalıştırma ve liderlik tablosu.
* `experiment_03_m2s_fsa_matrix/`: 3. Deney çalıştırma ve nihai MusicXML skorları.
* `MASTER_M2S_BENCHMARK.md`: Tüm deneylerin özetlendiği ana bilimsel rapor.
