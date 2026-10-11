-- Script para criar o banco e importar o dataset de pessoas
-- Execute no psql depois de criar o banco PostgreSQL

CREATE TABLE IF NOT EXISTS public.pessoas (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(200) NOT NULL,
    telefone VARCHAR(30),
    cidade VARCHAR(100),
    data_cadastro DATE,
    status VARCHAR(20)
);

CREATE SEQUENCE IF NOT EXISTS public.pessoas_id_seq
    OWNED BY public.pessoas.id;

ALTER TABLE public.pessoas
    ALTER COLUMN id SET DEFAULT nextval('public.pessoas_id_seq');

-- Importa o CSV gerado em Python
-- Ajuste o caminho conforme seu ambiente local
\copy public.pessoas (id, nome, email, telefone, cidade, data_cadastro, status)
FROM 'C:/Users/WINDOWS 10 PRO/Documents/SistemasDistribuidos1/dataset_pessoas_100k.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');

-- Garante que novos cadastros usem ids acima do maior id importado
SELECT setval(
    'public.pessoas_id_seq',
    COALESCE((SELECT MAX(id) FROM public.pessoas), 0) + 1,
    false
);

-- Índices úteis para consultas e testes de desempenho
CREATE INDEX IF NOT EXISTS idx_pessoas_cidade
    ON public.pessoas (cidade);

CREATE INDEX IF NOT EXISTS idx_pessoas_data_cadastro
    ON public.pessoas (data_cadastro);

CREATE INDEX IF NOT EXISTS idx_pessoas_status
    ON public.pessoas (status);

-- Verificações rápidas
SELECT COUNT(*) AS total_pessoas FROM public.pessoas;
SELECT cidade, COUNT(*) AS quantidade
FROM public.pessoas
GROUP BY cidade
ORDER BY quantidade DESC
LIMIT 10;
