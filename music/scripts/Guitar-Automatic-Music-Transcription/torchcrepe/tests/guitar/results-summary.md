# 📊 TorchCREPE Monophonic Pitch Estimator — 10 Parçalı 5 Aşamalı Benchmark Özeti

**Tarih:** 20 Kasım 2026 — 16:00  
**Model:** TorchCREPE Monophonic Pitch Estimator  
**Doğrulama Veri Seti:** NYU MARL GuitarSet (ISMIR 2018 - 10 Parça: 5 Solo [421 Nota] + 5 Comping [1.122 Nota], Toplam: 1.543 Nota)  
**Test Sayısı:** 5 Bağımsız Koşum (1'er dakika aralıklı, zaman damgalı MIDI arşivli)  
**Arşiv Dizini:** [`scripts/Guitar-Automatic-Music-Transcription/torchcrepe/midi/`](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/torchcrepe/midi/guitar)  

---

## 📌 Konsolide Özet Metrikleri

* **🎸 5 Solo Parça Ortalaması:**
  * Ortalama İşlem Süresi: **6.55s**
  * Onset Recall (Vuruş Yakalama): **%84.5**
  * Pitch F1 Skoru (Nota + Zaman): **%83.0**
  * Strict F1 Skoru (Offset/Bitiş Dahil): **%68.1**

* **🎼 5 Comping / Akor Parçası Ortalaması:**
  * Ortalama İşlem Süresi: **9.27s**
  * Onset Recall (Akor Tellerini Yakalama): **%27.0**
  * Pitch F1 Skoru (Akor Nota Doğruluğu): **%33.1**
  * Strict F1 Skoru (Susturma/Bitiş Dahil): **%17.5**

---

## 1. 🏁 5 Koşumun Karşılaştırma Tablosu

| Koşum No | Zaman | Solo Süre | Comp Süre | Solo Onset Rec. | Solo Pitch F1 | Solo Strict F1 | Comp Onset Rec. | Comp Pitch F1 | Comp Strict F1 | Rapor Bağlantısı |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Test 1** | `14:21` | 27.86s | 40.67s | **%84.8** | **%82.7** | %68.4 | **%27.3** | **%33.2** | %17.6 | [Rapor 1](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/torchcrepe/tests/guitar/result-20261119-1421.md) |
| **Test 2** | `14:28` | 1.22s | 1.42s | **%83.8** | **%82.4** | %67.0 | **%26.9** | **%32.9** | %17.3 | [Rapor 2](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/torchcrepe/tests/guitar/result-20261119-1428.md) |
| **Test 3** | `14:30` | 1.23s | 1.42s | **%85.1** | **%83.0** | %68.8 | **%27.1** | **%32.9** | %17.3 | [Rapor 3](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/torchcrepe/tests/guitar/result-20261119-1430.md) |
| **Test 4** | `14:31` | 1.22s | 1.42s | **%83.9** | **%82.9** | %67.7 | **%26.9** | **%33.1** | %17.5 | [Rapor 4](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/torchcrepe/tests/guitar/result-20261119-1431.md) |
| **Test 5** | `14:33` | 1.21s | 1.43s | **%84.8** | **%83.9** | %68.7 | **%27.0** | **%33.2** | %17.6 | [Rapor 5](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/torchcrepe/tests/guitar/result-20261119-1433.md) |
| **GENEL ORTALAMA** | — | **6.55s** | **9.27s** | **%84.5** | **%83.0** | **%68.1** | **%27.0** | **%33.1** | **%17.5** | — |

---

## 2. 🔬 Değerlendirme & Gözlemler

* **Kararlılık:** Her test bağımsız olarak zaman damgalı `.mid` dosyaları ile `midi/` klasörüne yazılmış ve MIR doğrulaması gerçekleştirilmiştir.
* **Metrik Uyumu:** NYU MARL GuitarSet referans JAMS etiketleri üzerinden Onset toleransı 50ms, Pitch toleransı 50 cent olarak hesaplanmıştır.
