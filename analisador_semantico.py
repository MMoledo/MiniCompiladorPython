# analisador_semantico.py

class TabelaDeSimbolos:
    """
    Representa um único escopo (global ou de função).
    Pode ser encadeada para representar escopos aninhados.
    """
    def __init__(self, escopo_pai=None):
        self.simbolos = {}
        self.escopo_pai = escopo_pai

    def declarar(self, nome, tipo, **kwargs):
        """Declara um novo símbolo no escopo atual."""
        if nome in self.simbolos:
            # Permite redeclaração de variável, mas não de função
            if self.simbolos[nome]['tipo'] == 'funcao' or tipo == 'funcao':
                 raise Exception(f"Erro Semântico: Símbolo '{nome}' já foi declarado neste escopo.")
        self.simbolos[nome] = {'tipo': tipo, **kwargs}

    def buscar(self, nome):
        """Busca por um símbolo no escopo atual e nos escopos pais."""
        simbolo = self.simbolos.get(nome)
        if simbolo:
            return simbolo
        if self.escopo_pai:
            return self.escopo_pai.buscar(nome)
        raise Exception(f"Erro Semântico: Símbolo '{nome}' não foi declarado.")


class AnalisadorSemantico:
    def __init__(self):
        # A pilha de escopos. Começa com o escopo global.
        self.pilha_escopos = [TabelaDeSimbolos()]
        self.erros = []

    @property
    def escopo_atual(self):
        """Retorna o escopo que está no topo da pilha."""
        return self.pilha_escopos[-1]

    def entrar_escopo(self):
        """Cria um novo escopo e o coloca no topo da pilha."""
        novo_escopo = TabelaDeSimbolos(escopo_pai=self.escopo_atual)
        self.pilha_escopos.append(novo_escopo)

    def sair_escopo(self):
        """Remove o escopo do topo da pilha."""
        if len(self.pilha_escopos) > 1:
            self.pilha_escopos.pop()

    def analisar(self, ast):
        """Método principal para iniciar a análise da AST."""
        try:
            self.visitar(ast)
            if self.erros:
                # Imprime todos os erros coletados
                for erro in self.erros:
                    print(erro)
                # Lança uma exceção para parar a compilação
                raise Exception("Falha na Análise Semântica. Compilação interrompida.")
            else:
                print("Análise Semântica concluída com sucesso.")
        except Exception as e:
            # Captura a exceção final para a mensagem de falha
            if not self.erros: # Se o erro não foi um dos registrados
                print(e)
            raise e


    def registrar_erro(self, mensagem):
        """Adiciona uma mensagem de erro à lista de erros."""
        if mensagem not in self.erros:
            self.erros.append(mensagem)

    def visitar(self, no):
        """Chama o método 'visitar' apropriado para o tipo do nó da AST."""
        metodo = f'visitar_{no[0]}'
        visitante = getattr(self, metodo, self.visitar_default)
        return visitante(no)

    def visitar_default(self, no):
        raise Exception(f'Nenhum método visitar_{no[0]} encontrado.')

    def visitar_programa(self, no):
        for declaracao in no[1]:
            self.visitar(declaracao)

    def visitar_declaracao_funcao(self, no):
        _, nome_funcao, params, corpo = no
        try:
            # Declara a função no escopo atual (global)
            self.escopo_atual.declarar(nome_funcao, 'funcao', num_params=len(params))
        except Exception as e:
            self.registrar_erro(str(e))

        # --- Lógica de Escopo ---
        self.entrar_escopo()

        # Declara os parâmetros no novo escopo local da função
        for param in params:
            try:
                self.escopo_atual.declarar(param, 'parametro')
            except Exception as e:
                self.registrar_erro(str(e))

        # Visita o corpo da função, agora dentro do escopo local
        self.visitar(corpo)

        self.sair_escopo()
        # --- Fim da Lógica de Escopo ---

    def visitar_atribuicao(self, no):
        _, nome_var, expressao = no
        # Visita a expressão do lado direito primeiro
        self.visitar(expressao)
        try:
            # Tenta declarar a variável no escopo atual
            self.escopo_atual.declarar(nome_var, 'variavel')
        except Exception as e:
            self.registrar_erro(str(e))

    def visitar_binop(self, no):
        _, _, esq, dir = no
        self.visitar(esq)
        self.visitar(dir)

    def visitar_unop(self, no):
        _, _, expr = no
        self.visitar(expr)

    def visitar_chamada_funcao(self, no):
        _, nome_funcao, args = no
        try:
            simbolo = self.escopo_atual.buscar(nome_funcao)
            if simbolo['tipo'] != 'funcao':
                self.registrar_erro(f"Erro Semântico: '{nome_funcao}' não é uma função.")
            elif simbolo['num_params'] != len(args):
                self.registrar_erro(
                    f"Erro Semântico: Função '{nome_funcao}' espera {simbolo['num_params']} "
                    f"argumentos, mas recebeu {len(args)}."
                )
        except Exception as e:
            self.registrar_erro(str(e))

        for arg in args:
            self.visitar(arg)

    def visitar_numero(self, no):
        pass # Números são sempre válidos

    def visitar_id(self, no):
        _, nome_id = no
        try:
            # Apenas verifica se o ID existe no escopo atual ou em algum pai
            self.escopo_atual.buscar(nome_id)
        except Exception as e:
            self.registrar_erro(str(e))

