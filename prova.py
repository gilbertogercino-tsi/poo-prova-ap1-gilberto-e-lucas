from __future__ import annotations
from datetime import date, timedelta

# Exceções personalizadas

class QuantidadeInvalidaError(Exception):
    """Lançada quando a quantidade solicitada para dispensação for menor ou igual a 0 ou superior ao estoque."""
    pass


class MedicamentoVencidoError(Exception):
    """Lançada ao tentar dispensar um medicamento cuja data de validade já expirou."""
    pass


# Classe Principal

class Medicamento:
    """Representa um lote individual de medicamento no estoque de uma UPA."""

    def __init__(
        self,
        nome: str,
        lote: str,
        validade: date,
        quantidade: int,
        valor: float
    ) -> None:
        self.nome: str = nome
        self.lote: str = lote
        self.validade: date = validade
        
        # Atribuições utilizando os setters para validação imediata
        self.quantidade = quantidade
        self.valor = valor

    # Encapsulamento com @property e Setters

    @property
    def quantidade(self) -> int:
        return self._quantidade

    @quantidade.setter
    def quantidade(self, valor: int) -> None:
        if valor < 0:
            raise ValueError("A quantidade em estoque não pode ser um valor negativo.")
        self._quantidade = valor

    @property
    def valor(self) -> float:
        return self._valor

    @valor.setter
    def valor(self, novo_valor: float) -> None:
        if novo_valor <= 0:
            raise ValueError("O valor unitário do medicamento deve ser estritamente maior que zero.")
        self._valor = novo_valor

    # Métodos de classe e estáticos

    @classmethod
    def de_registro(cls, registro: str) -> Medicamento:
        """Construtor alternativo a partir de uma string no formato 'nome;lote;validade;quantidade;valor'."""
        partes: list[str] = registro.split(";")
        nome: str = partes[0]
        lote: str = partes[1]
        validade: date = date.fromisoformat(partes[2])
        quantidade: int = int(partes[3])
        valor: float = float(partes[4])
        
        return cls(nome, lote, validade, quantidade, valor)

    @staticmethod
    def dias_para_vencer(validade: date) -> int:
        """Calcula os dias restantes entre a data atual e a data de validade fornecida."""
        return (validade - date.today()).days

    # Métodos Especiais (Dunders)

    def __str__(self) -> str:
        """Retorna uma representação formatada para o usuário."""
        return (
            f"{self.nome} ({self.lote}) - {self.quantidade} un. - "
            f"val. {self.validade.strftime('%d/%m/%Y')}"
        )

    def __repr__(self) -> str:
        """Retorna a representação detalhada voltada para depuração."""
        return (
            f"Medicamento(nome='{self.nome}', lote='{self.lote}', "
            f"validade=date({self.validade.year}, {self.validade.month}, {self.validade.day}), "
            f"quantidade={self.quantidade}, valor={self.valor})"
        )

    def __eq__(self, outro: object) -> bool:
        """Dois medicamentos são iguais se possuem mesmo nome e lote."""
        if not isinstance(outro, Medicamento):
            return NotImplemented
        return self.nome == outro.nome and self.lote == outro.lote

    def __lt__(self, outro: object) -> bool:
        """Permite a ordenação por proximidade da data de validade (mais antigos/próximos primeiro)."""
        if not isinstance(outro, Medicamento):
            return NotImplemented
        return self.validade < outro.validade

    # Operações de estoque

    def dispensar(self, quantidade: int) -> None:
        """Registra a saída do estoque, validando disponibilidade e vencimento."""
        if quantidade <= 0 or quantidade > self.quantidade:
            raise QuantidadeInvalidaError(
                f"Quantidade de dispensação inválida ({quantidade}). "
                f"Estoque disponível: {self.quantidade}."
            )
        
        if self.validade < date.today():
            raise MedicamentoVencidoError(
                f"Não é possível dispensar o lote {self.lote} de {self.nome}: "
                f"Medicamento vencido em {self.validade.strftime('%d/%m/%Y')}."
            )

        self.quantidade -= quantidade

    def repor(self, quantidade: int) -> None:
        """Aumenta a quantidade em estoque utilizando a validação do setter."""
        if quantidade <= 0:
            raise ValueError("A quantidade reposta deve ser um número inteiro positivo.")
        
        self.quantidade += quantidade


# Bloco de demonstração

if __name__ == "__main__":
    m1 = Medicamento("Dipirona 500mg", "L2026A", date(2026, 12, 31), 100, 12.50)
    m2 = Medicamento.de_registro("Amoxicilina 500mg;L2026B;2026-10-15;40;18.90")

    print(f"Dados de m1: {m1}")
    print(f"Dados de m2: {m2}")
    print(f"Dias para vencer de m2: {Medicamento.dias_para_vencer(m2.validade)}")

    print("Dispensando 20 medicamentos de m1")
    m1.dispensar(20)
    print(f"Quantidade de m1: {m1.quantidade}")

    try:
        m2.dispensar(999)
    except QuantidadeInvalidaError as erro:
        print(f"Erro esperado: {erro}")

    vencido = Medicamento("Soro Fisiológico", "L2025X", date(2025, 1, 10), 10, 5.0)
    try:
        vencido.dispensar(1)
    except MedicamentoVencidoError as erro:
        print(f"Erro esperado: {erro}")

    outro = Medicamento("Dipirona 500mg", "L2026A", date(2026, 1, 1), 0, 1.0)
    print(f"m1 é igual a outro? {m1 == outro}")

    estoque = [m1, m2, vencido, outro]
    print("Exibindo lista ordenada por data (mais antigos primeiro): ")
    for lote in sorted(estoque):
        print(lote)

    try:
        m1.quantidade = -5
    except ValueError as erro:
        print(f"Erro esperado: {erro}")
