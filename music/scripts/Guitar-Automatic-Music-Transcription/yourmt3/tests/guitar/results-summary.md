# 📊 YourMT3+ Multi-Track Transformer — 10 Parçalı 5 Aşamalı Benchmark Özeti

**Tarih:** 20 Kasım 2026 — 16:00  
**Model:** YourMT3+ Multi-Track Transformer  
**Doğrulama Veri Seti:** NYU MARL GuitarSet (ISMIR 2018 - 10 Parça: 5 Solo [421 Nota] + 5 Comping [1.122 Nota], Toplam: 1.543 Nota)  
**Test Sayısı:** 5 Bağımsız Koşum (1'er dakika aralıklı, zaman damgalı MIDI arşivli)  
**Arşiv Dizini:** [`scripts/Guitar-Automatic-Music-Transcription/yourmt3/midi/`](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/yourmt3/midi/guitar)  

---

## 📌 Konsolide Özet Metrikleri

* **🎸 5 Solo Parça Ortalaması:**
  * Ortalama İşlem Süresi: **1.26s**
  * Onset Recall (Vuruş Yakalama): **%89.3**
  * Pitch F1 Skoru (Nota + Zaman): **%90.8**
  * Strict F1 Skoru (Offset/Bitiş Dahil): **%81.9**

* **🎼 5 Comping / Akor Parçası Ortalaması:**
  * Ortalama İşlem Süresi: **2.01s**
  * Onset Recall (Akor Tellerini Yakalama): **%86.3**
  * Pitch F1 Skoru (Akor Nota Doğruluğu): **%85.9**
  * Strict F1 Skoru (Susturma/Bitiş Dahil): **%73.9**

---

## 1. 🏁 5 Koşumun Karşılaştırma Tablosu

| Koşum No | Zaman | Solo Süre | Comp Süre | Solo Onset Rec. | Solo Pitch F1 | Solo Strict F1 | Comp Onset Rec. | Comp Pitch F1 | Comp Strict F1 | Rapor Bağlantısı |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Test 1** | `14:02` | 1.63s | 2.15s | **%89.3** | **%90.8** | %81.9 | **%86.3** | **%85.9** | %73.9 | [Rapor 1](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/yourmt3/tests/guitar/result-20261119-1402.md) |
| **Test 2** | `14:07` | 1.18s | 2.01s | **%89.3** | **%90.8** | %81.9 | **%86.3** | **%85.9** | %73.9 | [Rapor 2](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/yourmt3/tests/guitar/result-20261119-1407.md) |
| **Test 3** | `14:09` | 1.17s | 1.96s | **%89.3** | **%90.8** | %81.9 | **%86.3** | **%85.9** | %73.9 | [Rapor 3](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/yourmt3/tests/guitar/result-20261119-1409.md) |
| **Test 4** | `14:10` | 1.17s | 1.95s | **%89.3** | **%90.8** | %81.9 | **%86.3** | **%85.9** | %73.9 | [Rapor 4](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/yourmt3/tests/guitar/result-20261119-1410.md) |
| **Test 5** | `14:12` | 1.14s | 1.97s | **%89.3** | **%90.8** | %81.9 | **%86.3** | **%85.9** | %73.9 | [Rapor 5](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/yourmt3/tests/guitar/result-20261119-1412.md) |
| **GENEL ORTALAMA** | — | **1.26s** | **2.01s** | **%89.3** | **%90.8** | **%81.9** | **%86.3** | **%85.9** | **%73.9** | — |

---

## 2. 🔬 Değerlendirme & Gözlemler

* **Kararlılık:** Her test bağımsız olarak zaman damgalı `.mid` dosyaları ile `midi/` klasörüne yazılmış ve MIR doğrulaması gerçekleştirilmiştir.
* **Metrik Uyumu:** NYU MARL GuitarSet referans JAMS etiketleri üzerinden Onset toleransı 50ms, Pitch toleransı 50 cent olarak hesaplanmıştır.
