

import unicodedata

# Constantes globais
TIPOS_PLANTA_VALIDOS = ['BRIOFITA', 'PTERIDOFITA', 'GIMNOSPERMA', 'ANGIOSPERMA']
ESTACOES_VALIDAS = ['VERAO', 'INVERNO', 'OUTONO', 'PRIMAVERA']
UMIDADES_VALIDAS = ['MUITO SECO', 'SECO', 'MEDIA', 'UMIDO', 'ENCHARCADO']
ILUMINACOES_VALIDAS = ['MUITO BAIXA', 'BAIXA', 'MODERADA', 'ALTA', 'MUITO ALTA']
FREQUENCIAS_REGA_VALIDAS = ['DIARIA', 'DUAS VEZES NA SEMANA', 'SEMANAL', 'QUINZENAL']

class AuxiliarEntrada:
    """Classe para lidar com entradas e validações do usuário."""

    def remover_acentos(self, texto):
        """Remove acentos de uma string."""
        if not isinstance(texto, str):
            return ""
        nfkd_form = unicodedata.normalize('NFD', texto)
        return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

    def pedir_entrada_numerada(self, pergunta, opcoes_para_pergunta, nome_caracteristica):
        """Pede uma entrada numerada ao usuário e retorna a opção escolhida (normalizada)."""
        print(f"\n{pergunta}")
        for i, opcao in enumerate(opcoes_para_pergunta):
            # Capitaliza a primeira letra de cada palavra para melhor leitura
            opcao_display = " ".join(word.capitalize() for word in opcao.split())
            print(f"  {i + 1}. {opcao_display}")


        while True:
            try:
                resposta_num_str = input(
                    f"Escolha o número da opção para '{nome_caracteristica.capitalize()}': "
                ).strip()
                if not resposta_num_str:
                    print("Entrada vazia. Por favor, digite um número.")
                    continue
                resposta_num = int(resposta_num_str)

                if 1 <= resposta_num <= len(opcoes_para_pergunta):
                    # Retorna a string da opção, normalizada e em maiúsculas
                    return self.remover_acentos(opcoes_para_pergunta[resposta_num - 1].upper())
                else:
                    print(f"Número inválido. Escolha entre 1 e {len(opcoes_para_pergunta)}.")
            except ValueError:
                print("Entrada inválida. Digite apenas o número da opção.")
            except Exception as e:
                print(f"Ocorreu um erro: {e}. Tente novamente.")

    def pedir_confirmacao(self, pergunta_confirmacao, opcoes_confirmacao=('Sim', 'Nao', 'Escolher manualmente')):
        """Pede uma confirmação Sim/Nao/Outra opção, usando seleção numerada."""
        opcoes_confirmacao_lista = list(opcoes_confirmacao)
        resposta_confirmacao_str = self.pedir_entrada_numerada(
            pergunta_confirmacao,
            opcoes_confirmacao_lista,
            "Confirmação"
        )
        return resposta_confirmacao_str


class Identificador:
    """Classe para identificar características da planta e do ambiente por pontuação."""

    def __init__(self, aux_entrada):
        self.aux_entrada = aux_entrada

    def _desempatar_tipo_planta(self, pontos, tipos_empatados_nomes):
        """Faz perguntas bônus para desempatar a identificação do tipo de planta."""
        print("\n--- Perguntas Bônus para Desempate (Tipo de Planta) ---")

        if 'ANGIOSPERMA' in tipos_empatados_nomes and 'GIMNOSPERMA' in tipos_empatados_nomes:
            print("Detectamos um empate entre Angiosperma e Gimnosperma. Algumas perguntas adicionais para esclarecer:")

            resp_bonus_flor = self.aux_entrada.pedir_entrada_numerada(
                "Sobre as 'flores' ou estruturas reprodutivas que você observou:",
                ["São coloridas e vistosas, com pétalas distintas, e geralmente atraem polinizadores (insetos, pássaros)?",
                 "São mais discretas, como cones (pinhas) ou estruturas que liberam pólen ao vento, sem pétalas evidentes?",
                 "Não tenho certeza / Não se aplica / Nenhuma das anteriores de forma clara."],
                "Detalhe da Estrutura Reprodutiva"
            )
            if resp_bonus_flor == self.aux_entrada.remover_acentos("São coloridas e vistosas, com pétalas distintas, e geralmente atraem polinizadores (insetos, pássaros)?".upper()):
                pontos['ANGIOSPERMA'] += 2
                if pontos.get('GIMNOSPERMA', 0) > 0 : pontos['GIMNOSPERMA'] -= 1
            elif resp_bonus_flor == self.aux_entrada.remover_acentos("São mais discretas, como cones (pinhas) ou estruturas que liberam pólen ao vento, sem pétalas evidentes?".upper()):
                pontos['GIMNOSPERMA'] += 2
                if pontos.get('ANGIOSPERMA', 0) > 0 : pontos['ANGIOSPERMA'] -= 1

            resp_bonus_semente = self.aux_entrada.pedir_entrada_numerada(
                "Sobre as sementes (se observadas anteriormente e se aplica):",
                ["Ficam completamente envolvidas por uma estrutura carnosa ou seca que se desenvolveu a partir da flor (um fruto verdadeiro)?",
                 "Ficam expostas em escamas de cones (pinhas) ou estruturas semelhantes, sem um fruto verdadeiro ao redor?",
                 "Não observei sementes com clareza suficiente para este detalhe / Não se aplica."],
                "Detalhe da Proteção da Semente"
            )
            if resp_bonus_semente == self.aux_entrada.remover_acentos("Ficam completamente envolvidas por uma estrutura carnosa ou seca que se desenvolveu a partir da flor (um fruto verdadeiro)?".upper()):
                pontos['ANGIOSPERMA'] += 2
                if pontos.get('GIMNOSPERMA', 0) > 0 : pontos['GIMNOSPERMA'] -= 1
            elif resp_bonus_semente == self.aux_entrada.remover_acentos("Ficam expostas em escamas de cones (pinhas) ou estruturas semelhantes, sem um fruto verdadeiro ao redor?".upper()):
                pontos['GIMNOSPERMA'] += 2
                if pontos.get('ANGIOSPERMA', 0) > 0 : pontos['ANGIOSPERMA'] -= 1

        return pontos

    def _processar_sugestao_com_pontos(self, pontos, nome_identificacao, opcoes_validas_fallback, permitir_escolha_manual_direta=True):
        """Lógica base para determinar a sugestão com base nos pontos e pedir confirmação."""

        if not any(p > 0 for p in pontos.values()):
            print(f"\nNão foi possível sugerir {nome_identificacao.lower()} com base nas respostas iniciais.")
            if permitir_escolha_manual_direta:
                 return self.aux_entrada.pedir_entrada_numerada(
                    f"Por favor, informe {nome_identificacao.lower()}:",
                    opcoes_validas_fallback,
                    nome_identificacao
                )
            return None

        tipos_ordenados_inicial = sorted(pontos.items(), key=lambda item: item[1], reverse=True)

        is_tie_at_top = False
        tipos_empatados_nomes = []

        if len(tipos_ordenados_inicial) > 1 and tipos_ordenados_inicial[0][1] > 0:
            pontuacao_maxima = tipos_ordenados_inicial[0][1]
            if tipos_ordenados_inicial[1][1] == pontuacao_maxima:
                is_tie_at_top = True
                tipos_empatados_nomes = [t[0] for t in tipos_ordenados_inicial if t[1] == pontuacao_maxima]

        pontos_finais = pontos.copy()

        if is_tie_at_top and nome_identificacao == "Tipo de Planta" and len(tipos_empatados_nomes) > 1:
            print(f"\nDetectado empate na pontuação para {nome_identificacao} entre: {', '.join(tipos_empatados_nomes)}.")
            pontos_finais = self._desempatar_tipo_planta(pontos_finais, tipos_empatados_nomes)

        tipos_ordenados_final = sorted(pontos_finais.items(), key=lambda item: item[1], reverse=True)

        if not any(p > 0 for p in pontos_finais.values()):
             print(f"\nApós perguntas de desempate, não foi possível determinar {nome_identificacao.lower()} com clareza.")
             if permitir_escolha_manual_direta:
                return self.aux_entrada.pedir_entrada_numerada(
                    f"Por favor, informe {nome_identificacao.lower()}:",
                    opcoes_validas_fallback,
                    nome_identificacao
                )
             return None

        sugestao_principal = tipos_ordenados_final[0][0]

        print(f"\n--- Resultado Final da Identificação para {nome_identificacao} ---")
        print("Pontuações (maior = mais provável):")
        for tipo, ponto in tipos_ordenados_final:
            print(f"- {tipo.capitalize()}: {pontos_finais.get(tipo, 0)} pontos")

        print(f"\nSugestão final: {nome_identificacao} parece ser {sugestao_principal.capitalize()}.")

        if len(tipos_ordenados_final) > 1 and tipos_ordenados_final[1][1] > 0:
            segundo_tipo_nome = tipos_ordenados_final[1][0]
            segundo_tipo_pontos = tipos_ordenados_final[1][1]
            pontuacao_sugestao_principal = tipos_ordenados_final[0][1]

            if sugestao_principal != segundo_tipo_nome and (pontuacao_sugestao_principal - segundo_tipo_pontos <= 2):
                 print(f"Observação: O tipo {segundo_tipo_nome.capitalize()} também apresentou uma pontuação considerável ({segundo_tipo_pontos} pontos).")

        opcoes_confirmacao_validas = ('Sim', 'Nao', 'Escolher manualmente')
        opcoes_confirmacao_normalizadas = [self.aux_entrada.remover_acentos(opc.upper()) for opc in opcoes_confirmacao_validas]

        confirmacao_resposta = self.aux_entrada.pedir_confirmacao(
            f"Você concorda com a sugestão de '{sugestao_principal.capitalize()}'?",
            opcoes_confirmacao_validas
        )

        if confirmacao_resposta == opcoes_confirmacao_normalizadas[0]: # SIM
            return sugestao_principal
        else:
            print("Ok, por favor, selecione manualmente.")
            return self.aux_entrada.pedir_entrada_numerada(
                f"Qual é {nome_identificacao.lower()}?",
                opcoes_validas_fallback,
                nome_identificacao
            )

    def identificar_tipo_planta(self):
        print("\n--- Identificação do Tipo da Planta ---")
        print("Para ajudar a definir os melhores cuidados, vamos tentar identificar o tipo da sua planta.")
        print("  - Briófitas: Plantas pequenas (ex: musgos), geralmente em locais úmidos, sem flores ou sementes visíveis.")
        print("  - Pteridófitas: Como samambaias e avencas. Têm folhas, mas não produzem flores nem sementes; usam esporos.")
        print("  - Gimnospermas: Como pinheiros e araucárias. Produzem sementes 'nuas' (ex: pinhas), sem flores verdadeiras.")
        print("  - Angiospermas: O grupo mais comum. São as plantas que dão flores e frutos (que protegem as sementes).")

        pontos = {'BRIOFITA': 0, 'PTERIDOFITA': 0, 'GIMNOSPERMA': 0, 'ANGIOSPERMA': 0}
        resp_frutos = ""

        resp_flores = self.aux_entrada.pedir_entrada_numerada(
            "A planta costuma produzir flores?",
            ['Sim, produz flores', 'Nao produz flores', 'Nao sei / Nao observei'],
            "Presença de flores"
        )
        if resp_flores == self.aux_entrada.remover_acentos('Sim, produz flores'.upper()): pontos['ANGIOSPERMA'] += 3
        elif resp_flores == self.aux_entrada.remover_acentos('Nao produz flores'.upper()):
            pontos['BRIOFITA'] += 1; pontos['PTERIDOFITA'] += 1; pontos['GIMNOSPERMA'] += 1

        if resp_flores != self.aux_entrada.remover_acentos('Nao produz flores'.upper()):
            resp_frutos = self.aux_entrada.pedir_entrada_numerada(
                "A planta produz frutos (estruturas com sementes)?",
                ['Sim, produz frutos', 'Nao produz frutos', 'Nao sei / Nao observei'],
                "Presença de frutos"
            )
            if resp_frutos == self.aux_entrada.remover_acentos('Sim, produz frutos'.upper()):
                pontos['ANGIOSPERMA'] += 3
                if pontos.get('GIMNOSPERMA', 0) > 0: pontos['GIMNOSPERMA'] = 0
                if pontos.get('PTERIDOFITA', 0) > 0: pontos['PTERIDOFITA'] = 0
                if pontos.get('BRIOFITA', 0) > 0: pontos['BRIOFITA'] = 0
            elif resp_frutos == self.aux_entrada.remover_acentos('Nao produz frutos'.upper()):
                if resp_flores == self.aux_entrada.remover_acentos('Sim, produz flores'.upper()): pontos['ANGIOSPERMA'] += 1
                else: pontos['GIMNOSPERMA'] += 1

        resp_sementes = self.aux_entrada.pedir_entrada_numerada(
            "Você observa sementes na planta? Se sim, como são?",
            ['Nao sao observadas sementes',
             'Sementes expostas (ex: pinhas), nao dentro de um fruto',
             'Sementes dentro de frutos',
             'Nao sei / Nao observei'],
            "Tipo de sementes"
        )
        if resp_sementes == self.aux_entrada.remover_acentos('Nao sao observadas sementes'.upper()):
            pontos['BRIOFITA'] += 2; pontos['PTERIDOFITA'] += 2
        elif resp_sementes == self.aux_entrada.remover_acentos('Sementes expostas (ex: pinhas), nao dentro de um fruto'.upper()):
            pontos['GIMNOSPERMA'] += 3
            if pontos.get('ANGIOSPERMA', 0) > 0 and resp_frutos != self.aux_entrada.remover_acentos('Sim, produz frutos'.upper()):
                pontos['ANGIOSPERMA'] = 0
        elif resp_sementes == self.aux_entrada.remover_acentos('Sementes dentro de frutos'.upper()):
            pontos['ANGIOSPERMA'] += 3
            if pontos.get('GIMNOSPERMA', 0) > 0: pontos['GIMNOSPERMA'] = 0

        resp_porte = self.aux_entrada.pedir_entrada_numerada(
            "Qual o porte (tamanho geral) da planta?",
            ['Muito pequena, rasteira ou formando tapete (ate 15 cm)',
             'Pequena a media (15 cm a 1 metro), herbacea ou caule fino',
             'Media a grande, arbusto ou arvore (acima de 1 metro)'],
            "Porte da planta"
        )
        if resp_porte == self.aux_entrada.remover_acentos('Muito pequena, rasteira ou formando tapete (ate 15 cm)'.upper()):
            pontos['BRIOFITA'] += 3; pontos['PTERIDOFITA'] += 1
        elif resp_porte == self.aux_entrada.remover_acentos('Pequena a media (15 cm a 1 metro), herbacea ou caule fino'.upper()):
            pontos['PTERIDOFITA'] += 2; pontos['ANGIOSPERMA'] += 1; pontos['GIMNOSPERMA'] += 1
        elif resp_porte == self.aux_entrada.remover_acentos('Media a grande, arbusto ou arvore (acima de 1 metro)'.upper()):
            pontos['GIMNOSPERMA'] += 2; pontos['ANGIOSPERMA'] += 2

        resp_folhas = self.aux_entrada.pedir_entrada_numerada(
            "Como são as folhas predominantes da planta?",
            ['Estruturas muito pequenas/delicadas, tipo escamas (musgos)',
             'Folhas grandes e divididas (samambaias), as vezes com esporos',
             'Folhas em forma de agulha ou escamas (pinheiros, ciprestes)',
             'Folhas com formatos variados (largas, finas, etc.), com nervuras',
             'Nao parece ter folhas verdadeiras, mas estruturas achatadas/filamentosas'],
            "Tipo de folhas"
        )
        if resp_folhas == self.aux_entrada.remover_acentos('Estruturas muito pequenas/delicadas, tipo escamas (musgos)'.upper()): pontos['BRIOFITA'] += 3
        elif resp_folhas == self.aux_entrada.remover_acentos('Folhas grandes e divididas (samambaias), as vezes com esporos'.upper()): pontos['PTERIDOFITA'] += 3
        elif resp_folhas == self.aux_entrada.remover_acentos('Folhas em forma de agulha ou escamas (pinheiros, ciprestes)'.upper()): pontos['GIMNOSPERMA'] += 3
        elif resp_folhas == self.aux_entrada.remover_acentos('Folhas com formatos variados (largas, finas, etc.), com nervuras'.upper()): pontos['ANGIOSPERMA'] += 2
        elif resp_folhas == self.aux_entrada.remover_acentos('Nao parece ter folhas verdadeiras, mas estruturas achatadas/filamentosas'.upper()): pontos['BRIOFITA'] += 2

        resp_estrutura = self.aux_entrada.pedir_entrada_numerada(
            "A planta tem caule/folhas firmes (sugere vasos condutores) ou é delicada e absorve umidade do ambiente?",
            ['Estrutura firme, caule/folhas bem definidos',
             'Estrutura delicada, dependente da umidade ambiente'],
            "Estrutura geral"
        )
        if resp_estrutura == self.aux_entrada.remover_acentos('Estrutura firme, caule/folhas bem definidos'.upper()):
            pontos['PTERIDOFITA'] += 1; pontos['GIMNOSPERMA'] += 1; pontos['ANGIOSPERMA'] += 1
        elif resp_estrutura == self.aux_entrada.remover_acentos('Estrutura delicada, dependente da umidade ambiente'.upper()): pontos['BRIOFITA'] += 2

        return self._processar_sugestao_com_pontos(pontos, "Tipo de Planta", TIPOS_PLANTA_VALIDOS)

    def identificar_umidade_solo(self):
        print("\n--- Identificação da Umidade do Solo ---")
        pontos = {'MUITO SECO': 0, 'SECO': 0, 'MEDIA': 0, 'UMIDO': 0, 'ENCHARCADO': 0}

        resp_toque = self.aux_entrada.pedir_entrada_numerada(
            "Ao inserir o dedo uns 2-3 cm no solo, como você o sente?",
            ['Totalmente seco, esfarelento, poeirento',
             'Seco na superfície, mas levemente menos seco abaixo',
             'Levemente úmido, como uma esponja bem torcida',
             'Claramente úmido, a terra gruda um pouco no dedo',
             'Molhado, a água quase escorre se apertado',
             'Encharcado, água visível na superfície ou escorrendo do vaso'],
            "Umidade do solo ao toque"
        )
        if resp_toque == self.aux_entrada.remover_acentos('Totalmente seco, esfarelento, poeirento'.upper()): pontos['MUITO SECO'] += 3
        elif resp_toque == self.aux_entrada.remover_acentos('Seco na superfície, mas levemente menos seco abaixo'.upper()): pontos['SECO'] += 3
        elif resp_toque == self.aux_entrada.remover_acentos('Levemente úmido, como uma esponja bem torcida'.upper()): pontos['MEDIA'] += 3
        elif resp_toque == self.aux_entrada.remover_acentos('Claramente úmido, a terra gruda um pouco no dedo'.upper()): pontos['UMIDO'] += 3
        elif resp_toque == self.aux_entrada.remover_acentos('Molhado, a água quase escorre se apertado'.upper()): pontos['UMIDO'] += 2; pontos['ENCHARCADO'] +=1
        elif resp_toque == self.aux_entrada.remover_acentos('Encharcado, água visível na superfície ou escorrendo do vaso'.upper()): pontos['ENCHARCADO'] += 3

        return self._processar_sugestao_com_pontos(pontos, "Umidade do Solo", UMIDADES_VALIDAS)

    def identificar_iluminacao_local(self):
        print("\n--- Identificação da Iluminação do Local ---")
        pontos = {'MUITO BAIXA': 0, 'BAIXA': 0, 'MODERADA': 0, 'ALTA': 0, 'MUITO ALTA': 0}

        resp_sol_direto = self.aux_entrada.pedir_entrada_numerada(
            "A planta recebe luz solar direta? Se sim, por quantas horas aproximadamente?",
            ['Nenhuma luz solar direta', 'Menos de 2 horas de sol direto fraco (inicio/fim do dia)',
             'Entre 2-4 horas de sol direto', 'Entre 4-6 horas de sol direto', 'Mais de 6 horas de sol direto forte'],
            "Horas de sol direto"
        )
        if resp_sol_direto == self.aux_entrada.remover_acentos('Nenhuma luz solar direta'.upper()): pontos['MUITO BAIXA'] +=1; pontos['BAIXA'] +=1; pontos['MODERADA'] +=1
        elif resp_sol_direto == self.aux_entrada.remover_acentos('Menos de 2 horas de sol direto fraco (inicio/fim do dia)'.upper()): pontos['MODERADA'] += 2; pontos['BAIXA'] +=1
        elif resp_sol_direto == self.aux_entrada.remover_acentos('Entre 2-4 horas de sol direto'.upper()): pontos['ALTA'] += 2; pontos['MODERADA'] +=1
        elif resp_sol_direto == self.aux_entrada.remover_acentos('Entre 4-6 horas de sol direto'.upper()): pontos['ALTA'] += 2; pontos['MUITO ALTA'] +=1
        elif resp_sol_direto == self.aux_entrada.remover_acentos('Mais de 6 horas de sol direto forte'.upper()): pontos['MUITO ALTA'] += 3

        resp_intensidade_indireta = self.aux_entrada.pedir_entrada_numerada(
            "Qual a intensidade da luz INDIRETA no local na maior parte do dia?",
            ['Escuro, dificil de ler (ex: corredor sem janela)',
             'Luz suficiente para leitura confortavel, mas sem sol (ex: perto de janela norte/sombra externa)',
             'Luz clara e abundante, ambiente bem iluminado (ex: perto de janela leste/oeste com luz filtrada)',
             'Muito claro, quase como sol direto fraco (ex: varanda coberta muito iluminada)'],
            "Intensidade da luz indireta"
        )
        if resp_intensidade_indireta == self.aux_entrada.remover_acentos('Escuro, dificil de ler (ex: corredor sem janela)'.upper()): pontos['MUITO BAIXA'] += 2
        elif resp_intensidade_indireta == self.aux_entrada.remover_acentos('Luz suficiente para leitura confortavel, mas sem sol (ex: perto de janela norte/sombra externa)'.upper()): pontos['BAIXA'] += 2; pontos['MODERADA'] += 1
        elif resp_intensidade_indireta == self.aux_entrada.remover_acentos('Luz clara e abundante, ambiente bem iluminado (ex: perto de janela leste/oeste com luz filtrada)'.upper()): pontos['MODERADA'] += 2; pontos['ALTA'] += 1
        elif resp_intensidade_indireta == self.aux_entrada.remover_acentos('Muito claro, quase como sol direto fraco (ex: varanda coberta muito iluminada)'.upper()): pontos['ALTA'] += 2

        return self._processar_sugestao_com_pontos(pontos, "Iluminação do Local", ILUMINACOES_VALIDAS)

class Planta:
    """Representa a planta do usuário."""
    def __init__(self, nome_popular, tipo=None):
        self.nome_popular = nome_popular.capitalize() if nome_popular else "Planta Desconhecida"
        self.tipo = tipo

class CondicoesAmbientais:
    """Armazena as condições ambientais da planta."""
    def __init__(self, estacao=None, umidade_solo=None, iluminacao_local=None, frequencia_rega_atual=None):
        self.estacao = estacao
        self.umidade_solo = umidade_solo
        self.iluminacao_local = iluminacao_local
        self.frequencia_rega_atual = frequencia_rega_atual

class SistemaRecomendacao:
    """Gera recomendações de cuidados com base na planta e no ambiente."""

    def __init__(self, aux_entrada):
        self.aux_entrada = aux_entrada
        self._cuidados_gerados = []
        self._frequencia_rega_sugerida_final = None
        self._razao_rega_sugerida_final = "Monitoramento padrão."


    def _adicionar_cuidado(self, mensagem):
        if mensagem and mensagem not in self._cuidados_gerados:
            self._cuidados_gerados.append(mensagem)

    def _definir_sugestao_rega(self, frequencia, razao, prioridade, sugestoes_atuais):
        sugestoes_atuais.append({'freq': frequencia, 'razao': razao, 'prioridade': prioridade})

    def _resolver_conflitos_rega(self, planta, condicoes):
        sugestoes_rega_candidatas = []

        # PRIORIDADE 6: Plantas com necessidades extremas
        if planta.nome_popular.upper() in ['CACTO', 'SUCULENTA']:
            if condicoes.umidade_solo not in ['MUITO SECO', 'SECO'] or \
               (condicoes.frequencia_rega_atual != 'QUINZENAL' and condicoes.frequencia_rega_atual is not None) :
                self._definir_sugestao_rega('QUINZENAL',
                                           f"{planta.nome_popular} é uma planta de deserto e prefere solo muito seco entre as regas. A rega excessiva pode ser fatal.",
                                           6, sugestoes_rega_candidatas)
        elif planta.nome_popular.upper() == 'VITORIA-REGIA':
             pass # Tratado na umidade, não frequência

        # PRIORIDADE 5: Condições críticas de umidade
        if condicoes.umidade_solo == 'ENCHARCADO' and planta.tipo != 'BRIOFITA' and planta.nome_popular.upper() != 'VITORIA-REGIA':
            self._definir_sugestao_rega('QUINZENAL',
                                       "O solo está encharcado. É crucial reduzir drasticamente a rega para permitir que as raízes respirem e evitar o apodrecimento, que pode matar a planta.",
                                       5, sugestoes_rega_candidatas)
        elif condicoes.umidade_solo == 'MUITO SECO' and planta.nome_popular.upper() not in ['CACTO', 'SUCULENTA']:
            self._definir_sugestao_rega('DIARIA',
                                       "O solo está muito seco. A maioria das plantas (exceto as de deserto) precisa de umidade para sobreviver. Regar diariamente ajudará a reidratar o solo e a planta.",
                                       5, sugestoes_rega_candidatas)

        # PRIORIDADE 4: Necessidades do TIPO de planta
        if planta.tipo == 'BRIOFITA' and planta.nome_popular.upper() != 'MUSGO SECO':
            if condicoes.umidade_solo not in ['UMIDO', 'ENCHARCADO']:
                self._definir_sugestao_rega('DIARIA',
                                           "Briófitas, como musgos, são plantas que não possuem raízes verdadeiras para buscar água profundamente e dependem de alta umidade constante no ambiente e no solo para se manterem hidratadas.",
                                           4, sugestoes_rega_candidatas)
        elif planta.tipo == 'ANGIOSPERMA' and planta.nome_popular.upper() not in ['CACTO', 'SUCULENTA', 'VITORIA-REGIA']:
            if condicoes.umidade_solo == 'MUITO SECO':
                self._definir_sugestao_rega('DUAS VEZES NA SEMANA',
                                           f"Angiospermas (como {planta.nome_popular}) com solo muito seco precisam de um aumento na rega para atingir uma umidade média, ideal para a maioria delas. Comece com duas vezes na semana e observe.",
                                           4, sugestoes_rega_candidatas)
            elif condicoes.umidade_solo == 'ENCHARCADO':
                 self._definir_sugestao_rega('SEMANAL',
                                            f"Para Angiospermas (como {planta.nome_popular}) com solo encharcado, é importante reduzir a rega para semanal, permitindo que o excesso de água drene e o solo seque um pouco, evitando problemas nas raízes.",
                                            4, sugestoes_rega_candidatas)

        # PRIORIDADE 3: Ajustes sazonais (baseados na FREQUÊNCIA ATUAL)
        if condicoes.frequencia_rega_atual:
            if condicoes.estacao in ['PRIMAVERA','VERAO'] and condicoes.frequencia_rega_atual in ['SEMANAL', 'QUINZENAL'] and \
               planta.tipo != 'GIMNOSPERMA' and planta.nome_popular.upper() not in ['CACTO', 'SUCULENTA', 'MUSGO SECO']:
                self._definir_sugestao_rega('DUAS VEZES NA SEMANA',
                                           f"Durante estações quentes como {condicoes.estacao.lower()}, as plantas tendem a perder mais água pela transpiração e o solo seca mais rápido. Com sua rega atual de {condicoes.frequencia_rega_atual.lower()}, pode ser necessário aumentar para duas vezes na semana.",
                                           3, sugestoes_rega_candidatas)
            elif condicoes.estacao in ['OUTONO','INVERNO'] and condicoes.frequencia_rega_atual in ['DIARIA', 'DUAS VEZES NA SEMANA'] and \
                 planta.tipo not in ['BRIOFITA', 'PTERIDOFITA'] and planta.nome_popular.upper() != 'VITORIA-REGIA':
                self._definir_sugestao_rega('SEMANAL',
                                           f"Em estações mais frias como {condicoes.estacao.lower()}, o metabolismo da planta diminui e a evaporação do solo é menor. Sua rega atual de {condicoes.frequencia_rega_atual.lower()} pode ser excessiva. Reduzir para semanal ajuda a evitar o encharcamento.",
                                           3, sugestoes_rega_candidatas)

        # PRIORIDADE 2: Ajustes gerais de umidade (se não cobertos por regras mais fortes)
        if condicoes.umidade_solo == 'SECO' and \
           (condicoes.frequencia_rega_atual is None or condicoes.frequencia_rega_atual in ['SEMANAL', 'QUINZENAL']) and \
           planta.nome_popular.upper() not in ['CACTO', 'PINHEIRO', 'SUCULENTA']:
            self._definir_sugestao_rega('DUAS VEZES NA SEMANA',
                                       "O solo está seco e sua rega atual é espaçada. Aumentar para duas vezes na semana pode fornecer a umidade necessária para a maioria das plantas que não são de clima árido.",
                                       2, sugestoes_rega_candidatas)
        elif condicoes.umidade_solo == 'UMIDO' and \
             (condicoes.frequencia_rega_atual is None or condicoes.frequencia_rega_atual in ['DIARIA', 'DUAS VEZES NA SEMANA']) and \
             planta.tipo not in ['BRIOFITA', 'PTERIDOFITA'] and planta.nome_popular.upper() != 'VITORIA-REGIA':
            self._definir_sugestao_rega('SEMANAL',
                                       "O solo já está úmido e sua rega é frequente. Diminuir para semanal permite que a superfície do solo seque um pouco entre as regas, o que é benéfico para a aeração das raízes da maioria das plantas.",
                                       2, sugestoes_rega_candidatas)

        if sugestoes_rega_candidatas:
            sugestoes_rega_candidatas.sort(key=lambda x: x['prioridade'], reverse=True)
            sugestao_final_obj = sugestoes_rega_candidatas[0]
            self._frequencia_rega_sugerida_final = sugestao_final_obj['freq']
            self._razao_rega_sugerida_final = sugestao_final_obj['razao']

            if condicoes.frequencia_rega_atual and self._frequencia_rega_sugerida_final != condicoes.frequencia_rega_atual:
                self._adicionar_cuidado(
                    f"RECOMENDAÇÃO DE REGA: Mude a frequência de '{condicoes.frequencia_rega_atual.lower()}' para '{self._frequencia_rega_sugerida_final.lower()}'.\n   Motivo: {self._razao_rega_sugerida_final}"
                )
            elif not condicoes.frequencia_rega_atual:
                 self._adicionar_cuidado(
                    f"RECOMENDAÇÃO DE REGA: Sugerimos uma frequência de '{self._frequencia_rega_sugerida_final.lower()}'.\n   Motivo: {self._razao_rega_sugerida_final}"
                )
            else:
                 self._adicionar_cuidado(
                    f"REGA: A frequência atual de '{condicoes.frequencia_rega_atual.lower()}' parece adequada, considerando: {self._razao_rega_sugerida_final}"
                )
        elif condicoes.frequencia_rega_atual:
            self._adicionar_cuidado(f"REGA: Mantenha a frequência de rega atual ({condicoes.frequencia_rega_atual.lower()}) e observe a planta. Nenhuma mudança urgente foi identificada com base nas informações fornecidas.")
            self._frequencia_rega_sugerida_final = condicoes.frequencia_rega_atual
        else:
            self._adicionar_cuidado("REGA: Não foi possível determinar uma frequência de rega ideal com os dados. Monitore a umidade do solo e as necessidades da planta para definir uma rotina.")
            self._frequencia_rega_sugerida_final = None


    def gerar_recomendacoes(self, planta, condicoes):
        self._cuidados_gerados = []
        self._frequencia_rega_sugerida_final = None
        self._razao_rega_sugerida_final = "Monitoramento padrão."

        self._resolver_conflitos_rega(planta, condicoes)

        if condicoes.iluminacao_local == 'MUITO BAIXA':
            self._adicionar_cuidado(f"ILUMINAÇÃO: Está {condicoes.iluminacao_local.lower()}. A maioria das plantas precisa de luz para fotossíntese. Mova {planta.nome_popular} para um local com mais luz indireta, se possível.")
        elif condicoes.iluminacao_local == 'MUITO ALTA' and planta.tipo != 'GIMNOSPERMA' and planta.nome_popular.upper() not in ['CACTO', 'SUCULENTA']:
            self._adicionar_cuidado(f"ILUMINAÇÃO: Está {condicoes.iluminacao_local.lower()}. Se {planta.nome_popular} não for uma planta de sol pleno, a luz solar direta e intensa pode queimar suas folhas. Mova para local com luz filtrada ou menos horas de sol direto.")

        if planta.tipo == 'BRIOFITA' and planta.nome_popular.upper() != 'MUSGO SECO':
            self._adicionar_cuidado(f"TIPO ({planta.tipo}): {planta.nome_popular} (Briófita) prefere ambientes consistentemente úmidos e sombreados, pois absorve água e nutrientes diretamente pelas suas estruturas delicadas.")
            if condicoes.iluminacao_local in ['ALTA', 'MUITO ALTA']:
                self._adicionar_cuidado(f"  -> Iluminação atual ({condicoes.iluminacao_local.lower()}) é excessiva para Briófitas. Mova para local com iluminação BAIXA ou MODERADA, protegida do sol direto forte, que pode dessecá-la rapidamente.")
            if condicoes.umidade_solo not in ['UMIDO', 'ENCHARCADO']:
                self._adicionar_cuidado(f"  -> Solo atual ({condicoes.umidade_solo.lower()}) está seco para Briófitas. Elas precisam de alta umidade. Considere borrifar água nas folhas/ambiente frequentemente para manter a umidade elevada.")

        elif planta.tipo == 'PTERIDOFITA':
            self._adicionar_cuidado(f"TIPO ({planta.tipo}): {planta.nome_popular} (Pteridófita), como samambaias, geralmente se desenvolve bem em locais com umidade no ar e no solo, e luz indireta ou filtrada, similar ao seu ambiente natural de sub-bosque.")
            if condicoes.iluminacao_local not in ['BAIXA', 'MODERADA']:
                self._adicionar_cuidado(f"  -> Iluminação atual ({condicoes.iluminacao_local.lower()}) pode ser inadequada. Prefira locais com iluminação MODERADA ou BAIXA (luz filtrada), evitando sol direto que pode queimar as folhas delicadas.")
            if condicoes.umidade_solo not in ['MEDIA', 'UMIDO']:
                self._adicionar_cuidado(f"  -> Solo atual ({condicoes.umidade_solo.lower()}) pode estar seco. Pteridófitas apreciam solo consistentemente úmido (mas não encharcado para a maioria das espécies de vaso).")

        elif planta.tipo == 'GIMNOSPERMA':
            self._adicionar_cuidado(f"TIPO ({planta.tipo}): {planta.nome_popular} (Gimnosperma), como pinheiros, geralmente são plantas robustas que preferem sol pleno para um bom desenvolvimento e solo que permita boa drenagem da água.")
            if condicoes.iluminacao_local not in ['ALTA', 'MUITO ALTA']:
                self._adicionar_cuidado(f"  -> Iluminação atual ({condicoes.iluminacao_local.lower()}) pode ser insuficiente. Gimnospermas geralmente precisam de bastante sol direto. Mova para local com iluminação ALTA, se possível.")
            if condicoes.umidade_solo not in ['SECO', 'MEDIA'] and condicoes.umidade_solo != 'MUITO SECO':
                 self._adicionar_cuidado(f"  -> Solo atual ({condicoes.umidade_solo.lower()}) pode estar muito úmido. Gimnospermas preferem solos que sequem bem entre as regas para evitar problemas radiculares.")

        elif planta.tipo == 'ANGIOSPERMA' and planta.nome_popular.upper() not in ['CACTO', 'SUCULENTA', 'VITORIA-REGIA']:
            self._adicionar_cuidado(f"TIPO ({planta.tipo}): {planta.nome_popular} (Angiosperma) pertence ao grupo mais diverso de plantas. As necessidades específicas variam muito, mas geralmente apreciam luz adequada à sua espécie e uma rega equilibrada, evitando extremos de secura ou encharcamento prolongados.")
            if condicoes.iluminacao_local not in ['MODERADA', 'ALTA'] and condicoes.iluminacao_local != 'MUITO ALTA':
                 self._adicionar_cuidado(f"  -> Iluminação atual ({condicoes.iluminacao_local.lower()}) pode não ser ideal. Muitas Angiospermas precisam de luz MODERADA a ALTA. Verifique a necessidade específica da sua planta (ex: plantas de sombra, meia-sombra ou sol pleno).")

        if planta.nome_popular.upper() in ['CACTO', 'SUCULENTA']:
            self._adicionar_cuidado(f"ESPECÍFICO ({planta.nome_popular}): Esta planta é adaptada a ambientes áridos e armazena água em suas estruturas. Excesso de água é o principal risco.")
            if condicoes.iluminacao_local not in ['MUITO ALTA', 'ALTA']:
                self._adicionar_cuidado(f"  -> Iluminação atual ({condicoes.iluminacao_local.lower()}) é baixa para Cactos/Suculentas. Elas precisam de muita luz solar direta. Mude para iluminação MUITO ALTA ou ALTA.")

        elif planta.nome_popular.upper() == 'VITORIA-REGIA':
            self._adicionar_cuidado(f"ESPECÍFICO ({planta.nome_popular}): Esta é uma planta aquática que vive com suas raízes submersas e folhas flutuando na água.")
            if condicoes.umidade_solo != 'ENCHARCADO':
                self._adicionar_cuidado(f"  -> Solo atual ({condicoes.umidade_solo.lower()}) não é adequado. A Vitória-Régia precisa estar em ambiente constantemente ENCHARCADO, ou seja, dentro d'água.")
            if condicoes.iluminacao_local != 'MUITO ALTA':
                 self._adicionar_cuidado(f"  -> Iluminação atual ({condicoes.iluminacao_local.lower()}) é baixa. A Vitória-Régia necessita de sol pleno (MUITO ALTA iluminação) para um bom desenvolvimento.")

        self._adicionar_cuidado(f"GERAL: Monitore regularmente {planta.nome_popular} quanto a sinais de pragas (pulgões, cochonilhas, etc.) ou doenças (manchas nas folhas, mofo). Inspecione folhas (ambos os lados), caules e raízes (se possível ao transplantar) quinzenalmente.")
        self._adicionar_cuidado(f"GERAL: A adubação fornece nutrientes essenciais que podem faltar no substrato. Pesquise as necessidades específicas de {planta.nome_popular} e a época ideal para adubar (geralmente na estação de crescimento).")
        self._adicionar_cuidado(f"GERAL: Observe a temperatura ambiente. Proteja {planta.nome_popular} de mudanças bruscas, geadas (se não for resistente) ou calor excessivo, dependendo das suas necessidades de origem.")

        if not self._cuidados_gerados:
            self._adicionar_cuidado(f"Nenhuma recomendação específica gerada para {planta.nome_popular} com os parâmetros atuais. Verifique as condições gerais da planta e pesquise sobre suas necessidades específicas.")

        return self._cuidados_gerados

# --- Início do Programa Principal ---
if __name__ == "__main__":
    aux_entrada = AuxiliarEntrada()
    identificador = Identificador(aux_entrada)
    sistema_recomendacao = SistemaRecomendacao(aux_entrada)

    print("--- Bem-vindo ao Sistema Especialista em Cuidados com Plantas ---\n")

    nome_planta_input = input("Qual é o nome popular da sua planta? (Ex: Samambaia, Cacto, Roseira): ").strip()
    planta_atual = Planta(nome_planta_input)

    planta_atual.tipo = identificador.identificar_tipo_planta()
    if not planta_atual.tipo:
        print("Tipo de planta não definido. Encerrando o programa.")
        exit()
    print(f"Tipo de planta definido como: {planta_atual.tipo.capitalize()}")


    print("\n--- Coleta de Informações do Ambiente ---")
    estacao_informada = aux_entrada.pedir_entrada_numerada(
        "Qual é a estação do ano atual?",
        ESTACOES_VALIDAS,
        "Estação do Ano"
    )
    umidade_identificada = identificador.identificar_umidade_solo()
    iluminacao_identificada = identificador.identificar_iluminacao_local()

    frequencia_rega_usuario = aux_entrada.pedir_entrada_numerada(
        "Qual a frequência com que você costuma regar a planta atualmente?",
        FREQUENCIAS_REGA_VALIDAS,
        "Frequência de Rega Atual"
    )

    if not all([estacao_informada, umidade_identificada, iluminacao_identificada, frequencia_rega_usuario]):
        print("Uma ou mais informações do ambiente não foram definidas. Encerrando o programa.")
        exit()


    condicoes_atuais = CondicoesAmbientais(
        estacao_informada,
        umidade_identificada,
        iluminacao_identificada,
        frequencia_rega_usuario
    )
    print(f"\nCondições registradas: Estação ({condicoes_atuais.estacao.capitalize()}), Umidade ({condicoes_atuais.umidade_solo.capitalize()}), Iluminação ({condicoes_atuais.iluminacao_local.capitalize()}), Rega Atual ({condicoes_atuais.frequencia_rega_atual.capitalize()})")

    cuidados_finais = sistema_recomendacao.gerar_recomendacoes(planta_atual, condicoes_atuais)

    print(f"\n--- Cuidados Recomendados para {planta_atual.nome_popular} ({planta_atual.tipo.capitalize()}) ---")
    if cuidados_finais:
        for i, cuidado in enumerate(cuidados_finais):
            print(f"{i + 1}. {cuidado}")
    else:
        print("Não foi possível gerar recomendações específicas com os dados fornecidos.")

    print("\nLembre-se: estas são sugestões gerais. Observe sempre sua planta e ajuste os cuidados conforme necessário!")
