# Simulador de Memória Cache

Simulador de uma memória cache associativa por conjunto com arquitetura
configurável, desenvolvido para a disciplina de Arquitetura de Computadores.
Permite configurar política de escrita, tamanho da linha, número de linhas,
associatividade, tempo de acerto, política de substituição e tempo de acesso
à memória principal, produzindo estatísticas de desempenho a partir de um
arquivo de trace de endereços.

## Requisitos

- Python 3.8 ou superior
- matplotlib (apenas para o script de experimentos): `pip install matplotlib`

## Arquivos

| Arquivo | Descrição |
|---|---|
| `simulacaoDeCache.py` | Simulador principal (executável por linha de comando) |
| `experimentos.py` | Automação que roda todas as análises e gera gráficos e tabelas |
| `oficial.cache` | Trace de endereços com 51.200 entradas (simulações) |
| `teste.cache` | Trace reduzido com 100 entradas (testes) |

## Como executar o simulador

```bash
python simulacaoDeCache.py <politica> <tam_linha> <num_linhas> <assoc> <hit_time> <subst> <tempo_mp> <arquivo>
```

### Parâmetros

| Posição | Parâmetro | Valores |
|---|---|---|
| 1 | Política de escrita | `0` = write-through, `1` = write-back |
| 2 | Tamanho da linha (bytes) | potência de 2 |
| 3 | Número de linhas | potência de 2 |
| 4 | Associatividade | potência de 2 (1 até o número de linhas) |
| 5 | Hit time (ns) | inteiro |
| 6 | Política de substituição | `LRU` ou `RANDOM` |
| 7 | Tempo da memória principal (ns) | inteiro |
| 8 | Arquivo de trace | caminho do arquivo |

### Exemplo

```bash
python simulacaoDeCache.py 0 128 16 4 4 LRU 60 oficial.cache
```

## Como gerar os experimentos

```bash
python experimentos.py
```

Os gráficos (`.png`) e as tabelas (`.txt`) são gerados na pasta `resultados/`.

## Observação sobre a política write-through

O enunciado apresenta uma ambiguidade na política write-through: o texto a descreve
como write-non-allocate, mas as tabelas-exemplo só são reproduzidas com write-allocate.
Adotou-se a estratégia write-allocate, que reproduz os valores de referência do
enunciado. A constante `WT_WRITE_ALLOCATE`, no início do arquivo `simulacaoDeCache.py`,
permite alternar entre os dois comportamentos.
