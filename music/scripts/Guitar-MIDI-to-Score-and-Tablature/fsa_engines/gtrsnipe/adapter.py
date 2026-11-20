"""
gtrsnipe (Biomechanical Viterbi Optimizer) FSA Adaptörü.
"""

from typing import Dict, List
from gtrsnipe.formats.mid.reader import MidiReader
from gtrsnipe.arguments import MapperConfig
from gtrsnipe.guitar.fingering import positioned
from gtrsnipe.formats.tab.generator.ascii import _config_with_tempo
from gtrsnipe.guitar.mapper import GuitarMapper


class GtrsnipeFsaAdapter:
    """gtrsnipe biyomekanik Viterbi motorunu evrensel tahmin formatına köprüleyen adaptör."""

    def __init__(self, optimizer: str = "viterbi"):
        self.optimizer = optimizer

    def predict(self, midi_path: str) -> List[Dict]:
        song = MidiReader.parse(midi_path, None)
        config = MapperConfig(optimizer=self.optimizer)
        mapper = GuitarMapper(config=_config_with_tempo(config, song))

        bpm = float(song.tempo) if song.tempo and song.tempo > 0 else 120.0
        sec_per_beat = 60.0 / bpm

        predictions: List[Dict] = []
        for track in song.tracks:
            events = positioned(song, track.events, mapper)
            for ev in events:
                # ev.string: 0 (E4 / 1. tel) to 5 (E2 / 6. tel)
                string_number = int(ev.string) + 1
                fret = int(ev.fret)
                pitch = int(ev.pitch)
                start_sec = float(ev.time) * sec_per_beat
                dur_sec = float(getattr(ev, "duration", 0.5)) * sec_per_beat

                predictions.append({
                    "start": start_sec,
                    "end": start_sec + dur_sec,
                    "pitch": pitch,
                    "string_number": string_number,
                    "fret": fret,
                })

        predictions.sort(key=lambda x: (x["start"], x["string_number"]))
        return predictions
