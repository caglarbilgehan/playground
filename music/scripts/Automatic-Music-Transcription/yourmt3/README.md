# 🎵 YourMT3+ - Multi-Track Music Transcription & Evaluation

Bu modül, KAIST ve mimbres ekibi tarafından geliştirilen state-of-the-art [YourMT3+](https://github.com/mimbres/yourmt3) modelini kullanarak çok enstrümanlı ve çok kanallı müzik transkripsiyonu gerçekleştirir ve GuitarSet veri seti üzerinde test eder.

## 📁 Dizin Yapısı
* `transcribe.py`: Giriş ses dosyasını transkribe eder ve `midi/guitar/` klasörüne kaydeder.
* `evaluate.py`: Üretilen MIDI dosyasını GuitarSet JAMS referansıyla `mir_eval` kullanarak bilimsel olarak değerlendirir.
* `benchmark.py`: Solo ve Comping testlerini çalıştırır, MIDI çıktılarını `midi/guitar/` altına zaman damgasıyla kaydeder ve `tests/guitar/result-<zaman>.md` raporunu oluşturur.
* `midi/guitar/`: Zaman damgalı üretilen tüm `.mid` dosyaları.
* `tests/guitar/`: Bireysel ve özet benchmark raporları (`result-*.md`, `results-summary.md`).
