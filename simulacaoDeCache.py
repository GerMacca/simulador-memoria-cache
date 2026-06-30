import sys
import random
from dataclasses import dataclass

WRITE_THROUGH = 0
WRITE_BACK = 1
WT_WRITE_ALLOCATE = True

SUBST_LRU = 0
SUBST_RANDOM = 1


@dataclass
class Config:
    politica: int
    tam_linha: int
    num_linhas: int
    assoc: int
    hit_time: int
    subst: int
    tempo_mp: int
    arquivo: str


def log2_pot(n: int) -> int:
    r = 0
    while n > 1:
        n >>= 1
        r += 1
    return r


def parse_args(argv) -> Config:
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
    with open(caminho, "r") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            partes = linha.split()
            endereco = int(partes[0], 16)
            operacao = partes[1]
            yield endereco, operacao


def calcular_campos(cfg: Config):
    bits_offset = log2_pot(cfg.tam_linha)
    num_conjuntos = cfg.num_linhas // cfg.assoc
    bits_indice = log2_pot(num_conjuntos)
    return num_conjuntos, bits_offset, bits_indice


def decompor(endereco: int, bits_offset: int, bits_indice: int):
    indice = (endereco >> bits_offset) & ((1 << bits_indice) - 1)
    tag = endereco >> (bits_offset + bits_indice)
    return tag, indice


def criar_cache(num_conjuntos: int):
    return [[] for _ in range(num_conjuntos)]


def acessar(cache, conjunto_idx, tag, cfg, contadores, operacao):
    conjunto = cache[conjunto_idx]
    eh_escrita = (operacao == "W")

    for linha in conjunto:
        if linha["tag"] == tag:
            conjunto.remove(linha)
            conjunto.append(linha)

            if eh_escrita:
                contadores["write_hits"] += 1
                if cfg.politica == WRITE_THROUGH:
                    contadores["escritas_mp"] += 1
                else:
                    linha["dirty"] = 1
            else:
                contadores["read_hits"] += 1
            return

    if eh_escrita:
        contadores["write_misses"] += 1
    else:
        contadores["read_misses"] += 1

    if eh_escrita and cfg.politica == WRITE_THROUGH:
        contadores["escritas_mp"] += 1
        if not WT_WRITE_ALLOCATE:
            return

    contadores["leituras_mp"] += 1

    nova = {"tag": tag, "dirty": 0}
    if eh_escrita and cfg.politica == WRITE_BACK:
        nova["dirty"] = 1

    if len(conjunto) >= cfg.assoc:
        vitima = escolher_vitima(conjunto, cfg)
        if vitima["dirty"] == 1:
            contadores["escritas_mp"] += 1
        conjunto.remove(vitima)

    conjunto.append(nova)


def escolher_vitima(conjunto, cfg):
    if cfg.subst == SUBST_LRU:
        return conjunto[0]
    else:
        return random.choice(conjunto)


def tempo_medio_acesso(contadores, cfg):
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


if __name__ == "__main__":
    main()
