"""
Cálculo de médias, justiça (índice de Jain) e comparações.
"""


def medias(metricas):
    if not metricas:
        return {}
    n = len(metricas)
    return {
        "espera_media": sum(m["espera"] for m in metricas.values()) / n,
        "retorno_medio": sum(m["retorno"] for m in metricas.values()) / n,
        "resposta_media": sum(m["resposta"] for m in metricas.values()) / n,
    }


def indice_jain(valores):
    """Índice de Jain: 1.0 = totalmente justo, próximo de 1/n = injusto."""
    n = len(valores)
    if n == 0 or sum(v * v for v in valores) == 0:
        return 0
    return (sum(valores) ** 2) / (n * sum(v * v for v in valores))


def analisar(resultados):
    """Recebe lista de resultados de escalonadores e devolve análise consolidada."""
    analise = []
    for r in resultados:
        m = medias(r["metricas"])
        m["nome"] = r["nome"]
        m["trocas"] = r["trocas"]
        m["jain"] = indice_jain([x["espera"] for x in r["metricas"].values()])
        analise.append(m)
    return analise