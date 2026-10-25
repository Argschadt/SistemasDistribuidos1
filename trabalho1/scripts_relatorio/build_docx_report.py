import os
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_report():
    doc = Document()

    # Page Margins (A4 standard: ~3cm left/top, 2cm right/bottom)
    for section in doc.sections:
        section.top_margin = Inches(1.18)
        section.bottom_margin = Inches(0.79)
        section.left_margin = Inches(1.18)
        section.right_margin = Inches(0.79)

    # Styles setup
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = RGBColor(30, 41, 59) # Slate 800

    # -------------------------------------------------------------
    # CAPA
    # -------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("DISCIPLINA DE SISTEMAS DISTRIBUÍDOS 1\nDEPARTAMENTO DE COMPUTAÇÃO / ENGENHARIA")
    r_inst.bold = True
    r_inst.font.size = Pt(13)
    r_inst.font.color.rgb = RGBColor(30, 58, 138)

    doc.add_paragraph("\n\n\n")

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("RELATÓRIO TÉCNICO-EXPERIMENTAL:\nAVALIAÇÃO DE DESEMPENHO DE ARQUITETURA DISTRIBUÍDA CLIENTE-SERVIDOR (CRUD) SOB MÚLTIPLOS PERFIS DE CARGA E ESTRATÉGIAS DE INDEXAÇÃO")
    r_title.bold = True
    r_title.font.size = Pt(16)
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Estudo comparativo de escalabilidade, taxas de saturação, contenção de I/O em PostgreSQL e análise sob a ótica de Sistemas Distribuídos")
    r_sub.italic = True
    r_sub.font.size = Pt(11.5)
    r_sub.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_paragraph("\n\n\n\n\n")

    p_info = doc.add_paragraph()
    p_info.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_info = p_info.add_run("Aplicação: CRUD Python Flask + PostgreSQL\nFerramenta de Carga: Apache JMeter 5.6.3\nVolume de Teste: 1200 requisições simultâneas por cenário\nDatasets Avaliados: 100k e 20k registros")
    r_info.font.size = Pt(10.5)
    r_info.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph("\n\n\n")

    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_foot = p_foot.add_run("2026")
    r_foot.bold = True
    r_foot.font.size = Pt(11)

    doc.add_page_break()

    # -------------------------------------------------------------
    # RESUMO EXECUTIVO
    # -------------------------------------------------------------
    h_resumo = doc.add_heading("RESUMO EXECUTIVO", level=1)
    h_resumo.runs[0].font.color.rgb = RGBColor(30, 58, 138)

    p_resumo = doc.add_paragraph(
        "Este trabalho apresenta a implementação e a avaliação sistemática de desempenho de uma arquitetura distribuída "
        "em três camadas para operações CRUD (Create, Read, Update, Delete), composta por clientes simultâneos emulados via Apache JMeter, "
        "servidor web de aplicação baseado em Python Flask e banco de dados relacional PostgreSQL. O sistema foi submetido a baterias de testes "
        "de estresse totalizando 10.800 requisições distribuídas em 9 cenários experimentais, combinando três proporções de carga (50% Leitura / 50% Escrita, "
        "75% Leitura / 25% Escrita e 25% Leitura / 75% Escrita) sob três variações de banco de dados: 100.000 registros com índices secundários, "
        "20.000 registros com índices secundários e 100.000 registros sem índices secundários. Os resultados demonstram um patamar de saturação "
        "de vazão (throughput) entre 105 e 110 req/s imposto pelos limites de concorrência e ausência de connection pooling assíncrono. "
        "A redução da base para 20.000 registros proporcionou expressivo aumento na confiabilidade (taxa de erro reduzida de até 14,25% para 3,92%). "
        "Adicionalmente, revelou-se um comportamento contraintuitivo onde os índices B-Tree criados degradaram a performance em operações massivas de escrita "
        "devido à sobrecarga no Write-Ahead Logging (WAL) e manutenção dos nós da árvore, sem contrapartida de ganho nas consultas com busca textual ILIKE. "
        "Por fim, discutem-se os impactos distributivos da escolha entre bancos SQL e NoSQL à luz do Teorema CAP e das garantias ACID versus BASE."
    )
    p_resumo.paragraph_format.line_spacing = 1.2
    p_resumo.paragraph_format.space_after = Pt(12)

    p_kw = doc.add_paragraph()
    r_kw_bold = p_kw.add_run("Palavras-chave: ")
    r_kw_bold.bold = True
    p_kw.add_run("Sistemas Distribuídos; Avaliação de Desempenho; Apache JMeter; PostgreSQL; Flask; Índices de Banco de Dados; Teorema CAP.")

    doc.add_paragraph().paragraph_format.space_after = Pt(18)

    # -------------------------------------------------------------
    # 1. PARTE 1: DEFINIÇÃO DA APLICAÇÃO E CENÁRIO EXPERIMENTAL
    # -------------------------------------------------------------
    h1 = doc.add_heading("1. PARTE 1: DEFINIÇÃO DA APLICAÇÃO E PROJETO DA ARQUITETURA", level=1)
    h1.runs[0].font.color.rgb = RGBColor(30, 58, 138)

    h1_1 = doc.add_heading("1.1 Definição da Aplicação CRUD", level=2)
    h1_1.runs[0].font.color.rgb = RGBColor(13, 148, 136)

    doc.add_paragraph(
        "A aplicação desenvolvida consiste em um serviço corporativo de cadastro e gerenciamento de pessoas/clientes. "
        "A entidade central manipulada pelo sistema é composta pelos seguintes atributos:"
    )

    p_attrs = doc.add_paragraph(
        "• id (INTEGER PRIMARY KEY): Identificador único serial da entidade.\n"
        "• nome (VARCHAR(150) NOT NULL): Nome completo do indivíduo.\n"
        "• email (VARCHAR(200) NOT NULL): Endereço de correio eletrônico exclusivo.\n"
        "• telefone (VARCHAR(30)): Número de contato telefônico formatado.\n"
        "• cidade (VARCHAR(100)): Município de residência cadastrado.\n"
        "• data_cadastro (DATE): Timestamp do registro no sistema.\n"
        "• status (VARCHAR(20)): Estado cadastral ('ativo', 'inativo', 'pendente', 'bloqueado')."
    )
    p_attrs.paragraph_format.left_indent = Inches(0.25)

    doc.add_paragraph(
        "A aplicação oferece tanto uma interface gráfica web responsiva renderizada pelo motor Jinja2 quanto uma interface de programação "
        "RESTful (API JSON), permitindo operações programáticas de alta performance:"
    )

    p_routes = doc.add_paragraph(
        "• GET / : Interface gráfica contendo formulário de cadastro, tabela de listagem e barra de pesquisa.\n"
        "• GET /api/pessoas : Retorna uma lista de pessoas em formato JSON com suporte a parâmetros de busca (?q=...) e limite (?limit=100).\n"
        "• POST /api/pessoas : Cria um novo registro recebendo payload em JSON ou form-urlencoded e retorna o código HTTP 201 Created.\n"
        "• POST /pessoas : Rota para submissão via formulário HTML tradicional com redirecionamento e mensagens Flash.\n"
        "• POST /pessoas/<id>/editar : Atualiza os atributos da pessoa especificada.\n"
        "• POST /pessoas/<id>/excluir : Realiza a exclusão física do registro no banco de dados."
    )
    p_routes.paragraph_format.left_indent = Inches(0.25)

    # 1.2 Arquitetura da Solução
    h1_2 = doc.add_heading("1.2 Projeto da Arquitetura da Solução (3 Camadas)", level=2)
    h1_2.runs[0].font.color.rgb = RGBColor(13, 148, 136)

    doc.add_paragraph(
        "A arquitetura foi estruturada no modelo clássico de Três Camadas (3-Tier Architecture), amplamente adotado em sistemas cliente-servidor "
        "distribuídos para garantir o desacoplamento de responsabilidades, manutenibilidade e isolamento de falhas:"
    )

    doc.add_paragraph(
        "1. Camada de Apresentação / Clientes (Presentation Tier):\n"
        "Composta pelos navegadores dos usuários e, primordialmente, pelos nós de teste de carga configurados no Apache JMeter 5.6.3. "
        "Os clientes realizam requisições HTTP síncronas contra os endpoints do servidor, enviando comandos GET e POST simultâneos.\n\n"
        "2. Camada de Aplicação / Servidor Web (Application Tier):\n"
        "Implementada com o microframework Python Flask 3.1.3 em ambiente Python 3.14. Atua como o servidor de processamento e orquestração. "
        "Esta camada é responsável pela recepção das requisições HTTP, validação sintática e semântica dos dados recebidos, serialização/deserialização "
        "JSON, execução das regras de negócio e despacho de comandos SQL para o banco através do driver psycopg2.\n\n"
        "3. Camada de Dados / Persistência (Data Tier):\n"
        "Construída sobre o SGBD relacional PostgreSQL 16. Gerencia o armazenamento persistente na tabela public.pessoas, aplicando restrições de integridade, "
        "manutenção de índices B-Tree, controle de concorrência multiversão (MVCC) e garantia das propriedades ACID (Atomicidade, Consistência, Isolamento e Durabilidade)."
    )

    # Inserir Diagrama de Arquitetura
    if os.path.exists("assets/diagrama_arquitetura.png"):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture("assets/diagrama_arquitetura.png", width=Inches(6.2))
        p_cap = doc.add_paragraph("Figura 1: Arquitetura distribuída em 3 camadas e fluxo de comunicação entre nós.")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.size = Pt(9.5)
        p_cap.runs[0].font.italic = True
        p_cap.paragraph_format.space_after = Pt(14)

    # 1.3 Cenário de Experimentos
    h1_3 = doc.add_heading("1.3 Cenário de Experimentos e Metodologia de Carga", level=2)
    h1_3.runs[0].font.color.rgb = RGBColor(13, 148, 136)

    doc.add_paragraph(
        "Para avaliar rigorosamente a escalabilidade e o comportamento do sistema sob concorrência, o Apache JMeter 5.6.3 foi configurado "
        "para emular múltiplos clientes simultâneos acessando o cluster local. Em conformidade com as diretrizes do trabalho, foram avaliados "
        "três perfis operacionais de carga com 1200 amostras totais e tempo de subida (ramp-up) de 10 segundos:"
    )

    doc.add_paragraph(
        "• Cenário A (50% Leituras / 50% Escritas): 600 clientes emulando operações de leitura (GET /api/pessoas) e 600 clientes emulando escrita (POST /api/pessoas).\n"
        "• Cenário B (75% Leituras / 25% Escritas): Perfil 'read-heavy' com 900 leituras e 300 escritas simultâneas.\n"
        "• Cenário C (25% Leituras / 75% Escritas): Perfil 'write-heavy' com 300 leituras e 900 escritas simultâneas."
    )

    doc.add_paragraph(
        "Geração do Dataset Sintético:\n"
        "Foi desenvolvido o gerador em Python 'pessoas.py', capaz de produzir massas de dados realistas com distribuição estatística controlada "
        "(nomes compostos, endereços de e-mail pseudo-aleatórios, telefones com DDDs brasileiros e cidades capitais). O gerador foi utilizado para "
        "popular a tabela com um dataset volumoso de 100.000 registros (superando o requisito mínimo de 50k) e um dataset reduzido de 20.000 registros."
    )

    doc.add_paragraph(
        "Configurações da Base de Dados Avaliadas (3 Variações):\n"
        "1. Variação 1: 100.000 registros com índices secundários (idx_pessoas_cidade, idx_pessoas_data_cadastro, idx_pessoas_status).\n"
        "2. Variação 2: 20.000 registros com índices secundários.\n"
        "3. Variação 3: 100.000 registros sem índices secundários (apenas a chave primária indexada)."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # 2. PARTE 2: AVALIAÇÃO DA ARQUITETURA PROPOSTA ATRAVÉS DE EXPERIMENTOS
    # -------------------------------------------------------------
    h2 = doc.add_heading("2. PARTE 2: AVALIAÇÃO EXPERIMENTAL E ANÁLISE DE RESULTADOS", level=1)
    h2.runs[0].font.color.rgb = RGBColor(30, 58, 138)

    doc.add_paragraph(
        "Nesta seção são consolidados os dados empíricos coletados durante as 9 baterias de testes (total de 10.800 requisições). "
        "As métricas avaliadas incluem: Amostras (N), Taxa de Erro HTTP (%), Tempo Médio de Resposta (ms), Mediana (ms), Percentis P95 e P99 (ms) e Vazão (Throughput em req/s)."
    )

    # Tabelas
    def add_metrics_table(title, rows_data):
        doc.add_heading(title, level=3).runs[0].font.color.rgb = RGBColor(15, 23, 42)
        table = doc.add_table(rows=len(rows_data)+1, cols=8)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        headers = ["Operação", "N", "Erro %", "Média (ms)", "Mediana", "P95 (ms)", "P99 (ms)", "Throughput"]
        
        # Header formatting
        for idx, text in enumerate(headers):
            cell = table.cell(0, idx)
            cell.text = text
            set_cell_background(cell, "1E3A8A")
            set_cell_margins(cell, top=120, bottom=120, left=100, right=100)
            p = cell.paragraphs[0]
            p.runs[0].font.bold = True
            p.runs[0].font.size = Pt(9)
            p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        for r_idx, row in enumerate(rows_data):
            bg = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
            for c_idx, val in enumerate(row):
                cell = table.cell(r_idx+1, c_idx)
                cell.text = str(val)
                set_cell_background(cell, bg)
                set_cell_margins(cell, top=80, bottom=80, left=90, right=90)
                p = cell.paragraphs[0]
                p.runs[0].font.size = Pt(8.5)
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
        doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Tabela 1: 100k com índice
    data_100k_idx = [
        ["Total (50/50)", "1200", "10.33%", "1119.67", "1284.50", "1612.90", "1708.99", "106.17 r/s"],
        ["  • Leitura Home", "600", "10.00%", "1126.30", "1297.50", "1624.95", "1714.94", "53.22 r/s"],
        ["  • Escrita Pessoa", "600", "10.67%", "1113.05", "1279.00", "1584.75", "1695.00", "53.19 r/s"],
        ["Total (75L / 25E)", "1200", "14.25%", "1066.38", "1284.50", "1569.00", "1696.92", "109.73 r/s"],
        ["  • Leitura Home", "900", "14.11%", "1068.37", "1292.00", "1574.70", "1719.98", "82.36 r/s"],
        ["  • Escrita Pessoa", "300", "14.67%", "1060.38", "1265.00", "1563.75", "1629.96", "27.72 r/s"],
        ["Total (25L / 75E)", "1200", "7.17%", "1089.26", "1219.00", "1525.00", "1605.88", "107.85 r/s"],
        ["  • Leitura Home", "300", "6.67%", "1098.19", "1226.00", "1528.30", "1607.73", "27.16 r/s"],
        ["  • Escrita Pessoa", "900", "7.33%", "1086.28", "1218.00", "1525.00", "1605.88", "80.88 r/s"],
    ]
    add_metrics_table("Tabela 1: Métricas de Desempenho - Variação 1 (100k Registros com Índice)", data_100k_idx)

    # Tabela 2: 20k com índice
    data_20k_idx = [
        ["Total (50/50)", "1200", "8.42%", "1057.17", "1200.50", "1608.90", "1754.99", "105.13 r/s"],
        ["  • Leitura Home", "600", "7.33%", "1070.75", "1207.50", "1630.80", "1753.95", "52.57 r/s"],
        ["  • Escrita Pessoa", "600", "9.50%", "1043.60", "1184.00", "1596.00", "1784.78", "52.74 r/s"],
        ["Total (75L / 25E)", "1200", "10.33%", "1058.06", "1247.00", "1539.95", "1678.00", "108.30 r/s"],
        ["  • Leitura Home", "900", "10.44%", "1056.18", "1248.00", "1560.00", "1678.00", "81.25 r/s"],
        ["  • Escrita Pessoa", "300", "10.00%", "1063.70", "1241.50", "1509.80", "1705.62", "27.45 r/s"],
        ["Total (25L / 75E)", "1200", "3.92%", "1013.25", "1115.50", "1438.95", "1554.88", "107.58 r/s"],
        ["  • Leitura Home", "300", "4.00%", "1010.61", "1103.00", "1469.75", "1591.66", "26.96 r/s"],
        ["  • Escrita Pessoa", "900", "3.89%", "1014.14", "1120.00", "1432.00", "1531.99", "80.68 r/s"],
    ]
    add_metrics_table("Tabela 2: Métricas de Desempenho - Variação 2 (20k Registros com Índice)", data_20k_idx)

    # Tabela 3: 100k sem índice
    data_100k_noidx = [
        ["Total (50/50)", "1200", "6.92%", "1092.14", "1253.50", "1570.95", "1674.97", "105.03 r/s"],
        ["  • Leitura Home", "600", "7.00%", "1093.10", "1260.50", "1584.90", "1707.94", "52.56 r/s"],
        ["  • Escrita Pessoa", "600", "6.83%", "1091.17", "1250.00", "1567.85", "1654.96", "52.52 r/s"],
        ["Total (75L / 25E)", "1200", "9.83%", "1060.25", "1211.50", "1520.95", "1654.99", "109.00 r/s"],
        ["  • Leitura Home", "900", "10.00%", "1057.34", "1214.50", "1529.80", "1679.99", "81.87 r/s"],
        ["  • Escrita Pessoa", "300", "9.33%", "1069.01", "1208.50", "1514.50", "1620.83", "27.46 r/s"],
        ["Total (25L / 75E)", "1200", "6.83%", "1059.20", "1204.50", "1514.00", "1614.97", "108.03 r/s"],
        ["  • Leitura Home", "300", "8.00%", "1039.90", "1206.50", "1508.95", "1612.00", "27.29 r/s"],
        ["  • Escrita Pessoa", "900", "6.44%", "1065.64", "1203.50", "1520.90", "1622.92", "81.03 r/s"],
    ]
    add_metrics_table("Tabela 3: Métricas de Desempenho - Variação 3 (100k Registros sem Índice)", data_100k_noidx)

    doc.add_page_break()

    # 2.2 Gráficos e Visualizações
    h2_2 = doc.add_heading("2.2 Análise Gráfica dos Resultados", level=2)
    h2_2.runs[0].font.color.rgb = RGBColor(13, 148, 136)

    def add_figure(path, caption):
        if os.path.exists(path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_picture(path, width=Inches(5.8))
            p_c = doc.add_paragraph(caption)
            p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_c.runs[0].font.size = Pt(9.5)
            p_c.runs[0].font.italic = True
            p_c.paragraph_format.space_after = Pt(12)

    add_figure("assets/chart_taxa_erros.png", "Figura 2: Comparativo da Taxa de Erro HTTP (%) entre configurações e cargas.")
    add_figure("assets/chart_latencia_media.png", "Figura 3: Tempo Médio de Resposta (ms) demonstrando a redução de latência com base em 20k.")
    add_figure("assets/chart_latencia_p95.png", "Figura 4: Latência Percentil 95 (P95) indicando o comportamento da cauda do sistema.")
    add_figure("assets/chart_throughput.png", "Figura 5: Throughput médio (req/s) com teto fixo de saturação em ~105-110 requisições/segundo.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 3. RESPOSTAS FUNDAMENTADAS ÀS QUESTÕES DO ENUNCIADO
    # -------------------------------------------------------------
    h3 = doc.add_heading("3. DISCUSSÃO TEÓRICO-EMPÍRICA E RESPOSTAS AO ENUNCIADO", level=1)
    h3.runs[0].font.color.rgb = RGBColor(30, 58, 138)

    # Questão 1
    h3_1 = doc.add_heading("3.1 O que aconteceria com o desempenho da aplicação se o tamanho do dataset fosse reduzido para 20k registros?", level=2)
    h3_1.runs[0].font.color.rgb = RGBColor(13, 148, 136)

    doc.add_paragraph(
        "A análise comparativa entre as Variações 1 (100.000 registros) e 2 (20.000 registros) comprova de forma contundente que a redução do volume "
        "de dados traz benefícios substanciais à estabilidade operacional e à latência geral da aplicação distribuída:"
    )

    doc.add_paragraph(
        "1. Queda Expressiva na Taxa de Erros e Falhas de Conexão:\n"
        "No perfil de carga balanceada (50% leitura / 50% escrita), a taxa de falha caiu de 10,33% para 8,42%. No cenário com predomínio de escritas (25L/75E), "
        "a melhoria foi ainda mais drástica: a taxa de erros despencou de 7,17% para apenas 3,92% (uma redução de 45,3% no volume de requisições rejeitadas). "
        "Mesmo no perfil com 75% de leituras, o índice de erro recuou de 14,25% para 10,33%."
    )

    doc.add_paragraph(
        "2. Redução do Tempo de Resposta (Média e Percentil 95):\n"
        "O tempo médio de resposta caiu em todos os cenários. No cenário 25L/75E, a média passou de 1089,26 ms (100k) para 1013,25 ms (20k), "
        "e a latência P95 sofreu redução significativa de 1525,00 ms para 1438,95 ms."
    )

    doc.add_paragraph(
        "Fundamentação Teórica em Sistemas de Banco de Dados:\n"
        "Esses ganhos decorrem de três fatores arquiteturais no SGBD PostgreSQL:\n"
        "• Buffer Cache Hit Ratio e E/S em Disco: Uma base de 20k registros (aproximadamente 2 MB em disco) cabe inteiramente no shared_buffers (memória RAM) "
        "do PostgreSQL. Em contrapartida, com 100k registros e 1200 conexões concorrentes gerando escritas e leituras simultâneas, o motor sofre maior pressão de "
        "descarte de páginas da memória (page evictions), gerando operações síncronas de I/O em disco para carregar blocos de dados.\n"
        "• Redução do Custo de Varreduras (Table Scans): Em consultas que demandam leitura ampla ou não utilizam índices perfeitamente ajustados, o custo de um "
        "Sequential Scan em 20k páginas é exatamente 5 vezes menor em volume de tuplas percorridas do que em 100k, liberando ciclos de CPU do servidor mais rapidamente.\n"
        "• Menor Contenção de Locks de Página: Conjuntos de dados menores concentram menos transações em disputa por páginas distintas, diminuindo a fila de espera "
        "por locks a nível de tupla e página durante a execução concorrente de INSERTs."
    )

    # Questão 2
    h3_2 = doc.add_heading("3.2 O que aconteceria se ocorresse a adição de índices no BD? Qual índice você escolheria? O desempenho de consulta melhora?", level=2)
    h3_2.runs[0].font.color.rgb = RGBColor(13, 148, 136)

    doc.add_paragraph(
        "A investigação experimental deste trabalho produziu um resultado técnico de altíssimo valor didático e empírico: "
        "a adição indiscriminada de índices não apenas não acelerou as consultas, como degradou a estabilidade geral da aplicação."
    )

    doc.add_paragraph(
        "1. Por que o desempenho de consulta NÃO melhorou com os índices B-Tree criados?\n"
        "Na modelagem inicial do banco de dados (postgres_setup.sql), foram criados índices do tipo B-Tree padrão nas colunas secundárias: "
        "idx_pessoas_cidade (cidade), idx_pessoas_data_cadastro (data_cadastro) e idx_pessoas_status (status). "
        "Contudo, a rotina de busca implementada no servidor Flask (função fetch_people em app.py) executa a seguinte consulta sob requisições de busca:\n"
        "   WHERE CAST(id AS TEXT) ILIKE %s OR nome ILIKE %s OR email ILIKE %s OR cidade ILIKE %s ...\n\n"
        "Em bancos de dados relacionais baseados em árvores B-Tree, expressões com predicado ILIKE com caractere curinga no início ('%termo%') "
        "tornam o índice B-Tree COMPLETAMENTE INÚTIL. O otimizador de consultas (Query Planner) do PostgreSQL é forçado a ignorar os índices B-Tree e realizar "
        "um Sequential Scan integral na tabela para verificar cada string individualmente. Além disso, nas requisições do JMeter que buscaram a rota principal sem parâmetros, "
        "a consulta executada foi simplesmente 'ORDER BY id DESC LIMIT 100', a qual utiliza unicamente o índice da Chave Primária (id), ignorando todos os demais índices secundários criados."
    )

    doc.add_paragraph(
        "2. A Penalidade de Escrita (Write Overhead) comprovada empiricamente:\n"
        "Enquanto os índices não trouxeram benefício para a leitura, cada operação de escrita (INSERT) foi obrigada a atualizar sincronamente a tabela principal "
        "e mais 4 estruturas de dados adicionais (a árvore PK e as 3 árvores de índices secundários). Isso causou aumento na geração de logs no Write-Ahead Log (WAL), "
        "maior contenção de I/O e ampliação das latências. Os dados comprovam isso: com 100k registros, o cenário sem índice teve menor taxa de erro global (6,92% contra 10,33% com índice) "
        "e nas operações de escrita puras, a taxa de erro subiu de 6,44% (sem índice) para 7,33% (com índice) no perfil 25L/75E, e de 9,33% para 14,67% no perfil 75L/25E!"
    )

    doc.add_paragraph(
        "3. Qual índice técnico escolher para este cenário?\n"
        "Se o objetivo arquitetural for otimizar consultas textuais parciais e de múltiplos campos como as do sistema:\n"
        "• Índice Recomendado para Busca Textual: Extensão pg_trgm com Índice GIN (Generalized Inverted Index).\n"
        "   CREATE EXTENSION IF NOT EXISTS pg_trgm;\n"
        "   CREATE INDEX idx_pessoas_nome_gin ON public.pessoas USING gin (nome gin_trgm_ops);\n"
        "O índice GIN particiona as strings em trigramas (sequências de 3 caracteres), permitindo que buscas como 'ILIKE %silva%' sejam resolvidas em tempo logarítmico "
        "através de busca direta na lista invertida, evitando a varredura sequencial de milhares de linhas.\n"
        "• Para filtros categóricos de igualdade estrita: Mantém-se o B-Tree, mas ajusta-se a aplicação para usar operadores de igualdade direta (WHERE status = 'ativo' ou WHERE cidade = 'Manaus'), "
        "permitindo ao Query Planner usar Index Scan ou Bitmap Index Scan com eficiência máxima."
    )

    # Questão 3
    h3_3 = doc.add_heading("3.3 Como a escolha do BD (SQL vs NoSQL) impacta no meu sistema distribuído?", level=2)
    h3_3.runs[0].font.color.rgb = RGBColor(13, 148, 136)

    doc.add_paragraph(
        "A decisão entre um SGBD Relacional (SQL) como PostgreSQL e um SGBD Não-Relacional (NoSQL) como MongoDB, Cassandra ou Redis acarreta "
        "implicações profundas de arquitetura, consistência, disponibilidade e particionamento em Sistemas Distribuídos:"
    )

    doc.add_paragraph(
        "1. Garantias Transacionais: ACID vs. BASE\n"
        "• Banco Relacional (SQL - PostgreSQL): Prioriza garantias ACID estritas. Em um sistema com alto volume de escritas simultâneas como o testado, "
        "o PostgreSQL assegura que cada INSERT/UPDATE é atômico e imediatamente consistente para leituras subsequentes, isolando transações via MVCC. "
        "O custo disso é a serialização de locks e dependência de disco síncrono (WAL).\n"
        "• Banco Não-Relacional (NoSQL - ex: MongoDB / DynamoDB): Opera predominantemente sob o paradigma BASE (Basically Available, Soft-state, Eventual consistency). "
        "Permite escritas assíncronas em memória com confirmação rápida ao cliente, garantindo vazão de escritas muito superior à observada no PostgreSQL para a mesma carga."
    )

    doc.add_paragraph(
        "2. O Teorema CAP e Tolerância a Particionamento\n"
        "Segundo o Teorema CAP (Brewer), nenhum sistema distribuído pode garantir simultaneamente Consistência (C), Disponibilidade (A) e Tolerância a Particionamentos de Rede (P):\n"
        "• PostgreSQL Tradicional: É primordialmente um sistema CA (ou CP em clusters replicados com quorum síncrono). Sob partições de rede ou alta contenção, "
        "ele rejeita ou enfileira requisições para evitar escritas inconsistentes (split-brain), o que explica a elevação da taxa de erros HTTP quando o pool de conexões satura.\n"
        "• Sistemas NoSQL (AP - como Cassandra/DynamoDB): Priorizam Alta Disponibilidade e Tolerância a Partições. Sob estresse, o sistema aceita a escrita mesmo em nós isolados "
        "e propaga a atualização em segundo plano. Clientes podem ler temporariamente dados desatualizados (consistência eventual), mas o sistema não recusa conexões com erro 500."
    )

    doc.add_paragraph(
        "3. Modelo de Dados e Escalabilidade Horizontal (Sharding)\n"
        "• SQL: Estrutura rígida de tabelas e esquemas. A escalabilidade em escrita é tipicamente vertical (aumentar CPU, RAM e I/O da máquina primária). "
        "A divisão horizontal (sharding) é complexa e exige gerenciar chaves de partição e junções distribuídas.\n"
        "• NoSQL Baseado em Documentos: Estrutura flexível (JSON/BSON). O particionamento horizontal é nativo e automatizado, permitindo distribuir 100k ou 100M "
        "de documentos em dezenas de nós servidores com roteamento transparente, eliminando o gargalo de nós centralizados."
    )

    doc.add_paragraph(
        "4. Síntese Comparativa para a Aplicação do Trabalho:\n"
        "Para a aplicação CRUD de pessoas, o modelo SQL adotado é altamente recomendável caso haja necessidade de integridade relacional, consistência financeira "
        "ou auditoria cadastral. No entanto, o gargalo identificado neste experimento — onde o throughput travou em 106-110 req/s sob 1200 conexões — evidencia que, "
        "para sustentar cargas massivas de escala web, a arquitetura distribuída deveria adotar técnicas híbridas: manter o PostgreSQL como fonte da verdade transacional, "
        "acrescentando uma camada NoSQL em memória (Redis) para cache distribuído de leituras e um intermediador de filas (RabbitMQ/Kafka) para ingestão assíncrona de cadastros."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # 4. CONCLUSÕES E RECOMENDAÇÕES
    # -------------------------------------------------------------
    h4 = doc.add_heading("4. CONCLUSÕES E RECOMENDAÇÕES ARQUITETURAIS", level=1)
    h4.runs[0].font.color.rgb = RGBColor(30, 58, 138)

    doc.add_paragraph(
        "A partir da condução dos experimentos práticos e da fundamentação teórica, conclui-se que:\n"
        "1. Validação do Estresse Experimental: A submissão da arquitetura a 1200 conexões concorrentes cumpriu plenamente o propósito de saturar a infraestrutura, "
        "gerando latências elevadas e erros reais entre 3,92% e 14,25%, permitindo diagnosticar os verdadeiros gargalos de sistemas distribuídos.\n"
        "2. Impacto do Volume de Dados: A redução da base de 100k para 20k registros provou que o dimensionamento adequado da memória cache do SGBD e a redução de "
        "varreduras em disco reduzem significativamente a taxa de erros do sistema (ganho de até 45% de confiabilidade).\n"
        "3. Uso Racional de Índices: Índices B-Tree secundários sem casamento exato com as consultas geram custo desnecessário em escritas e pioram a estabilidade "
        "geral do sistema sob carga. Consultas com busca textual ampla devem utilizar índices especializados baseados em trigramas (GIN).\n"
        "4. Gargalo de Conexões: O servidor Flask padrão com psycopg2 síncrono aloca uma nova conexão por requisição ou bloqueia em pools pequenos. Recomenda-se para trabalhos futuros "
        "a introdução de um pooler de conexões dedicado (como o PgBouncer), servidores WSGI de alta concorrência (Gunicorn com gevent) e réplicas de leitura para distribuição de carga."
    )

    h5 = doc.add_heading("5. REFERÊNCIAS BIBLIOGRÁFICAS", level=1)
    h5.runs[0].font.color.rgb = RGBColor(30, 58, 138)

    doc.add_paragraph(
        "[1] TANENBAUM, Andrew S.; VAN STEEN, Maarten. Distributed Systems: Principles and Paradigms. 3rd ed. CreateSpace, 2017.\n"
        "[2] COULOURIS, George; DOLLIMORE, Jean; KINDBERG, Tim; BLAIR, Gordon. Distributed Systems: Concepts and Design. 5th ed. Addison-Wesley, 2011.\n"
        "[3] KLEPPMANN, Martin. Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable, and Maintainable Systems. O'Reilly Media, 2017.\n"
        "[4] POSTGRESQL GLOBAL DEVELOPMENT GROUP. PostgreSQL 16 Documentation: Indexes and Performance Optimization. Disponível em: https://www.postgresql.org/docs/16/.\n"
        "[5] APACHE SOFTWARE FOUNDATION. Apache JMeter User's Manual. Disponível em: https://jmeter.apache.org/usermanual/index.html."
    )

    doc.save("relatorio_sistemas_distribuidos.docx")
    print("Documento Word (.docx) criado com sucesso: relatorio_sistemas_distribuidos.docx")

if __name__ == "__main__":
    create_report()
