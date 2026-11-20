"""
GuitarSet JAMS Ground Truth Okuyucu ve Doğrulayıcı Modülü.
Hexaphonic manyetik verilerini (6 ayrı tel) okuyarak zaman damgalı (tel, perde, nota) zemin gerçeğini çıkarır.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional
import jams
import mido


# Standart Gitar Akort Haritası (E2, A2, D3, G3, B3, E4)
# GuitarSet data_source: "0" -> En kalın tel (6. tel), "5" -> En ince tel (1. tel)
GUITAR_STRINGS_CONFIG = {
    0: {"string_number": 6, "open_pitch": 40, "name": "E2 (6. Tel)"},
    1: {"string_number": 5, "open_pitch": 45, "name": "A2 (5. Tel)"},
    2: {"string_number": 4, "open_pitch": 50, "name": "D3 (4. Tel)"},
    3: {"string_number": 3, "open_pitch": 55, "name": "G3 (3. Tel)"},
    4: {"string_number": 2, "open_pitch": 59, "name": "B3 (2. Tel)"},
    5: {"string_number": 1, "open_pitch": 64, "name": "E4 (1. Tel)"},
}


@dataclass
class GroundTruthNote:
    start: float
    end: float
    duration: float
    pitch: float
    rounded_pitch: int
    string_number: int  # 1 (en ince) - 6 (en kalın)
    fret: int


class GuitarSetJamsReader:
    """GuitarSet .jams dosyalarını okuyan sınıf."""

    def __init__(self, jams_path: str):
        self.jams_path = Path(jams_path)
        if not self.jams_path.exists():
            raise FileNotFoundError(f"JAMS dosyası bulunamadı: {jams_path}")
        self.jam = jams.load(str(self.jams_path))

    def extract_notes(self) -> List[GroundTruthNote]:
        """Tüm tellerdeki notaları zaman sırasına göre çıkartır."""
        all_notes: List[GroundTruthNote] = []

        for ann in self.jam.annotations:
            if ann.namespace == "note_midi":
                try:
                    data_source_id = int(ann.annotation_metadata.data_source)
                except (ValueError, TypeError, AttributeError):
                    continue

                if data_source_id not in GUITAR_STRINGS_CONFIG:
                    continue

                cfg = GUITAR_STRINGS_CONFIG[data_source_id]
                string_num = cfg["string_number"]
                open_pitch = cfg["open_pitch"]

                for obs in ann.data:
                    pitch = float(obs.value)
                    rounded_pitch = int(round(pitch))
                    fret = rounded_pitch - open_pitch
                    start = float(obs.time)
                    duration = float(obs.duration)
                    end = start + duration

                    # Fiziksel sınır kontrolü (perde negatif olamaz, 24'ten büyük olamaz)
                    if 0 <= fret <= 24:
                        all_notes.append(
                            GroundTruthNote(
                                start=start,
                                end=end,
                                duration=duration,
                                pitch=pitch,
                                rounded_pitch=rounded_pitch,
                                string_number=string_num,
                                fret=fret,
                            )
                        )

        # Başlangıç zamanına göre sırala
        all_notes.sort(key=lambda n: (n.start, n.string_number))
        return all_notes

    def export_to_midi(self, output_midi_path: str) -> None:
        """
        Zemin gerçeği notalarını standart bir MIDI dosyasına dönüştürür.
        Her tel ayrı bir MIDI kanalına (Kanal 0-5) atanır.
        """
        notes = self.extract_notes()
        mid = mido.MidiFile(ticks_per_beat=480)
        track = mido.MidiTrack()
        mid.tracks.append(track)

        # Olayları zaman sırasına göre event listesine dönüştür
        events = []
        for n in notes:
            channel = n.string_number - 1  # 0 to 5
            events.append((n.start, "note_on", n.rounded_pitch, 80, channel))
            events.append((n.end, "note_off", n.rounded_pitch, 0, channel))

        events.sort(key=lambda e: e[0])

        current_time = 0.0
        tempo = 500000  # 120 BPM varsayılan (mikrosaniye/beat)
        ticks_per_second = (mid.ticks_per_beat * 1_000_000) / tempo

        for event_time, event_type, pitch, vel, channel in events:
            delta_sec = max(0.0, event_time - current_time)
            delta_ticks = int(round(delta_sec * ticks_per_second))
            current_time = event_time

            track.append(
                mido.Message(
                    event_type,
                    note=pitch,
                    velocity=vel,
                    channel=channel,
                    time=delta_ticks,
                )
            )

        mid.save(output_midi_path)


if __name__ == "__main__":
    import sys
    test_path = sys.argv[1] if len(sys.argv) > 1 else "/home/cserver/projects/open-projects/playground/music/scripts/Guitar-MIDI-to-Score-and-Tablature/data_sources/ground_truth_jams/05_BN3-119-G_solo.jams"
    reader = GuitarSetJamsReader(test_path)
    notes = reader.extract_notes()
    print(f"Toplam Çıkarılan Zemin Gerçeği Notaları: {len(notes)}")
    for n in notes[:5]:
        print(f"Zaman: {n.start:.2f}s | Nota: {n.rounded_pitch} | Tel: {n.string_number}. Tel | Perde: {n.fret}. Perde")
