# Spotify Basic Pitch - Test & Doğrulama Araçları

Bu klasör, ses dosyalarını (Audio) MIDI'ye çevirme ve GuitarSet bilimsel veri seti ile doğrulama yapabilmeniz için hazırlandı.

---

## 🚀 Hızlı Başlangıç

Klasör konumundayken sanal ortamı aktif edin:

```bash
cd /home/cserver/projects/open-projects/playground/music/scripts/Automatic-Music-Transcription/basic-pitch
source ../../../.venv/bin/activate
```

---

## 📜 Scriptler ve Kullanımları

### 1. `benchmark.py` (Tek Tıkla Karşılaştırma)
10 parçalık benchmark testini (5 Solo + 5 Comping) çalıştırır, MIDI çıktılarını `midi/guitar/` altına kaydeder, `mir_eval` ile metrikleri hesaplar ve `tests/guitar/result-<zaman>.md` raporunu oluşturur:

```bash
python benchmark.py [--run-num 1] [--total-runs 5]
```

---

### 2. `transcribe.py` (Ses -> MIDI Dönüştürme)
İstediğiniz bir ses dosyasını MIDI'ye dönüştürür. Çıkan notaların başlangıç-bitiş zamanlarını ve frekans aralığını terminalde listeler:

```bash
python transcribe.py
python transcribe.py --audio /yol/ses.wav --output /yol/cikti.mid
python transcribe.py --onset-thresh 0.6 --frame-thresh 0.4
```

---

### 3. `evaluate.py` (GuitarSet Doğrulaması)
Üretilen MIDI dosyasını GuitarSet'in gerçek anotasyonlarıyla (`.jams`) karşılaştırarak `mir_eval` standartlarında kesinlik (Precision), yakalama (Recall) ve F-Measure skorlarını hesaplar:

```bash
python evaluate.py [--midi /yol/cikti.mid] [--jams /yol/referans.jams]
```

---

## 📊 Metrikler Ne Anlama Geliyor?

| Metrik | Açıklama |
| :--- | :--- |
| **Onset Recall** | Gerçek notaların vuruluş anını yakalama oranı (%90 üzeri mükemmeldir). |
| **Pitch F1** | Hem vuruş anı hem de doğru nota (frekans) eşleşme oranı (Tablatür için en kritik oran). |
| **Strict F1** | Notanın bitiş (tel titreşiminin sönüm) süresini de 50ms hassasiyetle arayan en katı metrik. |
