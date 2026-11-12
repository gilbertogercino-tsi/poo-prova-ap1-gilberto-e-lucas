"""
    - Validador da segunda avaliação de POO em TSI 2026.2

"""
import dataclasses
import inspect

# Alterar os imports conforme a estrutura de módulos do projeto dos alunos
from excecoes import AgendaError, HorarioIndisponivelError, PacienteJaAgendadoError
from modelos import Agenda, Atendimento, Consulta, Exame, Paciente, Vacinacao


def secao(titulo: str) -> None:
    print(f"\n== {titulo}")


def verificar(descricao: str, condicao: bool) -> None:
    assert condicao, f"FALHOU: {descricao}"
    print(f"  OK  {descricao}")


def levanta(excecao: type[BaseException], chamada) -> BaseException:
    """Executa chamada() e devolve a exceção esperada; falha se não ocorrer."""
    try:
        chamada()
    except excecao as erro:
        return erro
    raise AssertionError(f"não levantou {excecao.__name__}")


ana = Paciente("Ana Souza", "700000000000001")
leo = Paciente("Leo Lima", "700000000000002")
rui = Paciente("Rui Alves", "700000000000003")



# ---------------------------------------------------------------- item a ----------------------------------------------------------------
secao("a) Paciente: dataclass imutável")
verificar("pacientes com os mesmos dados são iguais",
          ana == Paciente("Ana Souza", "700000000000001"))
verificar("nome diferente => diferentes", ana != Paciente("Outra", "700000000000001"))
verificar("cartão diferente (homônimo) => diferentes",
          ana != Paciente("Ana Souza", "700000000000999"))
verificar("é hashable (usável em set/dict)",
          len({ana, Paciente("Ana Souza", "700000000000001")}) == 1)
verificar("alterar nome gera FrozenInstanceError",
          levanta(dataclasses.FrozenInstanceError, lambda: setattr(ana, "nome", "X")) is not None)
verificar("alterar cartão gera FrozenInstanceError",
          levanta(dataclasses.FrozenInstanceError, lambda: setattr(ana, "cartao_sus", "1")) is not None)
verificar("repr mostra os campos (gerado pela dataclass)", "Ana Souza" in repr(ana))



# ---------------------------------------------------------------- item b ----------------------------------------------------------------
secao("b) Atendimento abstrata e subclasses: todas as durações")
verificar("Atendimento é abstrata", inspect.isabstract(Atendimento))
verificar("Atendimento(ana) gera TypeError", levanta(TypeError, lambda: Atendimento(ana)) is not None)


class Incompleta(Atendimento):          # esqueceu duracao_minutos
    pass


verificar("subclasse sem duracao_minutos também não instancia",
          levanta(TypeError, lambda: Incompleta(ana)) is not None)


duracoes = [
    (Consulta(ana, "Clínica Geral"), 30),
    (Consulta(ana, "Clínica Geral", retorno=True), 15),
    (Exame(ana, "Glicemia"), 20),
    (Exame(ana, "Glicemia", jejum=True), 30),
    (Vacinacao(ana, "Influenza"), 10),
    (Vacinacao(ana, "Influenza", doses=1), 10),
    (Vacinacao(ana, "Influenza", doses=2), 20),
    (Vacinacao(ana, "Influenza", doses=5), 50),
]
for obj, esperado in duracoes:
    verificar(f"{type(obj).__name__} => {esperado} min", obj.duracao_minutos() == esperado)


verificar("subclasses são Atendimento (herança)",
          all(isinstance(o, Atendimento) for o, _ in duracoes))
verificar("valores padrão: retorno=False, jejum=False, doses=1",
          not Consulta(ana, "X").retorno and not Exame(ana, "X").jejum
          and Vacinacao(ana, "X").doses == 1)
verificar("atributos específicos guardados",
          Consulta(ana, "Pediatria").especialidade == "Pediatria"
          and Exame(ana, "Glicemia").tipo == "Glicemia"
          and Vacinacao(ana, "Influenza").vacina == "Influenza")
verificar("paciente exposto pela property", Consulta(ana, "X").paciente == ana)
verificar("paciente é somente leitura",
          levanta(AttributeError, lambda: setattr(Consulta(ana, "X"), "paciente", leo)) is not None)
for obj in (Consulta(ana, "X"), Exame(ana, "X"), Vacinacao(ana, "X")):
    texto = str(obj)
    verificar(f"__str__ de {type(obj).__name__}: tipo + paciente + duração",
              type(obj).__name__ in texto and "Ana Souza" in texto
              and str(obj.duracao_minutos()) in texto)



# ---------------------------------------------------------------- item c ----------------------------------------------------------------
secao("c) Hierarquia de exceções")
verificar("AgendaError herda de Exception", issubclass(AgendaError, Exception))
verificar("HorarioIndisponivelError herda de AgendaError",
          issubclass(HorarioIndisponivelError, AgendaError))
verificar("PacienteJaAgendadoError herda de AgendaError",
          issubclass(PacienteJaAgendadoError, AgendaError))
verificar("as duas específicas são distintas entre si",
          not issubclass(HorarioIndisponivelError, PacienteJaAgendadoError)
          and not issubclass(PacienteJaAgendadoError, HorarioIndisponivelError))
verificar("não herdam de ValueError", not issubclass(AgendaError, ValueError))



# ---------------------------------------------------------------- item d ----------------------------------------------------------------
secao("d) Agenda: estado inicial e limite padrão")
vazia = Agenda()
verificar("agenda nova: 0 minutos ocupados", vazia.minutos_ocupados == 0)
verificar("agenda nova: nenhum atendimento", vazia.atendimentos == ())
cheia = Agenda()                                  # limite padrão = 240
for numero in range(8):                           # 8 x 30 = 240 exatos
    cheia.agendar(Consulta(Paciente(f"P{numero}", str(numero)), "CG"))
verificar("limite padrão 240: 8 consultas (240 min) cabem", cheia.minutos_ocupados == 240)
verificar("limite padrão 240: a 9ª não cabe",
          levanta(HorarioIndisponivelError,
                  lambda: cheia.agendar(Consulta(Paciente("P9", "9"), "CG"))) is not None)

secao("d) Agenda: fronteira do limite")
limite = Agenda(limite_minutos=60)
limite.agendar(Consulta(ana, "CG"))
limite.agendar(Exame(leo, "G", jejum=True))
verificar("soma exatamente igual ao limite é ACEITA (60 de 60)", limite.minutos_ocupados == 60)
verificar("1 minuto a mais é REJEITADO (61 > 60)",
          levanta(HorarioIndisponivelError,
                  lambda: limite.agendar(Vacinacao(rui, "I"))) is not None)
quase = Agenda(limite_minutos=59)
quase.agendar(Consulta(ana, "CG"))                # 30
verificar("limite 59: 30 + 30 = 60 estoura por 1 minuto",
          levanta(HorarioIndisponivelError,
                  lambda: quase.agendar(Exame(leo, "G", jejum=True))) is not None)
verificar("limite 59: 30 + 20 = 50 cabe", quase.agendar(Exame(leo, "G")) is None)
zero = Agenda(limite_minutos=0)
verificar("limite 0: nada cabe (qualquer atendimento tem duração > 0)",
          levanta(HorarioIndisponivelError, lambda: zero.agendar(Vacinacao(ana, "I"))) is not None)
verificar("limite 0: agenda continua vazia", zero.atendimentos == ())

secao("d) Agenda: paciente repetido")
agenda = Agenda(limite_minutos=120)
agenda.agendar(Consulta(ana, "CG"))
verificar("mesmo objeto Paciente, tipo de atendimento diferente => rejeitado",
          levanta(PacienteJaAgendadoError, lambda: agenda.agendar(Exame(ana, "G"))) is not None)
verificar("OUTRO objeto Paciente com os mesmos dados => rejeitado (igualdade)",
          levanta(PacienteJaAgendadoError,
                  lambda: agenda.agendar(Consulta(Paciente("Ana Souza", "700000000000001"), "P"))) is not None)
verificar("mesmo nome, cartão diferente (homônimo) => ACEITO",
          agenda.agendar(Consulta(Paciente("Ana Souza", "700000000000777"), "CG")) is None)
verificar("paciente repetido é rejeitado mesmo havendo tempo livre",
          agenda.minutos_ocupados == 60 < 120)

secao("d) Agenda: precedência quando as duas regras são violadas")
dupla = Agenda(limite_minutos=30)
dupla.agendar(Consulta(ana, "CG"))               # agenda cheia E ana repetida
verificar("Ana de novo com agenda cheia => PacienteJaAgendadoError (1ª regra)",
          levanta(PacienteJaAgendadoError, lambda: dupla.agendar(Consulta(ana, "P"))) is not None)

secao("d) Agenda: mensagens informativas")
erro_paciente = levanta(PacienteJaAgendadoError, lambda: agenda.agendar(Exame(ana, "G")))
verificar("mensagem do paciente repetido cita o nome", "Ana Souza" in str(erro_paciente))
erro_horario = levanta(HorarioIndisponivelError, lambda: limite.agendar(Vacinacao(rui, "I")))
verificar("mensagem de horário cita minutos necessários e restantes",
          "10" in str(erro_horario) and "0" in str(erro_horario))
verificar("mensagens não são vazias", str(erro_paciente) != "" and str(erro_horario) != "")

secao("d) Agenda: falha não altera o estado")
antes_min, antes_lista = limite.minutos_ocupados, limite.atendimentos
levanta(HorarioIndisponivelError, lambda: limite.agendar(Vacinacao(rui, "I")))
levanta(PacienteJaAgendadoError, lambda: limite.agendar(Consulta(ana, "P")))
verificar("minutos iguais após falhas", limite.minutos_ocupados == antes_min)
verificar("lista igual após falhas", limite.atendimentos == antes_lista)

secao("d) Agenda: encapsulamento")
verificar("minutos_ocupados é somente leitura",
          levanta(AttributeError, lambda: setattr(limite, "minutos_ocupados", 0)) is not None)
verificar("atendimentos é somente leitura",
          levanta(AttributeError, lambda: setattr(limite, "atendimentos", ())) is not None)
verificar("atendimentos devolve tupla (cópia imutável)", isinstance(limite.atendimentos, tuple))
verificar("não dá para dar append no retorno",
          levanta(AttributeError, lambda: limite.atendimentos.append(None)) is not None)
agenda_nova = Agenda(limite_minutos=60)
verificar("a lista interna é protegida (convenção _)", hasattr(limite, "_atendimentos"))
agenda_nova.agendar(Consulta(ana, "CG"))
foto = agenda_nova.atendimentos
agenda_nova.agendar(Consulta(leo, "CG"))
verificar("tupla já obtida NÃO muda quando a agenda cresce (é cópia)", len(foto) == 1)
verificar("a agenda enxerga o novo atendimento", len(agenda_nova.atendimentos) == 2)

secao("d) Agenda: instâncias independentes (sem estado compartilhado)")
a1, a2 = Agenda(60), Agenda(60)
a1.agendar(Consulta(ana, "CG"))
verificar("agendar em a1 não afeta a2", a2.minutos_ocupados == 0 and a2.atendimentos == ())
a2.agendar(Consulta(ana, "CG"))                  # mesma paciente em outra agenda: ok
verificar("o mesmo paciente pode estar em agendas diferentes", len(a2.atendimentos) == 1)

secao("d) Agenda: polimorfismo (soma heterogênea sem verificar tipo)")
mista = Agenda(limite_minutos=240)
mista.agendar(Consulta(ana, "CG"))                       # 30
mista.agendar(Consulta(leo, "CG", retorno=True))         # 15
mista.agendar(Exame(rui, "G", jejum=True))               # 30
mista.agendar(Vacinacao(Paciente("Bia", "4"), "I", doses=3))   # 30
verificar("30 + 15 + 30 + 30 = 105", mista.minutos_ocupados == 105)
fonte = inspect.getsource(Agenda)
verificar("Agenda não usa isinstance nem type()", "isinstance" not in fonte and "type(" not in fonte)

secao("d) Agenda: captura das exceções")
for chamada, esperado in [
    (lambda: limite.agendar(Vacinacao(rui, "I")), HorarioIndisponivelError),
    (lambda: agenda.agendar(Exame(ana, "G")), PacienteJaAgendadoError),
]:
    capturadas = []
    try:
        chamada()
    except AgendaError as erro:
        capturadas.append(type(erro))
    verificar(f"um único 'except AgendaError' captura {esperado.__name__}",
              capturadas == [esperado])

print("\nTodas as verificações passaram.")
