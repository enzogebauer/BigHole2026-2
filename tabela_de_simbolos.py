"""Tabela de símbolos

Guarda os identificadores e constantes criados por quem escreve o programa.
Começa vazia e é preenchida pelo léxico durante a análise.
- Uma entrada por lexeme; registros repetidos só acrescentam a linha.
- Guarda até as cinco primeiras linhas em que o lexeme aparece (repetições contam).
- O tipo das constantes vem do código do átomo (C04 ST, C05 CH, C06 IN, C07 FP).
- definir_tipo só grava quando o tipo ainda está vazio ("-").
- Número da entrada, código do átomo e lexeme não mudam depois de gravados.
"""

from dataclasses import dataclass, field

# O tipo das constantes é deduzido pelo código do átomo.
TIPO_POR_CODIGO = {
    "C04": "ST",  # stringConst
    "C05": "CH",  # charConst
    "C06": "IN",  # intConst
    "C07": "FP",  # realConst
}


@dataclass
class Entrada:
    """Uma entrada da tabela de símbolos (uma por lexeme)."""

    numero_da_entrada: int
    codigo_do_atomo: str
    lexeme: str
    quantidade_antes_truncagem: int
    quantidade_depois_truncagem: int
    tipo_do_simbolo: str = "-"
    cinco_primeiras_linhas: list[int] = field(default_factory=list)


class TabelaDeSimbolos:
    """Gerenciador da tabela de símbolos: começa vazia e é preenchida durante a análise."""

    def __init__(self) -> None:
        self.entradas_por_lexeme: dict[str, Entrada] = {}
        self.entradas_em_ordem: list[Entrada] = []  # posição + 1 = número da entrada

    def registrar(self, lexeme: str, codigo: str, antes: int, depois: int, linha: int) -> int:
        """Registra uma ocorrência do lexeme e devolve o número da entrada.

        Lexeme novo: cria a entrada. Lexeme existente: só acrescenta a linha,
        guardando no máximo as cinco primeiras ocorrências.
        Número, código, lexeme e contagens não mudam depois de gravados.
        """
        entrada = self.entradas_por_lexeme.get(lexeme)
        if entrada is None:
            entrada = Entrada(
                numero_da_entrada=len(self.entradas_em_ordem) + 1,
                codigo_do_atomo=codigo,
                lexeme=lexeme,
                quantidade_antes_truncagem=antes,
                quantidade_depois_truncagem=depois,
                tipo_do_simbolo=TIPO_POR_CODIGO.get(codigo, "-"),
            )
            self.entradas_por_lexeme[lexeme] = entrada
            self.entradas_em_ordem.append(entrada)
        if len(entrada.cinco_primeiras_linhas) < 5:
            entrada.cinco_primeiras_linhas.append(linha)
        return entrada.numero_da_entrada

    def definir_tipo(self, numero: int, tipo: str) -> None:
        """Grava o tipo do símbolo, apenas se ele ainda estiver vazio ("-")."""
        if not 1 <= numero <= len(self.entradas_em_ordem):
            raise ValueError(f"Entrada inexistente na tabela de símbolos: {numero}")
        entrada = self.entradas_em_ordem[numero - 1]
        if entrada.tipo_do_simbolo == "-":
            entrada.tipo_do_simbolo = tipo

    def entradas(self) -> list[Entrada]:
        """Devolve as entradas em ordem de número, para o relatório da tabela de símbolos."""
        return list(self.entradas_em_ordem)
