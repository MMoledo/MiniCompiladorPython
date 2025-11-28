# Mini Compilador para Linguagem de Expressões Funcionais

## 1. Objetivo do Projeto

Este projeto é um mini compilador para uma linguagem de programação simples, focada em expressões matemáticas e funções. O objetivo é ler arquivos de código escritos nesta nova linguagem (com extensão `.comp`), verificar se eles estão escritos corretamente (análises léxica, sintática e semântica) e informar o usuário sobre o sucesso ou a falha da compilação.

Ele foi desenvolvido em Python utilizando a biblioteca `PLY`.

## 2. O que cada arquivo faz?

O projeto é dividido em módulos, cada um com uma responsabilidade clara:

-   **`lexer.py` (Analisador Léxico):** Funciona como os "olhos" do compilador. Ele lê o código-fonte e o quebra em pequenas peças chamadas "tokens" (números, operadores, nomes de variáveis, etc.). Ele também é responsável por ignorar espaços e comentários.

-   **`parser.py` (Analisador Sintático):** Funciona como o "verificador de gramática". Ele pega os tokens do lexer e verifica se eles estão em uma ordem que faz sentido, de acordo com as regras da linguagem. Se a sintaxe estiver correta, ele monta uma "Árvore Sintática Abstrata" (AST), que é uma representação estruturada do programa.

-   **`analisador_semantico.py` (Analisador Semântico):** Funciona como o "detetive lógico". Ele analisa a AST para encontrar erros que a sintaxe não pega, como usar uma variável que não existe, ou chamar uma função com o número errado de argumentos. Ele gerencia os "escopos" para entender quais variáveis existem dentro de cada função.

-   **`compilador.py` (O Orquestrador):** Este é o programa principal que você executa. Ele gerencia todo o processo: lê o arquivo, passa para o lexer, depois para o parser e, finalmente, para o analisador semântico, exibindo o resultado final.

## 3. Como Executar o Compilador

Siga os passos abaixo para testar o compilador.

### Pré-requisitos

-   Python 3.6 ou superior instalado.

### Passo 1: Instalar a Biblioteca `PLY`

Abra seu terminal ou prompt de comando e execute o seguinte comando para instalar a dependência necessária:

```bash 
pip install ply
```

### Passo 2: Salvar os Arquivos
Certifique-se de que todos os arquivos de código (compilador.py, lexer.py, parser.py, analisador_semantico.py) e os arquivos de exemplo que você deseja testar (com a extensão .comp) estejam salvos na mesma pasta.

### Passo 3: Executar a Compilação
Para compilar um arquivo, navegue com o terminal até a pasta onde salvou os arquivos e use o comando python seguido do nome do script compilador.py e, por fim, o nome do arquivo que você deseja analisar.

**Sintaxe do comando:**
```Bash
python compilador.py Exemplos\<nome_do_arquivo.comp>
```

**Exemplo com um arquivo válido:**

```Bash
python compilador.py Exemplos\exemplo_completo_correto.comp
```

**Saída esperada:** O programa mostrará o progresso de cada etapa e terminará com uma mensagem de sucesso, como "Arquivo compilado com sucesso! (Sintaxe e Semântica OK)".

**Exemplo com um arquivo que contém um erro:**
```Bash
python compilador.py exemplo_erro_semantico.comp
```

**Saída esperada:** O compilador informará o erro encontrado (seja ele de sintaxe ou semântico), apontando a falha e interrompendo a execução com uma mensagem como "Falha na compilação: Erro Semântico...".

### 4. Arquivos Gerados Automaticamente
Após a primeira execução, você notará que dois novos arquivos aparecerão na sua pasta: parser.out e parsetab.py.
- parser.out: Um relatório de texto legível por humanos sobre a gramática. É muito útil para depurar problemas nas regras de sintaxe.
- parsetab.py: Uma versão em cache da tabela de análise sintática. A biblioteca PLY gera este arquivo para acelerar drasticamente as execuções futuras, pois não precisa reconstruir a tabela de análise do zero toda vez.

**Você pode apagar esses dois arquivos com segurança a qualquer momento.** Eles serão recriados automaticamente na próxima vez que você executar o compilador. É uma prática comum adicioná-los ao .gitignore para não incluí-los no controle de versão.