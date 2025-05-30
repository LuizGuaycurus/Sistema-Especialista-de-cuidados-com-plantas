import unicodedata

# Constantes globais
TIPOS_PLANTA_VALIDOS = ['BRIOFITA', 'PTERIDOFITA', 'GIMNOSPERMA', 'ANGIOSPERMA']
ESTACOES_VALIDAS = ['VERAO', 'INVERNO', 'OUTONO', 'PRIMAVERA']
UMIDADES_VALIDAS = ['MUITO SECO', 'SECO', 'MEDIA', 'UMIDO', 'ENCHARCADO']
ILUMINACOES_VALIDAS = ['MUITO BAIXA', 'BAIXA', 'MODERADA', 'ALTA', 'MUITO ALTA']
FREQUENCIAS_REGA_VALIDAS = ['DIARIA', 'DUAS VEZES NA SEMANA', 'SEMANAL', 'QUINZENAL']

# --- Novas Constantes para Detalhes Adicionais ---
LOCAL_PLANTIO_OPCOES = ["EM VASO OU RECIPIENTE", "DIRETAMENTE NO CHAO/JARDIM"] # Nova constante
VASO_MATERIAIS = ["BARRO/TERRACOTA (SECA MAIS RAPIDO)", "PLASTICO (RETEM MAIS UMIDADE)", 
                  "CERAMICA ESMALTADA (RETEM UMIDADE)", "CIMENTO (PODE ALTERAR PH, RETEM UMIDADE)",
                  "FIBRA DE COCO (BOM AREJAMENTO, SECA MODERADAMENTE)", 
                  "AUTOIRRIGAVEL (RESERVATORIO DE AGUA)", "OUTRO/NAO SEI"]
VASO_DRENAGENS = ["SIM, POSSUI FUROS E A AGUA ESCOA BEM", 
                  "SIM, POSSUI FUROS MAS A DRENAGEM PARECE LENTA", 
                  "NAO POSSUI FUROS VISIVEIS (RISCO ALTO!)", 
                  "NAO TENHO CERTEZA/USO CACHEPO SEM FURO DIRETO"]
SUBSTRATO_TIPOS = ["TERRA COMUM DE JARDIM (PODE COMPACTAR EM VASOS)", # Ajuste na descrição
                   "SUBSTRATO COMPRADO PRONTO (LEVE, COM PERLITA/FIBRA, ETC.)", 
                   "MISTURA CASEIRA COM MUITA AREIA (DRENA MUITO RAPIDO)", 
                   "MISTURA CASEIRA RICA EM MATERIA ORGANICA (HUMUS, ESTERCO)", 
                   "SOLO ORIGINAL DO LOCAL (PARA PLANTAS DIRETAMENTE NO CHAO)", # Ajuste na descrição
                   "NAO SEI DESCREVER"]
VENTILACAO_LOCAIS = ["BEM VENTILADO, BRISA SUAVE FREQUENTE", 
                     "VENTILACAO MODERADA, AR CIRCULA SEM VENTO FORTE", 
                     "POUCO VENTILADO, AR PARADO NA MAIOR PARTE DO TEMPO", 
                     "RECEBE CORRENTES DE AR FORTES E DIRETAS (EX: CORREDOR DE VENTO)"]
PROXIMIDADE_FONTES_CALOR_FRIO = ["SIM, PERTO DE JANELA COM SOL DA TARDE MUITO FORTE", 
                                 "SIM, DIRETAMENTE SOB/EM FRENTE A SAIDA DE AR CONDICIONADO/AQUECEDOR", 
                                 "SIM, PERTO DE FORNO/FOGAO USADO FREQUENTEMENTE", 
                                 "NAO, LONGE DESSAS FONTES DIRETAS"]
IDADE_PLANTA_OPCOES = ["MUDA RECEM-PLANTADA/ADQUIRIDA (MENOS DE 3 MESES)", 
                       "PLANTA JOVEM, CRESCIMENTO ATIVO (3 MESES A 1-2 ANOS)", 
                       "PLANTA ADULTA, ESTABELECIDA (MAIS DE 1-2 ANOS)", 
                       "PLANTA MUITO ANTIGA/IDOSA (APARENCIA DE DECLINIO NATURAL)"]
HISTORICO_PROBLEMAS_OPCOES = ["SIM, TEVE PRAGAS (PULGOES, COCHONILHAS, ETC.) RECENTEMENTE (ULTIMOS 2 MESES)", 
                              "SIM, TEVE DOENCAS (MANCHAS, MOFO, ETC.) RECENTEMENTE (ULTIMOS 2 MESES)", 
                              "NAO, SEM PROBLEMAS SIGNIFICATIVOS NOS ULTIMOS MESES", 
                              "NAO SEI/NAO OBSERVEI"]
ADUBACAO_QUANDO_OPCOES = ["ESTA SEMANA", "NO ULTIMO MES (ATE 30 DIAS)", 
                          "ENTRE 1 A 3 MESES ATRAS", "MAIS DE 3 MESES ATRAS", 
                          "NUNCA ADUBEI / NAO LEMBRO"]
ADUBACAO_TIPO_OPCOES = ["ADUBO ORGANICO (HUMUS, ESTERCO, BOKASHI, ETC.)", 
                        "ADUBO QUIMICO NPK (GRANULADO OU LIQUIDO)", 
                        "ADUBO FOLIAR (APLICADO NAS FOLHAS)", 
                        "ADUBO ESPECIFICO PARA [FLORES/FRUTOS/ORQUIDEAS, ETC.]", 
                        "NAO SEI O TIPO / NAO ADUBEI"]
TRANSPLANTE_RECENTE_OPCOES = ["SIM, NA ULTIMA SEMANA", "SIM, NO ULTIMO MES", 
                              "SIM, ENTRE 1 A 3 MESES ATRAS", 
                              "NAO, FAZ MAIS DE 3 MESES OU NUNCA FOI TRANSPLANTADA (SE EM VASO)"]
QUALIDADE_AGUA_OPCOES = ["AGUA DA TORNEIRA DIRETAMENTE", 
                         "AGUA DA TORNEIRA DESCANSADA (PARA EVAPORAR CLORO)", 
                         "AGUA FILTRADA", "AGUA DA CHUVA COLETADA", 
                         "AGUA DE POCO/MINA (VERIFICAR QUALIDADE)", "OUTRA"]
METODO_REGA_OPCOES = ["MOLHANDO A TERRA POR CIMA ATE ESCORRER UM POUCO NO PRATO (SE EM VASO)", 
                      "MOLHANDO A TERRA POR CIMA, MAS SEM DEIXAR ESCORRER (SE EM VASO)",
                      "MOLHANDO A AREA AO REDOR DA PLANTA (SE NO CHAO)",
                      "COLOCANDO AGUA APENAS NO PRATINHO PARA A PLANTA ABSORVER POR BAIXO (SE EM VASO)", 
                      "IMERSAO DO VASO NA AGUA POR UM TEMPO (SE EM VASO)", 
                      "APENAS BORRIFO AGUA NAS FOLHAS (NAO E REGA EFETIVA PARA O SOLO)"]
PODA_RECENTE_OPCOES = ["SIM, PODA DE LIMPEZA (FOLHAS/GALHOS SECOS) RECENTEMENTE", 
                       "SIM, PODA DE FORMACAO/MANUTENCAO RECENTEMENTE", 
                       "SIM, PODA MAIS DRASTICA RECENTEMENTE", 
                       "NAO FOI PODADA NOS ULTIMOS MESES"]


class AuxiliarEntrada:
    """Classe para lidar com entradas e validações do usuário."""

    def remover_acentos(self, texto):
        if not isinstance(texto, str): return ""
        return "".join(c for c in unicodedata.normalize('NFD', texto) if not unicodedata.combining(c))

    def pedir_entrada_numerada(self, pergunta, opcoes_para_pergunta, nome_caracteristica):
        print(f"\n{pergunta}")
        for i, opcao in enumerate(opcoes_para_pergunta):
            opcao_display = " ".join(word.capitalize() for word in opcao.split())
            print(f"  {i + 1}. {opcao_display}")
        while True:
            try:
                resposta_num_str = input(f"Escolha o número da opção para '{nome_caracteristica.capitalize()}': ").strip()
                if not resposta_num_str: print("Entrada vazia. Por favor, digite um número."); continue
                resposta_num = int(resposta_num_str)
                if 1 <= resposta_num <= len(opcoes_para_pergunta):
                    return self.remover_acentos(opcoes_para_pergunta[resposta_num - 1].upper())
                else: print(f"Número inválido. Escolha entre 1 e {len(opcoes_para_pergunta)}.")
            except ValueError: print("Entrada inválida. Digite apenas o número da opção.")
            except Exception as e: print(f"Ocorreu um erro: {e}. Tente novamente.")

    def pedir_confirmacao(self, pergunta_confirmacao, opcoes_confirmacao=('Sim', 'Nao', 'Escolher manualmente')):
        opcoes_confirmacao_lista = list(opcoes_confirmacao)
        return self.pedir_entrada_numerada(pergunta_confirmacao, opcoes_confirmacao_lista, "Confirmação")

class DetalhesAdicionais:
    """Armazena detalhes adicionais sobre a planta e suas condições."""
    def __init__(self, local_plantio=None, tipo_vaso_material=None, tipo_vaso_drenagem=None, # Adicionado local_plantio
                 tipo_substrato=None, ventilacao_local=None,
                 proximidade_calor_frio=None, idade_planta=None,
                 historico_problemas=None, ultima_adubacao_quando=None,
                 ultima_adubacao_tipo=None, transplante_recente=None,
                 qualidade_agua=None, metodo_rega=None, poda_recente=None):
        self.local_plantio = local_plantio
        self.tipo_vaso_material = tipo_vaso_material
        self.tipo_vaso_drenagem = tipo_vaso_drenagem
        self.tipo_substrato = tipo_substrato
        self.ventilacao_local = ventilacao_local
        self.proximidade_calor_frio = proximidade_calor_frio
        self.idade_planta = idade_planta
        self.historico_problemas = historico_problemas
        self.ultima_adubacao_quando = ultima_adubacao_quando
        self.ultima_adubacao_tipo = ultima_adubacao_tipo
        self.transplante_recente = transplante_recente
        self.qualidade_agua = qualidade_agua
        self.metodo_rega = metodo_rega
        self.poda_recente = poda_recente

class Identificador:
    """Classe para identificar características da planta e do ambiente por pontuação."""

    def __init__(self, aux_entrada):
        self.aux_entrada = aux_entrada

    def _desempatar_tipo_planta(self, pontos, tipos_empatados_nomes):
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

    def coletar_detalhes_vaso_substrato(self):
        print("\n--- Detalhes sobre o Local de Plantio, Vaso e Substrato ---")
        local_plantio = self.aux_entrada.pedir_entrada_numerada(
            "A planta está em um vaso/recipiente ou plantada diretamente no chão/jardim?",
            LOCAL_PLANTIO_OPCOES, # Usando a nova constante
            "Local de Plantio"
        )

        material_vaso = "NAO_APLICAVEL_CHAO" # Valor padrão se plantada no chão
        drenagem_vaso = "NAO_APLICAVEL_CHAO" # Valor padrão se plantada no chão

        # Só pergunta sobre vaso se a planta estiver em um
        if local_plantio == self.aux_entrada.remover_acentos("EM VASO OU RECIPIENTE".upper()):
            material_vaso = self.aux_entrada.pedir_entrada_numerada(
                "Material principal do vaso:",
                VASO_MATERIAIS,
                "Material do Vaso"
            )
            drenagem_vaso = self.aux_entrada.pedir_entrada_numerada(
                "Drenagem do vaso (furos no fundo):",
                VASO_DRENAGENS,
                "Drenagem do Vaso"
            )
        
        tipo_substrato = self.aux_entrada.pedir_entrada_numerada(
            "Como você descreveria o solo/substrato onde a planta está?",
            SUBSTRATO_TIPOS,
            "Tipo de Solo/Substrato"
        )
        return local_plantio, material_vaso, drenagem_vaso, tipo_substrato # Retorna local_plantio também

    def coletar_detalhes_ambiente_especifico(self):
        print("\n--- Detalhes Adicionais do Ambiente ---")
        ventilacao = self.aux_entrada.pedir_entrada_numerada("Ventilação no local da planta:", VENTILACAO_LOCAIS, "Ventilação")
        prox_calor_frio = self.aux_entrada.pedir_entrada_numerada("Proximidade a fontes de calor/frio (ar condicionado, janela com sol forte, etc.):", PROXIMIDADE_FONTES_CALOR_FRIO, "Proximidade Calor/Frio")
        return ventilacao, prox_calor_frio

    def coletar_historico_planta(self):
        print("\n--- Histórico e Características da Planta ---")
        idade = self.aux_entrada.pedir_entrada_numerada("Estágio de desenvolvimento da planta:", IDADE_PLANTA_OPCOES, "Idade da Planta")
        hist_problemas = self.aux_entrada.pedir_entrada_numerada("Histórico recente de pragas ou doenças (últimos 2 meses):", HISTORICO_PROBLEMAS_OPCOES, "Histórico de Problemas")
        transplante = self.aux_entrada.pedir_entrada_numerada("Transplante recente (mudança de vaso/local, se aplicável):", TRANSPLANTE_RECENTE_OPCOES, "Transplante Recente")
        return idade, hist_problemas, transplante

    def coletar_detalhes_cuidados_habituais(self):
        print("\n--- Detalhes Adicionais sobre seus Cuidados Habituais ---")
        adub_quando = self.aux_entrada.pedir_entrada_numerada("Última vez que adubou esta planta:", ADUBACAO_QUANDO_OPCOES, "Última Adubação")
        adub_tipo = "NAO SE APLICA" # Valor padrão
        if adub_quando != self.aux_entrada.remover_acentos("NUNCA ADUBEI / NAO LEMBRO".upper()):
            adub_tipo = self.aux_entrada.pedir_entrada_numerada("Tipo de adubo utilizado (se souber):", ADUBACAO_TIPO_OPCOES, "Tipo de Adubo")
        
        qualidade_agua = self.aux_entrada.pedir_entrada_numerada("Qualidade da água usada na rega:", QUALIDADE_AGUA_OPCOES, "Qualidade da Água")
        metodo_rega = self.aux_entrada.pedir_entrada_numerada("Principal método de rega utilizado:", METODO_REGA_OPCOES, "Método de Rega")
        poda = self.aux_entrada.pedir_entrada_numerada("Poda recente na planta:", PODA_RECENTE_OPCOES, "Poda Recente")
        return adub_quando, adub_tipo, qualidade_agua, metodo_rega, poda


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

    def _resolver_conflitos_rega(self, planta, condicoes, detalhes_adicionais): 
        sugestoes_rega_candidatas = []
        
        # Verifica se a planta está em vaso para adicionar comentários sobre o material do vaso
        planta_em_vaso = detalhes_adicionais and detalhes_adicionais.local_plantio == self.aux_entrada.remover_acentos("EM VASO OU RECIPIENTE".upper())
        razao_material_vaso = ""

        if planta_em_vaso and detalhes_adicionais.tipo_vaso_material:
            if "BARRO" in detalhes_adicionais.tipo_vaso_material:
                razao_material_vaso = "Lembre-se que vasos de barro tendem a secar o substrato mais rapidamente. "
            elif "PLASTICO" in detalhes_adicionais.tipo_vaso_material or "CERAMICA ESMALTADA" in detalhes_adicionais.tipo_vaso_material:
                razao_material_vaso = "Vasos de plástico ou cerâmica esmaltada retêm mais umidade, observe bem antes de regar novamente. "
        
        # PRIORIDADE 6: Plantas com necessidades extremas
        if planta.nome_popular.upper() in ['CACTO', 'SUCULENTA']:
            if condicoes.umidade_solo not in ['MUITO SECO', 'SECO'] or \
               (condicoes.frequencia_rega_atual != 'QUINZENAL' and condicoes.frequencia_rega_atual is not None) :
                self._definir_sugestao_rega('QUINZENAL', 
                                           f"{planta.nome_popular} é uma planta de deserto e prefere solo muito seco entre as regas. A rega excessiva pode ser fatal. {razao_material_vaso}", 
                                           6, sugestoes_rega_candidatas)
        elif planta.nome_popular.upper() == 'VITORIA-REGIA':
             pass

        # PRIORIDADE 5: Condições críticas de umidade
        if condicoes.umidade_solo == 'ENCHARCADO' and planta.tipo != 'BRIOFITA' and planta.nome_popular.upper() != 'VITORIA-REGIA':
            alerta_drenagem = "Verifique a drenagem do vaso." if planta_em_vaso else "Se for uma área do jardim com má drenagem, considere melhorá-la."
            self._definir_sugestao_rega('QUINZENAL', 
                                       f"O solo está encharcado. É crucial reduzir drasticamente a rega para permitir que as raízes respirem e evitar o apodrecimento. {razao_material_vaso}{alerta_drenagem}", 
                                       5, sugestoes_rega_candidatas)
        elif condicoes.umidade_solo == 'MUITO SECO' and planta.nome_popular.upper() not in ['CACTO', 'SUCULENTA']:
            self._definir_sugestao_rega('DIARIA', 
                                       f"O solo está muito seco. A maioria das plantas precisa de umidade para sobreviver. Regar diariamente ajudará a reidratar. {razao_material_vaso}", 
                                       5, sugestoes_rega_candidatas)

        # PRIORIDADE 4: Necessidades do TIPO de planta
        if planta.tipo == 'BRIOFITA' and planta.nome_popular.upper() != 'MUSGO SECO':
            if condicoes.umidade_solo not in ['UMIDO', 'ENCHARCADO']:
                self._definir_sugestao_rega('DIARIA', 
                                           f"Briófitas dependem de alta umidade constante. {razao_material_vaso}", 
                                           4, sugestoes_rega_candidatas)
        elif planta.tipo == 'ANGIOSPERMA' and planta.nome_popular.upper() not in ['CACTO', 'SUCULENTA', 'VITORIA-REGIA']:
            if condicoes.umidade_solo == 'MUITO SECO':
                self._definir_sugestao_rega('DUAS VEZES NA SEMANA', 
                                           f"Angiospermas com solo muito seco precisam de aumento na rega para umidade média. {razao_material_vaso}", 
                                           4, sugestoes_rega_candidatas)
            elif condicoes.umidade_solo == 'ENCHARCADO': 
                 self._definir_sugestao_rega('SEMANAL', 
                                            f"Para Angiospermas com solo encharcado, reduza a rega, permitindo que o excesso drene. {razao_material_vaso}", 
                                            4, sugestoes_rega_candidatas)

        # PRIORIDADE 3: Ajustes sazonais
        if condicoes.frequencia_rega_atual: 
            if condicoes.estacao in ['PRIMAVERA','VERAO'] and condicoes.frequencia_rega_atual in ['SEMANAL', 'QUINZENAL'] and \
               planta.tipo != 'GIMNOSPERMA' and planta.nome_popular.upper() not in ['CACTO', 'SUCULENTA', 'MUSGO SECO']:
                self._definir_sugestao_rega('DUAS VEZES NA SEMANA', 
                                           f"Em estações quentes ({condicoes.estacao.lower()}), as plantas perdem mais água. Com rega atual de {condicoes.frequencia_rega_atual.lower()}, aumente. {razao_material_vaso}", 
                                           3, sugestoes_rega_candidatas)
            elif condicoes.estacao in ['OUTONO','INVERNO'] and condicoes.frequencia_rega_atual in ['DIARIA', 'DUAS VEZES NA SEMANA'] and \
                 planta.tipo not in ['BRIOFITA', 'PTERIDOFITA'] and planta.nome_popular.upper() != 'VITORIA-REGIA':
                self._definir_sugestao_rega('SEMANAL', 
                                           f"Em estações frias ({condicoes.estacao.lower()}), o metabolismo da planta diminui. Rega atual de {condicoes.frequencia_rega_atual.lower()} pode ser excessiva. {razao_material_vaso}", 
                                           3, sugestoes_rega_candidatas)

        # PRIORIDADE 2: Ajustes gerais de umidade
        if condicoes.umidade_solo == 'SECO' and \
           (condicoes.frequencia_rega_atual is None or condicoes.frequencia_rega_atual in ['SEMANAL', 'QUINZENAL']) and \
           planta.nome_popular.upper() not in ['CACTO', 'PINHEIRO', 'SUCULENTA']:
            self._definir_sugestao_rega('DUAS VEZES NA SEMANA', 
                                       f"Solo seco e rega atual espaçada. Aumentar pode fornecer umidade necessária. {razao_material_vaso}", 
                                       2, sugestoes_rega_candidatas)
        elif condicoes.umidade_solo == 'UMIDO' and \
             (condicoes.frequencia_rega_atual is None or condicoes.frequencia_rega_atual in ['DIARIA', 'DUAS VEZES NA SEMANA']) and \
             planta.tipo not in ['BRIOFITA', 'PTERIDOFITA'] and planta.nome_popular.upper() != 'VITORIA-REGIA':
            self._definir_sugestao_rega('SEMANAL', 
                                       f"Solo úmido e rega frequente. Diminuir permite aeração das raízes. {razao_material_vaso}", 
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
            self._adicionar_cuidado(f"REGA: Mantenha a frequência de rega atual ({condicoes.frequencia_rega_atual.lower()}) e observe. Nenhuma mudança urgente identificada. {razao_material_vaso}")
            self._frequencia_rega_sugerida_final = condicoes.frequencia_rega_atual
        else:
            self._adicionar_cuidado(f"REGA: Monitore umidade e necessidades para definir rotina. {razao_material_vaso}")
            self._frequencia_rega_sugerida_final = None


    def gerar_recomendacoes(self, planta, condicoes, detalhes_adicionais): 
        self._cuidados_gerados = []
        self._frequencia_rega_sugerida_final = None
        self._razao_rega_sugerida_final = "Monitoramento padrão."

        self._resolver_conflitos_rega(planta, condicoes, detalhes_adicionais) 
        
        planta_em_vaso = detalhes_adicionais and detalhes_adicionais.local_plantio == self.aux_entrada.remover_acentos("EM VASO OU RECIPIENTE".upper())

        if detalhes_adicionais:
            if planta_em_vaso: # Só mostra alertas de vaso se estiver em vaso
                if "NAO POSSUI FUROS" in detalhes_adicionais.tipo_vaso_drenagem:
                    self._adicionar_cuidado(f"ALERTA VASO: Seu vaso ('{detalhes_adicionais.tipo_vaso_drenagem.split('(')[0].strip()}') indica ausência de furos de drenagem. Isso é CRÍTICO e pode levar ao apodrecimento das raízes e morte da planta. Providencie furos ou troque de vaso URGENTEMENTE.")
                elif "DRENAGEM PARECE LENTA" in detalhes_adicionais.tipo_vaso_drenagem:
                    self._adicionar_cuidado(f"ATENÇÃO VASO: A drenagem lenta ('{detalhes_adicionais.tipo_vaso_drenagem.split('(')[0].strip()}') pode reter umidade excessiva. Verifique se os furos não estão obstruídos ou considere adicionar material drenante no fundo do vaso (argila expandida, brita) na próxima troca de substrato.")

            if "TERRA COMUM DE JARDIM" in detalhes_adicionais.tipo_substrato and planta_em_vaso: # Relevante principalmente para vasos
                self._adicionar_cuidado(f"SUBSTRATO: Terra comum de jardim tende a compactar em vasos, dificultando a aeração das raízes e a drenagem. Para plantas em vaso, prefira substratos comprados prontos ou misturas caseiras mais leves.")
            elif "MISTURA CASEIRA COM MUITA AREIA" in detalhes_adicionais.tipo_substrato:
                self._adicionar_cuidado(f"SUBSTRATO: Solos muito arenosos secam extremamente rápido, exigindo regas mais frequentes. Observe se a planta não está desidratando rapidamente, especialmente se estiver em vaso.")
            
            if "POUCO VENTILADO" in detalhes_adicionais.ventilacao_local:
                self._adicionar_cuidado(f"VENTILAÇÃO: Ambientes pouco ventilados podem aumentar a umidade ao redor da planta, o que é bom para algumas, mas pode favorecer fungos em outras. Tente melhorar a circulação de ar se possível, sem criar correntes diretas.")
            elif "CORRENTES DE AR FORTES" in detalhes_adicionais.ventilacao_local:
                self._adicionar_cuidado(f"VENTILAÇÃO: Correntes de ar fortes podem desidratar a planta rapidamente e causar estresse. Se possível, proteja a planta dessas correntes.")

            if "NAO, LONGE DESSAS FONTES DIRETAS" not in detalhes_adicionais.proximidade_calor_frio:
                self._adicionar_cuidado(f"AMBIENTE: A proximidade a fontes de calor/frio ('{detalhes_adicionais.proximidade_calor_frio.split('(')[0].strip()}') pode causar estresse, queimaduras ou desidratação. Monitore a planta de perto e considere afastá-la se notar problemas.")
            
            if "MUDA RECEM-PLANTADA" in detalhes_adicionais.idade_planta:
                self._adicionar_cuidado(f"IDADE: Mudas recém-plantadas são mais sensíveis. Evite adubação forte inicialmente, proteja de sol extremo e mantenha o substrato levemente úmido (sem encharcar) para ajudar no estabelecimento das raízes.")
            
            if "NAO, SEM PROBLEMAS SIGNIFICATIVOS" not in detalhes_adicionais.historico_problemas and "NAO SEI" not in detalhes_adicionais.historico_problemas:
                self._adicionar_cuidado(f"HISTÓRICO: Como a planta teve problemas recentes ('{detalhes_adicionais.historico_problemas.split('(')[0].strip()}'), fique atento a qualquer sinal de reaparecimento. Mantenha a planta fortalecida com os cuidados adequados.")

            if "NUNCA ADUBEI" in detalhes_adicionais.ultima_adubacao_quando:
                self._adicionar_cuidado(f"ADUBAÇÃO: Você mencionou que nunca adubou ou não lembra. A maioria das plantas (especialmente em vasos) se beneficia de adubação periódica para repor nutrientes. Pesquise sobre o tipo e frequência ideal para {planta.nome_popular}.")
            elif "ESTA SEMANA" in detalhes_adicionais.ultima_adubacao_quando or "NO ULTIMO MES" in detalhes_adicionais.ultima_adubacao_quando :
                 self._adicionar_cuidado(f"ADUBAÇÃO: Como a planta foi adubada recentemente ({detalhes_adicionais.ultima_adubacao_quando.lower()}), geralmente não é necessário adubar novamente por um tempo. Siga as instruções do adubo utilizado ('{detalhes_adicionais.ultima_adubacao_tipo.split('(')[0].strip()}').")
            
            if "NAO, FAZ MAIS DE 3 MESES" not in detalhes_adicionais.transplante_recente and planta_em_vaso: # Transplante é mais relevante para vasos
                self._adicionar_cuidado(f"TRANSPLANTE: Plantas recém-transplantadas ('{detalhes_adicionais.transplante_recente.split(',')[0].strip()}') passam por um estresse. Evite sol forte direto e adubação nas primeiras semanas. Mantenha o solo levemente úmido.")

            if "APENAS BORRIFO AGUA NAS FOLHAS" in detalhes_adicionais.metodo_rega:
                self._adicionar_cuidado(f"MÉTODO DE REGA: Borrifar água nas folhas NÃO substitui a rega do solo para a maioria das plantas, pois as raízes precisam absorver a água. Certifique-se de que o substrato está sendo adequadamente umedecido.")
            elif "COLOCANDO AGUA APENAS NO PRATINHO" in detalhes_adicionais.metodo_rega and planta_em_vaso:
                 self._adicionar_cuidado(f"MÉTODO DE REGA: Regar por baixo (pelo pratinho) pode ser eficaz, mas certifique-se de que toda a terra no vaso está umedecendo. Após 30 min a 1 hora, descarte a água que sobrou no prato para evitar encharcamento e mosquitos.")

        if condicoes.iluminacao_local == 'MUITO BAIXA':
            self._adicionar_cuidado(f"ILUMINAÇÃO: Está {condicoes.iluminacao_local.lower()}. Mova {planta.nome_popular} para um local com mais luz indireta, se possível.")
        elif condicoes.iluminacao_local == 'MUITO ALTA' and planta.tipo != 'GIMNOSPERMA' and planta.nome_popular.upper() not in ['CACTO', 'SUCULENTA']:
            self._adicionar_cuidado(f"ILUMINAÇÃO: Está {condicoes.iluminacao_local.lower()}. Se {planta.nome_popular} não for de sol pleno, mova para local com luz filtrada ou menos intensa para evitar queimaduras.")

        if planta.tipo == 'BRIOFITA' and planta.nome_popular.upper() != 'MUSGO SECO':
            self._adicionar_cuidado(f"TIPO ({planta.tipo}): {planta.nome_popular} prefere ambientes úmidos e sombreados.")
            if condicoes.iluminacao_local in ['ALTA', 'MUITO ALTA']:
                self._adicionar_cuidado(f"  -> Iluminação atual ({condicoes.iluminacao_local.lower()}) é excessiva. Mova para local com iluminação BAIXA ou MODERADA. Evite sol direto forte.")
            if condicoes.umidade_solo not in ['UMIDO', 'ENCHARCADO']: 
                self._adicionar_cuidado(f"  -> Solo atual ({condicoes.umidade_solo.lower()}) está seco para briófitas. Elas precisam de alta umidade. Considere borrifar água nas folhas/ambiente.")
        
        elif planta.tipo == 'PTERIDOFITA': 
            self._adicionar_cuidado(f"TIPO ({planta.tipo}): {planta.nome_popular}, como samambaias, geralmente gosta de umidade e luz indireta.")
            if condicoes.iluminacao_local not in ['BAIXA', 'MODERADA']:
                self._adicionar_cuidado(f"  -> Iluminação atual ({condicoes.iluminacao_local.lower()}) pode ser inadequada. Prefira locais com iluminação MODERADA ou BAIXA (luz filtrada).")
            if condicoes.umidade_solo not in ['MEDIA', 'UMIDO']: 
                self._adicionar_cuidado(f"  -> Solo atual ({condicoes.umidade_solo.lower()}) pode estar seco. Mantenha o solo consistentemente úmido (mas não encharcado).")

        elif planta.tipo == 'GIMNOSPERMA':
            self._adicionar_cuidado(f"TIPO ({planta.tipo}): {planta.nome_popular}, como pinheiros, geralmente prefere sol pleno e solo bem drenado.")
            if condicoes.iluminacao_local not in ['ALTA', 'MUITO ALTA']:
                self._adicionar_cuidado(f"  -> Iluminação atual ({condicoes.iluminacao_local.lower()}) pode ser insuficiente. Gimnospermas geralmente precisam de bastante sol. Mova para local com iluminação ALTA.")
            if condicoes.umidade_solo not in ['SECO', 'MEDIA'] and condicoes.umidade_solo != 'MUITO SECO': 
                 self._adicionar_cuidado(f"  -> Solo atual ({condicoes.umidade_solo.lower()}) pode estar muito úmido. Prefira solos que sequem bem entre as regas.")
        
        elif planta.tipo == 'ANGIOSPERMA' and planta.nome_popular.upper() not in ['CACTO', 'SUCULENTA', 'VITORIA-REGIA']:
            self._adicionar_cuidado(f"TIPO ({planta.tipo}): {planta.nome_popular} pertence a um grupo diverso. As necessidades variam, mas geralmente apreciam luz adequada e rega equilibrada.")
            if condicoes.iluminacao_local not in ['MODERADA', 'ALTA'] and condicoes.iluminacao_local != 'MUITO ALTA': 
                 self._adicionar_cuidado(f"  -> Iluminação atual ({condicoes.iluminacao_local.lower()}) pode não ser ideal. Muitas angiospermas precisam de luz MODERADA a ALTA.")

        if planta.nome_popular.upper() in ['CACTO', 'SUCULENTA']:
            self._adicionar_cuidado(f"ESPECÍFICO ({planta.nome_popular}): Planta adaptada a ambientes secos.")
            if condicoes.iluminacao_local not in ['MUITO ALTA', 'ALTA']:
                self._adicionar_cuidado(f"  -> Iluminação atual ({condicoes.iluminacao_local.lower()}) é baixa. {planta.nome_popular} precisa de muita luz. Mude para iluminação MUITO ALTA ou ALTA.")
        
        elif planta.nome_popular.upper() == 'VITORIA-REGIA':
            self._adicionar_cuidado(f"ESPECÍFICO ({planta.nome_popular}): Planta aquática.")
            if condicoes.umidade_solo != 'ENCHARCADO':
                self._adicionar_cuidado(f"  -> Solo atual ({condicoes.umidade_solo.lower()}) não é adequado. Precisa estar em ambiente constantemente ENCHARCADO.")
            if condicoes.iluminacao_local != 'MUITO ALTA':
                 self._adicionar_cuidado(f"  -> Iluminação atual ({condicoes.iluminacao_local.lower()}) é baixa. {planta.nome_popular} necessita de sol pleno (MUITO ALTA iluminação).")
        
        self._adicionar_cuidado(f"GERAL: Monitore regularmente {planta.nome_popular} quanto a sinais de pragas ou doenças. Inspecione folhas, caules e raízes quinzenalmente.")
        self._adicionar_cuidado(f"GERAL: A adubação pode ser necessária dependendo da planta e do substrato. Pesquise as necessidades específicas de {planta.nome_popular}.")
        self._adicionar_cuidado(f"GERAL: Observe a temperatura ambiente e proteja {planta.nome_popular} de mudanças bruscas ou condições extremas para seu tipo.")


        if not self._cuidados_gerados:
            self._adicionar_cuidado(f"Nenhuma recomendação específica gerada para {planta.nome_popular} com os parâmetros atuais. Verifique as condições gerais da planta.")
        
        return self._cuidados_gerados

# --- Início do Programa Principal ---
if __name__ == "__main__":
    aux_entrada = AuxiliarEntrada()
    identificador = Identificador(aux_entrada)
    sistema_recomendacao = SistemaRecomendacao(aux_entrada)

    print("--- Bem-vindo ao Sistema Especialista em Cuidados com Plantas (vOO Detalhado) ---")
    
    nome_planta_input = input("Qual é o nome popular da sua planta? (Ex: Samambaia, Cacto, Roseira): ").strip()
    planta_atual = Planta(nome_planta_input)
    
    planta_atual.tipo = identificador.identificar_tipo_planta()
    if not planta_atual.tipo:
        print("Tipo de planta não definido. Encerrando o programa.")
        exit()
    print(f"Tipo de planta definido como: {planta_atual.tipo.capitalize()}")

    print("\n--- Coleta de Informações do Ambiente (Básico) ---")
    estacao_informada = aux_entrada.pedir_entrada_numerada("Qual é a estação do ano atual?", ESTACOES_VALIDAS, "Estação do Ano")
    umidade_identificada = identificador.identificar_umidade_solo()
    iluminacao_identificada = identificador.identificar_iluminacao_local()
    frequencia_rega_usuario = aux_entrada.pedir_entrada_numerada("Qual a frequência com que você costuma regar a planta atualmente?", FREQUENCIAS_REGA_VALIDAS, "Frequência de Rega Atual")
    
    if not all([estacao_informada, umidade_identificada, iluminacao_identificada, frequencia_rega_usuario]):
        print("Uma ou mais informações básicas do ambiente não foram definidas. Encerrando o programa.")
        exit()

    condicoes_atuais = CondicoesAmbientais(
        estacao_informada, umidade_identificada, iluminacao_identificada, frequencia_rega_usuario
    )

    # --- Coleta de Detalhes Adicionais ---
    print("\n--- Para recomendações mais precisas, vamos coletar alguns detalhes adicionais ---")
    # Coleta local_plantio primeiro, pois influencia as outras perguntas de vaso/substrato
    loc_plantio, mat_vaso, dren_vaso, tip_substrato = identificador.coletar_detalhes_vaso_substrato()
    vent, prox_calor = identificador.coletar_detalhes_ambiente_especifico()
    idade_p, hist_prob, transp_rec = identificador.coletar_historico_planta()
    adub_q, adub_t, qual_agua, met_rega, poda_rec = identificador.coletar_detalhes_cuidados_habituais()

    detalhes_planta_ambiente = DetalhesAdicionais(
        local_plantio=loc_plantio, # Adicionado local_plantio
        tipo_vaso_material=mat_vaso, tipo_vaso_drenagem=dren_vaso,
        tipo_substrato=tip_substrato, ventilacao_local=vent,
        proximidade_calor_frio=prox_calor, idade_planta=idade_p,
        historico_problemas=hist_prob, ultima_adubacao_quando=adub_q,
        ultima_adubacao_tipo=adub_t, transplante_recente=transp_rec,
        qualidade_agua=qual_agua, metodo_rega=met_rega, poda_recente=poda_rec
    )
    
    print(f"\nCondições básicas registradas: Estação ({condicoes_atuais.estacao.capitalize()}), Umidade ({condicoes_atuais.umidade_solo.capitalize()}), Iluminação ({condicoes_atuais.iluminacao_local.capitalize()}), Rega Atual ({condicoes_atuais.frequencia_rega_atual.capitalize()})")
    print(f"Detalhes adicionais: Local de Plantio ({detalhes_planta_ambiente.local_plantio.capitalize() if detalhes_planta_ambiente.local_plantio else 'N/A'})")


    cuidados_finais = sistema_recomendacao.gerar_recomendacoes(planta_atual, condicoes_atuais, detalhes_planta_ambiente)

    print(f"\n--- Cuidados Recomendados para {planta_atual.nome_popular} ({planta_atual.tipo.capitalize()}) ---")
    if cuidados_finais:
        for i, cuidado in enumerate(cuidados_finais):
            print(f"{i + 1}. {cuidado}")
    else:
        print("Não foi possível gerar recomendações específicas com os dados fornecidos.")

    print("\nLembre-se: estas são sugestões gerais. Observe sempre sua planta e ajuste os cuidados conforme necessário!")

