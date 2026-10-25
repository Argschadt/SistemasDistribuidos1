import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Cores do tema
NAVY = RGBColor(30, 58, 138)       # #1E3A8A
DARK_SLATE = RGBColor(15, 23, 42)  # #0F172A
TEAL = RGBColor(13, 148, 136)      # #0D9488
LIGHT_BG = RGBColor(248, 250, 252) # #F8FAFC
WHITE = RGBColor(255, 255, 255)
MUTED = RGBColor(100, 116, 139)    # #64748B
BODY_TXT = RGBColor(30, 41, 59)    # #1E293B
BORDER_GRAY = RGBColor(203, 213, 225)
CARD_BLUE = RGBColor(239, 246, 255)
CARD_TEAL = RGBColor(240, 253, 250)
CARD_AMBER = RGBColor(255, 251, 235)
AMBER_BORDER = RGBColor(245, 158, 11)
RED_ACCENT = RGBColor(185, 28, 28)
GREEN_ACCENT = RGBColor(21, 128, 61)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]


def set_slide_bg(slide, color=LIGHT_BG):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_header(slide, title_text, subtitle_text, slide_num, total_slides=12):
    set_slide_bg(slide, LIGHT_BG)

    # Barra superior fina
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = NAVY
    top_bar.line.fill.background()

    # Título
    tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.28), Inches(11.0), Inches(0.55))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = DARK_SLATE
    p.font.name = "Calibri"

    # Subtítulo
    if subtitle_text:
        p2 = tf.add_paragraph()
        p2.text = subtitle_text
        p2.font.size = Pt(13)
        p2.font.color.rgb = MUTED
        p2.font.name = "Calibri"

    # Linha divisória
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.08), Inches(12.133), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER_GRAY
    line.line.fill.background()

    # Número do slide no rodapé
    fb = slide.shapes.add_textbox(Inches(0.6), Inches(7.05), Inches(12.133), Inches(0.3))
    ftf = fb.text_frame
    fp = ftf.paragraphs[0]
    fp.text = f"Sistemas Distribuídos 1  •  Avaliação de Desempenho CRUD          {slide_num} / {total_slides}"
    fp.font.size = Pt(10)
    fp.font.color.rgb = MUTED
    fp.font.name = "Calibri"
    fp.alignment = PP_ALIGN.RIGHT


def add_card(slide, left, top, width, height, title, items, bg_color=WHITE, border_color=BORDER_GRAY, title_color=NAVY, font_size=14):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.adjustments[0] = 0.03
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.2)

    tb = slide.shapes.add_textbox(Inches(left + 0.22), Inches(top + 0.16), Inches(width - 0.44), Inches(height - 0.32))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.size = Pt(font_size + 2)
    p0.font.bold = True
    p0.font.color.rgb = title_color
    p0.font.name = "Calibri"
    p0.space_after = Pt(6)

    for item in items:
        p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(font_size)
        p.font.color.rgb = BODY_TXT
        p.font.name = "Calibri"
        p.space_after = Pt(5)


# ==============================================================================
# SLIDE 1: CAPA
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_bg(s1, DARK_SLATE)

# Faixa lateral decorativa
side_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.35), Inches(7.5))
side_bar.fill.solid()
side_bar.fill.fore_color.rgb = TEAL
side_bar.line.fill.background()

tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.4), Inches(10.8), Inches(4.8))
tf1 = tb1.text_frame
tf1.word_wrap = True

p = tf1.paragraphs[0]
p.text = "SISTEMAS DISTRIBUÍDOS 1 — TRABALHO PRÁTICO 1"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = RGBColor(94, 234, 212)
p.font.name = "Calibri"
p.space_after = Pt(18)

p = tf1.add_paragraph()
p.text = "Avaliação de Desempenho de uma\nAplicação CRUD sob Carga Concorrente"
p.font.size = Pt(38)
p.font.bold = True
p.font.color.rgb = WHITE
p.font.name = "Calibri"
p.space_after = Pt(20)

p = tf1.add_paragraph()
p.text = "Análise prática com Python (Flask), PostgreSQL e Apache JMeter\nCenários de leitura/escrita, redução de dataset (100k vs 20k) e impacto de índices"
p.font.size = Pt(18)
p.font.color.rgb = RGBColor(203, 213, 225)
p.font.name = "Calibri"
p.space_after = Pt(44)

p = tf1.add_paragraph()
p.text = "Aluno: [Seu Nome Aqui]   •   Outubro de 2026"
p.font.size = Pt(15)
p.font.color.rgb = WHITE
p.font.name = "Calibri"


# ==============================================================================
# SLIDE 2: OBJETIVO E ESCOPO DO TRABALHO
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, "1. Objetivo e Escopo do Trabalho", "O que foi proposto no enunciado da disciplina", 2)

add_card(
    s2, 0.6, 1.35, 5.9, 5.4,
    "Parte 1 — Projeto e Implementação",
    [
        "• Desenvolver uma aplicação CRUD completa (Cliente + Servidor Web + Banco de Dados).",
        "• Popular o banco de dados com um dataset de pelo menos 50.000 registros (utilizamos 100.000 registros).",
        "• Definir a arquitetura da solução e preparar os cenários de carga concorrente.",
        "• Utilizar ferramenta de teste de carga (Apache JMeter) simulando múltiplos clientes simultâneos."
    ],
    bg_color=WHITE, border_color=NAVY, title_color=NAVY, font_size=15
)

add_card(
    s2, 6.8, 1.35, 5.9, 5.4,
    "Parte 2 — Experimentos e Perguntas",
    [
        "• Avaliar o desempenho em 3 proporções de Leitura (L) e Escrita (E):",
        "     A) 50% Leituras e 50% Escritas",
        "     B) 75% Leituras e 25% Escritas",
        "     C) 25% Leituras e 75% Escritas",
        "• Responder com base nos testes:",
        "     1. O que acontece ao reduzir o dataset para 20k registros?",
        "     2. Qual o efeito da adição de índices no BD? Qual escolher?",
        "     3. Como a escolha entre SQL e NoSQL impacta o sistema?"
    ],
    bg_color=WHITE, border_color=TEAL, title_color=TEAL, font_size=15
)


# ==============================================================================
# SLIDE 3: A APLICAÇÃO DESENVOLVIDA (CRUD)
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, "2. A Aplicação Desenvolvida (CRUD)", "Sistema de cadastro e consulta de pessoas em Python Flask + PostgreSQL", 3)

add_card(
    s3, 0.6, 1.35, 5.9, 2.5,
    "Modelo de Dados (Tabela public.pessoas)",
    [
        "• id (INTEGER PRIMARY KEY, auto-incremento via Sequence)",
        "• nome (VARCHAR 150) e email (VARCHAR 200)",
        "• telefone (VARCHAR 30) e cidade (VARCHAR 100)",
        "• data_cadastro (DATE) e status (ativo, inativo, pendente, bloqueado)"
    ],
    bg_color=WHITE, title_color=NAVY, font_size=14
)

add_card(
    s3, 0.6, 4.1, 5.9, 2.65,
    "Geração da Massa de Dados (pessoas.py)",
    [
        "• Script gerador próprio em Python.",
        "• Dataset principal: 100.000 registros importados via \\copy.",
        "• Dataset reduzido: 20.000 registros para o experimento comparativo.",
        "• Dados realistas distribuídos entre diversas cidades e status."
    ],
    bg_color=CARD_BLUE, border_color=NAVY, title_color=NAVY, font_size=14
)

add_card(
    s3, 6.8, 1.35, 5.9, 5.4,
    "Endpoints da API Utilizados nos Testes",
    [
        "• Leitura: GET /api/pessoas",
        "   - Retorna lista de pessoas em JSON (limite padrão: 100 registros).",
        "   - Ordenação: ORDER BY id DESC LIMIT 100.",
        "   - Suporta busca textual via parâmetro ?q=termo (usando ILIKE).",
        "",
        "• Escrita: POST /api/pessoas",
        "   - Recebe payload JSON com dados de uma nova pessoa.",
        "   - Executa INSERT INTO public.pessoas ... RETURNING id.",
        "   - Realiza commit imediato e retorna HTTP 201 (Created).",
        "",
        "• Outras operações disponíveis: Edição (UPDATE) e Exclusão (DELETE)."
    ],
    bg_color=WHITE, border_color=TEAL, title_color=TEAL, font_size=14
)


# ==============================================================================
# SLIDE 4: ARQUITETURA DA SOLUÇÃO (DIAGRAMA NATIVO EM 3 CAMADAS)
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
add_header(s4, "3. Arquitetura da Solução", "Organização cliente-servidor em 3 camadas e fluxo de comunicação", 4)

def add_tier_box(slide, left, top, width, height, header_color, bg_color, tier_tag, title, sub, bullets):
    # Corpo do card
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.adjustments[0] = 0.03
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = header_color
    card.line.width = Pt(1.8)

    # Faixa de cabeçalho do card
    hdr = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(1.05))
    hdr.adjustments[0] = 0.03
    hdr.fill.solid()
    hdr.fill.fore_color.rgb = header_color
    hdr.line.color.rgb = header_color
    hdr.line.width = Pt(1)

    htb = slide.shapes.add_textbox(Inches(left + 0.12), Inches(top + 0.08), Inches(width - 0.24), Inches(0.9))
    htf = htb.text_frame
    htf.word_wrap = True
    p0 = htf.paragraphs[0]
    p0.text = tier_tag
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(203, 213, 225)
    p0.font.name = "Calibri"
    p0.alignment = PP_ALIGN.CENTER

    p1 = htf.add_paragraph()
    p1.text = title
    p1.font.size = Pt(16)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.font.name = "Calibri"
    p1.alignment = PP_ALIGN.CENTER

    p2 = htf.add_paragraph()
    p2.text = sub
    p2.font.size = Pt(11)
    p2.font.color.rgb = RGBColor(226, 232, 240)
    p2.font.name = "Calibri"
    p2.alignment = PP_ALIGN.CENTER

    # Lista de detalhes
    btb = slide.shapes.add_textbox(Inches(left + 0.2), Inches(top + 1.2), Inches(width - 0.4), Inches(height - 1.35))
    btf = btb.text_frame
    btf.word_wrap = True
    for i, b in enumerate(bullets):
        bp = btf.paragraphs[0] if i == 0 else btf.add_paragraph()
        bp.text = b
        bp.font.size = Pt(13.5)
        bp.font.color.rgb = BODY_TXT
        bp.font.name = "Calibri"
        bp.space_after = Pt(8)

# Camada 1
add_tier_box(
    s4, 0.6, 1.35, 3.3, 4.35,
    header_color=NAVY, bg_color=WHITE,
    tier_tag="CAMADA 1", title="Clientes (Carga)", sub="Apache JMeter 5.6.3 / Browser",
    bullets=[
        "• 1.200 clientes simultâneos disparando requisições concorrentes.",
        "• Ramp-up: 10 segundos.",
        "• Simula os 3 perfis de tráfego: 50/50, 75/25 e 25/75 (Leitura/Escrita)."
    ]
)

# Conector 1 (HTTP / REST)
c1_badge = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.02), Inches(2.65), Inches(1.18), Inches(0.42))
c1_badge.fill.solid()
c1_badge.fill.fore_color.rgb = CARD_BLUE
c1_badge.line.color.rgb = NAVY
c1_p = c1_badge.text_frame.paragraphs[0]
c1_p.text = "HTTP / REST"
c1_p.font.size = Pt(10.5)
c1_p.font.bold = True
c1_p.font.color.rgb = NAVY
c1_p.alignment = PP_ALIGN.CENTER

arr1 = s4.shapes.add_shape(MSO_SHAPE.LEFT_RIGHT_ARROW, Inches(4.08), Inches(3.2), Inches(1.06), Inches(0.38))
arr1.fill.solid()
arr1.fill.fore_color.rgb = NAVY
arr1.line.fill.background()

c1_sub = s4.shapes.add_textbox(Inches(3.95), Inches(3.65), Inches(1.32), Inches(0.6))
c1_stf = c1_sub.text_frame
c1_sp = c1_stf.paragraphs[0]
c1_sp.text = "JSON\nPorta 5000"
c1_sp.font.size = Pt(10)
c1_sp.font.color.rgb = MUTED
c1_sp.alignment = PP_ALIGN.CENTER

# Camada 2
add_tier_box(
    s4, 5.32, 1.35, 3.3, 4.35,
    header_color=TEAL, bg_color=CARD_TEAL,
    tier_tag="CAMADA 2", title="Servidor Web / API", sub="Python 3.14 + Flask 3.1.3",
    bullets=[
        "• Leitura: GET /api/pessoas",
        "• Escrita: POST /api/pessoas",
        "• Comunicação Síncrona: abre e fecha 1 conexão por requisição via psycopg2."
    ]
)

# Conector 2 (TCP / SQL)
c2_badge = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.74), Inches(2.65), Inches(1.18), Inches(0.42))
c2_badge.fill.solid()
c2_badge.fill.fore_color.rgb = CARD_TEAL
c2_badge.line.color.rgb = TEAL
c2_p = c2_badge.text_frame.paragraphs[0]
c2_p.text = "TCP / SQL"
c2_p.font.size = Pt(10.5)
c2_p.font.bold = True
c2_p.font.color.rgb = TEAL
c2_p.alignment = PP_ALIGN.CENTER

arr2 = s4.shapes.add_shape(MSO_SHAPE.LEFT_RIGHT_ARROW, Inches(8.80), Inches(3.2), Inches(1.06), Inches(0.38))
arr2.fill.solid()
arr2.fill.fore_color.rgb = TEAL
arr2.line.fill.background()

c2_sub = s4.shapes.add_textbox(Inches(8.67), Inches(3.65), Inches(1.32), Inches(0.6))
c2_stf = c2_sub.text_frame
c2_sp = c2_stf.paragraphs[0]
c2_sp.text = "psycopg2\nPorta 5432"
c2_sp.font.size = Pt(10)
c2_sp.font.color.rgb = MUTED
c2_sp.alignment = PP_ALIGN.CENTER

# Camada 3
add_tier_box(
    s4, 10.04, 1.35, 2.69, 4.35,
    header_color= RGBColor(51, 65, 85), bg_color=WHITE,
    tier_tag="CAMADA 3", title="Banco de Dados", sub="PostgreSQL 16",
    bullets=[
        "• Tabela public.pessoas",
        "• Datasets: 100k e 20k registros.",
        "• Índices B-Tree: cidade, data_cadastro e status."
    ]
)

# Barra de Fluxo inferior
flow_box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(5.9), Inches(12.133), Inches(0.85))
flow_box.adjustments[0] = 0.05
flow_box.fill.solid()
flow_box.fill.fore_color.rgb = CARD_BLUE
flow_box.line.color.rgb = NAVY
flow_box.line.width = Pt(1.2)
fp = flow_box.text_frame.paragraphs[0]
fp.text = "Fluxo da Requisição:   1. JMeter envia HTTP (GET/POST)   →   2. Flask abre conexão no PostgreSQL   →   3. Banco executa SQL   →   4. Flask retorna JSON"
fp.font.size = Pt(13)
fp.font.bold = True
fp.font.color.rgb = NAVY
fp.font.name = "Calibri"
fp.alignment = PP_ALIGN.CENTER


# ==============================================================================
# SLIDE 5: METODOLOGIA E CENÁRIOS DE TESTE
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
add_header(s5, "4. Metodologia e Cenários de Teste", "9 baterias de teste no total (10.800 requisições analisadas)", 5)

add_card(
    s5, 0.6, 1.35, 3.9, 5.4,
    "Configuração do JMeter",
    [
        "• 1.200 clientes simultâneos (threads) por teste.",
        "• Ramp-up: 10 segundos.",
        "• 1 iteração por thread (1.200 requisições por bateria).",
        "",
        "• Métricas coletadas:",
        "   - Taxa de Erro (%)",
        "   - Tempo Médio de Resposta (ms)",
        "   - Percentil 95 / P95 (ms)",
        "   - Vazão / Throughput (req/s)"
    ],
    bg_color=WHITE, title_color=NAVY, font_size=14
)

add_card(
    s5, 4.7, 1.35, 3.9, 5.4,
    "3 Perfis de Carga (L / E)",
    [
        "• Cenário A (50% L / 50% E):",
        "   - 600 clientes lendo (GET)",
        "   - 600 clientes escrevendo (POST)",
        "",
        "• Cenário B (75% L / 25% E):",
        "   - 900 clientes lendo (GET)",
        "   - 300 clientes escrevendo (POST)",
        "",
        "• Cenário C (25% L / 75% E):",
        "   - 300 clientes lendo (GET)",
        "   - 900 clientes escrevendo (POST)"
    ],
    bg_color=CARD_BLUE, border_color=NAVY, title_color=NAVY, font_size=14
)

add_card(
    s5, 8.8, 1.35, 3.9, 5.4,
    "3 Configurações do Banco",
    [
        "• Variação 1 (Base Principal):",
        "   - 100.000 registros",
        "   - Com índices B-Tree secundários",
        "",
        "• Variação 2 (Base Reduzida):",
        "   - 20.000 registros",
        "   - Com índices B-Tree secundários",
        "",
        "• Variação 3 (Sem Índices):",
        "   - 100.000 registros",
        "   - Apenas chave primária (id)"
    ],
    bg_color=CARD_TEAL, border_color=TEAL, title_color=TEAL, font_size=14
)


# ==============================================================================
# SLIDE 6: TABELA GERAL DE RESULTADOS
# ==============================================================================
s6 = prs.slides.add_slide(blank_layout)
add_header(s6, "5. Resultados Consolidados (9 Baterias)", "Resumo completo das métricas coletadas pelo Apache JMeter", 6)

rows_data = [
    ["Configuração do BD", "Cenário", "Erro Leitura", "Erro Escrita", "Erro Total", "Tempo Médio", "P95", "Vazão (req/s)"],
    ["100k com índice", "A (50% L / 50% E)", "10,00%", "10,67%", "10,33%", "1.120 ms", "1.613 ms", "106,17 req/s"],
    ["100k com índice", "B (75% L / 25% E)", "14,11%", "14,67%", "14,25%", "1.066 ms", "1.569 ms", "109,73 req/s"],
    ["100k com índice", "C (25% L / 75% E)", "6,67%", "7,33%", "7,17%", "1.089 ms", "1.525 ms", "107,85 req/s"],
    ["20k com índice", "A (50% L / 50% E)", "7,33%", "9,50%", "8,42%", "1.057 ms", "1.609 ms", "105,13 req/s"],
    ["20k com índice", "B (75% L / 25% E)", "10,44%", "10,00%", "10,33%", "1.058 ms", "1.540 ms", "108,30 req/s"],
    ["20k com índice", "C (25% L / 75% E)", "4,00%", "3,89%", "3,92%", "1.013 ms", "1.439 ms", "107,58 req/s"],
    ["100k sem índice", "A (50% L / 50% E)", "7,00%", "6,83%", "6,92%", "1.092 ms", "1.571 ms", "105,03 req/s"],
    ["100k sem índice", "B (75% L / 25% E)", "10,00%", "9,33%", "9,83%", "1.060 ms", "1.521 ms", "109,00 req/s"],
    ["100k sem índice", "C (25% L / 75% E)", "8,00%", "6,44%", "6,83%", "1.059 ms", "1.514 ms", "108,03 req/s"],
]

table_shape = s6.shapes.add_table(10, 8, Inches(0.6), Inches(1.35), Inches(12.133), Inches(5.3))
t = table_shape.table

col_widths = [Inches(2.1), Inches(2.0), Inches(1.3), Inches(1.3), Inches(1.3), Inches(1.4), Inches(1.3), Inches(1.433)]
for idx, w in enumerate(col_widths):
    t.columns[idx].width = w

for r_idx, row in enumerate(rows_data):
    for c_idx, val in enumerate(row):
        cell = t.cell(r_idx, c_idx)
        cell.text = val
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER if c_idx >= 2 else PP_ALIGN.LEFT
        p.font.name = "Calibri"
        if r_idx == 0:
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY
            p.font.bold = True
            p.font.size = Pt(12)
            p.font.color.rgb = WHITE
        else:
            p.font.size = Pt(11.5)
            p.font.color.rgb = BODY_TXT
            if r_idx in (1, 2, 3):
                cell.fill.solid()
                cell.fill.fore_color.rgb = WHITE
            elif r_idx in (4, 5, 6):
                cell.fill.solid()
                cell.fill.fore_color.rgb = CARD_TEAL
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = CARD_BLUE
            if c_idx in (4, 7):
                p.font.bold = True


# ==============================================================================
# SLIDE 7: COMPARAÇÃO GRÁFICA (ERROS E LATÊNCIA)
# ==============================================================================
s7 = prs.slides.add_slide(blank_layout)
add_header(s7, "6. Visão Gráfica: Taxa de Erros e Latência Média", "Comparativo visual entre os 3 cenários e as 3 configurações do banco", 7)

if os.path.exists("assets/chart_taxa_erros.png"):
    s7.shapes.add_picture("assets/chart_taxa_erros.png", Inches(0.6), Inches(1.35), width=Inches(5.9))
if os.path.exists("assets/chart_latencia_media.png"):
    s7.shapes.add_picture("assets/chart_latencia_media.png", Inches(6.8), Inches(1.35), width=Inches(5.9))

add_card(
    s7, 0.6, 5.25, 12.133, 1.55,
    "Principais Observações",
    [
        "• A Taxa de Erros variou bastante entre os cenários: foi mais alta no perfil B (75% Leitura, que trafega JSON com 100 registros por resposta) e mais baixa no perfil C (75% Escrita, que insere apenas 1 registro).",
        "• O Tempo Médio de Resposta ficou sempre próximo de ~1.010 ms a ~1.120 ms em todas as baterias."
    ],
    bg_color=WHITE, border_color=NAVY, title_color=NAVY, font_size=13.5
)


# ==============================================================================
# SLIDE 8: POR QUE A VAZÃO TRAVOU EM ~107 REQ/S?
# ==============================================================================
s8 = prs.slides.add_slide(blank_layout)
add_header(s8, "7. Análise de Gargalo: Por que a Vazão travou em ~107 req/s?", "O teto de throughput foi idêntico em todas as 9 baterias de teste", 8)

if os.path.exists("assets/chart_throughput.png"):
    s8.shapes.add_picture("assets/chart_throughput.png", Inches(0.6), Inches(1.45), width=Inches(6.0))

add_card(
    s8, 6.85, 1.45, 5.88, 5.25,
    "O Gargalo está na Camada de Aplicação",
    [
        "• Fato observado nos dados:",
        "   Mudamos o tamanho da base (100k → 20k), tiramos os índices e mudamos a proporção L/E, mas a vazão ficou sempre entre 105 e 110 req/s.",
        "",
        "• Causa técnica:",
        "   1. O Flask rodou com threaded=True (1 processo criando 1 thread por requisição, com I/O bloqueante).",
        "   2. Cada thread chama psycopg2.connect(), abrindo uma conexão TCP exclusiva com o PostgreSQL sem pool.",
        "   3. Quando as threads simultâneas passam de 100, esbarram no limite do PostgreSQL (max_connections = 100).",
        "",
        "• Conclusão: As requisições extras aguardavam na fila ou falhavam por timeout, limitando a vazão em ~107 req/s."
    ],
    bg_color=CARD_AMBER, border_color=AMBER_BORDER, title_color=DARK_SLATE, font_size=13.5
)


# ==============================================================================
# SLIDE 9: PERGUNTA 1 — REDUÇÃO DO DATASET PARA 20K
# ==============================================================================
s9 = prs.slides.add_slide(blank_layout)
add_header(s9, "8. Pergunta 1: Redução do Dataset (100k → 20k)", "O que acontece com o desempenho se o banco for reduzido para 20.000 registros?", 9)

add_card(
    s9, 0.6, 1.4, 5.9, 5.3,
    "Comparativo Direto (Com Índices)",
    [
        "• Cenário A (50% L / 50% E):",
        "   - Taxa de erro caiu de 10,33% → 8,42%",
        "   - Tempo médio caiu de 1.120 ms → 1.057 ms",
        "",
        "• Cenário B (75% L / 25% E):",
        "   - Taxa de erro caiu de 14,25% → 10,33%",
        "   - Tempo médio caiu de 1.066 ms → 1.058 ms",
        "",
        "• Cenário C (25% L / 75% E):",
        "   - Taxa de erro caiu de 7,17% → 3,92% (redução de 45%!)",
        "   - Tempo médio caiu de 1.089 ms → 1.013 ms"
    ],
    bg_color=CARD_TEAL, border_color=TEAL, title_color=TEAL, font_size=14
)

add_card(
    s9, 6.8, 1.4, 5.9, 5.3,
    "Por que o desempenho melhorou?",
    [
        "• Menor volume em memória (Cache Hit):",
        "   Com apenas 20.000 linhas (5x menor), a tabela inteira e seus índices cabem folgadamente na memória RAM do PostgreSQL (shared_buffers).",
        "",
        "• Menos I/O de disco:",
        "   As leituras e atualizações de índice sofrem menos espera de disco, liberando as conexões mais rápido.",
        "",
        "• Por que a vazão (req/s) não subiu?",
        "   Porque o limite de ~107 req/s era imposto pela abertura de conexões síncronas no Flask, mas o sistema ficou muito mais estável (menos erros)."
    ],
    bg_color=WHITE, border_color=NAVY, title_color=NAVY, font_size=14
)


# ==============================================================================
# SLIDE 10: PERGUNTA 2 — ADIÇÃO DE ÍNDICES NO BANCO
# ==============================================================================
s10 = prs.slides.add_slide(blank_layout)
add_header(s10, "9. Pergunta 2: Adição de Índices no Banco de Dados", "O que aconteceu ao adicionar índices? Qual índice escolher? A consulta melhorou?", 10)

add_card(
    s10, 0.6, 1.35, 3.9, 5.4,
    "O que aconteceu nos testes?",
    [
        "• Foram criados 3 índices B-Tree:",
        "   - idx_pessoas_cidade",
        "   - idx_pessoas_data_cadastro",
        "   - idx_pessoas_status",
        "",
        "• Resultado (100k Com vs Sem Índice):",
        "   - 50/50: 10,33% vs 6,92% erro",
        "   - 75/25: 14,25% vs 9,83% erro",
        "   - 25/75: 7,17% vs 6,83% erro",
        "",
        "• Com índice o sistema teve MAIS erros!"
    ],
    bg_color=CARD_AMBER, border_color=AMBER_BORDER, title_color=DARK_SLATE, font_size=13.5
)

add_card(
    s10, 4.7, 1.35, 3.9, 5.4,
    "Por que piorou e não ajudou?",
    [
        "• Nas Leituras (Zero Ganho):",
        "   1. O JMeter enviou ?cidade=Manaus, mas a API lia ?q=termo (parâmetro foi ignorado e rodou ORDER BY id DESC LIMIT 100).",
        "   2. Mesmo usando ?q=, a query usa ILIKE '%termo%' (curinga no início), que ignora índices B-Tree e faz Sequential Scan.",
        "",
        "• Nas Escritas (Custo Extra):",
        "   Cada INSERT precisou atualizar a tabela + 3 árvores B-Tree + log WAL no disco, atrasando as transações."
    ],
    bg_color=WHITE, border_color=NAVY, title_color=NAVY, font_size=13.5
)

add_card(
    s10, 8.8, 1.35, 3.9, 5.4,
    "Qual índice escolher então?",
    [
        "• Caso 1 — Busca exata por cidade:",
        "   Ajustar a API para filtrar WHERE cidade = %s e manter apenas o índice B-Tree em cidade.",
        "",
        "• Caso 2 — Busca textual com ILIKE '%termo%':",
        "   O índice correto no PostgreSQL é o GIN com trigramas (extensão pg_trgm):",
        "",
        "   CREATE EXTENSION pg_trgm;",
        "   CREATE INDEX idx_pessoas_gin",
        "   ON pessoas USING gin",
        "   (nome gin_trgm_ops);"
    ],
    bg_color=CARD_TEAL, border_color=TEAL, title_color=TEAL, font_size=13.5
)


# ==============================================================================
# SLIDE 11: PERGUNTA 3 — IMPACTO SQL VS NOSQL
# ==============================================================================
s11 = prs.slides.add_slide(blank_layout)
add_header(s11, "10. Pergunta 3: Impacto da Escolha do BD (SQL vs NoSQL)", "Como a escolha entre banco relacional e não-relacional afeta o sistema?", 11)

add_card(
    s11, 0.6, 1.35, 5.9, 3.7,
    "Banco Relacional — SQL (Ex: PostgreSQL)",
    [
        "• Garante transações ACID e consistência imediata dos dados.",
        "• Esquema fixo e padronizado (ótimo para cadastros estruturados).",
        "• Sob alta concorrência de escrita, tem custo maior de controle de locks, atualização de índices e log transacional (WAL).",
        "• Escalabilidade predominantemente vertical (aumentar CPU/RAM do servidor)."
    ],
    bg_color=CARD_BLUE, border_color=NAVY, title_color=NAVY, font_size=14
)

add_card(
    s11, 6.8, 1.35, 5.9, 3.7,
    "Banco Não-Relacional — NoSQL (Ex: MongoDB, Cassandra)",
    [
        "• Focado em alta vazão de escrita e baixa latência sob carga massiva.",
        "• Escalabilidade horizontal nativa (distribuir dados em vários servidores / sharding).",
        "• Esquema flexível (documentos JSON ou chave-valor).",
        "• Geralmente adota consistência eventual (leituras podem não ver uma escrita imediatamente)."
    ],
    bg_color=CARD_TEAL, border_color=TEAL, title_color=TEAL, font_size=14
)

add_card(
    s11, 0.6, 5.25, 12.133, 1.55,
    "Conclusão para o nosso sistema",
    [
        "• Para um CRUD de cadastro de pessoas até centenas de milhares de registros, o PostgreSQL (SQL) é adequado pela integridade dos dados.",
        "• Caso o sistema precisasse escalar para milhares de escritas por segundo distribuídas em vários nós, um banco NoSQL seria mais indicado."
    ],
    bg_color=WHITE, border_color=BORDER_GRAY, title_color=DARK_SLATE, font_size=13.5
)


# ==============================================================================
# SLIDE 12: CONCLUSÃO E MELHORIAS FUTURAS
# ==============================================================================
s12 = prs.slides.add_slide(blank_layout)
add_header(s12, "11. Conclusão e Melhorias Futuras", "Síntese dos resultados obtidos e como escalar a arquitetura", 12)

add_card(
    s12, 0.6, 1.35, 5.9, 5.4,
    "Síntese dos Resultados",
    [
        "1. Vazão constante (~107 req/s): O gargalo principal foi a camada de aplicação síncrona abrindo conexão a cada requisição, e não o banco.",
        "",
        "2. Base de 20k vs 100k: Reduzir o dataset para 20k diminuiu os erros em todos os cenários (caindo para 3,92% no cenário 25L/75E) graças ao uso de cache em RAM.",
        "",
        "3. Índices precisam casar com a consulta: Índices B-Tree que não são usados nas queries de leitura apenas penalizam as operações de escrita (INSERT)."
    ],
    bg_color=WHITE, border_color=NAVY, title_color=NAVY, font_size=14
)

add_card(
    s12, 6.8, 1.35, 5.9, 5.4,
    "Como Escalar o Sistema na Prática?",
    [
        "1. Pool de Conexões (Connection Pooling):",
        "   Usar PgBouncer ou ThreadedConnectionPool para reaproveitar conexões já abertas com o PostgreSQL.",
        "",
        "2. Servidor WSGI de Produção:",
        "   Substituir o servidor embutido do Flask pelo Gunicorn com múltiplos workers / I/O assíncrono.",
        "",
        "3. Alinhamento de Índices e Queries:",
        "   Corrigir o filtro de cidade na API ou adotar índice GIN (pg_trgm) para buscas parciais com ILIKE."
    ],
    bg_color=CARD_TEAL, border_color=TEAL, title_color=TEAL, font_size=14
)

output_pptx = "apresentacao_slides.pptx"
try:
    prs.save(output_pptx)
    print(f"Apresentacao PPTX gerada com sucesso: {output_pptx} ({len(prs.slides)} slides)")
except PermissionError:
    alt_pptx = "apresentacao_slides_v2.pptx"
    prs.save(alt_pptx)
    print(f"Aviso: {output_pptx} esta aberto no PowerPoint. Salvo em: {alt_pptx} ({len(prs.slides)} slides)")

import subprocess
import pypdf

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
html_path = os.path.abspath("apresentacao_slides.html")
pdf_path = os.path.abspath("apresentacao_slides.pdf")

cmd = [
    chrome,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    f"file:///{html_path}",
]
subprocess.run(cmd, check=True)

reader = pypdf.PdfReader(pdf_path)
print(f"Apresentacao PDF gerada com sucesso: apresentacao_slides.pdf ({len(reader.pages)} slides)")
for i, page in enumerate(reader.pages):
    txt = page.extract_text().strip()
    first = txt.split("\n")[0] if txt else "[EMPTY]"
    print(f"  Slide {i+1:02d}: {first[:70]}")

