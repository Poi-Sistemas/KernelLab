"""
Módulo de escalonamento de CPU.
Implementa FCFS, SJF, Round Robin e Prioridade.
Todos recebem a lista de processos no formato:
{"pid": str, "chegada": int, "burst": int, "prioridade": int}
e retornam um dicionário com timeline, métricas e trocas de contexto.
"""
from collections import deque
import copy


def _metricas(timeline, processos):
    """Calcula espera, retorno e resposta a partir da timeline [(pid, inicio, fim)]."""
    resultado = {}
    for p in processos:
        pid = p["pid"]
        execs = [t for t in timeline if t[0] == pid]
        if not execs:
            continue
        primeiro_inicio = execs[0][1]
        ultimo_fim = execs[-1][2]
        espera = primeiro_inicio - p["chegada"]
        retorno = ultimo_fim - p["chegada"]
        resposta = primeiro_inicio - p["chegada"]
        resultado[pid] = {
            "espera": espera,
            "retorno": retorno,
            "resposta": resposta,
            "burst": p["burst"],
            "prioridade": p["prioridade"],
        }
    return resultado


def _trocas_contexto(timeline):
    """Cada mudança de PID na timeline conta como troca de contexto."""
    if not timeline:
        return 0
    trocas = 0
    for i in range(1, len(timeline)):
        if timeline[i][0] != timeline[i - 1][0]:
            trocas += 1
    return trocas


def fcfs(processos):
    procs = sorted(processos, key=lambda p: p["chegada"])
    tempo = 0
    timeline = []
    for p in procs:
        if tempo < p["chegada"]:
            tempo = p["chegada"]
        inicio = tempo
        tempo += p["burst"]
        timeline.append((p["pid"], inicio, tempo))
    return {
        "nome": "FCFS",
        "timeline": timeline,
        "metricas": _metricas(timeline, processos),
        "trocas": _trocas_contexto(timeline),
    }


def sjf(processos):
    """Shortest Job First não-preemptivo."""
    procs = copy.deepcopy(processos)
    tempo = 0
    timeline = []
    prontos = []
    restantes = sorted(procs, key=lambda p: p["chegada"])
    while restantes or prontos:
        while restantes and restantes[0]["chegada"] <= tempo:
            prontos.append(restantes.pop(0))
        if not prontos:
            tempo = restantes[0]["chegada"]
            continue
        prontos.sort(key=lambda p: p["burst"])
        p = prontos.pop(0)
        inicio = tempo
        tempo += p["burst"]
        timeline.append((p["pid"], inicio, tempo))
    return {
        "nome": "SJF",
        "timeline": timeline,
        "metricas": _metricas(timeline, processos),
        "trocas": _trocas_contexto(timeline),
    }


def round_robin(processos, quantum=3):
    procs = {p["pid"]: dict(p) for p in processos}
    tempo = 0
    timeline = []
    fila = deque()
    chegadas = sorted(processos, key=lambda p: p["chegada"])
    idx = 0
    restante = {pid: p["burst"] for pid, p in procs.items()}

    # primeiro processo chega em t=0
    while idx < len(chegadas) and chegadas[idx]["chegada"] <= tempo:
        fila.append(chegadas[idx]["pid"])
        idx += 1

    while fila:
        pid = fila.popleft()
        p = procs[pid]
        exec_time = min(quantum, restante[pid])
        inicio = tempo
        tempo += exec_time
        restante[pid] -= exec_time
        timeline.append((pid, inicio, tempo))

        # adiciona processos que chegaram durante a execução
        while idx < len(chegadas) and chegadas[idx]["chegada"] <= tempo:
            fila.append(chegadas[idx]["pid"])
            idx += 1

        if restante[pid] > 0:
            fila.append(pid)

    return {
        "nome": f"Round Robin (q={quantum})",
        "timeline": timeline,
        "metricas": _metricas(timeline, processos),
        "trocas": _trocas_contexto(timeline),
    }


def prioridade(processos):
    """Escalonamento por prioridade não-preemptivo (menor número = maior prioridade)."""
    procs = copy.deepcopy(processos)
    tempo = 0
    timeline = []
    prontos = []
    restantes = sorted(procs, key=lambda p: p["chegada"])
    while restantes or prontos:
        while restantes and restantes[0]["chegada"] <= tempo:
            prontos.append(restantes.pop(0))
        if not prontos:
            tempo = restantes[0]["chegada"]
            continue
        prontos.sort(key=lambda p: (p["prioridade"], p["chegada"]))
        p = prontos.pop(0)
        inicio = tempo
        tempo += p["burst"]
        timeline.append((p["pid"], inicio, tempo))
    return {
        "nome": "Prioridade",
        "timeline": timeline,
        "metricas": _metricas(timeline, processos),
        "trocas": _trocas_contexto(timeline),
    }


def detectar_starvation(metricas, limiar=20):
    """Processos com tempo de espera acima do limiar são suspeitos de starvation."""
    return [pid for pid, m in metricas.items() if m["espera"] > limiar]


def executar_todos(processos, quantum=3):
    return [
        fcfs(processos),
        sjf(processos),
        round_robin(processos, quantum),
        prioridade(processos),
    ]