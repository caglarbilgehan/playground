#!/usr/bin/env python3
"""
AMT Modelleri için 5 Testlik Konsolide Summary Oluşturucu
Kullanım:
    python summarize_benchmark.py <model_dir_name> [instrument]
Örnek:
    python summarize_benchmark.py yourmt3 guitar
    python summarize_benchmark.py basic-pitch guitar
"""

import os
import sys
import re
import glob
from datetime import datetime

AMT_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_TITLES = {
    "yourmt3": "YourMT3+ Multi-Track Transformer",
    "basic-pitch": "Spotify Basic Pitch (ICASSP 2022)",
    "torchcrepe": "TorchCREPE Monophonic Pitch Estimator",
    "omnizart": "Omnizart Music (Stream Mode)",
    "bytedance": "ByteDance CRNN (High-Resolution Piano Transcription)"
}

def parse_result_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    ts_match = re.search(r"result-(\d{8}-\d{4})\.md", file_path)
    ts = ts_match.group(1) if ts_match else "N/A"
    time_part = ts.split("-")[1] if "-" in ts else ts
    time_display = f"{time_part[:2]}:{time_part[2:]}" if len(time_part) == 4 else ts

    # Clean bold markers for effortless parsing
    c_clean = content.replace("*", "")
    
    # Hem Türkçe hem İngilizce raporları destekle
    solo_m = re.search(
        r"5 Solo (?:Ortalama|Average):\s*(?:Süre|Time):\s*([\d\.]+)s\s*\|\s*Onset Recall:\s*%([\d\.]+)\s*\|\s*Pitch Recall:\s*%([\d\.]+)\s*\|\s*Pitch F1:\s*%([\d\.]+)\s*\|\s*Strict F1:\s*%([\d\.]+)",
        c_clean, re.IGNORECASE
    )
    comp_m = re.search(
        r"5 Comping (?:Ortalama|Average):\s*(?:Süre|Time):\s*([\d\.]+)s\s*\|\s*Onset Recall:\s*%([\d\.]+)\s*\|\s*Pitch Recall:\s*%([\d\.]+)\s*\|\s*Pitch F1:\s*%([\d\.]+)\s*\|\s*Strict F1:\s*%([\d\.]+)",
        c_clean, re.IGNORECASE
    )

    if not solo_m or not comp_m:
        return None

    return {
        "file": file_path,
        "ts": ts,
        "time_display": time_display,
        "solo_time": float(solo_m.group(1)),
        "solo_orec": float(solo_m.group(2)),
        "solo_prec": float(solo_m.group(3)),
        "solo_pf1": float(solo_m.group(4)),
        "solo_sf1": float(solo_m.group(5)),
        "comp_time": float(comp_m.group(1)),
        "comp_orec": float(comp_m.group(2)),
        "comp_prec": float(comp_m.group(3)),
        "comp_pf1": float(comp_m.group(4)),
        "comp_sf1": float(comp_m.group(5)),
    }

def generate_summary(model_name, instrument="guitar"):
    target_dir = os.path.join(AMT_DIR, model_name)
    inst_tests_dir = os.path.join(target_dir, "tests", instrument)
    tests_dir = inst_tests_dir if os.path.isdir(inst_tests_dir) else os.path.join(target_dir, "tests")
    if not os.path.isdir(tests_dir):
        print(f"[HATA] Dizin bulunamadı: {tests_dir}")
        return

    result_files = sorted(glob.glob(os.path.join(tests_dir, "result-*.md")))
    if not result_files:
        print(f"[HATA] {tests_dir} içinde result-*.md dosyası bulunamadı!")
        return

    parsed = []
    for rf in result_files:
        p = parse_result_file(rf)
        if p:
            parsed.append(p)

    if not parsed:
        print(f"[UYARI] {model_name} için geçerli sonuç bulunamadı!")
        return

    parsed = parsed[-5:]
    model_title = MODEL_TITLES.get(model_name, model_name)
    now_str = datetime.now().strftime("%d Kasım %Y — %H:%M")

    table_rows = ""
    for idx, r in enumerate(parsed, 1):
        table_rows += (
            f"| **Test {idx}** | `{r['time_display']}` | "
            f"{r['solo_time']:.2f}s | {r['comp_time']:.2f}s | "
            f"**%{r['solo_orec']:.1f}** | **%{r['solo_pf1']:.1f}** | %{r['solo_sf1']:.1f} | "
            f"**%{r['comp_orec']:.1f}** | **%{r['comp_pf1']:.1f}** | %{r['comp_sf1']:.1f} | "
            f"[Rapor {idx}](file://{r['file']}) |\n"
        )

    import numpy as np
    avg_st = np.mean([r['solo_time'] for r in parsed])
    avg_ct = np.mean([r['comp_time'] for r in parsed])
    avg_so = np.mean([r['solo_orec'] for r in parsed])
    avg_spf = np.mean([r['solo_pf1'] for r in parsed])
    avg_ssf = np.mean([r['solo_sf1'] for r in parsed])
    avg_co = np.mean([r['comp_orec'] for r in parsed])
    avg_cpf = np.mean([r['comp_pf1'] for r in parsed])
    avg_csf = np.mean([r['comp_sf1'] for r in parsed])

    table_rows += (
        f"| **GENEL ORTALAMA** | — | "
        f"**{avg_st:.2f}s** | **{avg_ct:.2f}s** | "
        f"**%{avg_so:.1f}** | **%{avg_spf:.1f}** | **%{avg_ssf:.1f}** | "
        f"**%{avg_co:.1f}** | **%{avg_cpf:.1f}** | **%{avg_csf:.1f}** | — |\n"
    )

    summary_content = f"""# 📊 {model_title} — 10 Parçalı 5 Aşamalı Benchmark Özeti

**Tarih:** {now_str}  
**Model:** {model_title}  
**Doğrulama Veri Seti:** NYU MARL GuitarSet (ISMIR 2018 - 10 Parça: 5 Solo [421 Nota] + 5 Comping [1.122 Nota], Toplam: 1.543 Nota)  
**Test Sayısı:** {len(parsed)} Bağımsız Koşum (1'er dakika aralıklı, zaman damgalı MIDI arşivli)  
**Arşiv Dizini:** [`scripts/Automatic-Music-Transcription/{model_name}/midi/`](file://{os.path.join(target_dir, "midi", instrument)})  

---

## 📌 Konsolide Özet Metrikleri

* **🎸 5 Solo Parça Ortalaması:**
  * Ortalama İşlem Süresi: **{avg_st:.2f}s**
  * Onset Recall (Vuruş Yakalama): **%{avg_so:.1f}**
  * Pitch F1 Skoru (Nota + Zaman): **%{avg_spf:.1f}**
  * Strict F1 Skoru (Offset/Bitiş Dahil): **%{avg_ssf:.1f}**

* **🎼 5 Comping / Akor Parçası Ortalaması:**
  * Ortalama İşlem Süresi: **{avg_ct:.2f}s**
  * Onset Recall (Akor Tellerini Yakalama): **%{avg_co:.1f}**
  * Pitch F1 Skoru (Akor Nota Doğruluğu): **%{avg_cpf:.1f}**
  * Strict F1 Skoru (Susturma/Bitiş Dahil): **%{avg_csf:.1f}**

---

## 1. 🏁 5 Koşumun Karşılaştırma Tablosu

| Koşum No | Zaman | Solo Süre | Comp Süre | Solo Onset Rec. | Solo Pitch F1 | Solo Strict F1 | Comp Onset Rec. | Comp Pitch F1 | Comp Strict F1 | Rapor Bağlantısı |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
{table_rows}
---

## 2. 🔬 Değerlendirme & Gözlemler

* **Kararlılık:** Her test bağımsız olarak zaman damgalı `.mid` dosyaları ile `midi/` klasörüne yazılmış ve MIR doğrulaması gerçekleştirilmiştir.
* **Metrik Uyumu:** NYU MARL GuitarSet referans JAMS etiketleri üzerinden Onset toleransı 50ms, Pitch toleransı 50 cent olarak hesaplanmıştır.
"""
    summary_path = os.path.join(tests_dir, "results-summary.md")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary_content)

    print(f"[OK] Summary başarıyla oluşturuldu: {summary_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python summarize_benchmark.py <model_name> [instrument]")
        sys.exit(1)
    inst = sys.argv[2] if len(sys.argv) > 2 else "guitar"
    generate_summary(sys.argv[1], inst)
