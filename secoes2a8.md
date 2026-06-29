# 2. Impacto do Tamanho da Cache

Neste experimento, avaliou-se o efeito do número de linhas da cache sobre a taxa de
acerto. Mantiveram-se fixos o tamanho da linha em 128 bytes, a política de escrita
write-through, a política de substituição LRU e a associatividade de 4 linhas por
conjunto. Variou-se o número de linhas em potências de 2, partindo de 8 linhas, até
que a taxa de acerto se tornasse insensível ao tamanho da cache. A Figura 1 apresenta
a taxa de acerto em função do tamanho total da cache em bytes.

A curva obtida possui um formato de crescimento acentuado seguido de saturação. Para
caches pequenas, a taxa de acerto é baixa (51,00% para 1.024 bytes), cresce rapidamente
na região intermediária (92,93% para 8.192 bytes) e estabiliza próxima de 100% a partir
de 32.768 bytes (99,91%), permanecendo constante para tamanhos maiores. Esse comportamento
decorre da relação entre a capacidade da cache e o conjunto de trabalho do programa. Em
caches pequenas, predominam as faltas por capacidade, pois a cache não comporta
simultaneamente todos os blocos referenciados de forma frequente, o que provoca a expulsão
de blocos que ainda seriam reutilizados [1]. À medida que a capacidade aumenta, um número
maior de blocos do conjunto de trabalho passa a residir simultaneamente na cache, reduzindo
as faltas por capacidade e elevando a taxa de acerto [1]. A partir do ponto em que a cache
já comporta praticamente todo o conjunto de trabalho, restam apenas as faltas compulsórias,
que correspondem à primeira referência a cada bloco e não podem ser evitadas pelo aumento
da capacidade [2]. Por esse motivo, a curva satura e o aumento adicional da cache não produz
ganho de desempenho.

# 3. Impacto do Tamanho do Bloco

Neste experimento, avaliou-se o efeito do tamanho da linha sobre a taxa de acerto.
Mantiveram-se fixos o tamanho total da cache em 8 Kbytes, a política de escrita
write-through, a política de substituição LRU e a associatividade de 2 linhas por
conjunto. Variou-se o tamanho da linha de 8 a 4.096 bytes, em potências de 2. A Figura 2
apresenta a taxa de acerto em função do tamanho da linha.

A curva obtida é predominantemente decrescente, com a maior taxa de acerto observada para
as menores linhas (96,82% para 8 e 16 bytes) e a menor taxa para a maior linha (62,00%
para 4.096 bytes). Esse resultado evidencia o compromisso associado ao tamanho da linha.
O aumento do tamanho da linha tende a beneficiar a localidade espacial, uma vez que, a
cada falta, um volume maior de dados vizinhos é trazido para a cache, antecipando acessos
futuros a posições próximas [1]. Entretanto, para um tamanho total de cache fixo, o aumento
da linha reduz proporcionalmente o número de linhas disponíveis, diminuindo a quantidade de
blocos distintos que podem residir simultaneamente na cache e elevando as faltas por
conflito e por capacidade [1]. No trace utilizado, o segundo efeito predomina sobre o
primeiro, indicando que a localidade espacial presente nos acessos é limitada e não
compensa a redução do número de linhas. Dessa forma, o tamanho de linha ótimo observado é
de 16 bytes, valor que apresenta a maior taxa de acerto entre todas as configurações
avaliadas, com diferença marginal em relação a 8 bytes.

# 4. Impacto da Associatividade

Neste experimento, avaliou-se o efeito da associatividade sobre a taxa de acerto.
Mantiveram-se fixos o tamanho da linha em 128 bytes, a política de escrita write-back, a
política de substituição LRU e o tamanho total da cache em 8 Kbytes, o que corresponde a
64 linhas. Variou-se a associatividade entre 1 e 64, em potências de 2. A Figura 3 apresenta
a taxa de acerto em função da associatividade.

A curva obtida é predominantemente crescente, porém não estritamente monotônica. A taxa de
acerto cresce de 74,96% no mapeamento direto (associatividade 1) para 92,93% na
associatividade 4, apresenta uma leve queda na associatividade 8 (89,93%) e, em seguida,
eleva-se de forma acentuada na associatividade 16 (99,91%), permanecendo constante para
valores superiores. O comportamento geral crescente decorre da redução das faltas por
conflito: em configurações com baixa associatividade, diversos blocos que disputam o mesmo
conjunto são repetidamente expulsos, ainda que existam linhas livres em outros conjuntos,
fenômeno que a associatividade mais alta atenua ao oferecer mais alternativas de alocação
por conjunto [1]. A não monotonicidade observada na associatividade 8 deve-se à interação
entre o padrão de acesso do trace e a quantidade de conjuntos resultante: para um número
fixo de linhas, o aumento da associatividade reduz o número de conjuntos, o que altera o
mapeamento dos blocos e pode, em casos específicos, agravar pontualmente os conflitos antes
de eliminá-los [1]. A partir da associatividade 16, o número de conjuntos torna-se
suficientemente reduzido para que os blocos concorrentes do trace coexistam no mesmo
conjunto, praticamente eliminando as faltas por conflito.

# 5. Impacto da Política de Substituição

Neste experimento, comparou-se o desempenho das políticas de substituição LRU e aleatória.
Mantiveram-se fixos o tamanho da linha em 128 bytes, a política de escrita write-through e
a associatividade de 4 linhas por conjunto. Variou-se o número de linhas da cache em
potências de 2, a partir de 16 linhas, para ambas as políticas. A Figura 4 apresenta a taxa
de acerto em função do tamanho da cache, com uma curva para cada política.

As duas curvas apresentam o mesmo formato geral de crescimento e saturação observado no
experimento de tamanho da cache. Entretanto, nas caches de menor capacidade, a política
aleatória apresentou taxa de acerto superior à da LRU (54,84% contra 54,00% para 16 linhas,
e 72,67% contra 65,98% para 32 linhas), com as curvas convergindo para o mesmo valor à
medida que a cache cresce e as faltas passam a ser predominantemente compulsórias. Esse
resultado, ainda que contraintuitivo, é coerente com a literatura: a política LRU baseia-se
na hipótese de localidade temporal, segundo a qual o bloco menos recentemente utilizado é o
candidato mais adequado à substituição [1]. Quando o padrão de acesso contraria essa
hipótese, como em laços que percorrem ciclicamente um conjunto de blocos ligeiramente maior
que a associatividade, a LRU pode expulsar sistematicamente justamente o bloco que será
referenciado em seguida, degradando seu desempenho [2]. A política aleatória, por não seguir
um padrão determinístico, não é suscetível a esse comportamento adverso específico e, neste
trace, preservou com mais frequência os blocos reutilizados nas caches pequenas. Com o
aumento da capacidade, a influência da política de substituição diminui, pois há espaço
suficiente para acomodar o conjunto de trabalho independentemente da escolha da vítima.

# 6. Largura de Banda da Memória

Neste experimento, mediu-se o tráfego total gerado entre a cache e a memória principal para
as políticas de escrita write-through e write-back. Avaliaram-se caches de 8 Kbytes e 16
Kbytes, linhas de 64 e 128 bytes e associatividades de 2 e 4 linhas por conjunto, com
política de substituição LRU. As Tabelas 12 e 13 do Anexo A apresentam, para cada política, o
número de leituras e escritas na memória principal e o tráfego total, além da média dos
valores.

Os resultados indicam que a política write-back gera tráfego total substancialmente menor
que a política write-through. A média de tráfego total foi de 9.836,9 acessos para a política
write-through e de 4.459,9 acessos para a política write-back, o que representa uma redução
superior a 50%. O número médio de leituras na memória principal foi idêntico para ambas as
políticas (3.692,9), uma vez que o tratamento das faltas de leitura independe da política de
escrita. A diferença concentra-se nas escritas na memória principal: na política
write-through, toda operação de escrita é propagada imediatamente à memória principal,
resultando em um número constante de 6.144 escritas, igual ao total de operações de escrita
do trace [1]. Na política write-back, por outro lado, as escritas são acumuladas na cache e
apenas as linhas modificadas geram escrita na memória principal no momento de sua
substituição, reduzindo a média para 767 escritas [1]. Essa redução é acentuada pela
característica do trace, no qual um número reduzido de blocos distintos concentra a maior
parte das operações de escrita, sendo repetidamente modificado enquanto reside na cache.
Conclui-se, portanto, que a política write-back possui o menor tráfego de memória, por evitar
a propagação imediata de cada escrita à memória principal [1].

# 7. Avaliação Global

A partir do conjunto de experimentos realizados, é possível avaliar comparativamente as
configurações simuladas. Considerando exclusivamente a taxa de acerto, as configurações com
capacidade igual ou superior a 32 Kbytes e associatividade de 4 linhas, bem como a
configuração de 8 Kbytes com associatividade 16, alcançaram taxa de acerto de 99,91%,
correspondente à eliminação das faltas por capacidade e por conflito, restando apenas as
faltas compulsórias. Ponderando o desempenho em relação ao custo de implementação, a
configuração de 8 Kbytes com associatividade 16 destaca-se por atingir essa taxa máxima com
um quarto da capacidade exigida pela alternativa de associatividade 4, ainda que ao custo de
maior complexidade de hardware decorrente da busca associativa [1]. Quanto à política de
escrita, a write-back mostra-se preferível sob o critério de tráfego de memória, conforme
demonstrado na Seção 6. Dessa forma, o melhor projeto entre os simulados consiste em uma cache
de 8 Kbytes, associatividade 16, linha de 128 bytes e política write-back, que combina taxa de
acerto máxima com tráfego de memória reduzido.

Quanto à possibilidade de simular as demais formas de mapeamento, o simulador desenvolvido as
contempla integralmente, pois o mapeamento associativo por conjunto generaliza os demais [1].
O mapeamento direto corresponde ao caso particular em que a associatividade é igual a 1, isto
é, cada conjunto possui uma única linha, de modo que cada bloco possui uma posição fixa na
cache. O mapeamento totalmente associativo corresponde ao caso em que a associatividade é
igual ao número de linhas, resultando em um único conjunto no qual qualquer bloco pode ocupar
qualquer linha. Ambos os casos foram, inclusive, exercitados nos experimentos, uma vez que a
associatividade 1 integra a análise de associatividade e o caso totalmente associativo é
alcançado quando a associatividade iguala o número de linhas.

A parte mais difícil do processo de desenvolvimento consistiu na implementação correta da
lógica de escrita, em particular na distinção entre os comportamentos das políticas
write-through e write-back nas situações de acerto e de falta, e no tratamento da escrita de
linhas modificadas (dirty) no momento da substituição. A correta contabilização das leituras e
escritas na memória principal, base para a análise de largura de banda, exigiu atenção
especial para que cada situação fosse tratada de acordo com a política configurada.

# 8. Bibliografia

[1] STALLINGS, William. Arquitetura e organização de computadores. 10. ed. São Paulo:
Pearson, 2017.

[2] TANENBAUM, Andrew S.; AUSTIN, Todd. Organização estruturada de computadores. 6. ed.
São Paulo: Pearson, 2013.

[3] MONTEIRO, Mário Antonio. Introdução à organização de computadores. 5. ed. Rio de
Janeiro: LTC, 2007.

[4] DELGADO, José. Arquitetura de computadores. 5. ed. Rio de Janeiro: LTC, 2017.
