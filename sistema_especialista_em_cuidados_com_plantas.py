import unicodedata

TIPOS_PLANTA_VALIDOS = ['BRIOFITA', 'PTERIDOFITA', 'GIMNOSPERMA', 'ANGIOSPERMA']
ESTACOES_VALIDAS = ['VERAO', 'INVERNO', 'OUTONO', 'PRIMAVERA']
UMIDADES_VALIDAS = ['MUITO SECO', 'SECO', 'MEDIA', 'UMIDO', 'ENCHARCADO']
ILUMINACOES_VALIDAS = ['MUITO BAIXA', 'BAIXA', 'MODERADA', 'ALTA', 'MUITO ALTA']
FREQUENCIAS_REGA_VALIDAS = ['DIARIA', 'DUAS VEZES NA SEMANA', 'SEMANAL', 'QUINZENAL']

class AuxiliarEntrada:

    def remover_acentos(self, texto):
        if not isinstance(texto, str):
            return ""
        nfkd_form = unicodedata.normalize('NFD', texto)
        return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

    def pedir_entrada_numerada(self, pergunta, opcoes_para_pergunta, nome_caracteristica):
        print(f"\n{pergunta}")
        for i, opcao in enumerate(opcoes_para_pergunta):
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
                    return self.remover_acentos(opcoes_para_pergunta[resposta_num - 1].upper())
                else:
                    print(f"Número inválido. Escolha entre 1 e {len(opcoes_para_pergunta)}.")
            except ValueError:
                print("Entrada inválida. Digite apenas o número da opção.")

    def pedir_confirmacao(self, pergunta_confirmacao, opcoes_confirmacao=('Sim', 'Nao', 'Escolher manualmente')):
        opcoes_confirmacao_lista = list(opcoes_confirmacao)
        resposta_confirmacao_str = self.pedir_entrada_numerada(
            pergunta_confirmacao,
            opcoes_confirmacao_lista,
            "Confirmação"
        )
        return resposta_confirmacao_str


class Identificador:

    def __init__(self, aux_entrada):
        self.aux_entrada = aux_entrada

    def _processar_sugestao_com_pontos(self, pontos, nome_identificacao, opcoes_validas_fallback, permitir_escolha_manual_direta=True):

        if not any(p > 0 for p in pontos.values()):
            print(f"\nNão foi possível sugerir {nome_identificacao} com base nas respostas iniciais.")
            if permitir_escolha_manual_direta:
                return self.aux_entrada.pedir_entrada_numerada(
                    f"Por favor, informe {nome_identificacao}:",opcoes_validas_fallback,nome_identificacao
                )
            return None

        tipos_ordenados_inicial = sorted(pontos.items(), key=lambda item: item[1], reverse=True)

        if len(tipos_ordenados_inicial) > 1 and tipos_ordenados_inicial[0][1] > 0:
            pontuacao_maxima = tipos_ordenados_inicial[0][1]

        pontos_finais = pontos.copy()

        tipos_ordenados_final = sorted(pontos_finais.items(), key=lambda item: item[1], reverse=True)

        if not any(p > 0 for p in pontos_finais.values()):
            print(f"\nApós perguntas de desempate, não foi possível determinar {nome_identificacao} com clareza.")
            if permitir_escolha_manual_direta:
                return self.aux_entrada.pedir_entrada_numerada(
                    f"Por favor, informe {nome_identificacao}:",opcoes_validas_fallback,nome_identificacao
                )
            return None

        sugestao_principal = tipos_ordenados_final[0][0]

        print(f"\n--- Resultado Final da Identificação para {nome_identificacao} ---\n")
        print("Pontuações (maior = mais provável):")
        for tipo, ponto in tipos_ordenados_final:
            print(f"- {tipo.capitalize()}: {ponto} pontos")

        if len(tipos_ordenados_final) > 1 and tipos_ordenados_final[1][1] > 0:
            segundo_tipo_nome = tipos_ordenados_final[1][0]
            segundo_tipo_pontos = tipos_ordenados_final[1][1]
            pontuacao_sugestao_principal = tipos_ordenados_final[0][1]

            if sugestao_principal != segundo_tipo_nome and (pontuacao_sugestao_principal - segundo_tipo_pontos <= 2):
                print(f"Observação: O tipo {segundo_tipo_nome.capitalize()} também apresentou uma pontuação considerável ({segundo_tipo_pontos} pontos).")

        return sugestao_principal

    def identificar_tipo_planta(self):
        print("\n--- Identificação do Tipo da Planta ---\n")
        print("Para ajudar a identificar o tipo da sua planta, responda as seguintes perguntas.")

        pontos = {'BRIOFITA': 0, 'PTERIDOFITA': 0, 'GIMNOSPERMA': 0, 'ANGIOSPERMA': 0}

        resp_flores = self.aux_entrada.pedir_entrada_numerada(
            "A planta costuma produzir flores?",
            ['Sim, produz flores', 'Não produz flores', 'Não sei / Não observei'],
            "Presença de flores"
        )
        if resp_flores == self.aux_entrada.remover_acentos('Sim, produz flores'.upper()):
            pontos['ANGIOSPERMA'] += 5
            pontos['GIMNOSPERMA'] += 1
        elif resp_flores == self.aux_entrada.remover_acentos('Não produz flores'.upper()):
            pontos['BRIOFITA'] += 5
            pontos['PTERIDOFITA'] += 5
            pontos['GIMNOSPERMA'] += 4

        resp_frutos = ""
        if resp_flores != self.aux_entrada.remover_acentos('Não produz flores'.upper()):
            resp_frutos = self.aux_entrada.pedir_entrada_numerada(
                "A planta produz frutos?",
                ['Sim, produz frutos', 'Não produz frutos', 'Não sei / Não observei'],
                "Presença de frutos"
            )
            if resp_frutos == self.aux_entrada.remover_acentos('Sim, produz frutos'.upper()):
                pontos['ANGIOSPERMA'] += 5
            elif resp_frutos == self.aux_entrada.remover_acentos('Não produz frutos'.upper()):
                pontos['GIMNOSPERMA'] += 4
                pontos['ANGIOSPERMA'] += 1
                pontos['BRIOFITA'] += 5
                pontos['PTERIDOFITA'] += 5

        resp_sementes = self.aux_entrada.pedir_entrada_numerada(
            "Você observa sementes na planta?",
            ['Não são observadas sementes',
             'Sementes expostas, não dentro de um fruto',
             'Sementes dentro de frutos'],
            "Tipo de sementes"
        )
        if resp_sementes == self.aux_entrada.remover_acentos('Não são observadas sementes'.upper()):
            pontos['BRIOFITA'] += 5
            pontos['PTERIDOFITA'] += 5
        elif resp_sementes == self.aux_entrada.remover_acentos('Sementes expostas, não dentro de um fruto'.upper()):
            pontos['GIMNOSPERMA'] += 5
            pontos['ANGIOSPERMA'] += 1
        elif resp_sementes == self.aux_entrada.remover_acentos('Sementes dentro de frutos'.upper()):
            pontos['ANGIOSPERMA'] += 5

        resp_porte = self.aux_entrada.pedir_entrada_numerada(
            "Qual o tamanho da planta?",
            ['Muito pequena ou rasteira (até 15 cm)',
             'Pequena a média (15 cm a 1 metro)',
             'Média a grande (acima de 1 metro)'],
            "Tamanho da planta"
        )
        if resp_porte == self.aux_entrada.remover_acentos('Muito pequena ou rasteira (até 15 cm)'.upper()):
            pontos['BRIOFITA'] += 5
            pontos['PTERIDOFITA'] += 2
        elif resp_porte == self.aux_entrada.remover_acentos('Pequena a média (15 cm a 1 metro)'.upper()):
            pontos['PTERIDOFITA'] += 5
            pontos['ANGIOSPERMA'] += 3
            pontos['GIMNOSPERMA'] += 2
        elif resp_porte == self.aux_entrada.remover_acentos('Média a grande (acima de 1 metro)'.upper()):
            pontos['GIMNOSPERMA'] += 5
            pontos['ANGIOSPERMA'] += 4

        resp_folhas = self.aux_entrada.pedir_entrada_numerada(
            "Como são as folhas da planta?",
            ['Pequenas/delicadas, tipo escamas (musgos)',
             'Folhas grandes e divididas (samambaias), às vezes com esporos',
             'Folhas em forma de agulha (pinheiros, ciprestes)',
             'Folhas largas ou finas com nervuras',
             'Não parece ter folhas verdadeiras, mas estruturas achatadas'],
            "Tipo de folhas"
        )
        if resp_folhas == self.aux_entrada.remover_acentos('Pequenas/delicadas, tipo escamas (musgos)'.upper()):
            pontos['BRIOFITA'] += 4
        elif resp_folhas == self.aux_entrada.remover_acentos('Folhas grandes e divididas (samambaias), às vezes com esporos'.upper()):
            pontos['PTERIDOFITA'] += 5
        elif resp_folhas == self.aux_entrada.remover_acentos('Folhas em forma de agulha (pinheiros, ciprestes)'.upper()):
            pontos['GIMNOSPERMA'] += 5
        elif resp_folhas == self.aux_entrada.remover_acentos('Folhas largas ou finas com nervuras'.upper()):
            pontos['ANGIOSPERMA'] += 4
        elif resp_folhas == self.aux_entrada.remover_acentos('Não parece ter folhas verdadeiras, mas estruturas achatadas'.upper()):
            pontos['BRIOFITA'] += 3

        resp_estrutura = self.aux_entrada.pedir_entrada_numerada(
            "Como é a estrutura da planta?",
            ['Estrutura firme, caule e folhas bem definidos',
             'Estrutura delicada, dependente da umidade ambiente'],
            "Estrutura geral"
        )
        if resp_estrutura == self.aux_entrada.remover_acentos('Estrutura firme, caule e folhas bem definidos'.upper()):
            pontos['PTERIDOFITA'] += 3
            pontos['GIMNOSPERMA'] += 3
            pontos['ANGIOSPERMA'] += 3
        elif resp_estrutura == self.aux_entrada.remover_acentos('Estrutura delicada, dependente da umidade ambiente'.upper()):
            pontos['BRIOFITA'] += 5

        resp_espinhos = self.aux_entrada.pedir_entrada_numerada(
            "A planta possui espinhos visíveis (em folhas, caules ou ramos)?",
            ['Sim, possui espinhos', 'Não possui espinhos', 'Não sei / Não observei'],
            "Presença de espinhos"
        )

        if resp_espinhos == self.aux_entrada.remover_acentos('Sim, possui espinhos'.upper()):
            pontos['ANGIOSPERMA'] += 5
        elif resp_espinhos == self.aux_entrada.remover_acentos('Não possui espinhos'.upper()):
            pontos['ANGIOSPERMA'] += 2
            pontos['GIMNOSPERMA'] += 4
            pontos['PTERIDOFITA'] += 5
            pontos['BRIOFITA'] += 5

        return self._processar_sugestao_com_pontos(pontos, "Tipo de Planta", TIPOS_PLANTA_VALIDOS)

class Planta:

    def __init__(self, nome, tipo=None):
        self.nome = nome.capitalize() if nome else "Planta Desconhecida"
        self.tipo = tipo

class CondicoesAmbientais:

    def __init__(self, estacao=None, umidade_solo=None, iluminacao_local=None, frequencia_rega_atual=None):
        self.estacao = estacao
        self.umidade_solo = umidade_solo
        self.iluminacao_local = iluminacao_local
        self.frequencia_rega_atual = frequencia_rega_atual

class SistemaRecomendacao:

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

        if planta.nome.upper() in ['CACTO', 'SUCULENTA']:
            if condicoes.umidade_solo not in ['MUITO SECO', 'SECO'] or \
               (condicoes.frequencia_rega_atual != 'QUINZENAL' and condicoes.frequencia_rega_atual is not None) :
                self._definir_sugestao_rega('QUINZENAL',
                                           f"{planta.nome.upper()} é uma planta que prefere solo MUITO SECO entre as regas espaçadas.",
                                           6, sugestoes_rega_candidatas)
        elif planta.nome.upper() == 'VITORIA-REGIA':
             pass

        if condicoes.umidade_solo == 'ENCHARCADO' and planta.tipo != 'BRIOFITA' and planta.nome.upper() != 'VITORIA-REGIA':
            self._definir_sugestao_rega('QUINZENAL',"O solo está encharcado. Reduza a rega e evite o apodrecimento, que pode matar a planta.", 5, sugestoes_rega_candidatas)
        elif condicoes.umidade_solo == 'MUITO SECO' and planta.nome.upper() not in ['CACTO', 'SUCULENTA']:
            self._definir_sugestao_rega('DIARIA',
                                       "O solo está MUITO SECO. A maioria das plantas (exceto as de deserto) precisa de umidade para sobreviver. Regar de forma DIÁRIA ajudará a reidratar o solo e a planta.", 5, sugestoes_rega_candidatas)

        if planta.tipo == 'BRIOFITA' and planta.nome.upper() != 'MUSGO SECO':
            if condicoes.umidade_solo not in ['UMIDO', 'ENCHARCADO']:
                self._definir_sugestao_rega('DIARIA',
                                           "Briófitas, como musgos, são plantas que não possuem raízes verdadeiras para buscar água profundamente e dependem de alta umidade constante no ambiente e no solo para se manterem hidratadas.",
                                           4, sugestoes_rega_candidatas)
        elif planta.tipo == 'ANGIOSPERMA' and planta.nome.upper() not in ['CACTO', 'SUCULENTA', 'VITORIA-REGIA']:
            if condicoes.umidade_solo == 'MUITO SECO':
                self._definir_sugestao_rega('DUAS VEZES NA SEMANA',
                                           f"Angiospermas (como {planta.nome.upper()}) com solo muito seco precisam de um aumento na rega para atingir uma umidade média, ideal para a maioria delas. Comece com duas vezes na semana e observe.",
                                           4, sugestoes_rega_candidatas)

        if condicoes.frequencia_rega_atual:
            if condicoes.estacao in ['PRIMAVERA','VERAO'] and condicoes.frequencia_rega_atual in ['SEMANAL', 'QUINZENAL'] and \
               planta.tipo != 'GIMNOSPERMA' and planta.nome.upper() not in ['CACTO', 'SUCULENTA', 'MUSGO SECO']:
                self._definir_sugestao_rega('DUAS VEZES NA SEMANA',
                                           f"Durante estações quentes como {condicoes.estacao.upper()}, as plantas tendem a perder mais água e o solo seca mais rápido. Com sua rega atual de {condicoes.frequencia_rega_atual}, pode ser necessário aumentar para DUAS VEZES NA SEMANA.",
                                           3, sugestoes_rega_candidatas)
            elif condicoes.estacao in ['OUTONO','INVERNO'] and condicoes.frequencia_rega_atual in ['DIARIA', 'DUAS VEZES NA SEMANA'] and \
                 planta.tipo not in ['BRIOFITA', 'PTERIDOFITA'] and planta.nome.upper() != 'VITORIA-REGIA':
                self._definir_sugestao_rega('SEMANAL',
                                           f"Em estações mais frias como {condicoes.estacao.upper()}, o metabolismo da planta diminui e a evaporação do solo é menor. Sua rega atual de {condicoes.frequencia_rega_atual} pode ser excessiva. Reduzir para SEMANAL para evitar o encharcamento.",
                                           3, sugestoes_rega_candidatas)

        if condicoes.umidade_solo == 'SECO' and \
           (condicoes.frequencia_rega_atual is None or condicoes.frequencia_rega_atual in ['SEMANAL', 'QUINZENAL']) and \
           planta.nome.upper() not in ['CACTO', 'PINHEIRO', 'SUCULENTA']:
            self._definir_sugestao_rega('DUAS VEZES NA SEMANA',
                                       "O solo está seco e sua rega atual é espaçada. Aumentar para DUAS VEZES NA SEMANA pode fornecer a umidade necessária para a maioria das plantas que não são de clima árido.",
                                       2, sugestoes_rega_candidatas)
        elif condicoes.umidade_solo == 'UMIDO' and \
             (condicoes.frequencia_rega_atual is None or condicoes.frequencia_rega_atual in ['DIARIA', 'DUAS VEZES NA SEMANA']) and \
             planta.tipo not in ['BRIOFITA', 'PTERIDOFITA'] and planta.nome.upper() != 'VITORIA-REGIA':
            self._definir_sugestao_rega('SEMANAL',
                                       "O solo já está úmido e sua rega é frequente. Diminuir para SEMANAL permite que a superfície do solo seque um pouco entre as regas, o que é benéfico para a aeração das raízes da maioria das plantas.",
                                       2, sugestoes_rega_candidatas)

        if sugestoes_rega_candidatas:
            sugestoes_rega_candidatas.sort(key=lambda x: x['prioridade'], reverse=True)
            sugestao_final_obj = sugestoes_rega_candidatas[0]
            self._frequencia_rega_sugerida_final = sugestao_final_obj['freq']
            self._razao_rega_sugerida_final = sugestao_final_obj['razao']

            if condicoes.frequencia_rega_atual and self._frequencia_rega_sugerida_final != condicoes.frequencia_rega_atual:
                self._adicionar_cuidado(
                    f"RECOMENDAÇÃO DE REGA: Mude a frequência de '{condicoes.frequencia_rega_atual.upper()}' para '{self._frequencia_rega_sugerida_final}'.\n   Motivo: {self._razao_rega_sugerida_final}"
                )
            elif not condicoes.frequencia_rega_atual:
                 self._adicionar_cuidado(
                    f"RECOMENDAÇÃO DE REGA: Sugerimos uma frequência de '{self._frequencia_rega_sugerida_final}'.\n   Motivo: {self._razao_rega_sugerida_final}"
                )
            else:
                 self._adicionar_cuidado(
                    f"REGA: A frequência atual de '{condicoes.frequencia_rega_atual}' parece adequada, considerando: {self._razao_rega_sugerida_final}"
                )
        elif condicoes.frequencia_rega_atual:
            self._adicionar_cuidado(f"REGA: Mantenha a frequência de rega atual ({condicoes.frequencia_rega_atual}). Sem alterações necessárias com base nas informações fornecidas.")
            self._frequencia_rega_sugerida_final = condicoes.frequencia_rega_atual

    def gerar_recomendacoes(self, planta, condicoes):
        self._cuidados_gerados = []
        self._frequencia_rega_sugerida_final = None
        self._razao_rega_sugerida_final = "Monitoramento padrão."

        self._resolver_conflitos_rega(planta, condicoes)

        if condicoes.iluminacao_local == 'MUITO BAIXA':
            self._adicionar_cuidado(f"ILUMINAÇÃO: Está {condicoes.iluminacao_local}. Mova {planta.nome.upper()} para um local com mais luz indireta, se possível.")
        elif condicoes.iluminacao_local == 'MUITO ALTA' and planta.tipo != 'GIMNOSPERMA' and planta.nome.upper() not in ['CACTO', 'SUCULENTA']:
            self._adicionar_cuidado(f"ILUMINAÇÃO: Está {condicoes.iluminacao_local}. Se {planta.nome.upper()} não for uma planta de sol pleno, a luz solar direta e intensa pode queimar suas folhas. Mova para local com menos horas de sol direto.")

        if planta.tipo == 'BRIOFITA' and planta.nome.upper() != 'MUSGO SECO':
            self._adicionar_cuidado(f"TIPO ({planta.tipo}): {planta.nome.upper()} (Briófita) prefere ambientes consistentemente úmidos e sombreados, pois absorve água e nutrientes diretamente pelas suas estruturas delicadas.")
            if condicoes.iluminacao_local == 'ALTA':
                self._adicionar_cuidado(f"  -> Iluminação atual ({condicoes.iluminacao_local}) é excessiva para Briófitas. Mova para local com iluminação BAIXA ou MODERADA, protegida do sol direto forte, que pode dessecá-la rapidamente.")
            if condicoes.umidade_solo not in ['UMIDO', 'ENCHARCADO']:
                self._adicionar_cuidado(f"  -> Solo atual ({condicoes.umidade_solo}) está seco para Briófitas. Elas precisam de alta umidade, regue mais frequentemente para manter a umidade elevada.")

        elif planta.tipo == 'PTERIDOFITA':
            self._adicionar_cuidado(f"TIPO ({planta.tipo}): {planta.nome.upper()} (Pteridófita) geralmente se desenvolve bem em locais com umidade no ar e no solo, e luz indireta ou filtrada, similar ao seu ambiente natural de sub-bosque.")
            if condicoes.iluminacao_local not in ['BAIXA', 'MODERADA']:
                self._adicionar_cuidado(f"  -> Iluminação atual ({condicoes.iluminacao_local}) pode ser inadequada. Prefira locais com iluminação MODERADA ou BAIXA (luz filtrada), evitando sol direto que pode queimar as folhas.")
            if condicoes.umidade_solo not in ['MEDIA', 'UMIDO']:
                self._adicionar_cuidado(f"  -> Solo atual ({condicoes.umidade_solo}) pode estar seco. Pteridófitas apreciam solo consistentemente úmido (mas não encharcado).")

        elif planta.tipo == 'GIMNOSPERMA':
            self._adicionar_cuidado(f"TIPO ({planta.tipo}): {planta.nome.upper()} (Gimnosperma) geralmente são plantas robustas que preferem sol pleno para um bom desenvolvimento e solo que permita boa drenagem da água.")
            if condicoes.iluminacao_local not in ['ALTA', 'MUITO ALTA']:
                self._adicionar_cuidado(f"  -> Iluminação atual ({condicoes.iluminacao_local}) pode ser insuficiente. Gimnospermas geralmente precisam de bastante sol direto. Mova para local com iluminação ALTA, se possível.")
            if condicoes.umidade_solo not in ['SECO', 'MEDIA'] and condicoes.umidade_solo != 'MUITO SECO':
                 self._adicionar_cuidado(f"  -> Solo atual ({condicoes.umidade_solo}) pode estar muito úmido. Gimnospermas preferem solos que sequem bem entre as regas para evitar problemas radiculares.")

        elif planta.tipo == 'ANGIOSPERMA' and planta.nome.upper() not in ['CACTO', 'SUCULENTA', 'VITORIA-REGIA']:
            self._adicionar_cuidado(f"TIPO ({planta.tipo}): {planta.nome.upper()} (Angiosperma) pertence ao grupo mais diverso de plantas. As necessidades específicas variam muito, mas geralmente apreciam luz adequada à sua espécie e uma rega equilibrada, evitando extremos de secura ou encharcamento.")
            if condicoes.iluminacao_local not in ['MODERADA', 'ALTA'] and condicoes.iluminacao_local != 'MUITO ALTA':
                 self._adicionar_cuidado(f"  -> Iluminação atual ({condicoes.iluminacao_local}) pode não ser ideal. Muitas Angiospermas precisam de luz MODERADA a ALTA.")

        if planta.nome.upper() in ['CACTO', 'SUCULENTA']:
            self._adicionar_cuidado(f"ESPECÍFICO ({planta.nome.upper()}): Esta planta é adaptada a ambientes áridos e armazena água em suas estruturas. Excesso de água é o principal risco.")
            if condicoes.iluminacao_local not in ['MUITO ALTA', 'ALTA']:
                self._adicionar_cuidado(f"  -> Iluminação atual ({condicoes.iluminacao_local.upper()}) é baixa para {planta.nome.upper()}. Elas precisam de muita luz solar direta. Mude para iluminação MUITO ALTA ou ALTA.")

        self._adicionar_cuidado(f"GERAL: Monitore regularmente {planta.nome.upper()} quanto a sinais de pragas. Inspecione folhas, caules e raízes de forma QUINZENAL.")

        return self._cuidados_gerados

if __name__ == "__main__":
    aux_entrada = AuxiliarEntrada()
    identificador = Identificador(aux_entrada)
    sistema_recomendacao = SistemaRecomendacao(aux_entrada)

    print("--- Sistema Especialista em Cuidados com Plantas ---\n")

    nome_planta_input = input("Qual é o nome da planta?: ").strip()
    planta_atual = Planta(nome_planta_input)

    planta_atual.tipo = identificador.identificar_tipo_planta()
    if not planta_atual.tipo:
        print("Tipo de planta não definido. Encerrando o programa.")
        exit()
    print(f"\nTipo de planta definido como: {planta_atual.tipo.upper()}")

    print("\n--- Coleta de Informações do Ambiente ---\n")
    estacao_informada = aux_entrada.pedir_entrada_numerada("Qual é a estação do ano atual?",ESTACOES_VALIDAS,"Estação do Ano")
    umidade_informada = aux_entrada.pedir_entrada_numerada("Como é a umidade do solo?",UMIDADES_VALIDAS,"Umidade do Solo")
    iluminacao_informada = aux_entrada.pedir_entrada_numerada("Qual a iluminação do ambiente?",ILUMINACOES_VALIDAS,"Iluminação do Ambiente")

    frequencia_rega_usuario = aux_entrada.pedir_entrada_numerada( "Qual a frequência com que você rega a planta?",FREQUENCIAS_REGA_VALIDAS,"Frequência de Rega Atual")

    if not all([estacao_informada, umidade_informada, iluminacao_informada, frequencia_rega_usuario]):
        print("Uma ou mais informações do ambiente não foram definidas. Encerrando o programa.")
        exit()

    condicoes_atuais = CondicoesAmbientais(estacao_informada,umidade_informada,iluminacao_informada,frequencia_rega_usuario)
    print(f"\nCondições registradas: Estação ({condicoes_atuais.estacao.capitalize()}), Umidade ({condicoes_atuais.umidade_solo.capitalize()}), Iluminação ({condicoes_atuais.iluminacao_local.capitalize()}), Rega Atual ({condicoes_atuais.frequencia_rega_atual.capitalize()})")

    cuidados_finais = sistema_recomendacao.gerar_recomendacoes(planta_atual, condicoes_atuais)

    print(f"\n--- Cuidados Recomendados para {planta_atual.nome} ({planta_atual.tipo.capitalize()}) ---\n")
    if cuidados_finais:
        for i, cuidado in enumerate(cuidados_finais):
            print(f"\n{i + 1}. {cuidado}")
    else:
        print("Não foi possível gerar recomendações específicas com os dados fornecidos.")

    print("\nEstas são algumas recomendações básicos. Observe sua planta e ajuste os cuidados conforme necessário!")
