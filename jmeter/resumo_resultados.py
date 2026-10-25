import csv
import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Uso: python resumo_resultados.py <pasta_resultados>")
        return

    base_dir = Path(sys.argv[1])
    scenarios = [
        ("Cenario A (50% L / 50% E)", base_dir / "cenario_A_50L_50E" / "statistics.json"),
        ("Cenario B (75% L / 25% E)", base_dir / "cenario_B_75L_25E" / "statistics.json"),
        ("Cenario C (25% L / 75% E)", base_dir / "cenario_C_25L_75E" / "statistics.json"),
    ]

    lines = []
    csv_rows = [
        [
            "Cenario",
            "Operacao",
            "Amostras",
            "Erros",
            "Erro (%)",
            "Media (ms)",
            "Mediana (ms)",
            "P95 (ms)",
            "P99 (ms)",
            "Throughput (req/s)",
        ]
    ]

    header = (
        f"{'CENARIO / OPERACAO':<28} | {'N':>5} | {'ERRO %':>8} | "
        f"{'MEDIA (ms)':>10} | {'P95 (ms)':>10} | {'VAZAO (req/s)':>13}"
    )
    sep = "-" * len(header)
    lines.append(sep)
    lines.append(header)
    lines.append(sep)

    for label, stats_path in scenarios:
        if not stats_path.exists():
            lines.append(f"{label:<28} | [ARQUIVO NAO ENCONTRADO: {stats_path}]")
            continue

        with open(stats_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for key, display in [("Total", label), ("Leitura Home", "  -> Leitura (GET)"), ("Escrita", "  -> Escrita (POST)")]:
            if key not in data:
                continue
            m = data[key]
            samples = m.get("sampleCount", 0)
            errors = m.get("errorCount", 0)
            err_pct = m.get("errorPct", 0.0)
            mean_ms = m.get("meanResTime", 0.0)
            median_ms = m.get("medianResTime", 0.0)
            p95_ms = m.get("pct2ResTime", 0.0)
            p99_ms = m.get("pct3ResTime", 0.0)
            tput = m.get("throughput", 0.0)

            lines.append(
                f"{display:<28} | {samples:>5} | {err_pct:>7.2f}% | "
                f"{mean_ms:>10.2f} | {p95_ms:>10.2f} | {tput:>10.2f}/s"
            )
            csv_rows.append([
                label,
                key,
                samples,
                errors,
                f"{err_pct:.2f}",
                f"{mean_ms:.2f}",
                f"{median_ms:.2f}",
                f"{p95_ms:.2f}",
                f"{p99_ms:.2f}",
                f"{tput:.2f}",
            ])
        lines.append(sep)

    output_txt = "\n".join(lines)
    print("\n" + output_txt + "\n")

    txt_file = base_dir / "resumo_metricas.txt"
    csv_file = base_dir / "resumo_metricas.csv"

    txt_file.write_text(output_txt + "\n", encoding="utf-8")
    with open(csv_file, "w", newline="", encoding="utf-8-sig") as cf:
        writer = csv.writer(cf, delimiter=";")
        writer.writerows(csv_rows)

    print(f"Resumo salvo em:\n  - {txt_file}\n  - {csv_file}")


if __name__ == "__main__":
    main()
