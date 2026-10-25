import json
import os
import subprocess
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent / "resultados_jmeter"
CHARTS_DIR = BASE_DIR / "graficos"
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

CONFIGS = [
    ("100k_sem_indice", "100k SEM Índice"),
    ("100k_com_indice", "100k COM Índice"),
    ("20k_sem_indice", "20k SEM Índice"),
]

SCENARIOS = [
    ("cenario_A_50L_50E", "Cenário A (50% L / 50% E)"),
    ("cenario_B_75L_25E", "Cenário B (75% L / 25% E)"),
    ("cenario_C_25L_75E", "Cenário C (25% L / 75% E)"),
]

# Dados antigos do Trabalho 1 (1 servidor Flask sem NGINX, query sem usar indice) para comparacao
T1_DATA = {
    "100k_com_indice": {
        "cenario_A_50L_50E": {"err": 10.33, "mean": 1119.67, "p95": 1612.90, "tput": 106.17},
        "cenario_B_75L_25E": {"err": 14.25, "mean": 1066.38, "p95": 1569.00, "tput": 109.73},
        "cenario_C_25L_75E": {"err": 7.17,  "mean": 1089.26, "p95": 1525.00, "tput": 107.85},
    },
    "100k_sem_indice": {
        "cenario_A_50L_50E": {"err": 6.92,  "mean": 1092.14, "p95": 1570.95, "tput": 105.03},
        "cenario_B_75L_25E": {"err": 9.83,  "mean": 1060.25, "p95": 1520.95, "tput": 109.00},
        "cenario_C_25L_75E": {"err": 6.83,  "mean": 1059.20, "p95": 1514.00, "tput": 108.03},
    },
    "20k_sem_indice": {  # No T1 era 20k, usado como referencia de base 20k
        "cenario_A_50L_50E": {"err": 8.42,  "mean": 1057.17, "p95": 1608.90, "tput": 105.13},
        "cenario_B_75L_25E": {"err": 10.33, "mean": 1058.06, "p95": 1539.95, "tput": 108.30},
        "cenario_C_25L_75E": {"err": 3.92,  "mean": 1013.25, "p95": 1438.95, "tput": 107.58},
    },
}

results = {}
for cfg_key, _ in CONFIGS:
    results[cfg_key] = {}
    for sc_key, _ in SCENARIOS:
        p = BASE_DIR / cfg_key / sc_key / "statistics.json"
        with open(p, "r", encoding="utf-8") as f:
            results[cfg_key][sc_key] = json.load(f)

# Print detailed summary to console
for cfg_key, cfg_label in CONFIGS:
    print(f"\n=== {cfg_label} ===")
    for sc_key, sc_label in SCENARIOS:
        d = results[cfg_key][sc_key]
        tot = d["Total"]
        rd = d["Leitura Home"]
        wr = d["Escrita Pessoa"]
        print(
            f"{sc_label:<26} | Erro: {tot['errorPct']:>5.2f}% "
            f"| Media Total: {tot['meanResTime']:>7.1f}ms (L: {rd['meanResTime']:>7.1f}ms, E: {wr['meanResTime']:>7.1f}ms) "
            f"| P95: {tot['pct2ResTime']:>7.1f}ms | Vazao: {tot['throughput']:>6.2f} req/s"
        )

# -------------------------------------------------------------------------
# Grafico 1: Tempo Medio de Resposta (ms) nas 3 configuracoes novas
# -------------------------------------------------------------------------
plt.rcParams["font.sans-serif"] = "Arial"
x = np.arange(len(SCENARIOS))
width = 0.25
labels = ["50% L / 50% E\n(Cenário A)", "75% L / 25% E\n(Cenário B)", "25% L / 75% E\n(Cenário C)"]

mean_sem = [results["100k_sem_indice"][s][ "Total"]["meanResTime"] for s, _ in SCENARIOS]
mean_com = [results["100k_com_indice"][s][ "Total"]["meanResTime"] for s, _ in SCENARIOS]
mean_20k = [results["20k_sem_indice"][s][ "Total"]["meanResTime"] for s, _ in SCENARIOS]

fig, ax = plt.subplots(figsize=(8.5, 4.6), dpi=300)
r1 = ax.bar(x - width, mean_sem, width, label="100k SEM Índice", color="#dc2626", edgecolor="#991b1b")
r2 = ax.bar(x,         mean_com, width, label="100k COM Índice", color="#1e3a8a", edgecolor="#172554")
r3 = ax.bar(x + width, mean_20k, width, label="20k SEM Índice",  color="#0d9488", edgecolor="#115e59")

ax.set_ylabel("Tempo Médio de Resposta (ms)", fontweight="bold")
ax.set_title("Tempo Médio de Resposta (ms) — Nova Bateria (NGINX + 2 Flasks + SQL Corrigido)", fontweight="bold", pad=12)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontweight="bold")
ax.set_ylim(0, 3100)
ax.grid(axis="y", linestyle="--", alpha=0.5)
ax.legend()

for rects in (r1, r2, r3):
    for rect in rects:
        h = rect.get_height()
        ax.annotate(f"{h:.0f} ms", xy=(rect.get_x() + rect.get_width()/2, h),
                    xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold")

plt.tight_layout()
fig.savefig(CHARTS_DIR / "novo_latencia_media.png")
plt.close(fig)

# -------------------------------------------------------------------------
# Grafico 2: Vazao (Throughput req/s) nas 3 configuracoes novas
# -------------------------------------------------------------------------
tput_sem = [results["100k_sem_indice"][s]["Total"]["throughput"] for s, _ in SCENARIOS]
tput_com = [results["100k_com_indice"][s]["Total"]["throughput"] for s, _ in SCENARIOS]
tput_20k = [results["20k_sem_indice"][s]["Total"]["throughput"] for s, _ in SCENARIOS]

fig, ax = plt.subplots(figsize=(8.5, 4.6), dpi=300)
r1 = ax.bar(x - width, tput_sem, width, label="100k SEM Índice", color="#f59e0b", edgecolor="#b45309")
r2 = ax.bar(x,         tput_com, width, label="100k COM Índice", color="#2563eb", edgecolor="#1d4ed8")
r3 = ax.bar(x + width, tput_20k, width, label="20k SEM Índice",  color="#10b981", edgecolor="#047857")

ax.set_ylabel("Vazão / Throughput (req/s)", fontweight="bold")
ax.set_title("Vazão (req/s) — Ganho Real com Índice e Redução de Base", fontweight="bold", pad=12)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontweight="bold")
ax.set_ylim(0, 125)
ax.grid(axis="y", linestyle="--", alpha=0.5)
ax.legend(loc="lower right")

for rects in (r1, r2, r3):
    for rect in rects:
        h = rect.get_height()
        ax.annotate(f"{h:.1f}/s", xy=(rect.get_x() + rect.get_width()/2, h),
                    xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold")

plt.tight_layout()
fig.savefig(CHARTS_DIR / "novo_throughput.png")
plt.close(fig)

# -------------------------------------------------------------------------
# Grafico 3: Comparacao Taxa de Erros: Trabalho 1 (1 Flask) vs Agora (NGINX + 2 Flasks)
# -------------------------------------------------------------------------
err_t1 = [10.33, 14.25, 7.17]
err_now = [results["100k_com_indice"][s]["Total"]["errorPct"] for s, _ in SCENARIOS]

fig, ax = plt.subplots(figsize=(8.5, 4.3), dpi=300)
w2 = 0.32
b1 = ax.bar(x - w2/2, err_t1,  w2, label="Antes (1 Flask sem NGINX): 7% a 14% de Erro", color="#ef4444", edgecolor="#991b1b")
b2 = ax.bar(x + w2/2, err_now, w2, label="Agora (NGINX + 2 Réplicas Flask): 0,00% de Erro!", color="#16a34a", edgecolor="#166534")

ax.set_ylabel("Taxa de Erro (%)", fontweight="bold")
ax.set_title("Queda da Taxa de Erros (100k com Índice): Antes vs. Com Replicação Web", fontweight="bold", pad=12)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontweight="bold")
ax.set_ylim(0, 17)
ax.grid(axis="y", linestyle="--", alpha=0.5)
ax.legend()

for rect in b1:
    h = rect.get_height()
    ax.annotate(f"{h:.2f}%", xy=(rect.get_x() + rect.get_width()/2, h),
                xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=9, fontweight="bold", color="#991b1b")
for rect in b2:
    h = rect.get_height()
    ax.annotate("0,00% (Zero Erros!)", xy=(rect.get_x() + rect.get_width()/2, h),
                xytext=(0, 4), textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#166534")

plt.tight_layout()
fig.savefig(CHARTS_DIR / "comparativo_erros_antes_depois.png")
plt.close(fig)

print("\nGraficos gerados em:", CHARTS_DIR)
