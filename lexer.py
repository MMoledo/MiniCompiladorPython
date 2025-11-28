# lexer.py
import ply.lex as lex

# Lista de nomes dos tokens. É obrigatório.
tokens = (
    'FUNCAO',
    'ID',
    'NUMERO',
    'SOMA',
    'SUB',
    'MULT',
    'DIV',
    'POT',
    'IGUAL',
    'LPAREN',
    'RPAREN',
    'VIRGULA',
)

# Expressões regulares para tokens simples
t_SOMA    = r'\+'
t_SUB     = r'-'
t_MULT    = r'\*'
t_DIV     = r'/'
t_POT     = r'\^'
t_IGUAL   = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_VIRGULA = r','

# Expressão regular para a palavra-chave 'funcao'
def t_FUNCAO(t):
    r'funcao'
    t.type = 'FUNCAO'
    return t

# Expressão regular para IDs (variáveis e nomes de funções)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

# Expressão regular para números (inteiros e ponto flutuante)
def t_NUMERO(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# Regra para rastrear números de linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Regra para comentários de bloco (/* ... */)
def t_comment_block(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass # Não retorna valor, efetivamente ignorando o token

# Regra para comentários de linha (// ...)
def t_comment_line(t):
    r'//.*'
    pass # Não retorna valor

# String contendo caracteres ignorados (espaços e tabs)
t_ignore  = ' \t'

# Regra para tratamento de erros
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

# Constrói o lexer
lexer = lex.lex()
