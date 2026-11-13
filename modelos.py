from dataclasses import dataclass, field
from abc import ABC, abstractmethod

@dataclass(frozen=True)
class Paciente:
    nome: str
    cartao_sus: str

class Atendimento(ABC):
    def __init__(self, paciente: Paciente) -> None:
        self.paciente = paciente
    
    @property
    def paciente(self) -> Paciente:
        return self.paciente

    @abstractmethod
    def duracao_minutos(self) -> int:
        pass

    def __str__(self) -> str:
        tipo_nome = type(self).__name__
        return f"{tipo_nome} - Paciente: {self.paciente.nome}, Duração: {self.duracao_minutos()} minutos"

class Consulta(Atendimento):
    def __init__ (self, paciente: Paciente, especialidade: str, retorno: bool = False) -> None:
        super().__init__(paciente)
        self.especialidade = especialidade
        self.retorno = retorno

    def duracao_minutos(self) -> int:
        return 15 if self.retorno else 30

class Vacinacao(Atendimento):
    def __init__ (self, paciente: Paciente, vacina: str, doses: int = 1) -> None:
        super().__init__(paciente)
        self.vacina = vacina
        self.doses = doses

    def duracao_minutos(self) -> int:
        return self.doses * 10

class Exame(Atendimento):
    def __init__ (self, paciente: Paciente, tipo: str, jejum: bool = False) -> None:
        super().__init__(paciente)
        self.tipo = tipo
        self.jejum = jejum

    def duracao_minutos(self) -> int:
        return 15 if self.jejum else 30

@dataclass
class Agenda:
    limite_minutos: int = 240
    _atendimentos: list[Atendimento] = field(default_factory=list, init=False, repr=False)

    @property
    def atendimentos(self) -> tuple[Atendimento, ...]:
        return tuple(self._atendimentos)
    
    @property
    def minutos_ocupados(self) -> int:
        return sum(atendimento.duracao_minutos() for at in self._atendimentos)

    def agendar(self, atendimento: Atendimento) -> None:
        for at in self._atendimentos:
            if at.paciente == atendimento.paciente:
                raise ValueError(f"Paciente {at.paciente.nome} já possui atendimento agendado.")

        duracao_nova = atendimento.duracao_minutos()
        if self.minutos_ocupados + duracao_nova > self.limite_minutos:
            minutos_restantes = self.limite_minutos - self.minutos_ocupados
            raise ValueError(f"Horário indisponível. São necessários{duracao_nova} minutos, mas restam apenas {max(0, minutos_restantes)} minutos.")

        self.atendimentos.append(atendimento)

