"""
KernelLab — ponto de entrada.
Executa todas as etapas e imprime relatórios.
"""
import json
import os
import sys

# Garante que a pasta src está no path, mesmo rodando de fora
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from schedulers import executar_todos, detectar_starvation
from memory import comparar
from devices import demo_dispositivos
from metrics import analisar, medias


def carregar_dados(caminho="../data/processes.json"):
    if not os.path.exists(caminho):
        caminho = os.path.join(os.path.dirname(__file__), "..", "data", "processes.json")
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def imprimir_gantt(timeline, largura=50):
    if not timeline:
        return
    total = timeline[-1][2]
    print(f"  Gantt (0..{total}):")
    linha = ""
    for pid, ini, fim in timeline:
        bloco = f"[{pid}:{ini}-{fim}]"
        linha += bloco
    print("  " + linha)


def relatorio_escalonadores(processos, quantum):
    print("\n" + "=" * 70)
    print("ETAPA 1 — ESCALONAMENTO DA CPU")
    print("=" * 70)
    resultados = executar_todos(processos, quantum)
    for r in resultados:
        print(f"\n>>> {r['nome']}")
        imprimir_gantt(r["timeline"])
        print(f"  {'PID':<5}{'Espera':<10}{'Retorno':<10}{'Resposta':<10}")
        for pid, m in r["metricas"].items():
            print(f"  {pid:<5}{m['espera']:<10}{m['retorno']:<10}{m['resposta']:<10}")
        mm = medias(r["metricas"])
        print(f"  Médias: espera={mm['espera_media']:.2f} retorno={mm['retorno_medio']:.2f} resposta={mm['resposta_media']:.2f}")
        print(f"  Trocas de contexto: {r['trocas']}")
        starv = detectar_starvation(r["metricas"])
        print(f"  Risco de starvation: {starv if starv else 'nenhum'}")
    return resultados


def relatorio_comparativo(resultados):
    print("\n" + "=" * 70)
    print("ETAPA 2 — COMPARAÇÃO DOS ESCALONADORES")
    print("=" * 70)
    analise = analisar(resultados)
    print(f"  {'Algoritmo':<25}{'Esp.Média':<12}{'Ret.Média':<12}{'Resp.Média':<12}{'Trocas':<8}{'Jain':<6}")
    for a in analise:
        print(f"  {a['nome']:<25}{a['espera_media']:<12.2f}{a['retorno_medio']:<12.2f}{a['resposta_media']:<12.2f}{a['trocas']:<8}{a['jain']:<6.3f}")

    menor_espera = min(analise, key=lambda a: a["espera_media"])
    melhor_resposta = min(analise, key=lambda a: a["resposta_media"])
    mais_justo = max(analise, key=lambda a: a["jain"])
    print(f"\n  Menor tempo médio de espera : {menor_espera['nome']}")
    print(f"  Melhor tempo de resposta    : {melhor_resposta['nome']}")
    print(f"  Mais justo (Jain)           : {mais_justo['nome']}")
    print("  P4 (alarme crítico) tem prioridade 0 — prioridade e RR (com quantum curto) o tratam melhor.")
    print("  Maior risco de starvation   : SJF e Prioridade (processos longos/baixa prioridade).")
    return analise


def relatorio_memoria(sequencia=None, frames=4):
    if sequencia is None:
        sequencia = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5, 2, 1, 5, 3, 2]
    print("\n" + "=" * 70)
    print("ETAPA 3 — GERENCIAMENTO DE MEMÓRIA")
    print("=" * 70)
    print(f"  Sequência: {sequencia}")
    print(f"  Frames   : {frames}")
    resultados, melhor = comparar(sequencia, frames)
    for r in resultados:
        print(f"\n>>> {r['nome']}")
        for ref, estado, tipo in r["historico"]:
            print(f"  ref={ref:<3} frames={estado}  -> {tipo}")
        print(f"  Hits={r['hits']}  Faults={r['faults']}  Taxa={r['taxa_faults']:.2%}")
    print(f"\n  Melhor algoritmo: {melhor['nome']} ({melhor['faults']} faltas)")
    return resultados, melhor


def relatorio_dispositivos():
    print("\n" + "=" * 70)
    print("ETAPA 4 — CONTROLE DE DISPOSITIVOS")
    print("=" * 70)
    log = demo_dispositivos()
    for linha in log:
        print("  " + linha)


def main():
    dados = carregar_dados()
    processos = dados["processes"]
    quantum = dados.get("quantum", 3)

    resultados = relatorio_escalonadores(processos, quantum)
    relatorio_comparativo(resultados)
    relatorio_memoria()
    relatorio_dispositivos()

    print("\n" + "=" * 70)
    print("ETAPA 5 — RECOMENDAÇÃO FINAL")
    print("=" * 70)
    print("  Para a MedControl Systems, recomenda-se uma política HÍBRIDA:")
    print("  • Round Robin (q=3) para processos de monitoramento/telemetria")
    print("  • Prioridade preemptiva para alarmes críticos (P4)")
    print("  • Prioridade envelhecida (aging) para evitar starvation de P5/P6")
    print("  • LRU para memória (melhor desempenho empírico)")
    print("  • Mutex por dispositivo + matriz de permissões para segurança")


if __name__ == "__main__":
    main()