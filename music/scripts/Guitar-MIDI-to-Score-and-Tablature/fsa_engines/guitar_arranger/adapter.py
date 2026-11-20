"""
GuitarArranger Fretboard & Voicer FSA Adaptörü.
"""

import sys
from pathlib import Path
from typing import Dict, List
import pretty_midi

# Repo dizinini sys.path'e ekle
repo_path = Path(__file__).resolve().parent / "repo"
if str(repo_path) not in sys.path:
    sys.path.insert(0, str(repo_path))

import fretboard_util


class GuitarArrangerFsaAdapter:
    """GuitarArranger kütüphanesinin Fretboard ve Voicer mantığını köprüleyen adaptör."""

    def __init__(self):
        self.fb = fretboard_util.Fretboard()
        # self.fb.tuning: [64, 59, 55, 50, 45, 40] -> 0: E4 (1. tel), 5: E2 (6. tel)

    def predict(self, midi_path: str) -> List[Dict]:
        pm = pretty_midi.PrettyMIDI(midi_path)
        predictions: List[Dict] = []

        all_notes = []
        for inst in pm.instruments:
            all_notes.extend(inst.notes)
        all_notes.sort(key=lambda n: n.start)

        # Basit ardışık pozisyon hafızası (önceki perdeden en az sapan pozisyonu seçme)
        last_fret = 5

        for n in all_notes:
            pitch = int(n.pitch)
            # Tüm olası (string_idx, fret) ikililerini bul
            candidates = []
            for s_idx in range(6):
                open_p = self.fb.tuning[s_idx]
                fret = pitch - open_p
                if 0 <= fret <= 21:
                    candidates.append((s_idx + 1, fret))

            if not candidates:
                string_num, fret = 1, 0
            else:
                # Önceki perdeye en yakın olanı seç (GuitarArranger lokal el ekonomi kuralı)
                candidates.sort(key=lambda x: (abs(x[1] - last_fret), x[1]))
                string_num, fret = candidates[0]
                if fret > 0:
                    last_fret = fret

            predictions.append({
                "start": float(n.start),
                "end": float(n.end),
                "pitch": pitch,
                "string_number": string_num,
                "fret": fret,
            })

        predictions.sort(key=lambda x: (x["start"], x["string_number"]))
        return predictions
