#!/usr/bin/env python3
"""
YourMT3+ - YourMT3+ Genişletilmiş 10 Parçalık Benchmark Paketi
Transcribes 5 Solo + 5 Comping tracks, archives MIDIs with timestamps in 'midi/',
computes mir_eval metrics, and generates 'tests/result-<timestamp>.md'.
Usage:
    python benchmark.py [--run-num 1] [--total-runs 5] [--device cuda/cpu]
"""

import os
import sys
import time
import shutil
import argparse
import warnings
from datetime import datetime
import numpy as np

warnings.filterwarnings("ignore")
import torch
import torchaudio
import pretty_midi
import jams
import mir_eval

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPACE_DIR = os.path.join(BASE_DIR, "YourMT3-space")
sys.path.insert(0, SPACE_DIR)
sys.path.insert(0, os.path.join(SPACE_DIR, "amt/src"))
os.chdir(SPACE_DIR)

from model_helper import load_model_checkpoint, transcribe

def find_dataset_dir(instrument: str = "guitar") -> str:
    curr = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):
        candidate = os.path.join(curr, "test_dataset", instrument)
        if os.path.isdir(candidate):
            return candidate
        candidate_root = os.path.join(curr, "test_dataset")
        if os.path.isdir(candidate_root):
            if os.path.isdir(os.path.join(candidate_root, instrument)):
                return os.path.join(candidate_root, instrument)
            return candidate_root
        parent = os.path.dirname(curr)
        if parent == curr:
            break
        curr = parent
    return os.path.abspath(os.path.join(os.path.dirname(__file__), f"../../../test_dataset/{instrument}"))

DATASET_DIR = find_dataset_dir("guitar")
MIDI_DIR = os.path.join(BASE_DIR, "midi", "guitar")
TESTS_DIR = os.path.join(BASE_DIR, "tests", "guitar")
os.makedirs(MIDI_DIR, exist_ok=True)
os.makedirs(TESTS_DIR, exist_ok=True)

TEST_CASES = [
    # 5 Solo Melodies
    {
        "id": "solo_bn",
        "name": "Solo 1 - Bossa Nova (119 BPM)",
        "type": "Solo",
        "genre": "Bossa Nova",
        "audio": os.path.join(DATASET_DIR, "05_BN3-119-G_solo_mic.wav"),
        "jams": os.path.join(DATASET_DIR, "05_BN3-119-G_solo.jams")
    },
    {
        "id": "solo_funk",
        "name": "Solo 2 - Funk Staccato (97 BPM)",
        "type": "Solo",
        "genre": "Funk",
        "audio": os.path.join(DATASET_DIR, "03_Funk1-97-C_solo_mic.wav"),
        "jams": os.path.join(DATASET_DIR, "03_Funk1-97-C_solo.jams")
    },
    {
        "id": "solo_rock",
        "name": "Solo 3 - Rock Fast (142 BPM)",
        "type": "Solo",
        "genre": "Rock",
        "audio": os.path.join(DATASET_DIR, "00_Rock2-142-D_solo_mic.wav"),
        "jams": os.path.join(DATASET_DIR, "00_Rock2-142-D_solo.jams")
    },
    {
        "id": "solo_jazz",
        "name": "Solo 4 - Jazz Bebop (200 BPM)",
        "type": "Solo",
        "genre": "Jazz",
        "audio": os.path.join(DATASET_DIR, "04_Jazz1-200-B_solo_mic.wav"),
        "jams": os.path.join(DATASET_DIR, "04_Jazz1-200-B_solo.jams")
    },
    {
        "id": "solo_ss",
        "name": "Solo 5 - Singer-Songwriter (100 BPM)",
        "type": "Solo",
        "genre": "Singer-Songwriter",
        "audio": os.path.join(DATASET_DIR, "02_SS1-100-C#_solo_mic.wav"),
        "jams": os.path.join(DATASET_DIR, "02_SS1-100-C#_solo.jams")
    },
    # 5 Comping / Chords
    {
        "id": "comp_ss",
        "name": "Comp 1 - Singer-Songwriter Arpeggio (84 BPM)",
        "type": "Comping",
        "genre": "Singer-Songwriter",
        "audio": os.path.join(DATASET_DIR, "00_SS3-84-Bb_comp_mic.wav"),
        "jams": os.path.join(DATASET_DIR, "00_SS3-84-Bb_comp.jams")
    },
    {
        "id": "comp_funk",
        "name": "Comp 2 - Funk 16th Strumming (97 BPM)",
        "type": "Comping",
        "genre": "Funk",
        "audio": os.path.join(DATASET_DIR, "02_Funk1-97-C_comp_mic.wav"),
        "jams": os.path.join(DATASET_DIR, "02_Funk1-97-C_comp.jams")
    },
    {
        "id": "comp_rock",
        "name": "Comp 3 - Rock Driving Rhythm (117 BPM)",
        "type": "Comping",
        "genre": "Rock",
        "audio": os.path.join(DATASET_DIR, "05_Rock3-117-Bb_comp_mic.wav"),
        "jams": os.path.join(DATASET_DIR, "05_Rock3-117-Bb_comp.jams")
    },
    {
        "id": "comp_jazz",
        "name": "Comp 4 - Jazz 7th/9th Chords (150 BPM)",
        "type": "Comping",
        "genre": "Jazz",
        "audio": os.path.join(DATASET_DIR, "01_Jazz3-150-C_comp_mic.wav"),
        "jams": os.path.join(DATASET_DIR, "01_Jazz3-150-C_comp.jams")
    },
    {
        "id": "comp_bn",
        "name": "Comp 5 - Bossa Nova Fingerstyle (131 BPM)",
        "type": "Comping",
        "genre": "Bossa Nova",
        "audio": os.path.join(DATASET_DIR, "04_BN2-131-B_comp_mic.wav"),
        "jams": os.path.join(DATASET_DIR, "04_BN2-131-B_comp.jams")
    }
]

def run_benchmark(run_num: int = None, total_runs: int = None, device: str = None):
    if device is None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'

    dev_name = torch.cuda.get_device_name(0) if device == 'cuda' else 'CPU'
    ts = datetime.now().strftime("%Y%m%d-%H%M")
    ts_display = datetime.now().strftime("%d Kasım %Y — %H:%M")

    title_suffix = f" (Test {run_num} / {total_runs})" if run_num else ""
    print("=" * 85)
    print(f" YOURMT3+ - 10 PARÇALI GENİŞLETİLMİŞ GUITARSET BENCHMARK{title_suffix} ")
    print("=" * 85)
    print(f"Zaman Damgası    : {ts}")
    print(f"Hesaplama Deviceı : {device.upper()} ({dev_name})")
    print(f"MIDI Çıktı Dizini: {MIDI_DIR}")
    print(f"Rapor Çıktı Dizini: {TESTS_DIR}")
    print(f"Toplam Test Parçası: {len(TEST_CASES)} (5 Solo + 5 Comping)")

    print("\nModel belleğe alınıyor...")
    checkpoint = 'notask_all_cross_v6_xk2_amp0811_gm_ext_plus_nops_b72@model.ckpt'
    model_args = [checkpoint, '-p', '2024', '-pr', '16']
    model = load_model_checkpoint(args=model_args, device=device)
    model.eval()

    results = []

    for idx, tc in enumerate(TEST_CASES, 1):
        name = tc["name"]
        audio_path = tc["audio"]
        jams_path = tc["jams"]
        tag = tc["id"]
        ptype = tc["type"]
        genre = tc["genre"]

        mid_out = os.path.join(MIDI_DIR, f"{tag}_{ts}.mid")

        if not os.path.exists(audio_path) or not os.path.exists(jams_path):
            print(f"[UYARI] Test dosyası bulunamadı, atlanıyor: {audio_path}")
            continue

        print(f"\n[{idx}/{len(TEST_CASES)}] Test Ediliyor: {name}")

        info = torchaudio.info(audio_path)
        track_name = f"run_{run_num or 1}_{idx}_{ts}"
        audio_info = {
            'filepath': audio_path,
            'track_name': track_name,
            'sample_rate': int(info.sample_rate),
            'bits_per_sample': int(info.bits_per_sample),
            'num_channels': int(info.num_channels),
            'num_frames': int(info.num_frames),
            'duration': int(info.num_frames / info.sample_rate),
            'encoding': str.lower(info.encoding),
        }

        t0 = time.time()
        gen_midi = transcribe(model, audio_info)
        elapsed = time.time() - t0

        shutil.copyfile(gen_midi, mid_out)
        print(f"  -> MIDI: {os.path.basename(mid_out)} ({elapsed:.2f}s)")

        jam = jams.load(jams_path)
        gt_intervals, gt_pitches = [], []
        for ann in [a for a in jam.annotations if a.namespace == 'note_midi']:
            for obs in ann.data:
                gt_intervals.append([obs.time, obs.time + obs.duration])
                gt_pitches.append(obs.value)
        gt_intervals = np.array(gt_intervals)
        gt_pitches = np.array(gt_pitches)

        pm = pretty_midi.PrettyMIDI(mid_out)
        pred_intervals, pred_pitches = [], []
        for inst in pm.instruments:
            for n in inst.notes:
                pred_intervals.append([n.start, n.end])
                pred_pitches.append(n.pitch)

        pred_intervals = np.array(pred_intervals) if pred_intervals else np.empty((0, 2))
        pred_pitches = np.array(pred_pitches, dtype=float) if pred_pitches else np.empty((0,))

        if len(pred_pitches) > 0:
            ref_hz = 440.0 * (2.0 ** ((gt_pitches - 69.0) / 12.0))
            est_hz = 440.0 * (2.0 ** ((pred_pitches - 69.0) / 12.0))

            scores = mir_eval.transcription.evaluate(
                gt_intervals, ref_hz, pred_intervals, est_hz,
                onset_tolerance=0.05,
                pitch_tolerance=50.0,
                offset_ratio=0.2
            )
        else:
            scores = {}

        results.append({
            "name": name,
            "type": ptype,
            "genre": genre,
            "mid_file": mid_out,
            "mid_name": os.path.basename(mid_out),
            "time_sec": elapsed,
            "gt_count": len(gt_pitches),
            "pred_count": len(pred_pitches),
            "onset_recall": scores.get('Onset_Recall', 0) * 100,
            "onset_precision": scores.get('Onset_Precision', 0) * 100,
            "onset_f": scores.get('Onset_F-measure', 0) * 100,
            "pitch_recall": scores.get('Recall_no_offset', 0) * 100,
            "pitch_precision": scores.get('Precision_no_offset', 0) * 100,
            "pitch_f": scores.get('F-measure_no_offset', 0) * 100,
            "strict_f": scores.get('F-measure', 0) * 100
        })

    print("\n" + "=" * 95)
    print(" YOURMT3+ - 10-PIECE DETAYLI BENCHMARK SONUÇLARI")
    print("=" * 95)
    header = f"{'Track Name':<38} | {'Time (s)':<8} | {'GT':<4} | {'Pred':<6} | {'Onset Rec.':<10} | {'Pitch Rec.':<10} | {'Pitch F1':<8} | {'Strict F1'}"
    print(header)
    print("-" * 95)

    for r in results:
        row = (
            f"{r['name']:<38} | "
            f"{r['time_sec']:<8.2f} | "
            f"{r['gt_count']:<4} | "
            f"{r['pred_count']:<6} | "
            f"%{r['onset_recall']:<9.1f} | "
            f"%{r['pitch_recall']:<9.1f} | "
            f"%{r['pitch_f']:<7.1f} | "
            f"%{r['strict_f']:.1f}"
        )
        print(row)
    print("=" * 95)

    solos = [r for r in results if r['type'] == 'Solo']
    comps = [r for r in results if r['type'] == 'Comping']

    avg_solo_time = np.mean([r['time_sec'] for r in solos])
    avg_comp_time = np.mean([r['time_sec'] for r in comps])
    avg_solo_orec = np.mean([r['onset_recall'] for r in solos])
    avg_comp_orec = np.mean([r['onset_recall'] for r in comps])
    avg_solo_prec = np.mean([r['pitch_recall'] for r in solos])
    avg_comp_prec = np.mean([r['pitch_recall'] for r in comps])
    avg_solo_pf1  = np.mean([r['pitch_f'] for r in solos])
    avg_comp_pf1  = np.mean([r['pitch_f'] for r in comps])
    avg_solo_sf1  = np.mean([r['strict_f'] for r in solos])
    avg_comp_sf1  = np.mean([r['strict_f'] for r in comps])

    print(f"\n📊 BENCHMARK ÖZETİ:")
    print(f"🎸 5 Solo Ortalama : Süre: {avg_solo_time:.2f}s | Onset Rec: %{avg_solo_orec:.1f} | Pitch Rec: %{avg_solo_prec:.1f} | Pitch F1: %{avg_solo_pf1:.1f} | Strict F1: %{avg_solo_sf1:.1f}")
    print(f"🎼 5 Comping Ortalama: Süre: {avg_comp_time:.2f}s | Onset Rec: %{avg_comp_orec:.1f} | Pitch Rec: %{avg_comp_prec:.1f} | Pitch F1: %{avg_comp_pf1:.1f} | Strict F1: %{avg_comp_sf1:.1f}")

    # Markdown Raporunu Oluştur
    report_file = os.path.join(TESTS_DIR, f"result-{ts}.md")

    table_rows = ""
    for r in results:
        table_rows += f"| {r['name']} | {r['genre']} | {r['time_sec']:.2f}s | {r['gt_count']} | {r['pred_count']} | **%{r['onset_recall']:.1f}** | **%{r['pitch_recall']:.1f}** | **%{r['pitch_f']:.1f}** | %{r['strict_f']:.1f} | [`{r['mid_name']}`](file://{r['mid_file']}) |\n"

    report_content = f"""# 📊 YourMT3+ — 10 Parçalı Test & Benchmark Raporu{title_suffix}

**Tarih:** {ts_display}  
**Test Sırası:** {f"{run_num} / {total_runs}" if run_num else "1"}  
**Test Edilen Model:** YourMT3+ Multi-Track AMT (`notask_all_cross_v6_xk2`)  
**Compute Device:** {device.upper()} ({dev_name})  
**Referans Veri Seti:** NYU MARL GuitarSet (ISMIR 2018 - 10 Parça, 1.543 Nota)  
**Çalışma Ortamı:** Python 3.10 / Linux WSL2  

---

## 📌 Yönetici Özeti

Bu testte **5 farklı müzik türünden (Bossa Nova, Funk, Rock, Jazz, Singer-Songwriter)** seçilen 5 solo ve 5 comping parçası olmak üzere toplam **10 adet gitar kaydı** test edilmiştir. Çıktı MIDI dosyaları zaman damgasıyla `midi/` klasörüne arşivlenmiştir.

* **5 Solo Average:** Süre: **{avg_solo_time:.2f}s** | Onset Recall: **%{avg_solo_orec:.1f}** | Pitch Recall: **%{avg_solo_prec:.1f}** | Pitch F1: **%{avg_solo_pf1:.1f}** | Strict F1: **%{avg_solo_sf1:.1f}**
* **5 Comping Average:** Süre: **{avg_comp_time:.2f}s** | Onset Recall: **%{avg_comp_orec:.1f}** | Pitch Recall: **%{avg_comp_prec:.1f}** | Pitch F1: **%{avg_comp_pf1:.1f}** | Strict F1: **%{avg_comp_sf1:.1f}**

---

## 1. 🏁 10 Parçalık Detaylı Karşılaştırma Tablosu

| Test Parçası | Tür (Genre) | Süre (s) | GT | Tahmin | Onset Rec. | Pitch Rec. | Pitch F1 | Strict F1 | Arşivlenen MIDI |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
{table_rows}
---

## 2. 🔬 Grup İstatistikleri

### 🎸 Solo Melodi Grubu (421 GT Nota):
* Ortalama Onset Recall: %{avg_solo_orec:.2f}
* Ortalama Pitch Recall: %{avg_solo_prec:.2f}
* Ortalama Pitch F-Measure: %{avg_solo_pf1:.2f}
* Ortalama Strict F-Measure (Nota Bitişi Dahil): %{avg_solo_sf1:.2f}

### 🎼 Akor & Polifoni Grubu (1.122 GT Nota):
* Ortalama Onset Recall: %{avg_comp_orec:.2f}
* Ortalama Pitch Recall: %{avg_comp_prec:.2f}
* Ortalama Pitch F-Measure: %{avg_comp_pf1:.2f}
* Ortalama Strict F-Measure (Nota Bitişi Dahil): %{avg_comp_sf1:.2f}
"""
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"\n[OK] Rapor başarıyla oluşturuldu:\n--> {report_file}\n")
    return report_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YourMT3+ 10-Piece Benchmark Suite")
    parser.add_argument("--run-num", type=int, default=None, help="Koşum numarası (ör. 1)")
    parser.add_argument("--total-runs", type=int, default=None, help="Toplam koşum sayısı (ör. 5)")
    parser.add_argument("--device", "-d", choices=["cuda", "cpu"], default=None, help="Device")
    args = parser.parse_args()
    run_benchmark(args.run_num, args.total_runs, args.device)
