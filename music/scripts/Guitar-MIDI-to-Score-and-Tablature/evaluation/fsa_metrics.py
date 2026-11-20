"""
FSA (Fret-String Assignment) ve Tablature Karşılaştırma Metrikleri.
Tahmin edilen tel ve perdeleri GuitarSet zemin gerçeğiyle bilimsel olarak karşılaştırır.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import numpy as np


@dataclass
class FsaEvaluationReport:
    total_notes: int
    matched_notes: int
    string_accuracy: float        # Tel Doğruluğu (%)
    fret_accuracy: float          # Birebir Perde Doğruluğu (%)
    fret_mae: float               # Ortalama Perde Hatası (MAE)
    polyphony_violations: int     # Aynı telde aynı anda basılan imkansız nota sayısı
    avg_hand_shift_pred: float    # Tahminin ortalama el kaydırma mesafesi (ergonomi)
    avg_hand_shift_gt: float      # Zemin gerçeğinin ortalama el kaydırma mesafesi


def evaluate_fsa_predictions(
    ground_truth_notes: List[Dict],
    predicted_notes: List[Dict],
    time_tolerance: float = 0.05,
    pitch_tolerance: int = 0
) -> FsaEvaluationReport:
    """
    Zemin gerçeği ve tahmin listesini karşılaştırır.
    Her notada:
      - start: float
      - pitch: int
      - string_number: int (1..6)
      - fret: int (0..24)
    """
    total_gt = len(ground_truth_notes)
    if total_gt == 0:
        return FsaEvaluationReport(0, 0, 0.0, 0.0, 0.0, 0, 0.0, 0.0)

    matched = 0
    correct_strings = 0
    correct_frets = 0
    fret_errors = []

    # Eşleştirme için tahmin kopyası
    preds_pool = list(predicted_notes)

    for gt in ground_truth_notes:
        best_idx = None
        best_time_diff = float("inf")

        for idx, pred in enumerate(preds_pool):
            if abs(pred["pitch"] - gt["pitch"]) <= pitch_tolerance:
                t_diff = abs(pred["start"] - gt["start"])
                if t_diff <= time_tolerance and t_diff < best_time_diff:
                    best_time_diff = t_diff
                    best_idx = idx

        if best_idx is not None:
            matched += 1
            pred = preds_pool.pop(best_idx)
            is_string_correct = (pred["string_number"] == gt["string_number"])
            is_fret_correct = (pred["fret"] == gt["fret"])

            if is_string_correct:
                correct_strings += 1
            if is_fret_correct:
                correct_frets += 1

            fret_errors.append(abs(pred["fret"] - gt["fret"]))

    string_acc = (correct_strings / matched * 100.0) if matched > 0 else 0.0
    fret_acc = (correct_frets / matched * 100.0) if matched > 0 else 0.0
    fret_mae = float(np.mean(fret_errors)) if fret_errors else 0.0

    # Polifoni ihlalleri: Aynı telde çakışan notalar var mı?
    poly_violations = count_polyphony_violations(predicted_notes)

    # El ergonomisi (Ortalama perde atlama mesafesi)
    shift_pred = compute_average_hand_shift(predicted_notes)
    shift_gt = compute_average_hand_shift(ground_truth_notes)

    return FsaEvaluationReport(
        total_notes=total_gt,
        matched_notes=matched,
        string_accuracy=round(string_acc, 2),
        fret_accuracy=round(fret_acc, 2),
        fret_mae=round(fret_mae, 2),
        polyphony_violations=poly_violations,
        avg_hand_shift_pred=round(shift_pred, 2),
        avg_hand_shift_gt=round(shift_gt, 2),
    )


def count_polyphony_violations(notes: List[Dict]) -> int:
    """Aynı telde aynı anda çalan notaları tespit eder."""
    violations = 0
    sorted_notes = sorted(notes, key=lambda n: n["start"])
    for i in range(len(sorted_notes)):
        for j in range(i + 1, len(sorted_notes)):
            n1 = sorted_notes[i]
            n2 = sorted_notes[j]
            # Zaman çakışması bittiğinde döngüden çık
            if n2["start"] >= n1.get("end", n1["start"] + 0.1):
                break
            # Aynı telde çakışıyorsa ihlal
            if n1["string_number"] == n2["string_number"]:
                violations += 1
    return violations


def compute_average_hand_shift(notes: List[Dict]) -> float:
    """Sol elin ardışık perdeler arasındaki ortalama kayma mesafesini ölçer."""
    frets = [n["fret"] for n in notes if n.get("fret", 0) > 0]  # Boş tel hariç
    if len(frets) < 2:
        return 0.0
    shifts = [abs(frets[i] - frets[i - 1]) for i in range(1, len(frets))]
    return float(np.mean(shifts))
