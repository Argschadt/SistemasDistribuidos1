import csv
import io
import os
import sys
from pathlib import Path
import psycopg2

DB_CONFIG = {
    "host": os.getenv("PGHOST", "localhost"),
    "port": os.getenv("PGPORT", "5432"),
    "dbname": os.getenv("PGDATABASE", "postgres"),
    "user": os.getenv("PGUSER", "postgres"),
    "password": os.getenv("PGPASSWORD", "root"),
}

CSV_PATH = Path(__file__).resolve().parent / "dataset_pessoas_100k.csv"


def prepare_database(num_rows: int, with_indexes: bool):
    print(f"\n============================================================")
    print(f"  PREPARANDO BANCO: {num_rows} registros | Indices: {'SIM' if with_indexes else 'NAO'}")
    print(f"============================================================")

    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    with conn.cursor() as cur:
        # 1. Garante que a tabela existe
        cur.execute("""
            CREATE TABLE IF NOT EXISTS public.pessoas (
                id INTEGER PRIMARY KEY,
                nome VARCHAR(150) NOT NULL,
                email VARCHAR(200) NOT NULL,
                telefone VARCHAR(30),
                cidade VARCHAR(100),
                data_cadastro DATE,
                status VARCHAR(20)
            );
            CREATE SEQUENCE IF NOT EXISTS public.pessoas_id_seq OWNED BY public.pessoas.id;
            ALTER TABLE public.pessoas ALTER COLUMN id SET DEFAULT nextval('public.pessoas_id_seq');
        """)

        # 2. Remove indices secundarios antes de truncar/importar (muito mais rapido)
        print("-> Removendo indices secundarios existentes...")
        cur.execute("DROP INDEX IF EXISTS public.idx_pessoas_cidade;")
        cur.execute("DROP INDEX IF EXISTS public.idx_pessoas_data_cadastro;")
        cur.execute("DROP INDEX IF EXISTS public.idx_pessoas_status;")

        # 3. Limpa a tabela
        print("-> Limpando tabela public.pessoas (TRUNCATE)...")
        cur.execute("TRUNCATE TABLE public.pessoas RESTART IDENTITY;")

        # 4. Carrega exatamente num_rows linhas do CSV
        print(f"-> Importando {num_rows} registros de {CSV_PATH.name}...")
        buf = io.StringIO()
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            header = f.readline()
            buf.write(header)
            for i, line in enumerate(f):
                if i >= num_rows:
                    break
                buf.write(line)
        buf.seek(0)

        cur.copy_expert(
            """
            COPY public.pessoas (id, nome, email, telefone, cidade, data_cadastro, status)
            FROM STDIN WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8')
            """,
            buf,
        )

        # 5. Ajusta a sequence do ID para novos INSERTs do JMeter
        cur.execute("""
            SELECT setval(
                'public.pessoas_id_seq',
                COALESCE((SELECT MAX(id) FROM public.pessoas), 0) + 1,
                false
            );
        """)

        # 6. Cria indices secundarios se solicitado
        if with_indexes:
            print("-> Criando indices B-Tree (cidade, data_cadastro, status)...")
            cur.execute("CREATE INDEX idx_pessoas_cidade ON public.pessoas (cidade, data_cadastro DESC, id DESC);")
            cur.execute("CREATE INDEX idx_pessoas_data_cadastro ON public.pessoas (data_cadastro);")
            cur.execute("CREATE INDEX idx_pessoas_status ON public.pessoas (status);")

        # 7. Atualiza estatisticas do planejador do PostgreSQL
        print("-> Executando ANALYZE public.pessoas...")
        cur.execute("ANALYZE public.pessoas;")

        # 8. Confere contagem e plano de execucao
        cur.execute("SELECT COUNT(*) FROM public.pessoas;")
        total = cur.fetchone()[0]

        cur.execute("""
            EXPLAIN ANALYZE
            SELECT id, nome, email, telefone, cidade, data_cadastro, status
            FROM public.pessoas
            WHERE cidade = 'Manaus'
            ORDER BY data_cadastro DESC, id DESC
            LIMIT 100
        """)
        plan_lines = [r[0] for r in cur.fetchall()]

    conn.close()
    print(f"-> Concluido! Total de registros no banco: {total}")
    print("-> Plano de execucao da consulta por cidade:")
    for pl in plan_lines[:4]:
        print("   ", pl)
    print("============================================================\n")


if __name__ == "__main__":
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    if mode == "100k_com_indice":
        prepare_database(100000, True)
    elif mode == "100k_sem_indice":
        prepare_database(100000, False)
    elif mode == "20k_com_indice":
        prepare_database(20000, True)
    elif mode == "20k_sem_indice":
        prepare_database(20000, False)
    else:
        print("Escolha a configuracao do banco:")
        print("  1) 100k COM indice")
        print("  2) 100k SEM indice")
        print("  3) 20k  COM indice")
        print("  4) 20k  SEM indice")
        choice = input("Opcao (1-4): ").strip()
        mapping = {
            "1": (100000, True),
            "2": (100000, False),
            "3": (20000, True),
            "4": (20000, False),
        }
        if choice in mapping:
            prepare_database(*mapping[choice])
        else:
            print("Opcao invalida.")
            sys.exit(1)
