#!/usr/bin/env python3
"""
TorchCREPE - Gitar Monofonik Perde Tahmini ve MIDI Transkripsiyonu
Ses dosyasından CREPE derin öğrenme modeli ile sürekli perde çıkarır,
nota segmentasyonu yaparak MIDI dosyası oluşturur.
"""

import os
import sys
import time
import argparse
import warnings
import numpy as np

warnings.filterwarnings("ignore")
import torch
import torchcrepe
import librosa
import pretty_midi

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
os.makedirs(MIDI_DIR, exist_ok=True)
DEFAULT_AUDIO = os.path.join(DATASET_DIR, "guitar", "05_BN3-119-G_solo_mic.wav")

def pitch_to_midi_notes(pitch: np.ndarray, periodicity: np.ndarray, hop_time: float, threshold: float = 0.35):
    voiced = periodicity > threshold
    midi_cents = np.zeros_like(pitch)
    midi_cents[voiced] = 69.0 + 12.0 * np.log2(np.maximum(pitch[voiced], 1e-5) / 440.0)

    notes = []
    in_note = False
    curr_pitches = []
    start_idx = 0

    for i, (v, p_midi) in enumerate(zip(voiced, midi_cents)):
        if v and p_midi > 20:
            if not in_note:
                in_note = True
                start_idx = i
                curr_pitches = [p_midi]
            else:
                if abs(p_midi - np.median(curr_pitches[-5:])) > 0.75:
                    dur = (i - start_idx) * hop_time
                    if dur >= 0.05:
                        med_p = int(round(np.median(curr_pitches)))
                        notes.append((start_idx * hop_time, i * hop_time, med_p))
                    start_idx = i
                    curr_pitches = [p_midi]
                else:
                    curr_pitches.append(p_midi)
        else:
            if in_note:
                dur = (i - start_idx) * hop_time
                if dur >= 0.05:
                    med_p = int(round(np.median(curr_pitches)))
                    notes.append((start_idx * hop_time, i * hop_time, med_p))
                in_note = False
                curr_pitches = []

    if in_note and (len(voiced) - start_idx) * hop_time >= 0.05:
        med_p = int(round(np.median(curr_pitches)))
        notes.append((start_idx * hop_time, len(voiced) * hop_time, med_p))

    return notes

def transcribe(audio_path: str, output_path: str, device: str = None, hop_length: int = 160, threshold: float = 0.35):
    if device is None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'

    audio, sr = librosa.load(audio_path, sr=16000, mono=True)
    audio_tensor = torch.from_numpy(audio).unsqueeze(0).float().to(device)

    pitch, periodicity = torchcrepe.predict(
        audio_tensor,
        sample_rate=16000,
        hop_length=hop_length,
        fmin=50.0,
        fmax=1000.0,
        model='full',
        batch_size=2048,
        device=device,
        return_periodicity=True
    )

    pitch = pitch.squeeze(0).cpu().numpy()
    periodicity = periodicity.squeeze(0).cpu().numpy()
    hop_time = hop_length / 16000.0

    note_events = pitch_to_midi_notes(pitch, periodicity, hop_time, threshold=threshold)

    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=25) # Acoustic Guitar (steel)
    for start, end, p in note_events:
        inst.notes.append(pretty_midi.Note(velocity=100, pitch=p, start=start, end=end))
    pm.instruments.append(inst)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pm.write(output_path)
    return pm, note_events

def main():
    parser = argparse.ArgumentParser(description="TorchCREPE Monofonik Perde Tahmini ve MIDI Dönüşümü")
    parser.add_argument("--audio", type=str, default=DEFAULT_AUDIO, help="Giriş ses dosyası (.wav)")
    parser.add_argument("--output", type=str, default=None, help="Çıktı MIDI dosyası")
    parser.add_argument("--device", type=str, default=None, help="Hesaplama cihazı (cuda/cpu)")
    parser.add_argument("--threshold", type=float, default=0.35, help="Sesli (voiced) periyodiklik eşiği")
    args = parser.parse_args()

    if not os.path.exists(args.audio):
        print(f"[HATA] Ses dosyası bulunamadı: {args.audio}")
        sys.exit(1)

    os.makedirs(MIDI_DIR, exist_ok=True)
    if args.output is None:
        base_name = os.path.splitext(os.path.basename(args.audio))[0]
        output_path = os.path.join(MIDI_DIR, f"{base_name}.mid")
    else:
        output_path = args.output

    device = args.device or ('cuda' if torch.cuda.is_available() else 'cpu')
    print("=" * 70)
    print(" TORCHCREPE DERİN EVRİŞİMLİ PERDE TAKİBİ")
    print("=" * 70)
    print(f"Giriş Sesi        : {args.audio}")
    print(f"Çıktı MIDI        : {output_path}")
    print(f"Hesaplama Cihazı  : {device.upper()}")
    print("-" * 70)

    print("Perde çıkarılıyor ve nota segmentasyonu yapılıyor...")
    t0 = time.time()
    pm, notes = transcribe(args.audio, output_path, device=device, threshold=args.threshold)
    elapsed = time.time() - t0

    print(f"Transkripsiyon tamamlandı! Süre: {elapsed:.2f} saniye")
    print(f"Tespit Edilen Toplam Nota: {len(notes)}")
    print(f"MIDI Dosyası Kaydedildi: {output_path}")

if __name__ == "__main__":
    main()
