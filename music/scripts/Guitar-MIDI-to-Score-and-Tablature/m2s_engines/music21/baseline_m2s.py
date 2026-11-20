"""
Naive / Baseline MIDI-to-Score Dönüştürücüsü (music21 Tabanlı).
FSA optimizasyonu olmadan, standart açgözlü (greedy - en düşük perde) kuralıyla
MIDI notalarını porte ve MusicXML skoruna dönüştürür.
"""

from pathlib import Path
from typing import Dict, List, Tuple
import music21 as m21
from music21 import stream, note, chord, meter, tempo
from music21.articulations import StringIndication, FretIndication


# Standart Gitar Akordu (E2=40, A2=45, D3=50, G3=55, B3=59, E4=64)
# String 1: E4, String 2: B3, String 3: G3, String 4: D3, String 5: A2, String 6: E2
GUITAR_OPEN_PITCHES = {
    1: 64,  # E4
    2: 59,  # B3
    3: 55,  # G3
    4: 50,  # D3
    5: 45,  # A2
    6: 40,  # E2
}


class NaiveM2SConverter:
    """FSA optimizasyonu yapmayan taban hattı dönüştürücüsü."""

    def __init__(self, max_fret: int = 24):
        self.max_fret = max_fret

    def get_candidate_positions(self, pitch: int) -> List[Tuple[int, int]]:
        """Bir MIDI notasının klavyedeki tüm geçerli (tel, perde) kombinasyonlarını listeler."""
        candidates = []
        for string_num, open_pitch in GUITAR_OPEN_PITCHES.items():
            fret = pitch - open_pitch
            if 0 <= fret <= self.max_fret:
                candidates.append((string_num, fret))
        return candidates

    def assign_naive_fret_string(self, pitch: int) -> Tuple[int, int]:
        """
        Naive Greedy Kuralı: En düşük perdeyi seçer (Açık pozisyon tercihi).
        Eğer eşitlik varsa daha alt teli (kalın) seçer.
        """
        candidates = self.get_candidate_positions(pitch)
        if not candidates:
            # Sınır dışı nota ise varsayılan 1. tel
            return (1, 0)
        # En düşük perdeye göre sırala (fret artan, tel numarası artan)
        candidates.sort(key=lambda x: (x[1], -x[0]))
        return candidates[0]

    def convert_midi_to_predictions(self, midi_path: str) -> List[Dict]:
        """MIDI dosyasını pretty_midi ile okuyup her notaya naive (tel, perde) atar (zaman saniye cinsindendir)."""
        import pretty_midi
        pm = pretty_midi.PrettyMIDI(midi_path)
        predictions: List[Dict] = []

        for inst in pm.instruments:
            for n in inst.notes:
                str_num, fret = self.assign_naive_fret_string(int(n.pitch))
                predictions.append({
                    "start": float(n.start),
                    "end": float(n.end),
                    "duration": float(n.end - n.start),
                    "pitch": int(n.pitch),
                    "string_number": str_num,
                    "fret": fret,
                })

        predictions.sort(key=lambda x: (x["start"], x["string_number"]))
        return predictions

    def export_musicxml(self, midi_path: str, output_xml_path: str) -> str:
        """
        MIDI'yi music21 ile parse edip, naive tel/perde etiketlerini ekleyerek
        W3C standartlarında MusicXML olarak dışa aktarır.
        """
        score = m21.converter.parse(midi_path)
        part = score.parts[0] if score.parts else score

        for el in part.flatten().notes:
            if el.isChord:
                for p in el.pitches:
                    s_num, f_num = self.assign_naive_fret_string(int(p.midi))
                    el.articulations.append(StringIndication(s_num))
                    el.articulations.append(FretIndication(f_num))
            else:
                s_num, f_num = self.assign_naive_fret_string(int(el.pitch.midi))
                el.articulations.append(StringIndication(s_num))
                el.articulations.append(FretIndication(f_num))

        Path(output_xml_path).parent.mkdir(parents=True, exist_ok=True)
        score.write("musicxml", fp=output_xml_path)
        return output_xml_path
