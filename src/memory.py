"""
Algoritmos de substituição de páginas: FIFO, LRU e Optimal.
"""


def fifo(sequencia, frames):
    memoria = []
    hits = 0
    faults = 0
    historico = []
    for ref in sequencia:
        if ref in memoria:
            hits += 1
        else:
            faults += 1
            if len(memoria) < frames:
                memoria.append(ref)
            else:
                memoria.pop(0)
                memoria.append(ref)
        historico.append((ref, list(memoria), "HIT" if ref in memoria and historico and historico[-1][1] != memoria else "FAULT"))
    # corrige rótulo
    historico = []
    memoria = []
    hits = faults = 0
    for ref in sequencia:
        if ref in memoria:
            hits += 1
            historico.append((ref, list(memoria), "HIT"))
        else:
            faults += 1
            if len(memoria) < frames:
                memoria.append(ref)
            else:
                memoria.pop(0)
                memoria.append(ref)
            historico.append((ref, list(memoria), "FAULT"))
    return {"nome": "FIFO", "historico": historico, "hits": hits, "faults": faults}


def lru(sequencia, frames):
    memoria = []
    hits = faults = 0
    historico = []
    for ref in sequencia:
        if ref in memoria:
            hits += 1
            memoria.remove(ref)
            memoria.append(ref)
            historico.append((ref, list(memoria), "HIT"))
        else:
            faults += 1
            if len(memoria) < frames:
                memoria.append(ref)
            else:
                memoria.pop(0)
                memoria.append(ref)
            historico.append((ref, list(memoria), "FAULT"))
    return {"nome": "LRU", "historico": historico, "hits": hits, "faults": faults}


def optimal(sequencia, frames):
    memoria = []
    hits = faults = 0
    historico = []
    for i, ref in enumerate(sequencia):
        if ref in memoria:
            hits += 1
            historico.append((ref, list(memoria), "HIT"))
        else:
            faults += 1
            if len(memoria) < frames:
                memoria.append(ref)
            else:
                # escolhe página usada mais tarde no futuro
                futuro = sequencia[i + 1:]
                vitima = None
                mais_distante = -1
                for pag in memoria:
                    if pag not in futuro:
                        vitima = pag
                        break
                    dist = futuro.index(pag)
                    if dist > mais_distante:
                        mais_distante = dist
                        vitima = pag
                memoria.remove(vitima)
                memoria.append(ref)
            historico.append((ref, list(memoria), "FAULT"))
    return {"nome": "Optimal", "historico": historico, "hits": hits, "faults": faults}


def comparar(sequencia, frames):
    resultados = [fifo(sequencia, frames), lru(sequencia, frames), optimal(sequencia, frames)]
    for r in resultados:
        r["taxa_faults"] = r["faults"] / len(sequencia)
    melhor = min(resultados, key=lambda r: r["faults"])
    return resultados, melhor