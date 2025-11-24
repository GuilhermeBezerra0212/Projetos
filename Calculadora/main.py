import customtkinter as ctk  # Importa a biblioteca customtkinter para interface moderna
import math  # Importa funções matemáticas

ctk.set_appearance_mode("dark")  # Define o modo escuro
ctk.set_default_color_theme("dark-blue")  # Define o tema de cor escuro

class Calculator(ctk.CTk):  # Define a classe principal da calculadora
	def __init__(self):  # Inicializa a janela
		super().__init__()  # Inicializa a classe base CTk
		self.title("Calculadora Científica")  # Define o título da janela
		self.geometry("600x400")  # Define o tamanho da janela
		self.configure(bg="black")  # Define o fundo preto

		self.expression = ""  # Armazena a expressão digitada

		self.display = ctk.CTkEntry(self, font=("Arial", 28), width=560, height=50, justify="right", fg_color="black", text_color="white")  # Campo de texto para mostrar a expressão/resultados
		self.display.grid(row=0, column=0, columnspan=8, padx=20, pady=(20,10))  # Posiciona o campo de texto

		buttons = [  # Matriz com os textos dos botões
			["sin", "cos", "tan", "Rad", "√", "C", "(", ")"],
			["ln", "log", "1/x", "%", "7", "8", "9", "÷"],
			["eˣ", "x²", "xʸ", "|x|", "4", "5", "6", "×"],
			["π", "e", "+/-", ".", "1", "2", "3", "-"],
			["", "", "", "", "0", "=", "+", ""]
		]

		for r, row in enumerate(buttons, 1):  # Para cada linha e coluna da matriz de botões
			for c, text in enumerate(row):
				if text:  # Se o texto não for vazio
					if text == "=":  # Se for o botão de igual
						btn = ctk.CTkButton(self, text=text, width=60, height=50, fg_color="#a06a6a", text_color="white", font=("Arial", 20, "bold"), command=self.calculate)  # Botão de igual destacado
					else:
						btn = ctk.CTkButton(self, text=text, width=60, height=50, fg_color="#222", text_color="white", font=("Arial", 18), command=lambda t=text: self.on_button_click(t))  # Botão padrão
					btn.grid(row=r, column=c, padx=6, pady=6)  # Posiciona o botão na grade

	def on_button_click(self, char):  # Função chamada ao clicar em um botão
		if char == "C":  # Limpa a expressão
			self.expression = ""
		elif char == "Rad":  # Placeholder para alternar radiano/grau
			pass
		elif char == "√":  # Raiz quadrada
			self.expression += "math.sqrt("
		elif char == "sin":  # Seno
			self.expression += "math.sin("
		elif char == "cos":  # Cosseno
			self.expression += "math.cos("
		elif char == "tan":  # Tangente
			self.expression += "math.tan("
		elif char == "ln":  # Logaritmo natural
			self.expression += "math.log("  # ln = log base e
		elif char == "log":  # Logaritmo base 10
			self.expression += "math.log10("
		elif char == "eˣ":  # Exponencial
			self.expression += "math.exp("
		elif char == "x²":  # Quadrado
			self.expression += "**2"
		elif char == "xʸ":  # Potência
			self.expression += "**"
		elif char == "|x|":  # Valor absoluto
			self.expression += "abs("
		elif char == "π":  # Pi
			self.expression += str(math.pi)
		elif char == "e":  # Número de Euler
			self.expression += str(math.e)
		elif char == "1/x":  # Inverso
			self.expression += "1/"
		elif char == "+/-":  # Troca sinal
			if self.expression and self.expression[0] == "-":
				self.expression = self.expression[1:]
			else:
				self.expression = "-" + self.expression
		elif char == "÷":  # Divisão
			self.expression += "/"
		elif char == "×":  # Multiplicação
			self.expression += "*"
		elif char == "%":  # Porcentagem
			self.expression += "/100"
		else:  # Números, ponto, parênteses, etc
			self.expression += char
		self.display.delete(0, ctk.END)  # Limpa o campo de texto
		self.display.insert(0, self.expression)  # Mostra a expressão atual

	def calculate(self):  # Função chamada ao clicar no botão de igual
		try:
			result = eval(self.expression)  # Avalia a expressão
			self.display.delete(0, ctk.END)  # Limpa o campo de texto
			self.display.insert(0, str(result))  # Mostra o resultado
			self.expression = str(result)  # Atualiza a expressão com o resultado
		except Exception:  # Se ocorrer erro
			self.display.delete(0, ctk.END)  # Limpa o campo de texto
			self.display.insert(0, "Erro")  # Mostra mensagem de erro
			self.expression = ""  # Limpa a expressão

if __name__ == "__main__":  # Executa o programa principal
	app = Calculator()  # Cria a instância da calculadora
	app.mainloop()  # Inicia o loop da interface