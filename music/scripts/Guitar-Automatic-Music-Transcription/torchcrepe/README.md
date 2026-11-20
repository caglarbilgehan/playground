# 🎵 TorchCREPE - Monophonic Pitch Estimation & Evaluation

Bu modül, derin öğrenme tabanlı [TorchCREPE](https://github.com/maxrmorrison/torchcrepe) modelini kullanarak tek sesli (monofonik) melodi ve soloların frekansını GPU üzerinde yüksek hassasiyetle çıkarır, nota segmentasyonu yaparak MIDI'ye dönüştürür.

## 📁 Dizin Yapısı
* `transcribe.py`: Giriş ses dosyasından perde çıkararak `midi/guitar/` klasörüne kaydeder.
* `evaluate.py`: Üretilen MIDI dosyasını GuitarSet JAMS referansıyla `mir_eval` kullanarak bilimsel olarak değerlendirir.
* `benchmark.py`: Solo ve Comping testlerini çalıştırır, MIDI çıktılarını `midi/guitar/` altına zaman damgasıyla kaydeder ve `tests/guitar/result-<zaman>.md` raporunu oluşturur.
* `midi/guitar/`: Zaman damgalı üretilen tüm `.mid` dosyaları.
* `tests/guitar/`: Bireysel ve özet benchmark raporları (`result-*.md`, `results-summary.md`).
