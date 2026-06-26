from simulacaoDeCache import (
    Config, calcular_campos, criar_cache, decompor, acessar, ler_acessos,
    WRITE_THROUGH, WRITE_BACK, SUBST_LRU, SUBST_RANDOM, WT_WRITE_ALLOCATE,
)
import matplotlib.pyplot as plt
import os
import random

import matplotlib
matplotlib.use("Agg")


ARQUIVO = "oficial.cache"
HIT_TIME = 4
TEMPO_MP = 60
SEED = 42

PASTA = "resultados"
os.makedirs(PASTA, exist_ok=True)


def rodar(politica, tam_linha, num_linhas, assoc, subst, arquivo=ARQUIVO):
    cfg = Config(politica, tam_linha, num_linhas, assoc,
                 HIT_TIME, subst, TEMPO_MP, arquivo)
    random.seed(SEED)
    nconj, boff, bidx = calcular_campos(cfg)
    cache = criar_cache(nconj)
    c = {"read_hits": 0, "read_misses": 0, "write_hits": 0,
         "write_misses": 0, "leituras_mp": 0, "escritas_mp": 0}
    for end, op in ler_acessos(arquivo):
        tag, idx = decompor(end, boff, bidx)
        acessar(cache, idx, tag, cfg, c, op)
    hits = c["read_hits"] + c["write_hits"]
    misses = c["read_misses"] + c["write_misses"]
    total = hits + misses
    taxa = hits / total
    tempo = HIT_TIME + (misses / total) * TEMPO_MP
    return {"taxa": taxa, "tempo": tempo,
            "lmp": c["leituras_mp"], "emp": c["escritas_mp"],
            "hits": hits, "misses": misses, "total": total}


def salvar_grafico(xs, ys, xlabel, titulo, nome, logx=True, series=None):
    plt.figure(figsize=(8, 5))
    if series is None:
        plt.plot(xs, ys, marker="o", linewidth=2)
    else:
        for rotulo, valores in series.items():
            plt.plot(xs, valores, marker="o", linewidth=2, label=rotulo)
        plt.legend()
    if logx:
        plt.xscale("log", base=2)
    plt.xlabel(xlabel)
    plt.ylabel("Taxa de acerto (%)")
    plt.title(titulo)
    plt.grid(True, alpha=0.3)
    caminho = os.path.join(PASTA, nome)
    plt.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [grafico] {caminho}")


def salvar_tabela(texto, nome):
    caminho = os.path.join(PASTA, nome)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"  [tabela]  {caminho}")
    print(texto)


def analise_tamanho_cache():
    print("\n[1] Impacto do Tamanho da Cache")
    blocos = [8, 16, 32, 64, 128, 256, 512, 1024]
    tam_bloco = 128
    xs_bytes, taxas = [], []
    linhas = ["NumBlocos;TamCacheBytes;TaxaAcerto;TempoMedio;LeiturasMP;EscritasMP"]
    for nb in blocos:
        r = rodar(WRITE_THROUGH, tam_bloco, nb, 4, SUBST_LRU)
        tam_bytes = nb * tam_bloco
        xs_bytes.append(tam_bytes)
        taxas.append(r["taxa"] * 100)
        linhas.append(
            f"{nb};{tam_bytes};{r['taxa']*100:.4f};{r['tempo']:.4f};{r['lmp']};{r['emp']}")
    salvar_grafico(xs_bytes, taxas, "Tamanho da cache (bytes)",
                   "Impacto do Tamanho da Cache", "fig1_tamanho_cache.png")
    salvar_tabela("\n".join(linhas) + "\n", "tab1_tamanho_cache.txt")


def analise_tamanho_bloco():
    print("\n[2] Impacto do Tamanho do Bloco")
    cache_bytes = 8 * 1024
    blocos = [8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
    xs, taxas = [], []
    linhas = ["TamBloco;NumLinhas;TaxaAcerto;TempoMedio;LeiturasMP;EscritasMP"]
    for tb in blocos:
        num_linhas = cache_bytes // tb
        if num_linhas < 2:
            continue
        r = rodar(WRITE_THROUGH, tb, num_linhas, 2, SUBST_LRU)
        xs.append(tb)
        taxas.append(r["taxa"] * 100)
        linhas.append(
            f"{tb};{num_linhas};{r['taxa']*100:.4f};{r['tempo']:.4f};{r['lmp']};{r['emp']}")
    salvar_grafico(xs, taxas, "Tamanho do bloco (bytes)",
                   "Impacto do Tamanho do Bloco", "fig2_tamanho_bloco.png")
    salvar_tabela("\n".join(linhas) + "\n", "tab2_tamanho_bloco.txt")


def analise_associatividade():
    print("\n[3] Impacto da Associatividade")
    cache_bytes = 8 * 1024
    tam_bloco = 128
    num_linhas = cache_bytes // tam_bloco
    assocs = [1, 2, 4, 8, 16, 32, 64]
    xs, taxas = [], []
    linhas = ["Associatividade;TaxaAcerto;TempoMedio;LeiturasMP;EscritasMP"]
    for a in assocs:
        r = rodar(WRITE_BACK, tam_bloco, num_linhas, a, SUBST_LRU)
        xs.append(a)
        taxas.append(r["taxa"] * 100)
        linhas.append(
            f"{a};{r['taxa']*100:.4f};{r['tempo']:.4f};{r['lmp']};{r['emp']}")
    salvar_grafico(xs, taxas, "Associatividade (linhas por conjunto)",
                   "Impacto da Associatividade", "fig3_associatividade.png")
    salvar_tabela("\n".join(linhas) + "\n", "tab3_associatividade.txt")


def analise_substituicao():
    print("\n[4] Impacto da Politica de Substituicao")
    blocos = [16, 32, 64, 128, 256, 512, 1024]
    tam_bloco = 128
    xs_bytes = [nb * tam_bloco for nb in blocos]
    taxas_lru, taxas_rnd = [], []
    linhas = ["NumBlocos;TamCacheBytes;Taxa_LRU;Taxa_Aleatoria"]
    for nb in blocos:
        rl = rodar(WRITE_THROUGH, tam_bloco, nb, 4, SUBST_LRU)
        rr = rodar(WRITE_THROUGH, tam_bloco, nb, 4, SUBST_RANDOM)
        taxas_lru.append(rl["taxa"] * 100)
        taxas_rnd.append(rr["taxa"] * 100)
        linhas.append(
            f"{nb};{nb*tam_bloco};{rl['taxa']*100:.4f};{rr['taxa']*100:.4f}")
    salvar_grafico(xs_bytes, None, "Tamanho da cache (bytes)",
                   "Impacto da Politica de Substituicao", "fig4_substituicao.png",
                   series={"LRU": taxas_lru, "Aleatoria": taxas_rnd})
    salvar_tabela("\n".join(linhas) + "\n", "tab4_substituicao.txt")


def analise_largura_banda():
    print("\nLargura de Banda da Memoria")
    caches = [8 * 1024, 16 * 1024]
    blocos = [64, 128]
    assocs = [2, 4]
    for politica, nome in [(WRITE_THROUGH, "write-through"), (WRITE_BACK, "write-back")]:
        linhas = [f"=== {nome} ===",
                  "CacheKB;Bloco;Assoc;LeiturasMP;EscritasMP;TotalMP"]
        soma_l, soma_e, n = 0, 0, 0
        for cb in caches:
            for tb in blocos:
                for a in assocs:
                    num_linhas = cb // tb
                    r = rodar(politica, tb, num_linhas, a, SUBST_LRU)
                    total_mp = r["lmp"] + r["emp"]
                    linhas.append(
                        f"{cb//1024};{tb};{a};{r['lmp']};{r['emp']};{total_mp}")
                    soma_l += r["lmp"]
                    soma_e += r["emp"]
                    n += 1
        linhas.append(
            f"MEDIA;;;{soma_l/n:.1f};{soma_e/n:.1f};{(soma_l+soma_e)/n:.1f}")
        salvar_tabela("\n".join(linhas) + "\n", f"tab5_largura_{nome}.txt")


if __name__ == "__main__":
    print(
        f"Arquivo: {ARQUIVO} | hit_time={HIT_TIME}ns | tempo_mp={TEMPO_MP}ns | seed={SEED}")
    print(f"WT_WRITE_ALLOCATE = {WT_WRITE_ALLOCATE}  "
          f"({'allocate' if WT_WRITE_ALLOCATE else 'non-allocate (fiel ao texto)'})")
    analise_tamanho_cache()
    analise_tamanho_bloco()
    analise_associatividade()
    analise_substituicao()
    analise_largura_banda()
    print("\nConcluido. Veja a pasta 'resultados/'.")
