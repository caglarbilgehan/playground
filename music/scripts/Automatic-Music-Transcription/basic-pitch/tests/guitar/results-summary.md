# 📊 Spotify Basic Pitch (ICASSP 2022) — 10 Parçalı 5 Aşamalı Benchmark Özeti

**Tarih:** 20 Kasım 2026 — 16:00  
**Model:** Spotify Basic Pitch (ICASSP 2022)  
**Doğrulama Veri Seti:** NYU MARL GuitarSet (ISMIR 2018 - 10 Parça: 5 Solo [421 Nota] + 5 Comping [1.122 Nota], Toplam: 1.543 Nota)  
**Test Sayısı:** 5 Bağımsız Koşum (1'er dakika aralıklı, zaman damgalı MIDI arşivli)  
**Arşiv Dizini:** [`scripts/Automatic-Music-Transcription/basic-pitch/midi/`](file:///home/cserver/projects/open-projects/playground/music/scripts/Automatic-Music-Transcription/basic-pitch/midi/guitar)  

---

## 📌 Konsolide Özet Metrikleri

* **🎸 5 Solo Parça Ortalaması:**
  * Ortalama İşlem Süresi: **1.17s**
  * Onset Recall (Vuruş Yakalama): **%93.9**
  * Pitch F1 Skoru (Nota + Zaman): **%82.7**
  * Strict F1 Skoru (Offset/Bitiş Dahil): **%64.4**

* **🎼 5 Comping / Akor Parçası Ortalaması:**
  * Ortalama İşlem Süresi: **1.04s**
  * Onset Recall (Akor Tellerini Yakalama): **%91.0**
  * Pitch F1 Skoru (Akor Nota Doğruluğu): **%77.0**
  * Strict F1 Skoru (Susturma/Bitiş Dahil): **%51.9**

---

## 1. 🏁 5 Koşumun Karşılaştırma Tablosu

| Koşum No | Zaman | Solo Süre | Comp Süre | Solo Onset Rec. | Solo Pitch F1 | Solo Strict F1 | Comp Onset Rec. | Comp Pitch F1 | Comp Strict F1 | Rapor Bağlantısı |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Test 1** | `14:14` | 1.25s | 1.04s | **%93.9** | **%82.7** | %64.4 | **%91.0** | **%77.0** | %51.9 | [Rapor 1](file:///home/cserver/projects/open-projects/playground/music/scripts/Automatic-Music-Transcription/basic-pitch/tests/guitar/result-20261119-1414.md) |
| **Test 2** | `14:15` | 1.19s | 1.08s | **%93.9** | **%82.7** | %64.4 | **%91.0** | **%77.0** | %51.9 | [Rapor 2](file:///home/cserver/projects/open-projects/playground/music/scripts/Automatic-Music-Transcription/basic-pitch/tests/guitar/result-20261119-1415.md) |
| **Test 3** | `14:16` | 1.14s | 1.01s | **%93.9** | **%82.7** | %64.4 | **%91.0** | **%77.0** | %51.9 | [Rapor 3](file:///home/cserver/projects/open-projects/playground/music/scripts/Automatic-Music-Transcription/basic-pitch/tests/guitar/result-20261119-1416.md) |
| **Test 4** | `14:18` | 1.09s | 1.03s | **%93.9** | **%82.7** | %64.4 | **%91.0** | **%77.0** | %51.9 | [Rapor 4](file:///home/cserver/projects/open-projects/playground/music/scripts/Automatic-Music-Transcription/basic-pitch/tests/guitar/result-20261119-1418.md) |
| **Test 5** | `14:19` | 1.19s | 1.05s | **%93.9** | **%82.7** | %64.4 | **%91.0** | **%77.0** | %51.9 | [Rapor 5](file:///home/cserver/projects/open-projects/playground/music/scripts/Automatic-Music-Transcription/basic-pitch/tests/guitar/result-20261119-1419.md) |
| **GENEL ORTALAMA** | — | **1.17s** | **1.04s** | **%93.9** | **%82.7** | **%64.4** | **%91.0** | **%77.0** | **%51.9** | — |

---

## 2. 🔬 Değerlendirme & Gözlemler

* **Kararlılık:** Her test bağımsız olarak zaman damgalı `.mid` dosyaları ile `midi/` klasörüne yazılmış ve MIR doğrulaması gerçekleştirilmiştir.
* **Metrik Uyumu:** NYU MARL GuitarSet referans JAMS etiketleri üzerinden Onset toleransı 50ms, Pitch toleransı 50 cent olarak hesaplanmıştır.
