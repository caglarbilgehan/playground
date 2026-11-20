#!/usr/bin/env python3
"""
Omnizart - Çok Amaçlı Müzik Transkripsiyon Scripti
Gitar sesini MusiCNN Stream modeliyle transkribe eder ve MIDI dosyası oluşturur.
"""

import os
import sys
import time
import argparse
import warnings

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
warnings.filterwarnings("ignore")

from omnizart.music import app

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

def main():
    parser = argparse.ArgumentParser(description="Omnizart ile Ses Dosyasını MIDI'ye Çevir")
    parser.add_argument("--audio", type=str, default=DEFAULT_AUDIO, help="Giriş wav dosyası")
    parser.add_argument("--output", type=str, default=None, help="Çıktı midi dosya yolu")
    parser.add_argument("--mode", type=str, default="Stream", help="Model modu (Stream, Piano vb.)")
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

    print("=" * 70)
    print(" OMNIZART AUTOMATIC MUSIC TRANSCRIPTION (AMT)")
    print("=" * 70)
    print(f"Giriş Ses Dosyası : {args.audio}")
    print(f"Çıktı MIDI Yolu   : {output_path}")
    print(f"Model Modu        : {args.mode}")
    print("-" * 70)

    print("Transkripsiyon başlatılıyor (model yükleniyor ve spectrogram çıkarılıyor)...")
    t0 = time.time()
    midi = app.transcribe(args.audio, model_path=args.mode, output=output_path)
    elapsed = time.time() - t0

    total_notes = sum(len(inst.notes) for inst in midi.instruments)
    print(f"İşlem Tamamlandı! Süre: {elapsed:.2f} saniye")
    print(f"Oluşturulan Toplam Nota: {total_notes}")
    print(f"Enstrüman Sayısı: {len(midi.instruments)}")
    print(f"MIDI Dosyası Kaydedildi: {output_path}")

if __name__ == "__main__":
    main()
