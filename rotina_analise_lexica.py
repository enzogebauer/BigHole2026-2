"""Determina qual o padrão léxico que será seguido (dep escopo)
Seguir o padrão aceitando caracteres válidos que são do padrão
Filtrar os caracteres inválidos da linguagem
Controlar o tamanho do elemento lexeme
Truncar o tamanho do lexeme (30 caracteres)
Caractere válido da linguagem fora do padrão (delimitar)
Pesquisar na tabela de palavras e símbolos reservados (para ver se tá lá)
Filtro de construção nāo relevante (comentários ou outras construções de combinações de caracteres que nāo conseguimos associar a
 um padrāo de formação da linguagem)
Se tiver retorna ao código do reservado
se nāo tiver pesquisa na tabela de símbolos
se tiver retorna índice de onde está na tabela de símbolos
se nāo tiver cria-se uma nova entrada na tabela de símbolos para esse símbolo
Atualizar informaçōes da tabela de símbolos
Retornar átomo (lexeme, código, índice na tab de símbolos ou None, linha)
"""

import string
from dataclasses import dataclass

from tabela_de_palavras_e_simbolos_reservados import buscar
from tabela_de_simbolos import TabelaDeSimbolos

CODIGO_FIM_DE_ARQUIVO = "EOF"
TAMANHO_MAXIMO_DO_LEXEME = 30

BRANCOS = frozenset(" \t\n\r")

CARACTERES_VALIDOS = frozenset(
    string.ascii_letters
    + string.digits
    + "_$.\"'"
    + ";,:=?()[]{}+-*/%!#<>"
) | BRANCOS


@dataclass
class Atomo:
    """Um átomo reconhecido; indice_na_tabela é None para palavras e símbolos reservados."""

    lexeme: str
    codigo_do_atomo: str
    indice_na_tabela: int | None
    linha: int


@dataclass
class ContextoDaAnalise:
    """O que o léxico precisa consultar a cada chamada de proximo_atomo.

    O léxico consulta a tabela de reservados, registra na tabela de símbolos
    e usa escopo_atual como código dos nomes que não são reservados.
    Quem muda o escopo_atual é o programa principal: troca para C03 ou C02
    e, depois do nome reconhecido, volta para C01. O léxico nunca altera o escopo.
    """

    tabela_de_reservados: dict[str, str]
    tabela_de_simbolos: TabelaDeSimbolos
    escopo_atual: str = "C01"


@dataclass
class Fonte:
    """Texto fonte e o ponto onde a leitura parou entre uma chamada e outra."""

    texto: str
    posicao: int = 0
    linha: int = 1

    def caractere_atual(self) -> str | None:
        """Devolve o caractere na posição atual, ou None no fim do texto."""
        if self.posicao < len(self.texto):
            return self.texto[self.posicao]
        return None

    def espiar_proximo(self) -> str | None:
        """Devolve o caractere seguinte ao atual sem avançar, ou None se não houver."""
        if self.posicao + 1 < len(self.texto):
            return self.texto[self.posicao + 1]
        return None

    def avancar(self) -> None:
        """Passa para o próximo caractere; passar por um LF soma uma linha."""
        if self.caractere_atual() == "\n":
            self.linha += 1
        if self.posicao < len(self.texto):
            self.posicao += 1


def pular_brancos_invalidos_e_comentarios(fonte: Fonte) -> None:
    """Avança até o primeiro caractere que pode começar um átomo, ou até o fim do texto.

    Pula, em laço: brancos, caracteres inválidos, comentários de linha (// até o LF
    ou o fim do texto) e comentários de bloco (/* até */, ou até o fim do texto
    se não houver fechamento). Uma / que não inicia comentário fica para o léxico.
    """
    while (caractere := fonte.caractere_atual()) is not None:
        proximo = fonte.espiar_proximo()
        if caractere in BRANCOS or caractere not in CARACTERES_VALIDOS:
            fonte.avancar()
        elif caractere == "/" and proximo == "/":
            while fonte.caractere_atual() not in (None, "\n"):
                fonte.avancar()
        elif caractere == "/" and proximo == "*":
            fonte.avancar()
            fonte.avancar()
            while fonte.caractere_atual() is not None and not (
                fonte.caractere_atual() == "*" and fonte.espiar_proximo() == "/"
            ):
                fonte.avancar()
            fonte.avancar()  # o * do fechamento (no fim do texto, não faz nada)
            fonte.avancar()  # a / do fechamento
        else:
            return


def ler_identificador_ou_reservada(fonte: Fonte, contexto: ContextoDaAnalise, linha: int) -> Atomo:
    """Lê letras, dígitos e _ pelo máximo comprimento, a partir de uma letra ou _.

    Caracteres inválidos no meio são pulados sem contar e sem delimitar (va@r1 → VAR1).
    O lexeme sai em maiúsculas, com no máximo 30 caracteres guardados.
    Palavra reservada sai só com o código. Senão, o código vem do escopo atual
    (lexeme com _ é sempre C01) e o lexeme é registrado na tabela de símbolos.
    """
    caracteres_guardados: list[str] = []
    quantidade_antes_truncagem = 0
    while (caractere := fonte.caractere_atual()) is not None:
        if caractere not in CARACTERES_VALIDOS:
            fonte.avancar()
        elif caractere.isalnum() or caractere == "_":
            quantidade_antes_truncagem += 1
            if len(caracteres_guardados) < TAMANHO_MAXIMO_DO_LEXEME:
                caracteres_guardados.append(caractere.upper())
            fonte.avancar()
        else:
            break
    lexeme = "".join(caracteres_guardados)

    codigo = buscar(contexto.tabela_de_reservados, lexeme)
    if codigo is not None:
        return Atomo(lexeme, codigo, None, linha)

    codigo = "C01" if "_" in lexeme else contexto.escopo_atual
    indice = contexto.tabela_de_simbolos.registrar(
        lexeme, codigo, quantidade_antes_truncagem, len(lexeme), linha
    )
    codigo = contexto.tabela_de_simbolos.entradas_em_ordem[indice - 1].codigo_do_atomo
    return Atomo(lexeme, codigo, indice, linha)


def proximo_atomo(fonte: Fonte, contexto: ContextoDaAnalise) -> Atomo:
    """Reconhece e devolve o próximo átomo do texto fonte.

    No fim do texto, devolve o átomo de fim de arquivo. Símbolos compostos
    (:= == != <= >=) são testados antes dos simples. Um caractere válido que
    não inicia nenhum padrão ($, ., = ou ! sozinhos) delimita e é descartado,
    e a busca recomeça do início.
    """
    while True:
        pular_brancos_invalidos_e_comentarios(fonte)
        caractere = fonte.caractere_atual()
        if caractere is None:
            return Atomo("", CODIGO_FIM_DE_ARQUIVO, None, fonte.linha)
        linha = fonte.linha

        if caractere.isalpha() or caractere == "_":
            return ler_identificador_ou_reservada(fonte, contexto, linha)

        if caractere.isdigit() or caractere in "\"'":
            raise NotImplementedError(f"Padrão ainda não implementado: {caractere!r} (linha {linha})")

        dois_caracteres = caractere + (fonte.espiar_proximo() or "")
        codigo = buscar(contexto.tabela_de_reservados, dois_caracteres)
        if len(dois_caracteres) == 2 and codigo is not None:
            fonte.avancar()
            fonte.avancar()
            return Atomo(dois_caracteres, codigo, None, linha)

        codigo = buscar(contexto.tabela_de_reservados, caractere)
        fonte.avancar()
        if codigo is not None:
            return Atomo(caractere, codigo, None, linha)
