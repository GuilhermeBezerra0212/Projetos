import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re
from dataclasses import dataclass
from typing import Dict, List, Tuple

# --- Configuração das Perguntas e Pontuações ---
# Estrutura: [Pergunta, [[Resposta A, Pontos], [Resposta B, Pontos], ...]]
PERGUNTAS_BASE = [
    [
        "Qual é o seu nível de conhecimento e experiência em investimentos?",
        [
            ("Iniciante, com pouco ou nenhum conhecimento.", 1),
            ("Intermediário, com algum conhecimento e experiência.", 3),
            ("Avançado, com conhecimento profundo e experiência substancial.", 5)
        ]
    ],
    [
        "Como você reagiria a uma queda repentina no valor dos seus investimentos?",
        [
            ("Ficaria preocupado e consideraria vender para evitar maiores perdas.", 1),
            ("Monitoraria a situação, mas manteria meus investimenos a longo prazo.", 3),
            ("Aproveitaria a oportunidade para comprar mais, acreditando em uma recuperação futura", 5)
        ]
    ]
]

# Perguntas adicionais para cada perfil provisório (após as duas primeiras)
PERGUNTAS_CONSERVADOR = [
    [
        "Como os valores investidos vão te ajudar no seu momento de vida?",
        [
            ("Preservação de patrimônio.", 1),
            ("Combinação entre preservar e valorizar patrimônio, com certo risco.", 3),
            ("Aumentar patrimônio, assumindo risco", 5)
        ]
    ],
    [
        "Onde está seu maior volume de investimento?",
        [
            ("Conta corrente com investimentos automáticos e Poupança", 1),
            ("Tesouro Direto", 3),
            ("Diversificado, com foco em renda fixa", 5)
        ]
    ]
]

PERGUNTAS_MODERADO = [
    [
        "Onde está seu maior volume de investimento?",
        [
            ("FIIs", 1),
            ("Diversificado", 3),
            ("Ações", 5)
        ]
    ],
    [
        "A quanto tempo você investe no mercado de ações?",
        [
            ("Menos de 1 ano", 1),
            ("Mais de 1 ano", 5)
        ]
    ]
]

# Para perfil agressivo, manter um conjunto com as perguntas originais/mais aprofundadas
PERGUNTAS_AGRESSIVO = [
    [
        "Como os valores investidos vão te ajudar no seu momento de vida?",
        [
            ("Preservação de patrimônio.", 1),
            ("Combinação entre preservar e valorizar patrimônio, com certo risco.", 3),
            ("Aumentar patrimônio, assumindo risco", 5)
        ]
    ],
    [
        "O que você busca dentro dos seus investimentos?",
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
    "CONSERVADOR": {"max_score": 10, "descricao": "Busca segurança e previsibilidade, preferindo produtos de baixo risco."},
    "MODERADO": {"max_score": 15, "descricao": "Tolera um risco moderado em busca de retornos um pouco maiores."},
    "AGRESSIVO": {"max_score": 20, "descricao": "Busca altos retornos, aceitando alta volatilidade e risco em Renda Variável."}
}

# --- Definição de Carteiras por Perfil e Objetivo ---
@dataclass
class Ativo:
    nome: str
    classe: str
    percentual: int
    rentabilidade_estimada: str
    risco: str
    
CARTEIRAS = {
    "CONSERVADOR": {
        "objetivo_renda_mensal": {
            "descricao": "Carteira focada em renda mensal com baixo risco",
            "estrategia": "Maximizar fluxo de caixa mensal com segurança",
            "ativos": [
                Ativo("Tesouro IPCA+ 2035", "Renda Fixa", 25, "IPCA + 4-5% a.a.", "Muito Baixo"),
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

class TesteInvestidorApp:
    def __init__(self, master):
        self.master = master
        master.title("B3 - Teste de Perfil do Investidor + Recomendação de Carteira")
        master.geometry("700x500")
        # Aplica cor de fundo da janela
        master.configure(bg='#00145f')
        # Configura estilos ttk para que os frames/labels herdem o fundo escuro
        self.style = ttk.Style()
        try:
            # 'clam' costuma respeitar melhor cores customizadas em ttk
            self.style.theme_use('clam')
        except Exception:
            pass
        self.style.configure('TFrame', background='#00145f')
        self.style.configure('TLabel', background='#00145f', foreground='white')
        self.style.configure('TButton', background='#00145f', foreground='white')
        self.style.configure('TRadiobutton', background='#00145f', foreground='white')
        
        # Variáveis de Estado
        self.pontuacao_total = 0
        self.pergunta_atual = 0
        self.idade_usuario = 0
        self.objetivo_usuario = ""
        # Lista de perguntas que será montada dinamicamente: começar com as duas bases
        self.questions = list(PERGUNTAS_BASE)
        self.pontuacoes_por_pergunta = [0] * len(self.questions) # Lista para armazenar a pontuação de cada questão
        
        # --- Configuração dos Frames ---
        self.frame_quiz = ttk.Frame(master, padding="10")
        self.frame_quiz.pack(fill='both', expand=True)
        # Cabeçalho: título do teste acima da pergunta (não colado ao topo)
        self.header_label = ttk.Label(self.frame_quiz, text="Descubra Perfil de Investidor", font=('Arial', 16, 'bold'))
        self.header_label.pack(pady=(15, 8))
        
        # --- Componentes Comuns ---
        
        # 1. Barra de Progresso (Canto Inferior Direito)
        self.setup_progress_bar(master)
        
        # 2. Rótulo da Pergunta
        self.label_pergunta = ttk.Label(self.frame_quiz, text="", wraplength=550, font=('Arial', 16, 'bold'))
        self.label_pergunta.pack(pady=20)
        
        # 3. Frame para as Opções de Resposta
        self.frame_opcoes = ttk.Frame(self.frame_quiz)
        self.frame_opcoes.pack(pady=10)
        
        # Variável de controle para os RadioButtons
        self.resposta_selecionada = tk.IntVar() 
        
        # 4. Botão de Próxima Pergunta
        self.btn_proximo = ttk.Button(self.frame_quiz, text="Próxima Pergunta >", command=self.proxima_pergunta, state='disabled')
        self.btn_proximo.pack(pady=20)
        
        # Inicia o teste
        self.carregar_pergunta()

    def setup_progress_bar(self, master):
        """Cria e posiciona a barra de progresso no canto inferior direito."""
        # Estiliza a barra de progresso para usar a cor solicitada
        try:
            self.style.configure('Horizontal.TProgressbar', background='#00b0e6')
        except Exception:
            pass
        self.pbar = ttk.Progressbar(
            master,
            orient='horizontal',
            mode='determinate',
            length=120,
            maximum=len(self.questions) # O máximo é o número total de perguntas (dinâmico)
        )
        # Posicionamento no canto inferior direito com place()
        self.pbar.place(
            relx=1.0,
            rely=1.0,
            anchor='se',
            x=-10,
            y=-10
        )
        
    def carregar_pergunta(self):
        """Carrega a pergunta atual e suas opções na tela."""
        if self.pergunta_atual < len(self.questions):
            # Atualiza a barra de progresso
            self.pbar['value'] = self.pergunta_atual + 1

            pergunta_info = self.questions[self.pergunta_atual]
            # Exibe somente o texto da pergunta: remove numeração inicial como "1. "
            question_text = re.sub(r'^\s*\d+\.\s*', '', pergunta_info[0])
            self.label_pergunta.config(text=question_text)
            
            # Limpa opções antigas
            for widget in self.frame_opcoes.winfo_children():
                widget.destroy()
            
            self.resposta_selecionada.set(-1) # Reseta a seleção
            self.btn_proximo.config(state='disabled') # Desabilita o botão até selecionar algo
            
            # Cria os RadioButtons para cada opção
            for idx, (texto_resposta, pontos) in enumerate(pergunta_info[1]):
                # Usar tk.Radiobutton para suportar a propriedade `font` e cores personalizadas
                radio = tk.Radiobutton(
                    self.frame_opcoes,
                    text=texto_resposta,
                    value=pontos,  # O valor do RadioButton é a pontuação da resposta
                    variable=self.resposta_selecionada,
                    command=self.habilitar_proximo,
                    font=('Arial', 14),
                    bg='#00145f',
                    fg='white',
                    activebackground='#00145f',
                    activeforeground='white',
                    selectcolor='black',
                    indicatoron=1,
                    bd=0,
                    highlightthickness=2,
                    highlightcolor='white',
                    highlightbackground='white',
                    anchor='w',
                    justify='left',
                )
                # O RadioButton recebe como valor a pontuação da resposta.
                # Quando selecionado, ele atribui essa pontuação à variável self.resposta_selecionada
                radio.pack(anchor='w', pady=5, padx=10)
        else:
            self.finalizar_teste()

    def habilitar_proximo(self):
        """Habilita o botão 'Próxima Pergunta' ao selecionar uma opção."""
        if self.resposta_selecionada.get() != -1:
            self.btn_proximo.config(state='normal')
            
    def proxima_pergunta(self):
        """Salva a pontuação da pergunta e avança para a próxima."""
        pontos = self.resposta_selecionada.get()
        if pontos > 0:
            # Armazena a pontuação da questão atual
            self.pontuacoes_por_pergunta[self.pergunta_atual] = pontos
            self.pontuacao_total += pontos
            self.pergunta_atual += 1
            # Se acabamos de responder as duas primeiras perguntas (índice 2 é após responder índice 1),
            # definimos um perfil provisório e extendemos o conjunto de perguntas de acordo.
            if self.pergunta_atual == 2:
                soma_duas_primeiras = sum(self.pontuacoes_por_pergunta[:2])
                # Thresholds: 2/4 -> conservador, 6/8 -> moderado, 10 -> agressivo
                if soma_duas_primeiras <= 4:
                    perfil_prov = 'CONSERVADOR'
                    adicionais = PERGUNTAS_CONSERVADOR
                elif soma_duas_primeiras <= 8:
                    perfil_prov = 'MODERADO'
                    adicionais = PERGUNTAS_MODERADO
                else:
                    perfil_prov = 'AGRESSIVO'
                    adicionais = PERGUNTAS_AGRESSIVO

                # Anexa perguntas adicionais e atualiza estruturas de apoio
                self.questions.extend(adicionais)
                # Atualiza o tamanho do vetor de pontuações (preenche com zeros para as novas perguntas)
                self.pontuacoes_por_pergunta.extend([0] * len(adicionais))
                # Atualiza o máximo da barra de progresso
                try:
                    self.pbar['maximum'] = len(self.questions)
                except Exception:
                    pass

            if self.pergunta_atual < len(self.questions):
                self.carregar_pergunta()
            else:
                self.finalizar_teste()
        else:
            messagebox.showerror("Erro", "Por favor, selecione uma resposta antes de continuar.")

    def finalizar_teste(self):
        """Calcula o perfil final e exibe o resultado."""
        self.frame_quiz.pack_forget() # Esconde o quiz
        
        # 1. Determina o Perfil
        perfil_final = ""
        descricao_perfil = ""
        
        if self.pontuacao_total <= PERFIS["CONSERVADOR"]["max_score"]:
            perfil_final = "CONSERVADOR 🐢"
            descricao_perfil = PERFIS["CONSERVADOR"]["descricao"]
            self.perfil_detectado = "CONSERVADOR"
        elif self.pontuacao_total <= PERFIS["MODERADO"]["max_score"]:
            perfil_final = "MODERADO ⚖️"
            descricao_perfil = PERFIS["MODERADO"]["descricao"]
            self.perfil_detectado = "MODERADO"
        else:
            perfil_final = "AGRESSIVO (OU ARROJADO) 🚀"
            descricao_perfil = PERFIS["AGRESSIVO"]["descricao"]
            self.perfil_detectado = "AGRESSIVO"
            
        # 2. Exibe o Resultado em uma nova tela/Frame
        frame_resultado = ttk.Frame(self.master, padding="20")
        frame_resultado.pack(fill='both', expand=True)

        ttk.Label(frame_resultado, text="✅ TESTE CONCLUÍDO ✅", font=('Arial', 16, 'bold')).pack(pady=10)
        ttk.Separator(frame_resultado, orient='horizontal').pack(fill='x', pady=5)
        
        ttk.Label(frame_resultado, text=f"Sua Pontuação Total: {self.pontuacao_total} pontos", font=('Arial', 12)).pack(pady=5)
        
        ttk.Label(frame_resultado, text="SEU PERFIL DE INVESTIDOR É:", font=('Arial', 18, 'bold'), foreground='darkgreen').pack(pady=15)
        ttk.Label(frame_resultado, text=perfil_final, font=('Arial', 24, 'bold'), foreground='red').pack(pady=5)
        
        ttk.Label(frame_resultado, text=descricao_perfil, wraplength=550, justify='center').pack(pady=20)
        
        # 3. Agora pergunta Idade e Objetivo
        ttk.Separator(frame_resultado, orient='horizontal').pack(fill='x', pady=10)
        
        ttk.Label(frame_resultado, text="Para personalizar a recomendação, informe:", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Frame para Idade
        frame_idade = ttk.Frame(frame_resultado)
        frame_idade.pack(pady=5)
        ttk.Label(frame_idade, text="Sua Idade:", font=('Arial', 11)).pack(side='left', padx=5)
        spinbox_idade = ttk.Spinbox(frame_idade, from_=18, to=100, width=5, font=('Arial', 11))
        spinbox_idade.set(40)
        spinbox_idade.pack(side='left', padx=5)
        
        # Frame para Objetivo
        frame_objetivo = ttk.Frame(frame_resultado)
        frame_objetivo.pack(pady=5)
        ttk.Label(frame_objetivo, text="Seu Objetivo:", font=('Arial', 11)).pack(side='left', padx=5)
        
        objetivos_opcoes = self._get_objetivos_para_perfil(self.perfil_detectado)
        combo_objetivo = ttk.Combobox(frame_objetivo, values=objetivos_opcoes, state='readonly', width=30, font=('Arial', 11))
        if objetivos_opcoes:
            combo_objetivo.current(0)
        combo_objetivo.pack(side='left', padx=5)
        
        # Botão para Gerar Carteira
        def gerar_carteira():
            idade = int(spinbox_idade.get())
            objetivo_key = list(CARTEIRAS[self.perfil_detectado].keys())[combo_objetivo.current()]
            self.idade_usuario = idade
            self.objetivo_usuario = objetivo_key
            
            frame_resultado.pack_forget()
            self.pbar.destroy()
            self.mostrar_carteira_recomendada()
        
        ttk.Button(frame_resultado, text="Gerar Carteira Recomendada", command=gerar_carteira).pack(pady=15)
        
        self.pbar.destroy() # Remove a barra de progresso
    
    def _get_objetivos_para_perfil(self, perfil):
        """Retorna lista de objetivos disponíveis para um perfil"""
        if perfil in CARTEIRAS:
            return [nome.replace("_", " ").title() for nome in CARTEIRAS[perfil].keys()]
        return []
    
    def mostrar_carteira_recomendada(self):
        """Exibe a carteira recomendada com base no perfil, idade e objetivo"""
        frame_carteira = ttk.Frame(self.master, padding="20")
        frame_carteira.pack(fill='both', expand=True)
        
        # Título
        ttk.Label(frame_carteira, text="📊 SUA CARTEIRA RECOMENDADA 📊", font=('Arial', 18, 'bold')).pack(pady=10)
        ttk.Separator(frame_carteira, orient='horizontal').pack(fill='x', pady=5)
        
        # Informações do Usuário
        info_text = f"Perfil: {self.perfil_detectado} | Idade: {self.idade_usuario} anos | Objetivo: {self.objetivo_usuario.replace('_', ' ').title()}"
        ttk.Label(frame_carteira, text=info_text, font=('Arial', 11), foreground='cyan').pack(pady=5)
        
        # Recomendação por Idade
        faixa_idade = self._get_faixa_idade(self.idade_usuario)
        recomendacao_idade = RECOMENDACOES_IDADE.get(faixa_idade, {})
        
        ttk.Label(frame_carteira, text=recomendacao_idade.get("titulo", ""), font=('Arial', 12, 'bold'), foreground='yellow').pack(pady=8)
        ttk.Label(frame_carteira, text=recomendacao_idade.get("recomendacao", ""), wraplength=650, justify='left', font=('Arial', 10)).pack(pady=5)
        
        ttk.Separator(frame_carteira, orient='horizontal').pack(fill='x', pady=10)
        
        # Carteira de Ativos
        carteira_data = CARTEIRAS[self.perfil_detectado][self.objetivo_usuario]
        
        ttk.Label(frame_carteira, text=f"Estratégia: {carteira_data['estrategia']}", font=('Arial', 11, 'bold'), foreground='lightgreen').pack(pady=5)
        ttk.Label(frame_carteira, text=f"Descrição: {carteira_data['descricao']}", wraplength=650, justify='left', font=('Arial', 10)).pack(pady=5)
        
        # Frame com scroll para os ativos
        frame_scroll = ttk.Frame(frame_carteira)
        frame_scroll.pack(fill='both', expand=True, pady=10)
        
        canvas = tk.Canvas(frame_scroll, bg='#00145f', highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_scroll, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Exibir cada ativo
        ttk.Label(scrollable_frame, text="ALOCAÇÃO DE ATIVOS:", font=('Arial', 12, 'bold')).pack(pady=5)
        
        for ativo in carteira_data['ativos']:
            frame_ativo = ttk.Frame(scrollable_frame)
            frame_ativo.pack(fill='x', padx=10, pady=8)
            
            ttk.Label(frame_ativo, text=f"• {ativo.nome}", font=('Arial', 11, 'bold'), foreground='lightblue').pack(anchor='w')
            ttk.Label(frame_ativo, text=f"  Classe: {ativo.classe} | Alocação: {ativo.percentual}%", font=('Arial', 9)).pack(anchor='w', padx=15)
            ttk.Label(frame_ativo, text=f"  Rentabilidade Est.: {ativo.rentabilidade_estimada} | Risco: {ativo.risco}", font=('Arial', 9), foreground='lightyellow').pack(anchor='w', padx=15)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Ativa rolagem com a roda do mouse quando o ponteiro estiver sobre o canvas (Windows)
        def _on_mousewheel(event):
            # event.delta é múltiplo de 120 no Windows
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")

        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        # Recomendações Finais (movidas para dentro do scrollable_frame para poder rolar com o mouse)
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        
        ttk.Label(scrollable_frame, text="📌 RECOMENDAÇÕES FINAIS:", font=('Arial', 12, 'bold'), foreground='gold').pack(anchor='w', padx=10)
        ttk.Label(scrollable_frame, text=f"• Aporte Mensal Sugerido: {carteira_data['aporte_mensal']}", font=('Arial', 10)).pack(anchor='w', padx=20, pady=2)
        ttk.Label(scrollable_frame, text=f"• Tempo para Gerar Renda: {carteira_data['tempo_para_renda']}", font=('Arial', 10)).pack(anchor='w', padx=20, pady=2)
        ttk.Label(scrollable_frame, text="• Rebalanceie a carteira a cada 6-12 meses", font=('Arial', 10)).pack(anchor='w', padx=20, pady=2)
        ttk.Label(scrollable_frame, text="• Considere consultar um gestor patrimonial certificado (CFP)", font=('Arial', 10)).pack(anchor='w', padx=20, pady=2)

        # Mensagem final maior, centralizada e com quebra automática — dentro do scroll para continuidade
        mensagem_final = (
            "Resumo e próximos passos:\n\n"
            f"Esta carteira foi sugerida com base no seu perfil '{self.perfil_detectado}', na sua idade ({self.idade_usuario} anos) e no objetivo escolhido. "
            "Considere começar com aportes regulares, manter uma reserva de emergência e rebalancear conforme volatilidade do mercado.\n\n"
            "Atenção: a diversificação não elimina riscos. As alocações apresentadas são apenas exemplos educacionais e não constituem consultoria financeira personalizada. "
            "Para ajustar com precisão sua carteira, procure um profissional certificado (CFP) e valide produtos como CDBs, LCIs/LCAs, Tesouro Direto e Fundos Imobiliários antes de investir."
        )

        text_final = tk.Text(scrollable_frame, height=8, wrap='word', bg='#00145f', fg='white', bd=0, highlightthickness=0, font=('Arial', 11))
        text_final.tag_configure('center', justify='center')
        text_final.insert('1.0', mensagem_final)
        text_final.tag_add('center', '1.0', 'end')
        text_final.config(state='disabled')
        text_final.pack(fill='x', padx=10, pady=12)

        # Botões finais
        frame_botoes = ttk.Frame(frame_carteira)
        frame_botoes.pack(fill='x', pady=15)
        
        ttk.Button(frame_botoes, text="🔄 Refazer Teste", command=self.reiniciar_app).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="❌ Sair", command=self.master.quit).pack(side='left', padx=5)
    
    def _get_faixa_idade(self, idade):
        """Retorna a faixa etária do usuário"""
        if idade < 31:
            return "20-30"
        elif idade < 41:
            return "31-40"
        elif idade < 51:
            return "41-50"
        elif idade < 61:
            return "51-60"
        else:
            return "60+"
    
    def reiniciar_app(self):
        """Reinicia a aplicação"""
        self.master.destroy()
        root = tk.Tk()
        app = TesteInvestidorApp(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = TesteInvestidorApp(root)
    root.mainloop()