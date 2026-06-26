import sys
import random
from dataclasses import dataclass

# Política de escrita
WRITE_THROUGH = 0
WRITE_BACK = 1
WT_WRITE_ALLOCATE = False

# Política de substituição
SUBST_LRU = 0
SUBST_RANDOM = 1


@dataclass
class Config:
    """Agrupa toda a configuração da simulação.
    Em Delphi seria um record; aqui uso dataclass."""
    politica: int      # 0 = write-through, 1 = write-back
    tam_linha: int     # bytes por linha (potência de 2)
    num_linhas: int    # total de linhas (potência de 2)
    assoc: int         # linhas por conjunto (potência de 2)
    hit_time: int      # ns
    subst: int         # 0 = LRU, 1 = aleatória
    tempo_mp: int      # ns por acesso à memória principal
    arquivo: str


def log2_pot(n: int) -> int:
    """log2 de uma potência de 2.
    Conta quantas vezes dá pra dividir por 2 até chegar em 1.
    Ex.: log2_pot(128) = 7, porque 2**7 = 128.
    (Python já tem n.bit_length()-1, mas deixo explícito p/ o relatório.)"""
    r = 0
    while n > 1:
        n >>= 1   # desloca 1 bit pra direita = divide por 2
        r += 1
    return r


def parse_args(argv) -> Config:
    # argv inclui o nome do script em argv[0]. Esperamos 8 params + nome = 9.
    if len(argv) != 9:
        print(f"Uso: {argv[0]} <politica> <tam_linha> <num_linhas> "
              f"<assoc> <hit_time> <subst> <tempo_mp> <arquivo>",
              file=sys.stderr)
        sys.exit(1)

    subst_txt = argv[6].upper()
    subst = SUBST_LRU if subst_txt == "LRU" else SUBST_RANDOM

    return Config(
        politica=int(argv[1]),
        tam_linha=int(argv[2]),
        num_linhas=int(argv[3]),
        assoc=int(argv[4]),
        hit_time=int(argv[5]),
        subst=subst,
        tempo_mp=int(argv[7]),
        arquivo=argv[8],
    )


def ler_acessos(caminho: str):
    """Gera (endereco, operacao) para cada linha do arquivo.
    Usar um gerador evita carregar 51.200 linhas de uma vez na memória."""
    with open(caminho, "r") as f:
        for linha in f:
            linha = linha.strip()        # tira \r, \n e espaços das pontas
            if not linha:
                continue
            partes = linha.split()       # split() sem arg quebra em qualquer branco
            endereco = int(partes[0], 16)  # base 16 = hexadecimal
            operacao = partes[1]
            yield endereco, operacao


def calcular_campos(cfg: Config):
    """Calcula quantos bits cada campo do endereço ocupa.
    Isso depende só da config, então calcula UMA vez no início."""
    bits_offset = log2_pot(cfg.tam_linha)
    num_conjuntos = cfg.num_linhas // cfg.assoc   # // = divisão inteira
    bits_indice = log2_pot(num_conjuntos)
    return num_conjuntos, bits_offset, bits_indice


def decompor(endereco: int, bits_offset: int, bits_indice: int):
    """Quebra um endereço em (tag, indice).
    O offset é descartado: não simulamos o dado, só a localização."""
    indice = (endereco >> bits_offset) & ((1 << bits_indice) - 1)
    tag = endereco >> (bits_offset + bits_indice)
    return tag, indice


def criar_cache(num_conjuntos: int):
    """Cria a cache vazia: uma lista por conjunto, cada uma começa vazia."""
    return [[] for _ in range(num_conjuntos)]


def acessar(cache, conjunto_idx, tag, cfg, contadores, operacao):
    conjunto = cache[conjunto_idx]
    eh_escrita = (operacao == "W")

    # --- procura a tag no conjunto ---
    for linha in conjunto:
        if linha["tag"] == tag:
            # ===== HIT =====
            conjunto.remove(linha)
            conjunto.append(linha)        # atualiza LRU (move-to-end)

            if eh_escrita:
                contadores["write_hits"] += 1
                if cfg.politica == WRITE_THROUGH:
                    contadores["escritas_mp"] += 1   # escreve direto na MP
                else:  # WRITE_BACK
                    linha["dirty"] = 1               # só marca sujo
            else:
                contadores["read_hits"] += 1
            return

    # ===== MISS =====
    if eh_escrita:
        contadores["write_misses"] += 1
    else:
        contadores["read_misses"] += 1

    # --- write-through + write miss ---
    if eh_escrita and cfg.politica == WRITE_THROUGH:
        contadores["escritas_mp"] += 1
        if not WT_WRITE_ALLOCATE:
            # non-allocate (padrao, fiel ao texto): nao carrega bloco
            return
        # se WT_WRITE_ALLOCATE = True, segue para carregar o bloco abaixo

    # --- a partir daqui: vai CARREGAR um bloco na cache ---
    # (read miss em qualquer politica, OU write miss em write-back,
    #  OU write miss em write-through quando WT_WRITE_ALLOCATE = True)
    contadores["leituras_mp"] += 1   # busca o bloco na MP

    nova = {"tag": tag, "dirty": 0}
    if eh_escrita and cfg.politica == WRITE_BACK:   # so write-back marca sujo
        nova["dirty"] = 1

    if len(conjunto) >= cfg.assoc:
        # conjunto cheio: escolhe vitima e a remove
        vitima = escolher_vitima(conjunto, cfg)
        if vitima["dirty"] == 1:                 # write-back de linha suja
            contadores["escritas_mp"] += 1
        conjunto.remove(vitima)

    conjunto.append(nova)


def escolher_vitima(conjunto, cfg):
    if cfg.subst == SUBST_LRU:
        return conjunto[0]               # início = menos recentemente usado
    else:  # aleatória
        return random.choice(conjunto)


def tempo_medio_acesso(contadores, cfg):
    """AMAT = hit_time + miss_rate_global * tempo_mp"""
    hits = contadores["read_hits"] + contadores["write_hits"]
    misses = contadores["read_misses"] + contadores["write_misses"]
    total = hits + misses
    miss_rate = misses / total
    return cfg.hit_time + miss_rate * cfg.tempo_mp


def imprimir_saida(cfg, contadores):
    rh = contadores["read_hits"]
    rm = contadores["read_misses"]
    wh = contadores["write_hits"]
    wm = contadores["write_misses"]

    total_leituras = rh + rm
    total_escritas = wh + wm
    total_acessos = total_leituras + total_escritas

    hits = rh + wh
    misses = rm + wm

    # taxas (evita divisão por zero caso não haja leituras ou escritas)
    taxa_leitura = rh / total_leituras if total_leituras else 0.0
    taxa_escrita = wh / total_escritas if total_escritas else 0.0
    taxa_global = hits / total_acessos if total_acessos else 0.0

    politica_txt = "write-through" if cfg.politica == WRITE_THROUGH else "write-back"
    subst_txt = "LRU" if cfg.subst == SUBST_LRU else "Aleatoria"

    print("=" * 50)
    print("PARAMETROS DE ENTRADA")
    print("=" * 50)
    print(f"Politica de escrita......: {politica_txt}")
    print(f"Tamanho da linha (bytes).: {cfg.tam_linha}")
    print(f"Numero de linhas.........: {cfg.num_linhas}")
    print(f"Associatividade..........: {cfg.assoc}")
    print(f"Hit time (ns)............: {cfg.hit_time}")
    print(f"Politica de substituicao.: {subst_txt}")
    print(f"Tempo da MP (ns).........: {cfg.tempo_mp}")
    print(f"Arquivo..................: {cfg.arquivo}")

    print("=" * 50)
    print("ENDERECOS DO ARQUIVO")
    print("=" * 50)
    print(f"Leituras (R).............: {total_leituras}")
    print(f"Escritas (W).............: {total_escritas}")
    print(f"Total....................: {total_acessos}")

    print("=" * 50)
    print("ACESSOS A MEMORIA PRINCIPAL")
    print("=" * 50)
    print(f"Leituras na MP...........: {contadores['leituras_mp']}")
    print(f"Escritas na MP...........: {contadores['escritas_mp']}")

    print("=" * 50)
    print("TAXA DE ACERTO (HIT RATE)")
    print("=" * 50)
    print(f"Leitura..: {taxa_leitura:.4f}  ({rh} hits / {total_leituras})")
    print(f"Escrita..: {taxa_escrita:.4f}  ({wh} hits / {total_escritas})")
    print(f"Global...: {taxa_global:.4f}  ({hits} hits / {total_acessos})")

    print("=" * 50)
    print(
        f"TEMPO MEDIO DE ACESSO....: {tempo_medio_acesso(contadores, cfg):.4f} ns")
    print("=" * 50)


def main():
    cfg = parse_args(sys.argv)
    random.seed(42)

    num_conjuntos, bits_offset, bits_indice = calcular_campos(cfg)
    cache = criar_cache(num_conjuntos)
    contadores = {
        "read_hits": 0, "read_misses": 0,
        "write_hits": 0, "write_misses": 0,
        "leituras_mp": 0, "escritas_mp": 0,
    }

    for endereco, operacao in ler_acessos(cfg.arquivo):
        tag, indice = decompor(endereco, bits_offset, bits_indice)
        acessar(cache, indice, tag, cfg, contadores, operacao)

    imprimir_saida(cfg, contadores)


def main():
    cfg = parse_args(sys.argv)
    random.seed(42)

    num_conjuntos, bits_offset, bits_indice = calcular_campos(cfg)
    cache = criar_cache(num_conjuntos)
    contadores = {
        "read_hits": 0, "read_misses": 0,
        "write_hits": 0, "write_misses": 0,
        "leituras_mp": 0, "escritas_mp": 0,
    }

    for endereco, operacao in ler_acessos(cfg.arquivo):
        tag, indice = decompor(endereco, bits_offset, bits_indice)
        acessar(cache, indice, tag, cfg, contadores, operacao)

    imprimir_saida(cfg, contadores)


if __name__ == "__main__":
    main()
