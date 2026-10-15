import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from schedulers import fcfs, sjf, round_robin, prioridade
from memory import fifo, lru, optimal


PROCS = [
    {"pid": "P1", "chegada": 0, "burst": 8, "prioridade": 1},
    {"pid": "P2", "chegada": 1, "burst": 4, "prioridade": 2},
    {"pid": "P3", "chegada": 2, "burst": 9, "prioridade": 4},
    {"pid": "P4", "chegada": 3, "burst": 2, "prioridade": 0},
    {"pid": "P5", "chegada": 5, "burst": 12, "prioridade": 5},
    {"pid": "P6", "chegada": 6, "burst": 6, "prioridade": 3},
]


def test_fcfs_ordem():
    r = fcfs(PROCS)
    assert [t[0] for t in r["timeline"]] == ["P1", "P2", "P3", "P4", "P5", "P6"]


def test_sjf_primeiro_p1():
    r = sjf(PROCS)
    assert r["timeline"][0][0] == "P1"


def test_rr_quantum():
    r = round_robin(PROCS, 3)
    for pid, ini, fim in r["timeline"]:
        assert fim - ini <= 3


def test_prioridade_p4_primeiro_apos_chegada():
    r = prioridade(PROCS)
    pids = [t[0] for t in r["timeline"]]
    assert pids[0] == "P1"
    assert pids[1] == "P4"  # prioridade 0


def test_memoria_fifo():
    seq = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5, 2, 1, 5, 3, 2]
    r = fifo(seq, 4)
    assert r["hits"] + r["faults"] == len(seq)


def test_memoria_lru_e_optimal():
    seq = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5, 2, 1, 5, 3, 2]
    lru_r = lru(seq, 4)
    opt_r = optimal(seq, 4)
    assert opt_r["faults"] <= lru_r["faults"]


if __name__ == "__main__":
    import unittest
    # Converte os testes pytest em algo que o unittest roda
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Importa manualmente todas as funções test_* deste módulo
    import sys
    modulo_atual = sys.modules[__name__]
    for nome in dir(modulo_atual):
        if nome.startswith("test_"):
            suite.addTest(unittest.FunctionTestCase(getattr(modulo_atual, nome)))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)