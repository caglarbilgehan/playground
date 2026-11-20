"""
Evrensel MusicXML ve Tablature Skor Oluşturucu (music21 Tabanlı).
FSA motorlarından gelen (tel, perde) etiketlerini standart W3C MusicXML yapısına işler.
"""

from pathlib import Path
from typing import Dict, List, Optional
import music21 as m21
from music21 import stream, note, chord, meter, tempo, metadata
from music21.articulations import StringIndication, FretIndication


class MusicXmlScoreBuilder:
    """FSA tahminlerini içeren W3C standartlarında MusicXML üreten sınıf."""

    def __init__(self, instrument_name: str = "Acoustic Guitar"):
        self.instrument_name = instrument_name

    def export(
        self,
        midi_path: str,
        fsa_predictions: List[Dict],
        output_xml_path: str,
        title: str = "Guitar Transcription",
        bpm: float = 120.0
    ) -> str:
        """
        MIDI dosyasını music21 ile parse eder, FSA tel/perde etiketlerini
        nota artikülasyonlarına bağlar ve W3C MusicXML olarak kaydeder.
        """
        score = m21.converter.parse(midi_path)
        
        # Meta veriler
        if score.metadata is None:
            score.metadata = metadata.Metadata()
        score.metadata.title = title
        score.metadata.composer = "AI Audio-to-Score Pipeline (Antigravity)"

        preds_pool = list(fsa_predictions)

        # Tüm notalara tel ve perde etiketlerini bağla
        for el in score.flatten().notes:
            if el.isChord:
                for p in el.pitches:
                    midi_val = int(p.midi)
                    # En yakın FSA tahminini bul
                    matched_idx = None
                    for idx, pred in enumerate(preds_pool):
                        if pred["pitch"] == midi_val:
                            matched_idx = idx
                            break
                    if matched_idx is not None:
                        pred = preds_pool.pop(matched_idx)
                        el.articulations.append(StringIndication(pred["string_number"]))
                        el.articulations.append(FretIndication(pred["fret"]))
            else:
                midi_val = int(el.pitch.midi)
                matched_idx = None
                for idx, pred in enumerate(preds_pool):
                    if pred["pitch"] == midi_val:
                        matched_idx = idx
                        break
                if matched_idx is not None:
                    pred = preds_pool.pop(matched_idx)
                    el.articulations.append(StringIndication(pred["string_number"]))
                    el.articulations.append(FretIndication(pred["fret"]))

        out_p = Path(output_xml_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        score.write("musicxml", fp=str(out_p))
        return str(out_p)
