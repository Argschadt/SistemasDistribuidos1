import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


TOTAL_PESSOAS = 100_000
OUTPUT_FILE = Path("dataset_pessoas_100k.csv")

CIDADES = [
    "São Paulo",
    "Rio de Janeiro",
    "Belo Horizonte",
    "Curitiba",
    "Porto Alegre",
    "Salvador",
    "Recife",
    "Fortaleza",
    "Brasília",
    "Campinas",
    "Manaus",
    "Belém",
    "Goiânia",
    "Florianópolis",
    "Natal",
]

NOMES = [
    "Ana", "Bruno", "Carlos", "Daniela", "Eduardo", "Fernanda", "Gabriel", "Helena",
    "Igor", "Juliana", "Lucas", "Mariana", "Nicolas", "Olivia", "Pedro", "Quezia",
    "Rafael", "Sabrina", "Thiago", "Vitoria", "Wesley", "Ximena", "Yuri", "Zilda",
    "Beatriz", "Caio", "Diana", "Elias", "Fabiana", "Gustavo", "Heloisa", "Isabela",
    "João", "Karina", "Leonardo", "Matheus", "Naiara", "Otávio", "Patricia", "Ruan",
    "Sofia", "Tales", "Ulisses", "Valentina", "William", "Yasmin", "Arthur", "Camila",
]

SOBRENOMES = [
    "Silva", "Souza", "Oliveira", "Pereira", "Costa", "Santos", "Rodrigues", "Almeida",
    "Ferreira", "Carvalho", "Gomes", "Mendes", "Nascimento", "Araujo", "Lima", "Pinto",
    "Martins", "Ribeiro", "Teixeira", "Barbosa", "Cardoso", "Vieira", "Moreira", "Rocha",
    "Monteiro", "Campos", "Andrade", "Correia", "Moura", "Castro", "Freitas", "Nunes",
    "Sales", "Dias", "Melo", "Leite", "Farias", "Cavalcanti", "Borges", "Santana",
]

STATUS_POSSIVEIS = ["ativo", "inativo", "pendente", "bloqueado"]


def gerar_nome_aleatorio():
    nome = random.choice(NOMES)
    sobrenome = random.choice(SOBRENOMES)
    return f"{nome} {sobrenome}"


def gerar_email(nome_completo):
    base = nome_completo.lower().replace(" ", ".")
    dominio = random.choice(["gmail.com", "yahoo.com.br", "outlook.com", "icloud.com"])
    sufixo = random.randint(10, 999)
    return f"{base}.{sufixo}@{dominio}"


def gerar_telefone():
    ddd = random.randint(11, 99)
    parte1 = random.randint(9000, 9999)
    parte2 = random.randint(1000, 9999)
    return f"({ddd}) {parte1}-{parte2}"


def gerar_data_cadastro():
    data_inicio = datetime(2020, 1, 1)
    data_fim = datetime(2025, 12, 31)
    diferenca = (data_fim - data_inicio).days
    dias = random.randint(0, diferenca)
    return (data_inicio + timedelta(days=dias)).strftime("%Y-%m-%d")


def gerar_status():
    return random.choices(STATUS_POSSIVEIS, weights=[60, 20, 15, 5], k=1)[0]


def gerar_pessoas(total=TOTAL_PESSOAS, caminho_saida=OUTPUT_FILE):
    with caminho_saida.open("w", newline="", encoding="utf-8") as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        escritor.writerow(["id", "nome", "email", "telefone", "cidade", "data_cadastro", "status"])

        for id_pessoa in range(1, total + 1):
            nome = gerar_nome_aleatorio()
            cidade = random.choice(CIDADES)
            registro = [
                id_pessoa,
                nome,
                gerar_email(nome),
                gerar_telefone(),
                cidade,
                gerar_data_cadastro(),
                gerar_status(),
            ]
            escritor.writerow(registro)

    print(f"Arquivo gerado com sucesso: {caminho_saida.resolve()}")
    print(f"Total de registros: {total}")
    print("Colunas: id, nome, email, telefone, cidade, data_cadastro, status")


if __name__ == "__main__":
    gerar_pessoas()
