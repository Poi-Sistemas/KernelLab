"""
Controle de acesso a dispositivos compartilhados com mutex simulado.
"""
import threading
import time


# Matriz de controle: processo -> dispositivo -> permissões
MATRIZ_ACESSO = {
    "P1": {"rede":   {"ler": True,  "gravar": True,  "executar": False, "usar": True,  "exclusivo": False}},
    "P2": {"rede":   {"ler": True,  "gravar": True,  "executar": False, "usar": True,  "exclusivo": False}},
    "P3": {"disco":  {"ler": True,  "gravar": True,  "executar": False, "usar": True,  "exclusivo": True}},
    "P4": {"audio":  {"ler": False, "gravar": True,  "executar": True,  "usar": True,  "exclusivo": True},
           "rede":   {"ler": True,  "gravar": True,  "executar": False, "usar": True,  "exclusivo": False}},
    "P5": {"disco":  {"ler": True,  "gravar": True,  "executar": False, "usar": True,  "exclusivo": True}},
    "P6": {"disco":  {"ler": True,  "gravar": True,  "executar": False, "usar": True,  "exclusivo": False},
           "rede":   {"ler": True,  "gravar": True,  "executar": False, "usar": True,  "exclusivo": False}},
}


class Dispositivo:
    """Representa um dispositivo com mutex e fila de espera."""
    def __init__(self, nome):
        self.nome = nome
        self.mutex = threading.Lock()
        self.fila = []
        self.log = []

    def solicitar(self, pid, permissao="usar"):
        permitido = MATRIZ_ACESSO.get(pid, {}).get(self.nome, {}).get(permissao, False)
        if not permitido:
            self.log.append(f"[NEGADO] {pid} tentou {permissao} em {self.nome}")
            return False
        self.fila.append(pid)
        self.log.append(f"[FILA] {pid} solicitou {permissao} em {self.nome}")
        return True

    def acessar(self, pid, permissao="usar", duracao=0.05):
        if not self.solicitar(pid, permissao):
            return False
        with self.mutex:
            self.log.append(f"[ACESSO] {pid} usando {self.nome}")
            time.sleep(duracao)
            self.log.append(f"[LIBERADO] {pid} liberou {self.nome}")
        self.fila.remove(pid)
        return True


def demo_dispositivos():
    disco = Dispositivo("disco")
    rede = Dispositivo("rede")
    audio = Dispositivo("audio")

    # P4 pede áudio (exclusivo, permitido)
    threads = [
        threading.Thread(target=disco.acessar, args=("P3", "gravar")),
        threading.Thread(target=disco.acessar, args=("P5", "gravar")),
        threading.Thread(target=disco.acessar, args=("P6", "ler")),
        threading.Thread(target=rede.acessar,  args=("P1", "gravar")),
        threading.Thread(target=rede.acessar,  args=("P2", "gravar")),
        threading.Thread(target=audio.acessar, args=("P4", "executar")),
        threading.Thread(target=audio.acessar, args=("P1", "executar")),  # NEGADO
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return disco.log + rede.log + audio.log