# 1. Programa de Simulação

O simulador foi desenvolvido na linguagem Python e reproduz o comportamento de
uma memória cache associativa por conjunto com arquitetura configurável. Todos
os parâmetros exigidos, política de escrita, tamanho da linha, número de linhas,
associatividade, tempo de acerto, política de substituição e tempo de acesso à
memória principal, são fornecidos por meio de argumentos de linha de comando,
seguindo a ordem: `<politica> <tam_linha> <num_linhas> <assoc> <hit_time> <subst>
<tempo_mp> <arquivo>`. O programa lê um arquivo-texto de entrada contendo, em cada
linha, um endereço de 32 bits em hexadecimal seguido da operação (`R` para leitura
e `W` para escrita), e ao final produz um relatório com os parâmetros utilizados,
os totais de acessos, os totais de leituras e escritas na memória principal, a taxa
de acerto discriminada por leitura, escrita e global, e o tempo médio de acesso.

## 1.1 Estruturas de dados

A cache é representada como uma lista de conjuntos, em que cada conjunto é, por sua
vez, uma lista de linhas. O número de conjuntos é determinado pela razão entre o
número de linhas e a associatividade. Essa organização permite a indexação direta
do conjunto a partir do endereço, sem necessidade de varredura. Cada linha é
representada por um dicionário com dois campos: o Rótulo, que identifica o bloco de
memória armazenado, e o indicador de modificação (`dirty`), que assume o valor 1 quando
a linha foi modificada e ainda não foi escrita na memória principal, informação utilizada
exclusivamente pela política write-back.

A validade da linha é tratada de forma implícita pela ocupação da lista do conjunto:
um conjunto que ainda não atingiu sua associatividade possui menos elementos que o
limite, e as posições não preenchidas correspondem a linhas inválidas. Dessa forma,
as primeiras referências a um conjunto vazio caracterizam as faltas compulsórias,
sem a necessidade de um campo de validade explícito.

A política de substituição LRU (Least Recently Used) é implementada pela própria
ordenação da lista do conjunto, dispensando contadores ou marcas de tempo: a cada
acerto, a linha referenciada é removida de sua posição e reinserida ao final da
lista. Como consequência, o início da lista contém sempre a linha menos recentemente
utilizada e o final, a mais recente. Na ocorrência de uma substituição, a vítima é,
portanto, o primeiro elemento da lista.

## 1.2 Mapeamento do endereço

O mapeamento decompõe cada endereço de 32 bits em três campos: a Palavra,
o Conjunto e o Rótulo. O número de bits de cada campo é
calculado uma única vez no início da simulação, pois depende apenas da configuração.
O número de bits de Palavra corresponde ao logaritmo na base 2 do tamanho da
linha, e o número de bits de Conjunto corresponde ao logaritmo na base 2 do número de
conjuntos.

A extração dos campos é realizada por operações de deslocamento e mascaramento de
bits. O Conjunto é obtido descartando-se os bits de Palavra e
isolando-se os bits seguintes por meio de uma máscara, enquanto o Rótulo corresponde
aos bits restantes mais significativos. Como o simulador não armazena o conteúdo dos
dados, mas apenas a localização dos blocos, o campo de Palavra é descartado após
o cálculo. Essa formulação contempla naturalmente os casos extremos de mapeamento:
quando a associatividade é igual ao número de linhas, existe um único conjunto, o
campo de Conjunto ocupa zero bits e todos os endereços são mapeados para o mesmo
conjunto, caracterizando uma cache totalmente associativa.

## 1.3 Algoritmo de simulação

Para cada acesso, o simulador decompõe o endereço, identifica o conjunto de destino
e verifica a presença do Rótulo entre as linhas desse conjunto. Quando o Rótulo é
encontrado, registra-se um acerto e a linha é promovida ao final da lista, atualizando
a ordenação LRU. Quando não é encontrado, registra-se uma falta, cujo tratamento
depende da operação e da política de escrita configurada.

Em uma falta, quando há espaço disponível no conjunto, o novo bloco é simplesmente
inserido. Quando o conjunto está cheio, a linha vítima é selecionada conforme a
política de substituição vigente e removida; caso essa vítima esteja marcada como
modificada (dirty), seu conteúdo é primeiro escrito na memória principal, contabilizando
uma escrita adicional, operação conhecida como write-back.

O comportamento das escritas segue a política configurada. Na política write-through,
toda operação de escrita é propagada imediatamente à memória principal, mantendo-a
sempre sincronizada. Em uma falta de escrita, adotou-se a estratégia write-allocate,
em que o bloco correspondente é carregado para a cache antes da gravação, de modo a
reproduzir os resultados de referência fornecidos no enunciado. Na política write-back,
as escritas que resultam em acerto apenas marcam a linha como modificada, e as faltas de
escrita carregam o bloco para a cache (write-allocate), também marcando-o como modificado.
A memória principal só é atualizada quando uma linha modificada é posteriormente
substituída.

## 1.4 Política de substituição aleatória

A política de substituição aleatória seleciona a linha vítima de forma uniforme entre
as linhas do conjunto. Para garantir a reprodutibilidade dos experimentos, a semente do
gerador pseudoaleatório é fixada no início de cada simulação, de modo que execuções
sucessivas com os mesmos parâmetros produzam resultados idênticos.

## 1.5 Métricas de saída

A taxa de acerto é calculada separadamente para as operações de leitura e de escrita, e
também de forma global, indicando-se ao lado de cada taxa a quantidade absoluta de
acertos correspondente. O tempo médio de acesso é obtido pela fórmula do tempo médio de
acesso à memória, dada pela soma do tempo de acerto com o produto entre a taxa de falta
global e o tempo de acesso à memória principal. Todos os valores reais são apresentados
com quatro casas decimais.

## 1.6 Funções principais

O programa está organizado nas seguintes funções principais: a função de cálculo dos
campos do endereço, que determina o número de bits de Palavra e de Conjunto a partir
da configuração; a função de decomposição, que extrai o Conjunto e o Rótulo de um endereço;
a função de acesso, que concentra a lógica de acerto, falta, escrita e substituição; a
função de seleção da vítima, que isola a diferença entre as políticas LRU e aleatória;
e a função de leitura do arquivo de entrada, implementada como um gerador para processar
os endereços sem carregar todo o arquivo em memória.

O código-fonte completo e as instruções de execução estão disponíveis em:
https://github.com/GerMacca/simulador-memoria-cache
