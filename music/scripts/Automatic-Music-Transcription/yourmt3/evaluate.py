#!/usr/bin/env python3
"""
YourMT3+ - GuitarSet Doğrulama ve MIR Değerlendirme Scripti
Kullanım:
    python evaluate.py [--midi MIDI_DOSYASI] [--jams JAMS_DOSYASI]
"""

import os
import sys
import glob
import argparse
import warnings
import numpy as np

warnings.filterwarnings("ignore")
import pretty_midi
import jams
import mir_eval

def find_dataset_dir() -> str:
    curr = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):
        candidate = os.path.join(curr, "test_dataset")
        if os.path.isdir(candidate):
            return candidate
        parent = os.path.dirname(curr)
        if parent == curr:
            break
        curr = parent
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../test_dataset"))

DATASET_DIR = find_dataset_dir()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MIDI_DIR = os.path.join(BASE_DIR, "midi", "guitar")
DEFAULT_JAMS = os.path.join(DATASET_DIR, "guitar", "05_BN3-119-G_solo.jams")

def get_latest_midi() -> str:
    files = glob.glob(os.path.join(MIDI_DIR, "*.mid"))
    if not files:
        return None
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]

def midi_pitch_to_hz(pitch_array: np.ndarray) -> np.ndarray:
    return 440.0 * (2.0 ** ((pitch_array - 69.0) / 12.0))

def load_jams_ground_truth(jams_path: str):
    if not os.path.exists(jams_path):
        raise FileNotFoundError(f"JAMS dosyası bulunamadı: {jams_path}")
    
    jam = jams.load(jams_path)
    gt_intervals, gt_pitches = [], []
    for ann in [a for a in jam.annotations if a.namespace == 'note_midi']:
        for obs in ann.data:
            gt_intervals.append([obs.time, obs.time + obs.duration])
            gt_pitches.append(obs.value)
            
    gt_intervals = np.array(gt_intervals)
    gt_pitches = np.array(gt_pitches)
    sort_idx = np.argsort(gt_intervals[:, 0])
    return gt_intervals[sort_idx], gt_pitches[sort_idx]

def load_midi_predictions(midi_path: str):
    if not os.path.exists(midi_path):
        raise FileNotFoundError(f"MIDI dosyası bulunamadı: {midi_path}")
        
    pm = pretty_midi.PrettyMIDI(midi_path)
    pred_intervals, pred_pitches = [], []
    for inst in pm.instruments:
        for n in inst.notes:
            pred_intervals.append([n.start, n.end])
            pred_pitches.append(n.pitch)
            
    if not pred_intervals:
        return np.empty((0, 2)), np.empty((0,))
        
    pred_intervals = np.array(pred_intervals)
    pred_pitches = np.array(pred_pitches, dtype=float)
    sort_idx = np.argsort(pred_intervals[:, 0])
    return pred_intervals[sort_idx], pred_pitches[sort_idx]

def evaluate(midi_path: str, jams_path: str):
    print("=" * 70)
    print(" GUITARSET Ground Truth vs YOURMT3+ MIDI Doğrulama (mir_eval)")
    print("=" * 70)
    print(f"MIDI Tahmin Dosyası : {midi_path}")
    print(f"JAMS Referans (GT)  : {jams_path}")
    print("-" * 70)

    gt_intervals, gt_pitches = load_jams_ground_truth(jams_path)
    pred_intervals, pred_pitches = load_midi_predictions(midi_path)

    print(f"Gerçek (Ground Truth) Toplam Nota : {len(gt_pitches)}")
    print(f"Modelin Tahmin Ettiği Toplam Nota : {len(pred_pitches)}")
    print("-" * 70)

    if len(pred_pitches) == 0:
        print("[HATA] MIDI dosyasında hiç nota bulunamadı!")
        return

    ref_hz = midi_pitch_to_hz(gt_pitches)
    est_hz = midi_pitch_to_hz(pred_pitches)

    scores = mir_eval.transcription.evaluate(
        gt_intervals, ref_hz, pred_intervals, est_hz,
        onset_tolerance=0.05,
        pitch_tolerance=50.0,
        offset_ratio=0.2
    )

    print(" 📈 MIR_EVAL METRİKLERİ:")
    print("-" * 70)
    print("1. Onset Doğruluğu (Zamanlama +/- 50ms):")
    print(f"   * Onset Precision (Kesinlik) : %{scores['Onset_Precision'] * 100:.2f}")
    print(f"   * Onset Recall (Yakalama)    : %{scores['Onset_Recall'] * 100:.2f}")
    print(f"   * Onset F-Measure            : %{scores['Onset_F-measure'] * 100:.2f}")
    print()
    print("2. Nota Doğruluğu (Pitch + Onset, Offsetsiz):")
    print(f"   * Pitch Precision            : %{scores['Precision_no_offset'] * 100:.2f}")
    print(f"   * Pitch Recall               : %{scores['Recall_no_offset'] * 100:.2f}")
    print(f"   * Pitch F-Measure            : %{scores['F-measure_no_offset'] * 100:.2f}")
    print()
    print("3. Sıkı Doğruluk (Pitch + Onset + Offset):")
    print(f"   * Strict Precision           : %{scores['Precision'] * 100:.2f}")
    print(f"   * Strict Recall              : %{scores['Recall'] * 100:.2f}")
    print(f"   * Strict F-Measure           : %{scores['F-measure'] * 100:.2f}")
    print("=" * 70)
    return scores

def main():
    parser = argparse.ArgumentParser(description="YourMT3+ MIDI Çıktısını GuitarSet ile Değerlendir")
    parser.add_argument("--midi", type=str, default=None, help="Değerlendirilecek MIDI dosyası")
    parser.add_argument("--jams", type=str, default=DEFAULT_JAMS, help="GuitarSet JAMS referans dosyası")
    args = parser.parse_args()

    midi_path = args.midi or get_latest_midi()
    if not midi_path or not os.path.exists(midi_path):
        print("[HATA] Değerlendirilecek MIDI dosyası bulunamadı. Lütfen önce transkripsiyon yapın.")
        sys.exit(1)

    evaluate(midi_path, args.jams)

if __name__ == "__main__":
    main()
