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
# Chart 5: Architecture Diagram
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis('off')

# Tier 1 Box: Clients
rect_client = patches.FancyBboxPatch((0.5, 1.2), 2.3, 2.6, boxstyle="round,pad=0.2",
                                     edgecolor='#2563eb', facecolor='#eff6ff', linewidth=2)
ax.add_patch(rect_client)
ax.text(1.65, 3.4, "CAMADA 1: CLIENTES", ha='center', va='center', fontsize=11, fontweight='bold', color='#1e40af')
ax.text(1.65, 2.7, "Apache JMeter 5.6.3\n• 1200 Threads Totais\n• Ramp-up: 10s\n• Perfis: 50/50, 75/25, 25/75\n• Navegador Web (HTML/JS)",
        ha='center', va='center', fontsize=8.5, color='#1e293b')

# Arrow 1: HTTP / REST
ax.annotate('', xy=(3.6, 2.7), xytext=(2.9, 2.7),
            arrowprops=dict(arrowstyle="<->", color='#3b82f6', lw=2.5))
ax.text(3.25, 3.0, "HTTP / REST\nJSON / Form", ha='center', va='center', fontsize=8, fontweight='bold', color='#1e40af')

# Tier 2 Box: Web Server
rect_server = patches.FancyBboxPatch((3.8, 1.2), 2.4, 2.6, boxstyle="round,pad=0.2",
                                     edgecolor='#0d9488', facecolor='#f0fdfa', linewidth=2)
ax.add_patch(rect_server)
ax.text(5.0, 3.4, "CAMADA 2: SERVIDOR WEB", ha='center', va='center', fontsize=11, fontweight='bold', color='#0f766e')
ax.text(5.0, 2.7, "Python 3.14 + Flask\n• Porta: 5000\n• Endpoints:\n  GET /api/pessoas\n  POST /api/pessoas\n• Renderizador Jinja2",
        ha='center', va='center', fontsize=8.5, color='#1e293b')

# Arrow 2: TCP / SQL
ax.annotate('', xy=(7.0, 2.7), xytext=(6.3, 2.7),
            arrowprops=dict(arrowstyle="<->", color='#0d9488', lw=2.5))
ax.text(6.65, 3.0, "TCP / 5432\npsycopg2 (SQL)", ha='center', va='center', fontsize=8, fontweight='bold', color='#0f766e')

# Tier 3 Box: Database
rect_db = patches.FancyBboxPatch((7.2, 1.2), 2.3, 2.6, boxstyle="round,pad=0.2",
                                 edgecolor='#7c3aed', facecolor='#f5f3ff', linewidth=2)
ax.add_patch(rect_db)
ax.text(8.35, 3.4, "CAMADA 3: BANCO DE DADOS", ha='center', va='center', fontsize=11, fontweight='bold', color='#6d28d9')
ax.text(8.35, 2.7, "PostgreSQL 16\n• Tabela: public.pessoas\n• Datasets: 100k e 20k\n• Índices: B-Tree\n  (cidade, data, status)\n• Transações ACID / WAL",
        ha='center', va='center', fontsize=8.5, color='#1e293b')

ax.set_title("Arquitetura Distribuída em 3 Camadas da Solução CRUD", fontsize=13, fontweight='bold', pad=10, color='#0f172a')
plt.tight_layout()
fig.savefig(assets_dir / "diagrama_arquitetura.png")
plt.close(fig)

print("Gráficos gerados com sucesso na pasta 'assets'!")
