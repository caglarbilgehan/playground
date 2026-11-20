"""
tuttut (HMM & Graph Viterbi) FSA Adaptörü.
"""

from typing import Dict, List
import pretty_midi
import tuttut.logic.theory as theory
import tuttut.logic.tab as tab


class TuttutFsaAdapter:
    """tuttut kütüphanesini evrensel tahmin formatına köprüleyen adaptör."""

    def __init__(self):
        self.tuning = theory.Tuning()
        # tuttut tuning: [64, 59, 55, 50, 45, 40] -> index 0 = string 1 (E4), index 5 = string 6 (E2)

    def predict(self, midi_path: str) -> List[Dict]:
        pm = pretty_midi.PrettyMIDI(midi_path)
        t = tab.Tab("tuttut_eval", self.tuning, pm)
        predictions: List[Dict] = []

        for measure in t.tab.get("measures", []):
            for event in measure.get("events", []):
                t_sec = float(event.get("time", 0.0))
                for n in event.get("notes", []):
                    str_idx = int(n.get("string", 0))  # 0 to 5
                    fret = int(n.get("fret", 0))
                    # tuttut: 0 -> String 1, 5 -> String 6
                    string_number = str_idx + 1
                    open_pitch = self.tuning.strings[str_idx].pitch if hasattr(self.tuning.strings[str_idx], 'pitch') else [64, 59, 55, 50, 45, 40][str_idx]
                    pitch = open_pitch + fret

                    predictions.append({
                        "start": t_sec,
                        "end": t_sec + 0.5,
                        "pitch": pitch,
                        "string_number": string_number,
                        "fret": fret,
                    })

        predictions.sort(key=lambda x: (x["start"], x["string_number"]))
        return predictions
