#!/usr/bin/env python3
"""
Omnizart - GuitarSet Doğrulama ve MIR Değerlendirme Scripti
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
    print(" GUITARSET Ground Truth vs OMNIZART MIDI Doğrulama (mir_eval)")
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

    print(f"{'Metrik Adı':<32} | {'Değer':<10} | {'Yorum / Açıklama'}")
    print("-" * 70)
    
    o_rec = scores.get('Onset_Recall', 0) * 100
    o_prec = scores.get('Onset_Precision', 0) * 100
    o_f = scores.get('Onset_F-measure', 0) * 100
    print(f"{'Onset Recall (Yakalama)':<32} | %{o_rec:<9.2f} | Gerçek notaları vuruluş anını yakalama oranı")
    print(f"{'Onset Precision (Kesinlik)':<32} | %{o_prec:<9.2f} | Tespit edilen vuruşların doğruluk oranı")
    print(f"{'Onset F-measure (Denge)':<32} | %{o_f:<9.2f} | Vuruş anı genel başarı skoru")
    print("-" * 70)

    p_rec = scores.get('Recall_no_offset', 0) * 100
    p_prec = scores.get('Precision_no_offset', 0) * 100
    p_f = scores.get('F-measure_no_offset', 0) * 100
    print(f"{'Pitch+Onset Recall (Perde+Vuruş)':<32} | %{p_rec:<9.2f} | Hem doğru nota hem doğru zamanda yakalama")
    print(f"{'Pitch+Onset Precision':<32} | %{p_prec:<9.2f} | Tahminlerin doğru frekansa denk gelme oranı")
    print(f"{'Pitch+Onset F-measure':<32} | %{p_f:<9.2f} | Tablatür/Nota yazımı temel başarı skoru")
    print("-" * 70)

    s_rec = scores.get('Recall', 0) * 100
    s_prec = scores.get('Precision', 0) * 100
    s_f = scores.get('F-measure', 0) * 100
    print(f"{'Strict Recall (Offset Dahil)':<32} | %{s_rec:<9.2f} | Notanın bittiği an dahil yakalama")
    print(f"{'Strict Precision (Offset Dahil)':<32} | %{s_prec:<9.2f} | Bitiş zamanı hassasiyetli kesinlik")
    print(f"{'Strict F-measure (Tam Uyum)':<32} | %{s_f:<9.2f} | Tel titreşim sönme süresi dahil katı skor")
    print("=" * 70)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GuitarSet Ground Truth vs Omnizart MIDI Doğrulama")
    parser.add_argument("--midi", "-m", help="MIDI dosyası (.mid)")
    parser.add_argument("--jams", "-j", default=DEFAULT_JAMS, help="Ground Truth JAMS dosyası")

    args = parser.parse_args()
    midi_file = args.midi or get_latest_midi()
    if not midi_file:
        print("[BİLGİ] 'midi/' klasöründe hiç MIDI bulunamadı, önce transcribe.py çalıştırılıyor...")
        from transcribe import main as transcribe_main
        sys.argv = ["transcribe.py", "--audio", os.path.join(DATASET_DIR, "guitar", "05_BN3-119-G_solo_mic.wav")]
        transcribe_main()
        midi_file = get_latest_midi()

    evaluate(midi_file, args.jams)
