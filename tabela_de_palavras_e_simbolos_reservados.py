"""Tabela de palavras e símbolos reservados

Guarda o que a linguagem define (Apêndice A, colunas A e B).
É fixa: igual para todo texto fonte e preenchida no início, antes de abrir o fonte.
Durante a análise o léxico só consulta, nunca altera.
Chave: lexeme em maiúsculas. Valor: código do átomo.
"""

PALAVRAS_RESERVADAS = {
    "BOOLEAN": "A01",
    "BREAK": "A02",
    "CHARACTER": "A03",
    "DECLARATIONS": "A04",
    "ELSE": "A05",
    "ENDDECLARATIONS": "A06",
    "ENDFUNCTION": "A07",
    "ENDFUNCTIONS": "A08",
    "ENDIF": "A09",
    "ENDPROGRAM": "A10",
    "ENDWHILE": "A11",
    "FALSE": "A12",
    "FUNCTIONS": "A13",
    "FUNCTYPE": "A14",
    "IF": "A15",
    "INTEGER": "A16",
    "PARAMTYPE": "A17",
    "PRINT": "A18",
    "PROGRAM": "A19",
    "REAL": "A20",
    "RETURN": "A21",
    "STRING": "A22",
    "TRUE": "A23",
    "VARTYPE": "A24",
    "VOID": "A25",
    "WHILE": "A26",
}

SIMBOLOS_RESERVADOS = {
    ";": "B01",
    ",": "B02",
    ":": "B03",
    ":=": "B04",
    "?": "B05",
    "(": "B06",
    ")": "B07",
    "[": "B08",
    "]": "B09",
    "{": "B10",
    "}": "B11",
    "+": "B12",
    "-": "B13",
    "*": "B14",
    "/": "B15",
    "%": "B16",
    "==": "B17",
    "!=": "B18",
    "#": "B18",  # sinônimo de !=
    "<": "B19",
    "<=": "B20",
    ">": "B21",
    ">=": "B22",
}


def criar_tabela() -> dict[str, str]:
    """Cria a tabela juntando as palavras e os símbolos reservados."""
    return PALAVRAS_RESERVADAS | SIMBOLOS_RESERVADOS


def buscar(tabela: dict[str, str], lexeme: str) -> str | None:
    """Devolve o código do átomo se o lexeme for reservado; senão, None.

    O lexeme já deve chegar em maiúsculas (o léxico converte antes).
    """
    return tabela.get(lexeme)
