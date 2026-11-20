#!/usr/bin/env python3
"""
ByteDance CRNN Music Transcription - Ses Dosyasından MIDI Üretme Scripti
MIDI çıktısı otomatik olarak 'midi/' klasörüne zaman damgasıyla kaydedilir.
Kullanım:
    python transcribe.py [--audio DOSYA_YOLU] [--output CIKTI_YOLU] [--device cuda/cpu]
"""

import os
import sys
import time
import argparse
import warnings
from datetime import datetime

warnings.filterwarnings("ignore")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import torch
import librosa
import pretty_midi
from piano_transcription_inference import PianoTranscription

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

def format_time(seconds: float) -> str:
    mins = int(seconds // 60)
    secs = seconds % 60
    return f"{mins:02d}:{secs:05.2f}"

def pitch_to_name(pitch: int) -> str:
    names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (pitch // 12) - 1
    note = names[pitch % 12]
    return f"{note}{octave}"

def transcribe(audio_path: str, output_path: str = None, device: str = None):
    if not os.path.exists(audio_path):
        print(f"[HATA] Ses dosyası bulunamadı: {audio_path}")
        sys.exit(1)

    if device is None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    if output_path is None:
        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        output_path = os.path.join(MIDI_DIR, f"{base_name}_{ts}.mid")

    print("=" * 65)
    print(" BYTEDANCE CRNN - TRANSCRIPTION ")
    print("=" * 65)
    print(f"Girdi Sesi        : {audio_path}")
    print(f"Çıktı MIDI (Zaman): {output_path}")
    print(f"Hesaplama Cihazı  : {device.upper()} ({torch.cuda.get_device_name(0) if device == 'cuda' else 'CPU'})")
    print("-" * 65)

    audio, sr = librosa.load(audio_path, sr=16000, mono=True)
    dur_audio = len(audio) / sr
    print(f"Ses uzunluğu: {dur_audio:.2f} saniye")

    transcriptor = PianoTranscription(device=device)

    t0 = time.time()
    transcriptor.transcribe(audio, output_path)
    elapsed = time.time() - t0

    pm = pretty_midi.PrettyMIDI(output_path)
    total_notes = []
    for inst in pm.instruments:
        total_notes.extend(inst.notes)
    total_notes.sort(key=lambda n: n.start)
    pitches = [n.pitch for n in total_notes]

    print(f"Tamamlandı! Süre: {elapsed:.2f} saniye")
    print("-" * 65)
    print(" İSTATİSTİKLER:")
    print(f"  Toplam Yakalanan Nota : {len(total_notes)}")
    if pitches:
        min_p, max_p = min(pitches), max(pitches)
        print(f"  En Pes Nota           : {pitch_to_name(min_p)} (MIDI {min_p})")
        print(f"  En Tiz Nota           : {pitch_to_name(max_p)} (MIDI {max_p})")
        print(f"  İlk Nota Zamanı       : {format_time(total_notes[0].start)}")
        print(f"  Son Nota Zamanı       : {format_time(total_notes[-1].end)}")
    else:
        print("  [UYARI] Model bu ses kaydından hiç nota tespit edemedi!")

    print("=" * 65)
    print(f"[OK] Zaman damgalı MIDI kaydedildi: {output_path}\n")
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ByteDance CRNN ile Ses Dosyasını MIDI'ye Çevir")
    parser.add_argument("--audio", "-a", default=DEFAULT_AUDIO, help="Girdi ses dosyası (.wav, .mp3)")
    parser.add_argument("--output", "-o", default=None, help="Çıktı MIDI dosyası")
    parser.add_argument("--device", "-d", choices=["cuda", "cpu"], default=None, help="Cihaz (cuda/cpu)")

    args = parser.parse_args()
    transcribe(args.audio, args.output, args.device)
