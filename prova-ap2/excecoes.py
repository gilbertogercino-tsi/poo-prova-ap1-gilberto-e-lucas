class AgendaError(Exception):
    """Classe base para erros relacionados à agenda da UPA."""
    pass


class HorarioIndisponivelError(AgendaError):
    """Erro lançado quando não há tempo disponível na agenda."""
    pass


class PacienteJaAgendadoError(AgendaError):
    """Erro lançado quando o paciente já possui um atendimento na agenda."""
    pass