# 📊 ByteDance CRNN (High-Resolution Piano Transcription) — 10 Parçalı 5 Aşamalı Benchmark Özeti

**Tarih:** 20 Kasım 2026 — 16:00  
**Model:** ByteDance CRNN (High-Resolution Piano Transcription)  
**Doğrulama Veri Seti:** NYU MARL GuitarSet (ISMIR 2018 - 10 Parça: 5 Solo [421 Nota] + 5 Comping [1.122 Nota], Toplam: 1.543 Nota)  
**Test Sayısı:** 5 Bağımsız Koşum (1'er dakika aralıklı, zaman damgalı MIDI arşivli)  
**Arşiv Dizini:** [`scripts/Automatic-Music-Transcription/bytedance/midi/`](file:///home/cserver/projects/open-projects/playground/music/scripts/Automatic-Music-Transcription/bytedance/midi/guitar)  

---

## 📌 Konsolide Özet Metrikleri

* **🎸 5 Solo Parça Ortalaması:**
  * Ortalama İşlem Süresi: **2.93s**
  * Onset Recall (Vuruş Yakalama): **%35.3**
  * Pitch F1 Skoru (Nota + Zaman): **%38.4**
  * Strict F1 Skoru (Offset/Bitiş Dahil): **%18.5**

* **🎼 5 Comping / Akor Parçası Ortalaması:**
  * Ortalama İşlem Süresi: **3.50s**
  * Onset Recall (Akor Tellerini Yakalama): **%48.7**
  * Pitch F1 Skoru (Akor Nota Doğruluğu): **%53.3**
  * Strict F1 Skoru (Susturma/Bitiş Dahil): **%26.9**

---

## 1. 🏁 5 Koşumun Karşılaştırma Tablosu

| Koşum No | Zaman | Solo Süre | Comp Süre | Solo Onset Rec. | Solo Pitch F1 | Solo Strict F1 | Comp Onset Rec. | Comp Pitch F1 | Comp Strict F1 | Rapor Bağlantısı |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Test 1** | `14:54` | 2.85s | 3.43s | **%35.3** | **%38.4** | %18.5 | **%48.7** | **%53.3** | %26.9 | [Rapor 1](file:///home/cserver/projects/open-projects/playground/music/scripts/Automatic-Music-Transcription/bytedance/tests/guitar/result-20261119-1454.md) |
| **Test 2** | `14:56` | 2.90s | 3.54s | **%35.3** | **%38.4** | %18.5 | **%48.7** | **%53.3** | %26.9 | [Rapor 2](file:///home/cserver/projects/open-projects/playground/music/scripts/Automatic-Music-Transcription/bytedance/tests/guitar/result-20261119-1456.md) |
| **Test 3** | `14:58` | 2.92s | 3.49s | **%35.3** | **%38.4** | %18.5 | **%48.7** | **%53.3** | %26.9 | [Rapor 3](file:///home/cserver/projects/open-projects/playground/music/scripts/Automatic-Music-Transcription/bytedance/tests/guitar/result-20261119-1458.md) |
| **Test 4** | `15:00` | 2.83s | 3.56s | **%35.3** | **%38.4** | %18.5 | **%48.7** | **%53.3** | %26.9 | [Rapor 4](file:///home/cserver/projects/open-projects/playground/music/scripts/Automatic-Music-Transcription/bytedance/tests/guitar/result-20261119-1500.md) |
| **Test 5** | `15:01` | 3.15s | 3.48s | **%35.3** | **%38.4** | %18.5 | **%48.7** | **%53.3** | %26.9 | [Rapor 5](file:///home/cserver/projects/open-projects/playground/music/scripts/Automatic-Music-Transcription/bytedance/tests/guitar/result-20261119-1501.md) |
| **GENEL ORTALAMA** | — | **2.93s** | **3.50s** | **%35.3** | **%38.4** | **%18.5** | **%48.7** | **%53.3** | **%26.9** | — |

---

## 2. 🔬 Değerlendirme & Gözlemler

* **Kararlılık:** Her test bağımsız olarak zaman damgalı `.mid` dosyaları ile `midi/` klasörüne yazılmış ve MIR doğrulaması gerçekleştirilmiştir.
* **Metrik Uyumu:** NYU MARL GuitarSet referans JAMS etiketleri üzerinden Onset toleransı 50ms, Pitch toleransı 50 cent olarak hesaplanmıştır.
