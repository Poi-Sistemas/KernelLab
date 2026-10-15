# KernelLab — Simulador de Gerenciamento de Recursos

## Problema e objetivo
A MedControl Systems enfrenta atrasos em alarmes, disputa por CPU, faltas de página
e concorrência em dispositivos. Este simulador reproduz as decisões de um SO
(escalonamento, memória e dispositivos) para comparar políticas.

## Arquitetura
Entrada (JSON) → Escalonamento → Métricas → Memória → Dispositivos → Comparação.

## Algoritmos implementados
- **CPU:** FCFS, SJF, Round Robin (q configurável), Prioridade (menor = maior).
- **Memória:** FIFO, LRU, Optimal.
- **Dispositivos:** matriz de acesso + mutex + fila.

## Instalação
```bash
pip install -r requirements.txt