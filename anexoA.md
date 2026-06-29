# Anexo A

Este anexo apresenta, para cada análise, uma tabela com os parâmetros fixos do
experimento e uma tabela com os resultados produzidos pelo simulador. A numeração das
tabelas dá continuidade às Tabelas 1 e 2, apresentadas como exemplo no enunciado.

## A.1 Impacto do Tamanho da Cache

Tabela 3 – Parâmetros fixos da análise de tamanho da cache

| Parâmetro | Valor |
|---|---|
| Tamanho da linha | 128 bytes |
| Política de escrita | write-through |
| Algoritmo de substituição | LRU |
| Associatividade | 4 linhas |

Tabela 4 – Resultados da análise de tamanho da cache

| Número de linhas | Tamanho da cache (bytes) | Taxa de acerto (%) | Tempo médio (ns) | Leituras na MP | Escritas na MP |
|---|---|---|---|---|---|
| 8 | 1.024 | 51,0000 | 33,4000 | 25.088 | 6.144 |
| 16 | 2.048 | 54,0000 | 31,6000 | 23.552 | 6.144 |
| 32 | 4.096 | 65,9805 | 24,4117 | 17.418 | 6.144 |
| 64 | 8.192 | 92,9277 | 8,2434 | 3.621 | 6.144 |
| 128 | 16.384 | 94,9238 | 7,0457 | 2.599 | 6.144 |
| 256 | 32.768 | 99,9141 | 4,0516 | 44 | 6.144 |
| 512 | 65.536 | 99,9141 | 4,0516 | 44 | 6.144 |
| 1.024 | 131.072 | 99,9141 | 4,0516 | 44 | 6.144 |

## A.2 Impacto do Tamanho do Bloco

Tabela 5 – Parâmetros fixos da análise de tamanho do bloco

| Parâmetro | Valor |
|---|---|
| Tamanho total da cache | 8 Kbytes |
| Política de escrita | write-through |
| Algoritmo de substituição | LRU |
| Associatividade | 2 linhas |

Tabela 6 – Resultados da análise de tamanho do bloco

| Tamanho da linha (bytes) | Número de linhas | Taxa de acerto (%) | Tempo médio (ns) | Leituras na MP | Escritas na MP |
|---|---|---|---|---|---|
| 8 | 1.024 | 96,8223 | 5,9066 | 1.627 | 6.144 |
| 16 | 512 | 96,8242 | 5,9055 | 1.626 | 6.144 |
| 32 | 256 | 89,8398 | 10,0961 | 5.202 | 6.144 |
| 64 | 128 | 89,9023 | 10,0586 | 5.170 | 6.144 |
| 128 | 64 | 87,9375 | 11,2375 | 6.176 | 6.144 |
| 256 | 32 | 82,9668 | 14,2199 | 8.721 | 6.144 |
| 512 | 16 | 76,9883 | 17,8070 | 11.782 | 6.144 |
| 1.024 | 8 | 71,0000 | 21,4000 | 14.848 | 6.144 |
| 2.048 | 4 | 71,0000 | 21,4000 | 14.848 | 6.144 |
| 4.096 | 2 | 62,0000 | 26,8000 | 19.456 | 6.144 |

## A.3 Impacto da Associatividade

Tabela 7 – Parâmetros fixos da análise de associatividade

| Parâmetro | Valor |
|---|---|
| Tamanho da linha | 128 bytes |
| Tamanho total da cache | 8 Kbytes (64 linhas) |
| Política de escrita | write-back |
| Algoritmo de substituição | LRU |

Tabela 8 – Resultados da análise de associatividade

| Associatividade | Taxa de acerto (%) | Tempo médio (ns) | Leituras na MP | Escritas na MP |
|---|---|---|---|---|
| 1 | 74,9570 | 19,0258 | 12.822 | 2.046 |
| 2 | 87,9375 | 11,2375 | 6.176 | 1.023 |
| 4 | 92,9277 | 8,2434 | 3.621 | 511 |
| 8 | 89,9336 | 10,0398 | 5.154 | 1.022 |
| 16 | 99,9141 | 4,0516 | 44 | 0 |
| 32 | 99,9141 | 4,0516 | 44 | 0 |
| 64 | 99,9141 | 4,0516 | 44 | 0 |

## A.4 Impacto da Política de Substituição

Tabela 9 – Parâmetros fixos da análise de política de substituição

| Parâmetro | Valor |
|---|---|
| Tamanho da linha | 128 bytes |
| Política de escrita | write-through |
| Associatividade | 4 linhas |

Tabela 10 – Resultados da análise de política de substituição

| Número de linhas | Tamanho da cache (bytes) | Taxa de acerto LRU (%) | Taxa de acerto Aleatória (%) |
|---|---|---|---|
| 16 | 2.048 | 54,0000 | 54,8359 |
| 32 | 4.096 | 65,9805 | 72,6699 |
| 64 | 8.192 | 92,9277 | 94,7734 |
| 128 | 16.384 | 94,9238 | 97,9395 |
| 256 | 32.768 | 99,9141 | 99,9141 |
| 512 | 65.536 | 99,9141 | 99,9141 |
| 1.024 | 131.072 | 99,9141 | 99,9141 |

## A.5 Largura de Banda da Memória

Tabela 11 – Parâmetros fixos da análise de largura de banda

| Parâmetro | Valor |
|---|---|
| Algoritmo de substituição | LRU |
| Capacidades avaliadas | 8 Kbytes e 16 Kbytes |
| Tamanhos de linha avaliados | 64 e 128 bytes |
| Associatividades avaliadas | 2 e 4 linhas |

Tabela 12 – Tráfego de memória para a política write-through

| Cache (KB) | Linha (bytes) | Associatividade | Leituras na MP | Escritas na MP | Tráfego total |
|---|---|---|---|---|---|
| 8 | 64 | 2 | 5.170 | 6.144 | 11.314 |
| 8 | 64 | 4 | 3.126 | 6.144 | 9.270 |
| 8 | 128 | 2 | 6.176 | 6.144 | 12.320 |
| 8 | 128 | 4 | 3.621 | 6.144 | 9.765 |
| 16 | 64 | 2 | 2.615 | 6.144 | 8.759 |
| 16 | 64 | 4 | 2.615 | 6.144 | 8.759 |
| 16 | 128 | 2 | 3.621 | 6.144 | 9.765 |
| 16 | 128 | 4 | 2.599 | 6.144 | 8.743 |
| **Média** | | | **3.692,9** | **6.144,0** | **9.836,9** |

Tabela 13 – Tráfego de memória para a política write-back

| Cache (KB) | Linha (bytes) | Associatividade | Leituras na MP | Escritas na MP | Tráfego total |
|---|---|---|---|---|---|
| 8 | 64 | 2 | 5.170 | 1.023 | 6.193 |
| 8 | 64 | 4 | 3.126 | 511 | 3.637 |
| 8 | 128 | 2 | 6.176 | 1.023 | 7.199 |
| 8 | 128 | 4 | 3.621 | 511 | 4.132 |
| 16 | 64 | 2 | 2.615 | 1.023 | 3.638 |
| 16 | 64 | 4 | 2.615 | 511 | 3.126 |
| 16 | 128 | 2 | 3.621 | 1.023 | 4.644 |
| 16 | 128 | 4 | 2.599 | 511 | 3.110 |
| **Média** | | | **3.692,9** | **767,0** | **4.459,9** |
