# Sistema Especialista em Cuidados com Plantas (Python)

Este é um sistema especialista baseado em console, desenvolvido em Python, que visa auxiliar usuários, especialmente leigos em botânica, a identificar o tipo de suas plantas e receber recomendações de cuidados personalizadas. O sistema utiliza uma abordagem orientada a objetos e um sistema de pontuação para guiar o usuário através de perguntas de múltipla escolha.

## Funcionalidades Principais

1.  **Identificação do Tipo de Planta:**
    * Ajuda o usuário a classificar sua planta em um dos quatro grandes grupos botânicos: Briófitas, Pteridófitas, Gimnospermas ou Angiospermas.
    * Utiliza um sistema de perguntas sobre características visíveis da planta (flores, frutos, sementes, porte, tipo de folhas, estrutura geral).
    * Inclui um mecanismo de **desempate** com perguntas bônus caso a pontuação inicial entre dois tipos seja igual (atualmente focado no empate Angiosperma vs. Gimnosperma).

2.  **Avaliação das Condições Ambientais:**
    * Coleta informações sobre a estação do ano (entrada direta do usuário).
    * Identifica a umidade atual do solo através de perguntas sobre a sensação ao toque.
    * Identifica o nível de iluminação do local da planta com base em perguntas sobre luz solar direta e indireta.
    * Registra a frequência de rega atual praticada pelo usuário.
    * Todas as perguntas são de múltipla escolha, facilitando a interação.

3.  **Recomendações de Cuidados Personalizadas:**
    * Com base no tipo de planta e nas condições ambientais identificadas, o sistema gera uma lista de cuidados.
    * **Resolução de Conflitos de Rega:** Possui uma lógica para priorizar regras e fornecer uma única recomendação de frequência de rega, evitando sugestões contraditórias e explicando o motivo da sugestão.
    * Fornece dicas sobre iluminação, umidade, e cuidados gerais como monitoramento de pragas, adubação e temperatura.
    * As explicações para as recomendações buscam ser educativas e detalhadas.

4.  **Interface de Usuário:**
    * Interação via console (terminal).
    * Todas as perguntas são apresentadas com opções numeradas para seleção pelo usuário, minimizando erros de digitação.
    * Normalização de entradas (remoção de acentos, conversão para maiúsculas) para robustez.

## Estrutura do Código (Orientado a Objetos)

O projeto é organizado nas seguintes classes principais:

* `AuxiliarEntrada`: Responsável por toda a interação com o usuário (fazer perguntas, exibir opções, validar entradas).
* `Identificador`: Contém a lógica para identificar o tipo de planta, umidade do solo e iluminação através de um sistema de pontuação baseado nas respostas do usuário. Inclui o mecanismo de desempate.
* `Planta`: Armazena as informações da planta (nome popular e tipo identificado).
* `CondicoesAmbientais`: Armazena as informações sobre o ambiente da planta (estação, umidade, iluminação, frequência de rega atual).
* `SistemaRecomendacao`: Classe central que utiliza as informações da `Planta` e `CondicoesAmbientais` para aplicar regras e gerar a lista final de recomendações de cuidados.

## Como Executar o Projeto

1.  **Pré-requisitos:**
    * Python 3.x instalado em seu sistema.
    * Nenhuma biblioteca externa é necessária além das padrão do Python (como `unicodedata`).

2.  **Execução:**
    * Salve o código Python em um arquivo (por exemplo, `sistema_plantas.py`).
    * Abra um terminal ou prompt de comando.
    * Navegue até o diretório onde você salvou o arquivo.
    * Execute o script com o comando:
        ```bash
        python sistema_plantas.py
        ```
    * Siga as instruções apresentadas no console, respondendo às perguntas com o número da opção desejada.

## Exemplo de Interação


--- Bem-vindo ao Sistema Especialista em Cuidados com Plantas (vOO) ---
Qual é o nome popular da sua planta? (Ex: Samambaia, Cacto, Roseira): Roseira

--- Identificação do Tipo da Planta ---
Para ajudar a definir os melhores cuidados, vamos tentar identificar o tipo da sua planta.

Briófitas: Plantas pequenas (ex: musgos), geralmente em locais úmidos, sem flores ou sementes visíveis.

Pteridófitas: Como samambaias e avencas. Têm folhas, mas não produzem flores nem sementes; usam esporos.

Gimnospermas: Como pinheiros e araucárias. Produzem sementes 'nuas' (ex: pinhas), sem flores verdadeiras.

Angiospermas: O grupo mais comum. São as plantas que dão flores e frutos (que protegem as sementes).

A planta costuma produzir flores?

Sim, Produz Flores

Nao Produz Flores

Nao Sei / Nao Observei
Escolha o número da opção para 'Presença de flores': 1
... (continua com mais perguntas) ...


## Possíveis Melhorias Futuras

* Expandir o sistema de desempate para outros pares de tipos de plantas.
* Adicionar mais perguntas bônus para refinar a identificação das condições ambientais.
* Incluir uma base de dados de plantas específicas com suas necessidades particulares, para ir além das recomendações por grupo.
* Desenvolver uma interface gráfica (GUI) para uma experiência de usuário mais visual.
* Permitir que o usuário salve perfis de suas plantas.
* Integrar com APIs de previsão do tempo para recomendações mais dinâmicas.

