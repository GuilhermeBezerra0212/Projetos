import tkinter as tk  # importa tkinter com alias tk para criar GUI
from tkinter import ttk  # importa widgets themed (ttk)
from tkinter import messagebox  # importa caixas de mensagem
import re  # importa módulo de expressões regulares
from dataclasses import dataclass  # importa decorator para dataclasses
from typing import Dict, List, Tuple  # importa tipos para anotações

# --- Configuração das Perguntas e Pontuações ---
# Estrutura: [Pergunta, [[Resposta A, Pontos], [Resposta B, Pontos], ...]]
PERGUNTAS_BASE = [  # define as duas perguntas iniciais fixas
    [
        "Qual é o seu nível de conhecimento e experiência em investimentos?",  # texto da pergunta
        [
            ("Iniciante, com pouco ou nenhum conhecimento.", 1),  # opção e pontuação
            ("Intermediário, com algum conhecimento e experiência.", 3),
            ("Avançado, com conhecimento profundo e experiência substancial.", 5)
        ]
    ],
    [
        "Como você reagiria a uma queda repentina no valor dos seus investimentos?",  # segunda pergunta fixa
        [
            ("Ficaria preocupado e consideraria vender para evitar maiores perdas.", 1),  # opção 1
            ("Monitoraria a situação, mas manteria meus investimenos a longo prazo.", 3),  # opção 2
            ("Aproveitaria a oportunidade para comprar mais, acreditando em uma recuperação futura", 5)  # opção 3
        ]
    ]
]

# Perguntas adicionais para cada perfil provisório (após as duas primeiras)
PERGUNTAS_CONSERVADOR = [  # bloco de perguntas para perfil conservador
    [
        "Como os valores investidos vão te ajudar no seu momento de vida?",  # pergunta sobre objetivo de vida
        [
            ("Preservação de patrimônio.", 1),  # resposta 1
            ("Combinação entre preservar e valorizar patrimônio, com certo risco.", 3),  # resposta 2
            ("Aumentar patrimônio, assumindo risco", 5)  # resposta 3
        ]
    ],
    [
        "Onde está seu maior volume de investimento?",  # pergunta sobre onde está o volume
        [
            ("Conta corrente com investimentos automáticos e Poupança", 1),  # opção 1
            ("Tesouro Direto", 3),  # opção 2
            ("Diversificado, com foco em renda fixa", 5)  # opção 3
        ]
    ]
]

PERGUNTAS_MODERADO = [  # bloco de perguntas para perfil moderado
    [
        "Onde está seu maior volume de investimento?",  # pergunta de localização de investimentos
        [
            ("FIIs", 1),  # opção fundos imobiliários
            ("Diversificado", 3),  # opção diversificado
            ("Ações", 5)  # opção ações
        ]
    ],
    [
        "A quanto tempo você investe no mercado de ações?",  # pergunta sobre experiência em ações
        [
            ("Menos de 1 ano", 1),  # opção curto prazo
            ("Mais de 1 ano", 5)  # opção maior experiência
        ]
    ]
]

# Para perfil agressivo, manter um conjunto com as perguntas originais/mais aprofundadas
PERGUNTAS_AGRESSIVO = [  # bloco para agressivo
    [
        "Como os valores investidos vão te ajudar no seu momento de vida?",  # similar ao conservador
        [
            ("Preservação de patrimônio.", 1),
            ("Combinação entre preservar e valorizar patrimônio, com certo risco.", 3),
            ("Aumentar patrimônio, assumindo risco", 5)
        ]
    ],
    [
        "O que você busca dentro dos seus investimentos?",  # pergunta sobre objetivos de investimento
        [
            ("Oportunidade de mercado com ganhos imediatos", 1),
            ("Razoável. Conheço CDBs, LCIs, Fundos de Investimento.", 3),
            ("Avançado. Já investi em Ações, Fundos Imobiliários e Derivativos.", 5)
        ]
    ]
]

# Definição dos perfis baseada na pontuação total
# Máximo de pontos: 4 perguntas * 5 pontos = 20
# Mínimo de pontos: 4 perguntas * 1 ponto = 4
PERFIS = {
    "CONSERVADOR": {"max_score": 10, "descricao": "Busca segurança e previsibilidade, preferindo produtos de baixo risco."},  # mapeia limite e descrição
    "MODERADO": {"max_score": 15, "descricao": "Tolera um risco moderado em busca de retornos um pouco maiores."},
    "AGRESSIVO": {"max_score": 20, "descricao": "Busca altos retornos, aceitando alta volatilidade e risco em Renda Variável."}
}

# --- Definição de Carteiras por Perfil e Objetivo ---
@dataclass
class Ativo:  # dataclass que representa um ativo financeiro
    nome: str  # nome do ativo
    classe: str  # classe do ativo (renda fixa/variável)
    percentual: int  # percentual de alocação
    rentabilidade_estimada: str  # texto com expectativa de retorno
    risco: str  # nível de risco
    
CARTEIRAS = {  # dicionário com carteiras por perfil e objetivo
    "CONSERVADOR": {
        "objetivo_renda_mensal": {
            "descricao": "Carteira focada em renda mensal com baixo risco",
            "estrategia": "Maximizar fluxo de caixa mensal com segurança",
            "ativos": [
                Ativo("Tesouro IPCA+ 2035", "Renda Fixa", 25, "IPCA + 4-5% a.a.", "Muito Baixo"),  # exemplo de ativo
                Ativo("CDB Liquidez Diária (Banco Top 5)", "Renda Fixa", 20, "105-110% CDI", "Muito Baixo"),
                Ativo("LCI/LCA Operacional", "Renda Fixa", 20, "80-95% CDI", "Muito Baixo"),
                Ativo("Fundo Imobiliário com Distribuição", "Renda Variável", 20, "4-8% a.a.", "Médio"),
                Ativo("FIC Renda Fixa Curta Duração", "Renda Fixa", 15, "95-105% CDI", "Muito Baixo"),
            ],
            "aporte_mensal": "R$ 500 - R$ 2.000",
            "tempo_para_renda": "3-6 meses"
        },
        "objetivo_seguranca": {
            "descricao": "Carteira 100% Renda Fixa - Máxima Segurança",
            "estrategia": "Preservar capital com retorno previsível",
            "ativos": [
                Ativo("Tesouro Selic", "Renda Fixa", 30, "Selic - 0.5% a.a.", "Nenhum"),
                Ativo("CDB Liquidez Diária", "Renda Fixa", 35, "105-115% CDI", "Muito Baixo"),
                Ativo("LCI/LCA com Garantia FGC", "Renda Fixa", 25, "85-100% CDI", "Muito Baixo"),
                Ativo("Poupança (Manutenção)", "Renda Fixa", 10, "SELIC/2 + extra", "Nenhum"),
            ],
            "aporte_mensal": "R$ 1.000 - R$ 5.000",
            "tempo_para_renda": "Imediato"
        }
    },
    "MODERADO": {
        "objetivo_renda_mensal": {
            "descricao": "Carteira balanceada para renda com crescimento moderado",
            "estrategia": "Combinar renda fixa com fundos imobiliários e ações selecionadas",
            "ativos": [
                Ativo("Tesouro IPCA+ 2035", "Renda Fixa", 20, "IPCA + 4-5% a.a.", "Baixo"),
                Ativo("CDB Progressivo", "Renda Fixa", 15, "110-120% CDI", "Muito Baixo"),
                Ativo("Fundo Imobiliário Diversificado", "Renda Variável", 25, "5-10% a.a.", "Médio"),
                Ativo("Ações Dividend Yield (Top 50)", "Renda Variável", 25, "8-12% a.a.", "Médio"),
                Ativo("Fundo de Renda Fixa Balanceado", "Renda Fixa", 15, "100-110% CDI", "Baixo"),
            ],
            "aporte_mensal": "R$ 1.000 - R$ 3.000",
            "tempo_para_renda": "2-4 meses"
        },
        "objetivo_crescimento": {
            "descricao": "Carteira balanceada para crescimento patrimonial",
            "estrategia": "60/40 Renda Fixa vs Renda Variável",
            "ativos": [
                Ativo("Tesouro IPCA+ 2035-2045", "Renda Fixa", 25, "IPCA + 4-5% a.a.", "Baixo"),
                Ativo("CDB com Indexação", "Renda Fixa", 20, "115% CDI", "Muito Baixo"),
                Ativo("ETF IBOVESPA (BOVA11)", "Renda Variável", 35, "8-15% a.a.", "Médio-Alto"),
                Ativo("Ações com Dividendos", "Renda Variável", 15, "12-18% a.a.", "Médio-Alto"),
                Ativo("Fundo Imobiliário", "Renda Variável", 5, "6-10% a.a.", "Médio"),
            ],
            "aporte_mensal": "R$ 2.000 - R$ 5.000",
            "tempo_para_renda": "Longo prazo (5+ anos)"
        }
    },
    "AGRESSIVO": {
        "objetivo_crescimento_maximo": {
            "descricao": "Carteira agressiva focada em crescimento máximo",
            "estrategia": "70-80% Renda Variável com ênfase em crescimento",
            "ativos": [
                Ativo("ETF IBOVESPA (BOVA11)", "Renda Variável", 30, "10-18% a.a.", "Alto"),
                Ativo("Ações de Crescimento", "Renda Variável", 25, "15-30% a.a.", "Muito Alto"),
                Ativo("ETF Small Caps", "Renda Variável", 15, "15-25% a.a.", "Muito Alto"),
                Ativo("Tesouro IPCA+ Longo Prazo", "Renda Fixa", 20, "IPCA + 5-6% a.a.", "Baixo"),
                Ativo("Fundo de Ações Multiestrátégia", "Renda Variável", 10, "20-35% a.a.", "Muito Alto"),
            ],
            "aporte_mensal": "R$ 2.000 - R$ 10.000",
            "tempo_para_renda": "Muito Longo Prazo (7-10 anos)"
        },
        "objetivo_especulacao": {
            "descricao": "Carteira ultra-agressiva para perfis muito ousados",
            "estrategia": "Foco em crescimento máximo com derivativos",
            "ativos": [
                Ativo("Ações de Crescimento Agressivo", "Renda Variável", 40, "20-50% a.a.", "Muito Alto"),
                Ativo("ETF Small Caps", "Renda Variável", 25, "18-35% a.a.", "Muito Alto"),
                Ativo("Opções e Mini Índices", "Derivativos", 20, "30-100%+ a.a.", "Crítico"),
                Ativo("Fundo de Investimento em Ações", "Renda Variável", 10, "15-25% a.a.", "Muito Alto"),
                Ativo("Reserva em CDB", "Renda Fixa", 5, "105% CDI", "Muito Baixo"),
            ],
            "aporte_mensal": "R$ 3.000 - R$ 15.000",
            "tempo_para_renda": "Médio Prazo com alto risco"
        }
    }
}

# Recomendações por faixa etária
RECOMENDACOES_IDADE = {
    "20-30": {
        "titulo": "20-30 anos - Tempo é seu maior ativo",
        "recomendacao": "Invista agressivamente em ações e crescimento. O tempo permite recuperação de crises.",
        "perfil_sugerido": "AGRESSIVO"
    },
    "31-40": {
        "titulo": "31-40 anos - Equilíbrio entre Risco e Segurança",
        "recomendacao": "Considere perfil MODERADO a AGRESSIVO. Comece a construir base de renda fixa.",
        "perfil_sugerido": "MODERADO"
    },
    "41-50": {
        "titulo": "41-50 anos - Foco em Renda e Preservação",
        "recomendacao": "Perfil MODERADO é ideal. Aumente ponderação em renda fixa e fundos imobiliários.",
        "perfil_sugerido": "MODERADO"
    },
    "51-60": {
        "titulo": "51-60 anos - Segurança com Rentabilidade",
        "recomendacao": "Perfil CONSERVADOR com até 30% em Renda Variável. Foco em renda mensal.",
        "perfil_sugerido": "CONSERVADOR"
    },
    "60+": {
        "titulo": "60+ anos - Preservação e Renda",
        "recomendacao": "Perfil CONSERVADOR. 90-100% em Renda Fixa. Gere fluxo de caixa mensal.",
        "perfil_sugerido": "CONSERVADOR"
    }
}

class TesteInvestidorApp:  # classe principal da aplicação
    def __init__(self, master):  # construtor que recebe a janela root
        self.master = master  # armazena referência ao root
        master.title("B3 - Teste de Perfil do Investidor + Recomendação de Carteira")  # define título da janela
        master.geometry("700x500")  # define tamanho inicial da janela
        # Aplica cor de fundo da janela
        master.configure(bg='#00145f')  # define cor de fundo
        # Configura estilos ttk para que os frames/labels herdem o fundo escuro
        self.style = ttk.Style()  # cria objeto de estilo
        try:
            # 'clam' costuma respeitar melhor cores customizadas em ttk
            self.style.theme_use('clam')  # tenta aplicar tema clam
        except Exception:
            pass  # ignora erro se tema não estiver disponível
        self.style.configure('TFrame', background='#00145f')  # estilo para frames
        self.style.configure('TLabel', background='#00145f', foreground='white')  # estilo para labels
        self.style.configure('TButton', background='#00145f', foreground='white')  # estilo para botões
        self.style.configure('TRadiobutton', background='#00145f', foreground='white')  # estilo para radiobuttons
        
        # Variáveis de Estado
        self.pontuacao_total = 0  # soma total das pontuações
        self.pergunta_atual = 0  # índice da pergunta atual
        self.idade_usuario = 0  # idade do usuário (preenchida depois)
        self.objetivo_usuario = ""  # objetivo selecionado (preenchido depois)
        # Lista de perguntas que será montada dinamicamente: começar com as duas bases
        self.questions = list(PERGUNTAS_BASE)  # copia das perguntas base para manipular dinamicamente
        self.pontuacoes_por_pergunta = [0] * len(self.questions) # Lista para armazenar a pontuação de cada questão
        
        # --- Configuração dos Frames ---
        self.frame_quiz = ttk.Frame(master, padding="10")  # frame principal do quiz
        self.frame_quiz.pack(fill='both', expand=True)  # empacota para preencher janela
        # Cabeçalho: título do teste acima da pergunta (não colado ao topo)
        self.header_label = ttk.Label(self.frame_quiz, text="Descubra Perfil de Investidor", font=('Arial', 16, 'bold'))  # label do cabeçalho
        self.header_label.pack(pady=(15, 8))  # posiciona cabeçalho com espaçamento
        
        # --- Componentes Comuns ---
        
        # 1. Barra de Progresso (Canto Inferior Direito)
        self.setup_progress_bar(master)  # cria a barra de progresso
        
        # 2. Rótulo da Pergunta
        self.label_pergunta = ttk.Label(self.frame_quiz, text="", wraplength=550, font=('Arial', 16, 'bold'))  # label onde a pergunta aparecerá
        self.label_pergunta.pack(pady=20)  # posiciona label da pergunta
        
        # 3. Frame para as Opções de Resposta
        self.frame_opcoes = ttk.Frame(self.frame_quiz)  # frame para conter os radio buttons
        self.frame_opcoes.pack(pady=10)  # posiciona frame de opções
        
        # Variável de controle para os RadioButtons
        self.resposta_selecionada = tk.IntVar()  # armazena valor selecionado (a pontuação)
        
        # 4. Botão de Próxima Pergunta
        self.btn_proximo = ttk.Button(self.frame_quiz, text="Próxima Pergunta >", command=self.proxima_pergunta, state='disabled')  # botão próximo
        self.btn_proximo.pack(pady=20)  # posiciona botão
        
        # Inicia o teste
        self.carregar_pergunta()  # carrega a primeira pergunta

    def setup_progress_bar(self, master):
        """Cria e posiciona a barra de progresso no canto inferior direito."""  # docstring explicando função
        # Estiliza a barra de progresso para usar a cor solicitada
        try:
            self.style.configure('Horizontal.TProgressbar', background='#00b0e6')  # tenta customizar cor da barra
        except Exception:
            pass  # ignora se não for possível
        self.pbar = ttk.Progressbar(
            master,
            orient='horizontal',  # orientação horizontal
            mode='determinate',  # progresso determinado
            length=120,  # comprimento da barra em pixels
            maximum=len(self.questions) # O máximo é o número total de perguntas (dinâmico)
        )
        # Posicionamento no canto inferior direito com place()
        self.pbar.place(
            relx=1.0,  # posição relativa x (1.0 = direita)
            rely=1.0,  # posição relativa y (1.0 = baixo)
            anchor='se',  # ponto de ancoragem sudeste
            x=-10,  # deslocamento x negativo para dentro da janela
            y=-10  # deslocamento y negativo para dentro da janela
        )
        
    def carregar_pergunta(self):
        """Carrega a pergunta atual e suas opções na tela."""  # docstring
        if self.pergunta_atual < len(self.questions):  # verifica se ainda há perguntas
            # Atualiza a barra de progresso
            self.pbar['value'] = self.pergunta_atual + 1  # define valor atual da barra (1-based)

            pergunta_info = self.questions[self.pergunta_atual]  # obtém dados da pergunta atual
            # Exibe somente o texto da pergunta: remove numeração inicial como "1. "
            question_text = re.sub(r'^\s*\d+\.\s*', '', pergunta_info[0])  # remove numeração no início
            self.label_pergunta.config(text=question_text)  # atualiza label da pergunta
            
            # Limpa opções antigas
            for widget in self.frame_opcoes.winfo_children():  # itera widgets dentro do frame de opções
                widget.destroy()  # destrói cada widget antigo
            
            self.resposta_selecionada.set(-1) # Reseta a seleção para valor inválido
            self.btn_proximo.config(state='disabled') # Desabilita o botão até selecionar algo
            
            # Cria os RadioButtons para cada opção
            for idx, (texto_resposta, pontos) in enumerate(pergunta_info[1]):  # itera opções
                # Usar tk.Radiobutton para suportar a propriedade `font` e cores personalizadas
                radio = tk.Radiobutton(
                    self.frame_opcoes,  # parent frame
                    text=texto_resposta,  # texto da opção
                    value=pontos,  # O valor do RadioButton é a pontuação da resposta
                    variable=self.resposta_selecionada,  # vincula à IntVar
                    command=self.habilitar_proximo,  # chama função ao selecionar
                    font=('Arial', 14),  # fonte
                    bg='#00145f',  # cor de fundo (consistente com tema)
                    fg='white',  # cor do texto
                    activebackground='#00145f',  # cor de fundo quando ativo
                    activeforeground='white',  # cor do texto quando ativo
                    selectcolor='black',  # cor do indicador quando selecionado
                    indicatoron=1,  # mostra indicador circular
                    bd=0,  # sem borda
                    highlightthickness=2,  # espessura de destaque
                    highlightcolor='white',  # cor do destaque
                    highlightbackground='white',  # cor do fundo do destaque
                    anchor='w',  # ancoragem à esquerda
                    justify='left',  # justifica o texto à esquerda
                )
                # O RadioButton recebe como valor a pontuação da resposta.
                # Quando selecionado, ele atribui essa pontuação à variável self.resposta_selecionada
                radio.pack(anchor='w', pady=5, padx=10)  # empacota o radio button
        else:
            self.finalizar_teste()  # se não houver mais perguntas, finaliza

    def habilitar_proximo(self):
        """Habilita o botão 'Próxima Pergunta' ao selecionar uma opção."""  # docstring
        if self.resposta_selecionada.get() != -1:  # checa se valor válido foi setado
            self.btn_proximo.config(state='normal')  # habilita botão
            
    def proxima_pergunta(self):
        """Salva a pontuação da pergunta e avança para a próxima."""  # docstring
        pontos = self.resposta_selecionada.get()  # lê pontuação selecionada
        if pontos > 0:  # valida que existe pontuação positiva
            # Armazena a pontuação da questão atual
            self.pontuacoes_por_pergunta[self.pergunta_atual] = pontos  # salva pontuação na lista
            self.pontuacao_total += pontos  # acumula na pontuação total
            self.pergunta_atual += 1  # avança índice da pergunta
            # Se acabamos de responder as duas primeiras perguntas (índice 2 é após responder índice 1),
            # definimos um perfil provisório e extendemos o conjunto de perguntas de acordo.
            if self.pergunta_atual == 2:  # se respondemos as duas primeiras
                soma_duas_primeiras = sum(self.pontuacoes_por_pergunta[:2])  # soma das duas primeiras pontuações
                # Thresholds: 2/4 -> conservador, 6/8 -> moderado, 10 -> agressivo
                if soma_duas_primeiras <= 4:  # menor soma -> conservador
                    perfil_prov = 'CONSERVADOR'  # define perfil provisório
                    adicionais = PERGUNTAS_CONSERVADOR  # seleciona bloco conservador
                elif soma_duas_primeiras <= 8:  # soma intermediária -> moderado
                    perfil_prov = 'MODERADO'
                    adicionais = PERGUNTAS_MODERADO  # seleciona bloco moderado
                else:  # soma maior -> agressivo
                    perfil_prov = 'AGRESSIVO'
                    adicionais = PERGUNTAS_AGRESSIVO  # seleciona bloco agressivo

                # Anexa perguntas adicionais e atualiza estruturas de apoio
                self.questions.extend(adicionais)  # estende lista de perguntas com o bloco escolhido
                # Atualiza o tamanho do vetor de pontuações (preenche com zeros para as novas perguntas)
                self.pontuacoes_por_pergunta.extend([0] * len(adicionais))  # adiciona zeros para novas questões
                # Atualiza o máximo da barra de progresso
                try:
                    self.pbar['maximum'] = len(self.questions)  # atualiza máximo do progressbar dinamicamente
                except Exception:
                    pass  # ignora caso pbar ainda não exista

            if self.pergunta_atual < len(self.questions):  # se ainda houver perguntas
                self.carregar_pergunta()  # carrega próxima pergunta
            else:
                self.finalizar_teste()  # caso contrário, finaliza
        else:
            messagebox.showerror("Erro", "Por favor, selecione uma resposta antes de continuar.")  # alerta se nada selecionado

    def finalizar_teste(self):
        """Calcula o perfil final e exibe o resultado."""  # docstring
        self.frame_quiz.pack_forget() # Esconde o quiz
        
        # 1. Determina o Perfil
        perfil_final = ""  # guarda string exibida com ícone
        descricao_perfil = ""  # descrição curta do perfil
        
        if self.pontuacao_total <= PERFIS["CONSERVADOR"]["max_score"]:  # compara total com limite conservador
            perfil_final = "CONSERVADOR 🐢"  # texto final para conservador
            descricao_perfil = PERFIS["CONSERVADOR"]["descricao"]  # texto de descrição
            self.perfil_detectado = "CONSERVADOR"  # guarda perfil detectado
        elif self.pontuacao_total <= PERFIS["MODERADO"]["max_score"]:  # verifica moderado
            perfil_final = "MODERADO ⚖️"
            descricao_perfil = PERFIS["MODERADO"]["descricao"]
            self.perfil_detectado = "MODERADO"
        else:
            perfil_final = "AGRESSIVO (OU ARROJADO) 🚀"  # caso contrário, agressivo
            descricao_perfil = PERFIS["AGRESSIVO"]["descricao"]
            self.perfil_detectado = "AGRESSIVO"
            
        # 2. Exibe o Resultado em uma nova tela/Frame
        frame_resultado = ttk.Frame(self.master, padding="20")  # frame para resultado
        frame_resultado.pack(fill='both', expand=True)  # empacota frame de resultado

        ttk.Label(frame_resultado, text="✅ TESTE CONCLUÍDO ✅", font=('Arial', 16, 'bold')).pack(pady=10)  # título de conclusão
        ttk.Separator(frame_resultado, orient='horizontal').pack(fill='x', pady=5)  # separador horizontal
        
        ttk.Label(frame_resultado, text=f"Sua Pontuação Total: {self.pontuacao_total} pontos", font=('Arial', 12)).pack(pady=5)  # exibe pontuação
        
        ttk.Label(frame_resultado, text="SEU PERFIL DE INVESTIDOR É:", font=('Arial', 18, 'bold'), foreground='darkgreen').pack(pady=15)  # subtítulo
        ttk.Label(frame_resultado, text=perfil_final, font=('Arial', 24, 'bold'), foreground='red').pack(pady=5)  # exibe perfil
        
        ttk.Label(frame_resultado, text=descricao_perfil, wraplength=550, justify='center').pack(pady=20)  # descrição do perfil
        
        # 3. Agora pergunta Idade e Objetivo
        ttk.Separator(frame_resultado, orient='horizontal').pack(fill='x', pady=10)  # separador
        
        ttk.Label(frame_resultado, text="Para personalizar a recomendação, informe:", font=('Arial', 12, 'bold')).pack(pady=10)  # instrução
        
        # Frame para Idade
        frame_idade = ttk.Frame(frame_resultado)  # frame interno para idade
        frame_idade.pack(pady=5)  # empacota frame
        ttk.Label(frame_idade, text="Sua Idade:", font=('Arial', 11)).pack(side='left', padx=5)  # label idade
        spinbox_idade = ttk.Spinbox(frame_idade, from_=18, to=100, width=5, font=('Arial', 11))  # spinbox para idade
        spinbox_idade.set(40)  # valor default 40
        spinbox_idade.pack(side='left', padx=5)  # empacota spinbox
        
        # Frame para Objetivo
        frame_objetivo = ttk.Frame(frame_resultado)  # frame interno para objetivo
        frame_objetivo.pack(pady=5)
        ttk.Label(frame_objetivo, text="Seu Objetivo:", font=('Arial', 11)).pack(side='left', padx=5)  # label objetivo
        
        objetivos_opcoes = self._get_objetivos_para_perfil(self.perfil_detectado)  # obtém opções de objetivo para o perfil
        combo_objetivo = ttk.Combobox(frame_objetivo, values=objetivos_opcoes, state='readonly', width=30, font=('Arial', 11))  # combobox para objetivos
        if objetivos_opcoes:
            combo_objetivo.current(0)  # seleciona a primeira opção por padrão
        combo_objetivo.pack(side='left', padx=5)  # empacota combobox
        
        # Botão para Gerar Carteira
        def gerar_carteira():  # função interna chamada ao clicar
            idade = int(spinbox_idade.get())  # lê idade do spinbox
            objetivo_key = list(CARTEIRAS[self.perfil_detectado].keys())[combo_objetivo.current()]  # mapeia índice para chave de objetivo
            self.idade_usuario = idade  # salva idade
            self.objetivo_usuario = objetivo_key  # salva objetivo
            
            frame_resultado.pack_forget()  # esconde frame de resultado
            self.pbar.destroy()  # remove progressbar
            self.mostrar_carteira_recomendada()  # mostra a carteira
        
        ttk.Button(frame_resultado, text="Gerar Carteira Recomendada", command=gerar_carteira).pack(pady=15)  # botão gerar carteira
        
        self.pbar.destroy() # Remove a barra de progresso
    
    def _get_objetivos_para_perfil(self, perfil):
        """Retorna lista de objetivos disponíveis para um perfil"""  # docstring
        if perfil in CARTEIRAS:  # verifica se perfil existe nas carteiras
            return [nome.replace("_", " ").title() for nome in CARTEIRAS[perfil].keys()]  # formata nomes de chaves
        return []  # retorna lista vazia se não encontrar
    
    def mostrar_carteira_recomendada(self):
        """Exibe a carteira recomendada com base no perfil, idade e objetivo"""  # docstring
        frame_carteira = ttk.Frame(self.master, padding="20")  # frame principal da tela de carteira
        frame_carteira.pack(fill='both', expand=True)  # empacota frame
        
        # Título
        ttk.Label(frame_carteira, text="📊 SUA CARTEIRA RECOMENDADA 📊", font=('Arial', 18, 'bold')).pack(pady=10)  # título
        ttk.Separator(frame_carteira, orient='horizontal').pack(fill='x', pady=5)  # separador
        
        # Informações do Usuário
        info_text = f"Perfil: {self.perfil_detectado} | Idade: {self.idade_usuario} anos | Objetivo: {self.objetivo_usuario.replace('_', ' ').title()}"  # texto resumo
        ttk.Label(frame_carteira, text=info_text, font=('Arial', 11), foreground='cyan').pack(pady=5)  # exibe resumo
        
        # Recomendação por Idade
        faixa_idade = self._get_faixa_idade(self.idade_usuario)  # determina faixa etária
        recomendacao_idade = RECOMENDACOES_IDADE.get(faixa_idade, {})  # pega recomendação correspondente
        
        ttk.Label(frame_carteira, text=recomendacao_idade.get("titulo", ""), font=('Arial', 12, 'bold'), foreground='yellow').pack(pady=8)  # título da recomendação
        ttk.Label(frame_carteira, text=recomendacao_idade.get("recomendacao", ""), wraplength=650, justify='left', font=('Arial', 10)).pack(pady=5)  # texto da recomendação
        
        ttk.Separator(frame_carteira, orient='horizontal').pack(fill='x', pady=10)  # separador
        
        # Carteira de Ativos
        carteira_data = CARTEIRAS[self.perfil_detectado][self.objetivo_usuario]  # obtém dados da carteira selecionada
        
        ttk.Label(frame_carteira, text=f"Estratégia: {carteira_data['estrategia']}", font=('Arial', 11, 'bold'), foreground='lightgreen').pack(pady=5)  # exibe estratégia
        ttk.Label(frame_carteira, text=f"Descrição: {carteira_data['descricao']}", wraplength=650, justify='left', font=('Arial', 10)).pack(pady=5)  # exibe descrição
        
        # Frame com scroll para os ativos
        frame_scroll = ttk.Frame(frame_carteira)  # frame que conterá canvas e scrollbar
        frame_scroll.pack(fill='both', expand=True, pady=10)  # empacota frame
        
        canvas = tk.Canvas(frame_scroll, bg='#00145f', highlightthickness=0)  # canvas para scroll
        scrollbar = ttk.Scrollbar(frame_scroll, orient='vertical', command=canvas.yview)  # scrollbar vertical
        scrollable_frame = ttk.Frame(canvas)  # frame que será colocado dentro do canvas
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))  # atualiza região rolável quando o conteúdo mudar
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")  # cria a janela interna no canvas
        canvas.configure(yscrollcommand=scrollbar.set)  # vincula scrollbar ao canvas
        
        # Exibir cada ativo
        ttk.Label(scrollable_frame, text="ALOCAÇÃO DE ATIVOS:", font=('Arial', 12, 'bold')).pack(pady=5)  # título da seção de ativos
        
        for ativo in carteira_data['ativos']:  # itera ativos da carteira
            frame_ativo = ttk.Frame(scrollable_frame)  # frame para cada ativo
            frame_ativo.pack(fill='x', padx=10, pady=8)  # empacota frame do ativo
            
            ttk.Label(frame_ativo, text=f"• {ativo.nome}", font=('Arial', 11, 'bold'), foreground='lightblue').pack(anchor='w')  # nome do ativo
            ttk.Label(frame_ativo, text=f"  Classe: {ativo.classe} | Alocação: {ativo.percentual}%", font=('Arial', 9)).pack(anchor='w', padx=15)  # classe e alocação
            ttk.Label(frame_ativo, text=f"  Rentabilidade Est.: {ativo.rentabilidade_estimada} | Risco: {ativo.risco}", font=('Arial', 9), foreground='lightyellow').pack(anchor='w', padx=15)  # rendimento e risco
        
        canvas.pack(side='left', fill='both', expand=True)  # empacota canvas
        scrollbar.pack(side='right', fill='y')  # empacota scrollbar

        # Ativa rolagem com a roda do mouse quando o ponteiro estiver sobre o canvas (Windows)
        def _on_mousewheel(event):  # função para mapear evento da roda do mouse
            # event.delta é múltiplo de 120 no Windows
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")  # faz scroll vertical baseado em delta

        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))  # vincula rolagem ao entrar no canvas
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))  # remove vinculo ao sair do canvas

        # Recomendações Finais (movidas para dentro do scrollable_frame para poder rolar com o mouse)
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)  # separador
        
        ttk.Label(scrollable_frame, text="📌 RECOMENDAÇÕES FINAIS:", font=('Arial', 12, 'bold'), foreground='gold').pack(anchor='w', padx=10)  # título recomendações
        ttk.Label(scrollable_frame, text=f"• Aporte Mensal Sugerido: {carteira_data['aporte_mensal']}", font=('Arial', 10)).pack(anchor='w', padx=20, pady=2)  # aporte sugerido
        ttk.Label(scrollable_frame, text=f"• Tempo para Gerar Renda: {carteira_data['tempo_para_renda']}", font=('Arial', 10)).pack(anchor='w', padx=20, pady=2)  # tempo estimado
        ttk.Label(scrollable_frame, text="• Rebalanceie a carteira a cada 6-12 meses", font=('Arial', 10)).pack(anchor='w', padx=20, pady=2)  # dica de rebalanceamento
        ttk.Label(scrollable_frame, text="• Considere consultar um gestor patrimonial certificado (CFP)", font=('Arial', 10)).pack(anchor='w', padx=20, pady=2)  # recomendação profissional

        # Mensagem final maior, centralizada e com quebra automática — dentro do scroll para continuidade
        mensagem_final = (
            "Resumo e próximos passos:\n\n"  # início do texto final
            f"Esta carteira foi sugerida com base no seu perfil '{self.perfil_detectado}', na sua idade ({self.idade_usuario} anos) e no objetivo escolhido. "
            "Considere começar com aportes regulares, manter uma reserva de emergência e rebalancear conforme volatilidade do mercado.\n\n"
            "Atenção: a diversificação não elimina riscos. As alocações apresentadas são apenas exemplos educacionais e não constituem consultoria financeira personalizada. "
            "Para ajustar com precisão sua carteira, procure um profissional certificado (CFP) e valide produtos como CDBs, LCIs/LCAs, Tesouro Direto e Fundos Imobiliários antes de investir."
        )

        text_final = tk.Text(scrollable_frame, height=8, wrap='word', bg='#00145f', fg='white', bd=0, highlightthickness=0, font=('Arial', 11))  # widget de texto para mensagem final
        text_final.tag_configure('center', justify='center')  # configura tag de centralização
        text_final.insert('1.0', mensagem_final)  # insere mensagem no widget
        text_final.tag_add('center', '1.0', 'end')  # aplica centralização
        text_final.config(state='disabled')  # torna texto não editável
        text_final.pack(fill='x', padx=10, pady=12)  # empacota widget de texto

        # Botões finais
        frame_botoes = ttk.Frame(frame_carteira)  # frame para botões
        frame_botoes.pack(fill='x', pady=15)  # empacota frame
        
        ttk.Button(frame_botoes, text="🔄 Refazer Teste", command=self.reiniciar_app).pack(side='left', padx=5)  # botão refazer
        ttk.Button(frame_botoes, text="❌ Sair", command=self.master.quit).pack(side='left', padx=5)  # botão sair
    
    def _get_faixa_idade(self, idade):
        """Retorna a faixa etária do usuário"""  # docstring
        if idade < 31:  # checa faixa 20-30
            return "20-30"
        elif idade < 41:  # checa faixa 31-40
            return "31-40"
        elif idade < 51:  # checa faixa 41-50
            return "41-50"
        elif idade < 61:  # checa faixa 51-60
            return "51-60"
        else:  # caso contrário 60+
            return "60+"
    
    def reiniciar_app(self):
        """Reinicia a aplicação"""  # docstring
        self.master.destroy()  # fecha janela atual
        root = tk.Tk()  # cria nova janela
        app = TesteInvestidorApp(root)  # instancia nova aplicação (reusa classe)
        root.mainloop()  # entra no loop principal

if __name__ == "__main__":  # ponto de entrada quando executado diretamente
    root = tk.Tk()  # cria janela principal
    app = TesteInvestidorApp(root)  # instancia a aplicação
    root.mainloop()  # executa loop da GUI
