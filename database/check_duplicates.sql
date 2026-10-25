-- Script para verificar duplicidades na tabela pessoas
-- Execute após importar o dataset no PostgreSQL

-- 1) Nomes repetidos
SELECT 'nome' AS campo, nome AS valor, COUNT(*) AS quantidade
FROM pessoas
GROUP BY nome
HAVING COUNT(*) > 1
ORDER BY quantidade DESC, valor;

-- 2) E-mails repetidos
SELECT 'email' AS campo, email AS valor, COUNT(*) AS quantidade
FROM pessoas
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY quantidade DESC, valor;

-- 3) Telefones repetidos
SELECT 'telefone' AS campo, telefone AS valor, COUNT(*) AS quantidade
FROM pessoas
GROUP BY telefone
HAVING COUNT(*) > 1
ORDER BY quantidade DESC, valor;

-- 4) Cidades repetidas
SELECT 'cidade' AS campo, cidade AS valor, COUNT(*) AS quantidade
FROM pessoas
GROUP BY cidade
HAVING COUNT(*) > 1
ORDER BY quantidade DESC, valor;

-- 5) Status repetidos
SELECT 'status' AS campo, status AS valor, COUNT(*) AS quantidade
FROM pessoas
GROUP BY status
HAVING COUNT(*) > 1
ORDER BY quantidade DESC, valor;

-- 6) Datas de cadastro repetidas
SELECT 'data_cadastro' AS campo, data_cadastro::text AS valor, COUNT(*) AS quantidade
FROM pessoas
GROUP BY data_cadastro
HAVING COUNT(*) > 1
ORDER BY quantidade DESC, valor;

-- 7) Linhas completamente iguais
SELECT nome, email, telefone, cidade, data_cadastro, status, COUNT(*) AS quantidade
FROM pessoas
GROUP BY nome, email, telefone, cidade, data_cadastro, status
HAVING COUNT(*) > 1
ORDER BY quantidade DESC;

-- 8) Resumo geral
SELECT
    (SELECT COUNT(*) FROM pessoas) AS total_registros,
    (SELECT COUNT(DISTINCT nome) FROM pessoas) AS nomes_distintos,
    (SELECT COUNT(DISTINCT email) FROM pessoas) AS emails_distintos,
    (SELECT COUNT(DISTINCT telefone) FROM pessoas) AS telefones_distintos,
    (SELECT COUNT(DISTINCT cidade) FROM pessoas) AS cidades_distintas,
    (SELECT COUNT(DISTINCT status) FROM pessoas) AS status_distintos,
    (SELECT COUNT(DISTINCT data_cadastro) FROM pessoas) AS datas_distintas;
