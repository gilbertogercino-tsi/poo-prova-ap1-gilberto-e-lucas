from modelos immport Paciente, Consulta, Vacinacao, Exame, Agenda

def main() -> None:
    print("Sistema UPA - Gestão de Atendimentos")

    agenda = Agenda(limite_minutos=120)

    ana = Paciente("Ana Souza", "700000000000001")
    leo = Paciente("Leo Lima", "700000000000002")
    rui = Paciente("Rui Alves", "700000000000003")

    try:
        c1 = Consulta(ana, "Clínica Geral", retorno=False)
        agenda.agendar(c1)
        print(f"Agendado: {c1}")

        e1 = Exame(leo, "Hemograma", jejum=True)
        agenda.agendar(e1)
        print(f"Agendado: {e1}")

        print(f"\nMinutos ocupados: {agenda.minutos_ocupados} / {agenda.limite_minutos}")

        c2 = Consulta(ana, "Pediatria", retorno=True)
        agenda.agendar(c2)

if __name__ == "__main__":
    main()