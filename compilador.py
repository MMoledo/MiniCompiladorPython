# compilador.py
import sys
from lexer import lexer
from parser import parser
from analisador_semantico import AnalisadorSemantico

def compilar(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as arquivo:
            codigo = arquivo.read()
            print(f"--- Lendo código de: {nome_arquivo} ---")
            print(codigo)
            print("-" * 36)

            # Análise Léxica
            lexer.input(codigo)
            print("Iniciando Análise Léxica...")
            
            # Apenas para visualização dos tokens (opcional)
            # for tok in lexer:
            #     print(tok)
            print("Análise Léxica concluída com sucesso.")

            # Análise Sintática
            print("Iniciando Análise Sintática...")
            ast = parser.parse(codigo, lexer=lexer)
            if not ast:
                print("Falha na Análise Sintática. Compilação interrompida.")
                return

            print("Análise Sintática concluída com sucesso.")
            # print("AST Gerada:", ast) # Descomente para ver a AST

            # Análise Semântica
            print("Iniciando Análise Semântica...")
            analisador = AnalisadorSemantico()
            analisador.analisar(ast)

            print("\n>>> Arquivo compilado com sucesso! (Sintaxe e Semântica OK)")

    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
    except Exception as e:
        print(f"\n>>> Falha na compilação: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python compilador.py Exemplos\\<nome_do_arquivo.comp>")
    else:
        compilar(sys.argv[1])
