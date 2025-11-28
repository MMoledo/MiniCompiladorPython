# parser.py
import ply.yacc as yacc
from lexer import tokens

# Definição da precedência dos operadores
precedence = (
    ('left', 'SOMA', 'SUB'),
    ('left', 'MULT', 'DIV'),
    ('right', 'POT'),
    ('right', 'UMINUS'),
)

# --- Definições da Gramática e construção da AST ---

def p_programa(p):
    '''programa : declaracoes'''
    p[0] = ('programa', p[1])

def p_declaracoes(p):
    '''declaracoes : declaracoes declaracao
                   | declaracao'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_declaracao(p):
    '''declaracao : declaracao_funcao
                  | atribuicao'''
    p[0] = p[1]

def p_declaracao_funcao(p):
    '''declaracao_funcao : FUNCAO ID LPAREN params RPAREN IGUAL expressao'''
    p[0] = ('declaracao_funcao', p[2], p[4], p[7])

def p_params(p):
    '''params : params VIRGULA ID
              | ID
              | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_atribuicao(p):
    '''atribuicao : ID IGUAL expressao'''
    p[0] = ('atribuicao', p[1], p[3])

def p_expressao_binop(p):
    '''expressao : expressao SOMA expressao
                 | expressao SUB expressao
                 | expressao MULT expressao
                 | expressao DIV expressao
                 | expressao POT expressao'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expressao_uminus(p):
    '''expressao : SUB expressao %prec UMINUS'''
    p[0] = ('unop', '-', p[2])

def p_expressao_grupo(p):
    '''expressao : LPAREN expressao RPAREN'''
    p[0] = p[2]

def p_expressao_chamada_funcao(p):
    '''expressao : ID LPAREN args RPAREN'''
    p[0] = ('chamada_funcao', p[1], p[3])

def p_args(p):
    '''args : args VIRGULA expressao
            | expressao
            | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_expressao_numero(p):
    '''expressao : NUMERO'''
    p[0] = ('numero', p[1])

def p_expressao_id(p):
    '''expressao : ID'''
    p[0] = ('id', p[1])

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Erro de sintaxe em '{p.value}' na linha {p.lineno}")
    else:
        print("Erro de sintaxe: fim inesperado do arquivo")

parser = yacc.yacc()
