from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass(frozen=True)
class Paciente:
    nome: str
    cartao_sus: str

@abstractmethod
class Atendimento(Paciente):
    def __str__(duracao_minutos()) -> int:
        self.tipo = tipo
        self.nome = nome
        self.duracao_minutos() = 0


class Consulta(Funcionario):
    def __init__ (especialidade: str, retorno: bool) -> str:
        self.tipo = tipo
        self.nome = nome
        self.duracao_minutos() =  

class Vacinacao(Funcionario):
    def __init__ ():
        self.tipo = tipo
        self.nome = nome
        self.duracao_minutos() = 

class Exame(Funcionario):
    def tipo(self) -> str:
        self.tipo = tipo
        self.nome = nome
        self.duracao_minutos() = 

@property
class Agenda:
    def tempo(self) -> int:
        self.limite_minutos: int = 240,
        return

ana = Paciente("Ana Souza", "700000000000001")
leo = Paciente("Leo Lima", "700000000000002")
rui = Paciente("Rui Alves", "700000000000003")

# Agenda, Atendimento, Consulta, Exame, Paciente, Vacinacao

