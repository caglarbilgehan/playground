# 🎵 Omnizart - Müzik Transkripsiyon & Doğrulama Araçları

Bu modül, [Omnizart](https://github.com/Music-and-Culture-Technology-Lab/omnizart) çok amaçlı müzik transkripsiyon kütüphanesini kullanarak ses dosyalarını MIDI'ye dönüştürür ve GuitarSet veri seti üzerinde test eder.

## 📁 Dizin Yapısı
* `transcribe.py`: Tek bir ses dosyasını transkribe eder ve `midi/guitar/` klasörüne kaydeder.
* `evaluate.py`: Üretilen MIDI dosyasını GuitarSet JAMS referansıyla `mir_eval` kullanarak bilimsel olarak değerlendirir.
* `benchmark.py`: Solo ve Comping testlerini çalıştırır, MIDI çıktılarını `midi/guitar/` altına zaman damgasıyla kaydeder ve `tests/guitar/result-<zaman>.md` raporunu oluşturur.
* `midi/guitar/`: Zaman damgalı üretilen tüm `.mid` dosyaları.
* `tests/guitar/`: Bireysel ve özet benchmark raporları (`result-*.md`, `results-summary.md`).
