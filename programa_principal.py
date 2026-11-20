"""Criar a tabela de palavras e símbolos reservados
Popular a tabela de palavras e símbolos reservados 


Palavras reservadas (if, print,read,while,endif,begin,end…)

Símbolos reservados da linguagem (:,+-’(‘ )
Tabela de símbolos (começa vazia)
 Guardar os identificadores da linguagem:
 (simbolos que dependem do usuario da linguagem, ex: variaveis, strings, numeros inteiros)
Solicitar qual texto fonte será compilado
Localizar no disco o texto fonte
Abrir o texto fonte
Posicionar no primeiro caractere desse texto
Definir para o que depende de escopo de reconhecimento de átomos
	Qual é o escopo padrão
Chamar o analisador léxico
Tratar retorno do analisador léxico
Modifique o escopo válido de reconhecimento
Realizar a análise sintática nesse momento ou deixar para fazer depois
que toda a análise léxica estiver concluída.
Montar lista de átomos

Avaliar a sequência dos átomos (análise sintática algo possível, mas 
por contado tempo não conseguiremos fazer).
Gerar o relatório da análise léxica (Lista de todos os átomos reconhecidos
Na ordem em que reconheci, quantas vezes eles tenham aparecido no 
meu texto fonte)
Gerar o relatório da tabela de símbolos (O reflexo da estrutura 
montada que foi gravada pelo analisador léxico)
	"""


