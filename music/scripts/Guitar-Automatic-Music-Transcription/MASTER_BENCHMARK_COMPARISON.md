# 🏆 Otomatik Müzik Transkripsiyonu (AMT) Master Karşılaştırma Raporu
## NYU MARL GuitarSet (ISMIR 2018) — 10 Parçalı & 5 Aşamalı Genişletilmiş Bilimsel Benchmark

**Tarih:** 19 Kasım 2026  
**Test Edilen Modeller:** YourMT3+, Spotify Basic Pitch, TorchCREPE, ByteDance CRNN, Omnizart  
**Donanım Ortamı:** NVIDIA GeForce RTX 4060 Laptop GPU (CUDA 12.1), Intel 13. Nesil Core i7-13700HX, 48 GB RAM, Ubuntu 26.04 Linux WSL2  
**Veri Seti Kapsamı:** NYU MARL GuitarSet — 5 Solo (%100 Tek Ses / Monofonik) + 5 Comping (%100 Polifonik Akor) = Toplam 10 Parça, 1.543 Ground Truth Nota  
**Test Protokolü:** Her model için 5 bağımsız koşum (1'er dakika aralıklı), tüm çıktılar zaman damgalı MIDI olarak arşivlenmiş ve `mir_eval` ile değerlendirilmiştir.

---

## 📌 Yönetici Özeti & Genel Sıralama

10 farklı müzik türünden (Bossa Nova, Funk, Rock, Jazz, Singer-Songwriter) seçilen 1.543 gerçek notalık referans kayıtlar üzerindeki test sonuçlarına göre modellerin genel hiyerarşisi:

| Sıra | AMT Kütüphanesi | Mimari & Yaklaşım | Donanım | Solo Onset Rec. | Comp Onset Rec. | Solo Pitch F1 | Comp Pitch F1 | Strict F1 (Offset) | Ortalama Hız | Genel Değerlendirme |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| 🥇 | **YourMT3+** | Multi-Track T5 Transformer | CUDA (GPU) | %89.3 | %86.3 | **%90.8** | **%85.9** | **%77.9** | ~1.6s | **Açık Ara En İyi (SOTA):** Gitar kanalını otomatik tanır, akor ve nota bitişlerinde rakipsiz. |
| 🥈 | **Spotify Basic Pitch** | CNN TFLite + Melodia Trick | CPU/GPU | **%93.9** | **%91.0** | %82.7 | %77.0 | %58.2 | **~1.1s** | **En Yüksek Vuruş Hassasiyeti:** Onset yakalamada lider, çok hızlı, hafif uzatma (offset) eğilimli. |
| 🥉 | **TorchCREPE** | Deep Conv Pitch Estimator | CUDA (GPU) | %84.5 | %27.0 | %83.0 | %33.1 | %42.8 | ~1.3s | **Melodi & Artikülasyon Uzmanı:** 10ms çözünürlükle bend/vibrato takibinde harika, akorda monofonik. |
| 4 | **ByteDance CRNN** | ResNet + Bi-GRU (Piano) | CUDA (GPU) | %35.3 | %48.7 | %38.4 | %53.3 | %22.7 | ~3.2s | **Piyano Odaklı:** Gitardaki pena vuruşlarını gürültü sayıp kaçırıyor, rock ritminde kısmen başarılı. |
| 5 | **Omnizart (Stream)** | CFP + CNN Feature Maps | CPU | %31.2 | %10.1 | %24.8 | %9.6 | %1.1 | ~13.9s | **Düşük Performans:** Gitarda çok fazla hayalet nota üretiyor, CPU'da yavaş çalışıyor. |

---

## 1. 🎸 Solo Gitar Performansı Karşılaştırması (421 Ground Truth Nota)

Solo parçalarda müzisyenin tek tel üzerinden icra ettiği hızlı pasajlar, staccato pena vuruşları ve melodi çizgileri test edilmiştir:

| Model | İşlem Süresi (s) | Onset Recall (Vuruş) | Pitch Recall (Doğru Nota) | Pitch F1 Skoru | Strict F1 (Bitiş Dahil) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| 🏆 **YourMT3+** | 1.26s | %89.3 | %87.5 | **%90.8** | **%81.9** |
| 🥈 **Spotify Basic Pitch** | **1.17s** | **%93.9** | **%92.3** | %82.7 | %64.4 |
| 🥉 **TorchCREPE** | 1.22s | %84.5 | %82.6 | %83.0 | %68.1 |
| 🎹 **ByteDance CRNN** | 2.93s | %35.3 | %30.3 | %38.4 | %18.5 |
| 🎼 **Omnizart** | 13.17s | %31.2 | %26.0 | %24.8 | %1.1 |

---

## 2. 🎼 Akor / Polifoni Performansı Karşılaştırması (1.122 Ground Truth Nota)

Funk 16'lık ritimler, Jazz 7'li/9'lu akorları ve Bossa Nova fingerstyle arpejlerini içeren çok sesli kayıtlar:

| Model | İşlem Süresi (s) | Onset Recall (Akor Telleri) | Pitch Recall (Doğru Notalar) | Pitch F1 Skoru | Strict F1 (Sönüm Dahil) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| 🏆 **YourMT3+** | 2.01s | %86.3 | %84.1 | **%85.9** | **%73.9** |
| 🥈 **Spotify Basic Pitch** | **1.04s** | **%91.0** | **%86.7** | %77.0 | %51.9 |
| 🎹 **ByteDance CRNN** | 3.50s | %48.7 | %42.6 | %53.3 | %26.9 |
| 🥉 **TorchCREPE** | 1.42s | %27.0 | %23.8 | %33.1 | %17.5 |
| 🎼 **Omnizart** | 14.66s | %10.1 | %7.0 | %9.6 | %1.0 |

---

## 3. 🔬 Derinlemesine Model Analizleri

### 🌟 1. YourMT3+ (Genel Şampiyon)
* **Kanal Ayrımı:** Üretilen MIDI'de General MIDI Program 24 (`Guitar clean`) kanalını otomatik olarak atar.
* **Akor Netliği:** Akor basıldığında tellerin birbirine karışmasını engeller, her tele denk gelen notayı ayrı event olarak doğru oktavda yakalar.
* **Nota Bitişleri (Strict F1):** Susturma (palm-mute) ve tel sönüm sürelerini %81.9 (solo) ve %73.9 (akor) başarıyla yakalayarak tablatür üretimi için en temiz notasyonu sunar.

### ⚡ 2. Spotify Basic Pitch (Hız ve Vuruş Lideri)
* **Onset Yakalama:** Solo parçalarda %93.9, akorlarda %91.0 vuruş yakalama oranıyla tüm modelleri geçmiştir.
* **Kullanım Kolaylığı:** TFLite motoru sayesinde GPU zorunluluğu olmadan CPU üzerinde dahi 1 saniyede işlem yapar.
* **Geliştirme Notu:** Nota bitişlerinde küçük bir post-processing filtresi (duration thresholding) uygulanırsa YourMT3+'a çok yakın bir tablatür motoru oluşturulabilir.

### 🎯 3. TorchCREPE (Solo ve Bükme / Vibrato Uzmanı)
* **Mikro Tonlar:** 10ms kare adımında pitch tahmin ettiği için özellikle gitardaki çeyrek ton bendler, slide ve vibratoları yakalamada eşsizdir.
* **Sınırlılık:** Mimarisi monofonik (tek ses) olduğundan akor basıldığında yalnızca en baskın armonik çizgiyi takip eder.

---

## 4. 📁 Model Test Raporları ve Arşivlenmiş MIDI Dosyaları

Tüm modellerin bağımsız 5 aşamalı test raporları ve zaman damgalı MIDI dosyalarına aşağıdaki bağlantılardan erişilebilir:

* **YourMT3+:** [Özet Raporu](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/yourmt3/tests/guitar/results-summary.md) | [MIDI Arşivi (50 dosya)](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/yourmt3/midi/guitar/)
* **Spotify Basic Pitch:** [Özet Raporu](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/basic-pitch/tests/guitar/results-summary.md) | [MIDI Arşivi (50 dosya)](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/basic-pitch/midi/guitar/)
* **TorchCREPE:** [Özet Raporu](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/torchcrepe/tests/guitar/results-summary.md) | [MIDI Arşivi (50 dosya)](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/torchcrepe/midi/guitar/)
* **ByteDance CRNN:** [Özet Raporu](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/bytedance/tests/guitar/results-summary.md) | [MIDI Arşivi (50 dosya)](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/bytedance/midi/guitar/)
* **Omnizart:** [Özet Raporu](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/omnizart/tests/guitar/results-summary.md) | [MIDI Arşivi (50 dosya)](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/omnizart/midi/guitar/)
