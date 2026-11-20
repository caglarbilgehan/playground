#!/usr/bin/env python3
"""
YourMT3+ - Multi-Task & Multi-Track Music Transcription Script
Gitar sesini (solo veya comping) enstrüman ayrıştırmalı YourMT3+ modeliyle
transkribe eder ve General MIDI formatına dönüştürür.
"""

import os
import sys
import time
import argparse
import warnings

warnings.filterwarnings("ignore")
import torch
import torchaudio
import pretty_midi

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPACE_DIR = os.path.join(BASE_DIR, "YourMT3-space")
sys.path.insert(0, SPACE_DIR)
sys.path.insert(0, os.path.join(SPACE_DIR, "amt/src"))
os.chdir(SPACE_DIR)

from model_helper import load_model_checkpoint, transcribe

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
MIDI_DIR = os.path.join(BASE_DIR, "midi", "guitar")
os.makedirs(MIDI_DIR, exist_ok=True)
DEFAULT_AUDIO = os.path.join(DATASET_DIR, "guitar", "05_BN3-119-G_solo_mic.wav")

def main():
    parser = argparse.ArgumentParser(description="YourMT3+ Audio -> MIDI Transkripsiyonu")
    parser.add_argument("--audio", type=str, default=DEFAULT_AUDIO, help="Giriş wav dosyası")
    parser.add_argument("--output", type=str, default=None, help="Çıktı midi dosya yolu")
    parser.add_argument("--device", type=str, default="cuda", help="Cihaz (cuda/cpu)")
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
    print(" YOURMT3+ MULTI-TRACK & MULTI-TASK MUSIC TRANSCRIPTION")
    print("=" * 70)
    print(f"Giriş Ses Dosyası : {args.audio}")
    print(f"Çıktı MIDI Yolu   : {output_path}")
    print(f"Hesaplama Cihazı  : {args.device.upper()}")
    print("-" * 70)

    print("Model yükleniyor...")
    checkpoint = 'notask_all_cross_v6_xk2_amp0811_gm_ext_plus_nops_b72@model.ckpt'
    model_args = [checkpoint, '-p', '2024', '-pr', '16']
    model = load_model_checkpoint(args=model_args, device=args.device)
    model.eval()

    info = torchaudio.info(args.audio)
    track_name = os.path.splitext(os.path.basename(args.audio))[0]
    audio_info = {
        'filepath': args.audio,
        'track_name': track_name,
        'sample_rate': int(info.sample_rate),
        'bits_per_sample': int(info.bits_per_sample),
        'num_channels': int(info.num_channels),
        'num_frames': int(info.num_frames),
        'duration': int(info.num_frames / info.sample_rate),
        'encoding': str.lower(info.encoding),
    }

    print("Transkripsiyon başlatılıyor...")
    t0 = time.time()
    gen_midi = transcribe(model, audio_info)
    elapsed = time.time() - t0

    if os.path.abspath(gen_midi) != os.path.abspath(output_path):
        import shutil
        shutil.copyfile(gen_midi, output_path)

    pm = pretty_midi.PrettyMIDI(output_path)
    total_notes = sum(len(inst.notes) for inst in pm.instruments)
    print(f"İşlem Tamamlandı! Süre: {elapsed:.2f} saniye")
    print(f"Oluşturulan Toplam Nota: {total_notes}")
    print(f"MIDI Dosyası Kaydedildi: {output_path}")

if __name__ == "__main__":
    main()
