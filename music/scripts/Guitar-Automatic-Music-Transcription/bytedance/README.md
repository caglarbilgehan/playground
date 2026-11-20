# ByteDance CRNN Music Transcription - Test & Benchmark Araçları

Bu klasör, **ByteDance Research** tarafından geliştirilen yüksek çözünürlüklü evrişimli ve tekrarlayan sinir ağı (CRNN) modelini test etmek ve GuitarSet ile doğrulamak için hazırlandı.

---

## 🚀 Hızlı Başlangıç

```bash
cd /home/cserver/projects/open-projects/playground/music/scripts/Guitar-Automatic-Music-Transcription/bytedance
source ../../../.venv/bin/activate
```

---

## 📜 Scriptler

* **`benchmark.py`**: Solo ve Akor kayıtlarını GPU üzerinde test eder ve özet performans tablosunu çıkarır:
  ```bash
  python benchmark.py
  ```

* **`transcribe.py`**: Tek bir ses dosyasını GPU hızlandırmasıyla MIDI'ye dönüştürür:
  ```bash
  python transcribe.py
  ```

* **`evaluate.py`**: Çıkarılan MIDI dosyasını GuitarSet anotasyonlarıyla bilimsel olarak kıyaslar:
  ```bash
  python evaluate.py
  ```
