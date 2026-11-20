# 📊 Omnizart Music (Stream Mode) — 10 Parçalı 5 Aşamalı Benchmark Özeti

**Tarih:** 20 Kasım 2026 — 16:00  
**Model:** Omnizart Music (Stream Mode)  
**Doğrulama Veri Seti:** NYU MARL GuitarSet (ISMIR 2018 - 10 Parça: 5 Solo [421 Nota] + 5 Comping [1.122 Nota], Toplam: 1.543 Nota)  
**Test Sayısı:** 5 Bağımsız Koşum (1'er dakika aralıklı, zaman damgalı MIDI arşivli)  
**Arşiv Dizini:** [`scripts/Guitar-Automatic-Music-Transcription/omnizart/midi/`](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/omnizart/midi/guitar)  

---

## 📌 Konsolide Özet Metrikleri

* **🎸 5 Solo Parça Ortalaması:**
  * Ortalama İşlem Süresi: **13.17s**
  * Onset Recall (Vuruş Yakalama): **%31.2**
  * Pitch F1 Skoru (Nota + Zaman): **%24.8**
  * Strict F1 Skoru (Offset/Bitiş Dahil): **%1.1**

* **🎼 5 Comping / Akor Parçası Ortalaması:**
  * Ortalama İşlem Süresi: **14.66s**
  * Onset Recall (Akor Tellerini Yakalama): **%10.1**
  * Pitch F1 Skoru (Akor Nota Doğruluğu): **%9.6**
  * Strict F1 Skoru (Susturma/Bitiş Dahil): **%1.0**

---

## 1. 🏁 5 Koşumun Karşılaştırma Tablosu

| Koşum No | Zaman | Solo Süre | Comp Süre | Solo Onset Rec. | Solo Pitch F1 | Solo Strict F1 | Comp Onset Rec. | Comp Pitch F1 | Comp Strict F1 | Rapor Bağlantısı |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Test 1** | `14:34` | 11.34s | 12.39s | **%31.2** | **%24.8** | %1.1 | **%10.1** | **%9.6** | %1.0 | [Rapor 1](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/omnizart/tests/guitar/result-20261119-1434.md) |
| **Test 2** | `14:38` | 11.47s | 13.79s | **%31.2** | **%24.8** | %1.1 | **%10.1** | **%9.6** | %1.0 | [Rapor 2](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/omnizart/tests/guitar/result-20261119-1438.md) |
| **Test 3** | `14:42` | 13.30s | 14.60s | **%31.2** | **%24.8** | %1.1 | **%10.1** | **%9.6** | %1.0 | [Rapor 3](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/omnizart/tests/guitar/result-20261119-1442.md) |
| **Test 4** | `14:45` | 13.05s | 13.86s | **%31.2** | **%24.8** | %1.1 | **%10.1** | **%9.6** | %1.0 | [Rapor 4](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/omnizart/tests/guitar/result-20261119-1445.md) |
| **Test 5** | `14:49` | 16.67s | 18.64s | **%31.2** | **%24.8** | %1.1 | **%10.1** | **%9.6** | %1.0 | [Rapor 5](file:///home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/omnizart/tests/guitar/result-20261119-1449.md) |
| **GENEL ORTALAMA** | — | **13.17s** | **14.66s** | **%31.2** | **%24.8** | **%1.1** | **%10.1** | **%9.6** | **%1.0** | — |

---

## 2. 🔬 Değerlendirme & Gözlemler

* **Kararlılık:** Her test bağımsız olarak zaman damgalı `.mid` dosyaları ile `midi/` klasörüne yazılmış ve MIR doğrulaması gerçekleştirilmiştir.
* **Metrik Uyumu:** NYU MARL GuitarSet referans JAMS etiketleri üzerinden Onset toleransı 50ms, Pitch toleransı 50 cent olarak hesaplanmıştır.
