#!/usr/bin/env python3
"""
Spotify Basic Pitch - Ses Dosyasından MIDI Üretme Scripti
MIDI çıktısı otomatik olarak 'midi/' klasörüne zaman damgasıyla kaydedilir.
Kullanım:
    python transcribe.py [--audio DOSYA_YOLU] [--output CIKTI_YOLU]
"""

import os
import sys
import time
import logging
import argparse
from datetime import datetime

logging.getLogger().setLevel(logging.ERROR)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import pretty_midi
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH

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

def transcribe(
    audio_path: str,
    output_path: str = None,
    onset_threshold: float = 0.5,
    frame_threshold: float = 0.3,
    min_note_length: int = 58,
    include_pitch_bends: bool = True
):
    if not os.path.exists(audio_path):
        print(f"[HATA] Ses dosyası bulunamadı: {audio_path}")
        sys.exit(1)

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    if output_path is None:
        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        output_path = os.path.join(MIDI_DIR, f"{base_name}_{ts}.mid")

    print("=" * 65)
    print(" SPOTIFY BASIC PITCH - TRANSCRIPTION ")
    print("=" * 65)
    print(f"Girdi Sesi        : {audio_path}")
    print(f"Çıktı MIDI (Zaman): {output_path}")
    print(f"Onset Threshold   : {onset_threshold} (nota başlangıç hassasiyeti)")
    print(f"Frame Threshold   : {frame_threshold} (nota devamlılık hassasiyeti)")
    print(f"Min Nota Boyu     : {min_note_length} ms")
    print(f"Pitch Bend Desteği: {'Açık (MPE / Vibrato uyumlu)' if include_pitch_bends else 'Kapalı'}")
    print("-" * 65)
    print("Model çalıştırılıyor...")

    t0 = time.time()
    model_output, midi_data, note_events = predict(
        audio_path,
        model_or_model_path=ICASSP_2022_MODEL_PATH,
        onset_threshold=onset_threshold,
        frame_threshold=frame_threshold,
        minimum_note_length=min_note_length,
        minimum_frequency=None,
        maximum_frequency=None,
        multiple_pitch_bends=include_pitch_bends,
        melodia_trick=True
    )
    elapsed = time.time() - t0

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    midi_data.write(output_path)

    total_notes = []
    total_pitch_bends = 0
    for inst in midi_data.instruments:
        total_notes.extend(inst.notes)
        total_pitch_bends += len(inst.pitch_bends)

    total_notes.sort(key=lambda n: n.start)
    pitches = [n.pitch for n in total_notes]

    print(f"Tamamlandı! Süre: {elapsed:.2f} saniye")
    print("-" * 65)
    print(" İSTATİSTİKLER:")
    print(f"  Toplam Yakalanan Nota  : {len(total_notes)}")
    print(f"  Toplam Pitch Bend Olayı: {total_pitch_bends}")
    print(f"  Kullanılan MIDI Kanalı : {len(midi_data.instruments)}")
    if pitches:
        min_p, max_p = min(pitches), max(pitches)
        print(f"  En Pes Nota            : {pitch_to_name(min_p)} (MIDI {min_p})")
        print(f"  En Tiz Nota            : {pitch_to_name(max_p)} (MIDI {max_p})")
        print(f"  İlk Nota Zamanı        : {format_time(total_notes[0].start)}")
        print(f"  Son Nota Zamanı        : {format_time(total_notes[-1].end)}")

    print("-" * 65)
    print(" İLK 5 NOTA ÖRNEĞİ:")
    print(f"{'No':<4} | {'Başlangıç':<10} | {'Bitiş':<10} | {'Süre (s)':<8} | {'Nota':<6} | {'MIDI':<5}")
    print("-" * 55)
    for i, n in enumerate(total_notes[:5], 1):
        dur = n.end - n.start
        print(f"{i:<4} | {format_time(n.start):<10} | {format_time(n.end):<10} | {dur:<8.2f} | {pitch_to_name(n.pitch):<6} | {n.pitch:<5}")

    print("=" * 65)
    print(f"[OK] Zaman damgalı MIDI başarıyla kaydedildi: {output_path}\n")
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spotify Basic Pitch ile Ses Dosyasını MIDI'ye Çevir")
    parser.add_argument("--audio", "-a", default=DEFAULT_AUDIO, help="Girdi ses dosyası (.wav, .mp3)")
    parser.add_argument("--output", "-o", default=None, help="Çıktı MIDI dosyası")
    parser.add_argument("--onset-thresh", type=float, default=0.5, help="Vuruş başlangıç eşiği (0.0 - 1.0)")
    parser.add_argument("--frame-thresh", type=float, default=0.3, help="Kare devamlılık eşiği (0.0 - 1.0)")
    parser.add_argument("--min-note-len", type=int, default=58, help="Milisaniye cinsinden en kısa nota boyu")
    parser.add_argument("--no-pitch-bends", action="store_true", help="Pitch bend takibini kapat")

    args = parser.parse_args()
    transcribe(
        args.audio,
        args.output,
        args.onset_thresh,
        args.frame_thresh,
        args.min_note_len,
        not args.no_pitch_bends
    )
