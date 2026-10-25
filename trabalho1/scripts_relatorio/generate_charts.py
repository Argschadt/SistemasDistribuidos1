import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import matplotlib.patches as patches

# Set clean aesthetic style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 0.8

assets_dir = Path("assets")
assets_dir.mkdir(exist_ok=True)

# -------------------------------------------------------------
# Chart 1: Latency Comparison (Mean & P95) across configurations
# -------------------------------------------------------------
scenarios = ['50% L / 50% E', '75% L / 25% E', '25% L / 75% E']
x = np.arange(len(scenarios))
width = 0.25

mean_100k_idx = [1119.67, 1066.38, 1089.26]
mean_20k_idx  = [1057.17, 1058.06, 1013.25]
mean_100k_noidx = [1092.14, 1060.25, 1059.20]

fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
rects1 = ax.bar(x - width, mean_100k_idx, width, label='100k com Índice', color='#1e40af', edgecolor='#172554')
rects2 = ax.bar(x, mean_20k_idx, width, label='20k com Índice', color='#0d9488', edgecolor='#115e59')
rects3 = ax.bar(x + width, mean_100k_noidx, width, label='100k sem Índice', color='#f59e0b', edgecolor='#b45309')

ax.set_ylabel('Tempo Médio de Resposta (ms)', fontsize=11, fontweight='bold', color='#1e293b')
ax.set_title('Comparativo de Tempo Médio de Resposta por Perfil de Carga', fontsize=13, fontweight='bold', pad=15, color='#0f172a')
ax.set_xticks(x)
ax.set_xticklabels(scenarios, fontsize=10, fontweight='bold', color='#334155')
ax.set_ylim(0, 1350)
ax.legend(frameon=True, facecolor='#ffffff', edgecolor='#cbd5e1', fontsize=9.5)
ax.grid(axis='y', linestyle='--', alpha=0.5)

# Value labels on bars
for rects in [rects1, rects2, rects3]:
    for rect in rects:
        h = rect.get_height()
        ax.annotate(f'{h:.1f}',
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8.5, color='#1e293b', fontweight='semibold')

plt.tight_layout()
fig.savefig(assets_dir / "chart_latencia_media.png")
plt.close(fig)

# -------------------------------------------------------------
# Chart 2: P95 Latency (Tail Latency)
# -------------------------------------------------------------
p95_100k_idx = [1612.90, 1569.00, 1525.00]
p95_20k_idx  = [1608.90, 1539.95, 1438.95]
p95_100k_noidx = [1570.95, 1520.95, 1514.00]

fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
rects1 = ax.bar(x - width, p95_100k_idx, width, label='100k com Índice', color='#1e40af', edgecolor='#172554')
rects2 = ax.bar(x, p95_20k_idx, width, label='20k com Índice', color='#0d9488', edgecolor='#115e59')
rects3 = ax.bar(x + width, p95_100k_noidx, width, label='100k sem Índice', color='#f59e0b', edgecolor='#b45309')

ax.set_ylabel('Latência Percentil 95 - P95 (ms)', fontsize=11, fontweight='bold', color='#1e293b')
ax.set_title('Latência de Cauda (P95) sob Saturação de Concorrência', fontsize=13, fontweight='bold', pad=15, color='#0f172a')
ax.set_xticks(x)
ax.set_xticklabels(scenarios, fontsize=10, fontweight='bold', color='#334155')
ax.set_ylim(0, 1850)
ax.legend(frameon=True, facecolor='#ffffff', edgecolor='#cbd5e1', fontsize=9.5)
ax.grid(axis='y', linestyle='--', alpha=0.5)

for rects in [rects1, rects2, rects3]:
    for rect in rects:
        h = rect.get_height()
        ax.annotate(f'{h:.1f}',
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8.5, color='#1e293b', fontweight='semibold')

plt.tight_layout()
fig.savefig(assets_dir / "chart_latencia_p95.png")
plt.close(fig)

# -------------------------------------------------------------
# Chart 3: Error Rate (%) Across Configurations
# -------------------------------------------------------------
err_100k_idx = [10.33, 14.25, 7.17]
err_20k_idx  = [8.42, 10.33, 3.92]
err_100k_noidx = [6.92, 9.83, 6.83]

fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
rects1 = ax.bar(x - width, err_100k_idx, width, label='100k com Índice', color='#dc2626', edgecolor='#991b1b')
rects2 = ax.bar(x, err_20k_idx, width, label='20k com Índice (Melhor)', color='#059669', edgecolor='#047857')
rects3 = ax.bar(x + width, err_100k_noidx, width, label='100k sem Índice', color='#6366f1', edgecolor='#4338ca')

ax.set_ylabel('Taxa de Erro (%)', fontsize=11, fontweight='bold', color='#1e293b')
ax.set_title('Taxa de Falhas e Erros HTTP (%) sob Estresse de 1200 Requisições', fontsize=13, fontweight='bold', pad=15, color='#0f172a')
ax.set_xticks(x)
ax.set_xticklabels(scenarios, fontsize=10, fontweight='bold', color='#334155')
ax.set_ylim(0, 17)
ax.legend(frameon=True, facecolor='#ffffff', edgecolor='#cbd5e1', fontsize=9.5)
ax.grid(axis='y', linestyle='--', alpha=0.5)

for rects in [rects1, rects2, rects3]:
    for rect in rects:
        h = rect.get_height()
        ax.annotate(f'{h:.2f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8.5, color='#1e293b', fontweight='bold')

plt.tight_layout()
fig.savefig(assets_dir / "chart_taxa_erros.png")
plt.close(fig)

# -------------------------------------------------------------
# Chart 4: Throughput Comparison (Vazão)
# -------------------------------------------------------------
tput_100k_idx = [106.17, 109.73, 107.85]
tput_20k_idx  = [105.13, 108.30, 107.58]
tput_100k_noidx = [105.03, 109.00, 108.03]

fig, ax = plt.subplots(figsize=(9, 4.8), dpi=300)
rects1 = ax.bar(x - width, tput_100k_idx, width, label='100k com Índice', color='#3b82f6', edgecolor='#1d4ed8')
rects2 = ax.bar(x, tput_20k_idx, width, label='20k com Índice', color='#14b8a6', edgecolor='#0f766e')
rects3 = ax.bar(x + width, tput_100k_noidx, width, label='100k sem Índice', color='#8b5cf6', edgecolor='#6d28d9')

ax.set_ylabel('Throughput Médio (req/s)', fontsize=11, fontweight='bold', color='#1e293b')
ax.set_title('Estabilidade do Throughput (~105-110 req/s) - Saturação da CPU/Rede', fontsize=13, fontweight='bold', pad=15, color='#0f172a')
ax.set_xticks(x)
ax.set_xticklabels(scenarios, fontsize=10, fontweight='bold', color='#334155')
ax.set_ylim(0, 130)
ax.legend(frameon=True, facecolor='#ffffff', edgecolor='#cbd5e1', fontsize=9.5)
ax.grid(axis='y', linestyle='--', alpha=0.5)

for rects in [rects1, rects2, rects3]:
    for rect in rects:
        h = rect.get_height()
        ax.annotate(f'{h:.1f}',
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8.5, color='#1e293b', fontweight='semibold')

plt.tight_layout()
fig.savefig(assets_dir / "chart_throughput.png")
plt.close(fig)

# -------------------------------------------------------------
# Chart 5: Architecture Diagram (Clean, No Overlap, High Contrast)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11.5, 4.2), dpi=300)
ax.set_xlim(0, 11.5)
ax.set_ylim(0, 4.2)
ax.axis('off')

def draw_tier_card(ax, x, y, w, h, header_color, bg_color, title, subtitle, bullets):
    # Main card body
    body = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.08,rounding_size=0.15",
        edgecolor=header_color, facecolor=bg_color, linewidth=1.8
    )
    ax.add_patch(body)
    # Header bar
    header_h = 0.68
    header = patches.FancyBboxPatch(
        (x, y + h - header_h), w, header_h,
        boxstyle="round,pad=0.08,rounding_size=0.15",
        edgecolor=header_color, facecolor=header_color, linewidth=1.0
    )
    ax.add_patch(header)
    ax.text(x + w/2, y + h - header_h/2 + 0.08, title,
            ha='center', va='center', fontsize=10.5, fontweight='bold', color='#ffffff')
    ax.text(x + w/2, y + h - header_h/2 - 0.16, subtitle,
            ha='center', va='center', fontsize=8.5, color='#e2e8f0')

    # Bullets
    start_y = y + h - header_h - 0.32
    for i, line in enumerate(bullets):
        ax.text(x + 0.18, start_y - i * 0.36, line,
                ha='left', va='center', fontsize=9, color='#1e293b', fontweight='medium')

# Tier 1: Clientes
draw_tier_card(
    ax, 0.25, 0.45, 2.75, 3.1,
    header_color='#1e3a8a', bg_color='#f8fafc',
    title="1. CAMADA CLIENTE", subtitle="Apache JMeter 5.6.3",
    bullets=[
        "• 1.200 clientes simultâneos",
        "• Ramp-up de 10 segundos",
        "• Perfis: 50/50, 75/25, 25/75",
        "• Interface Web / Navegador",
        "• Disparo concorrente HTTP"
    ]
)

# Arrow 1: Client <-> Web Server
ax.annotate('', xy=(4.32, 2.15), xytext=(3.18, 2.15),
            arrowprops=dict(arrowstyle="-|>", color='#1e3a8a', lw=2.2, mutation_scale=16))
ax.annotate('', xy=(3.18, 1.75), xytext=(4.32, 1.75),
            arrowprops=dict(arrowstyle="-|>", color='#64748b', lw=1.8, linestyle='--', mutation_scale=14))
ax.text(3.75, 2.52, "HTTP / REST", ha='center', va='center', fontsize=9, fontweight='bold', color='#1e3a8a')
ax.text(3.75, 1.38, "JSON (Porta 5000)", ha='center', va='center', fontsize=8, color='#475569')

# Tier 2: Servidor Web
draw_tier_card(
    ax, 4.45, 0.45, 2.75, 3.1,
    header_color='#0d9488', bg_color='#f0fdfa',
    title="2. SERVIDOR WEB", subtitle="Python 3.14 + Flask 3.1",
    bullets=[
        "• Leitura: GET /api/pessoas",
        "• Escrita: POST /api/pessoas",
        "• Driver psycopg2 (síncrono)",
        "• 1 conexão por requisição",
        "• Serialização JSON / Jinja2"
    ]
)

# Arrow 2: Web Server <-> Database
ax.annotate('', xy=(8.52, 2.15), xytext=(7.38, 2.15),
            arrowprops=dict(arrowstyle="-|>", color='#0d9488', lw=2.2, mutation_scale=16))
ax.annotate('', xy=(7.38, 1.75), xytext=(8.52, 1.75),
            arrowprops=dict(arrowstyle="-|>", color='#64748b', lw=1.8, linestyle='--', mutation_scale=14))
ax.text(7.95, 2.52, "TCP / SQL", ha='center', va='center', fontsize=9, fontweight='bold', color='#0f766e')
ax.text(7.95, 1.38, "psycopg2 (Porta 5432)", ha='center', va='center', fontsize=8, color='#475569')

# Tier 3: Banco de Dados
draw_tier_card(
    ax, 8.65, 0.45, 2.6, 3.1,
    header_color='#334155', bg_color='#f8fafc',
    title="3. BANCO DE DADOS", subtitle="PostgreSQL 16",
    bullets=[
        "• Tabela: public.pessoas",
        "• Bases: 100k e 20k linhas",
        "• Índices B-Tree secundários",
        "• (cidade, data, status)",
        "• Transações ACID e WAL"
    ]
)

plt.tight_layout()
fig.savefig(assets_dir / "diagrama_arquitetura.png", bbox_inches='tight', pad_inches=0.12)
plt.close(fig)

print("Gráficos gerados com sucesso na pasta 'assets'!")
