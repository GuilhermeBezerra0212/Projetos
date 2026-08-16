# Projetos em Python

Coleção de estudos práticos desenvolvidos para transformar conceitos de programação em pequenas aplicações utilizáveis. Aqui o objetivo é mostrar evolução: cada projeto resolve um problema específico e registra o que foi aprendido no caminho.

> Todo mundo começa com um `Hello, World`. Eu só achei mais interessante dar a ele alguns botões e uma planilha mental.

## Projetos

| Projeto | O que faz | Competências demonstradas |
|---|---|---|
| [Calculadora científica](./Calculadora) | Interface gráfica com operações aritméticas e funções científicas | Python, CustomTkinter, eventos e organização em classes |
| [Perfil do investidor](./Perfil%20do%20Investidor) | Questionário educacional que classifica perfis e apresenta carteiras ilustrativas | Python, Tkinter, dataclasses, regras de negócio e experiência do usuário |

## Como executar

Clone o repositório e execute o arquivo `main.py` do projeto desejado.

```bash
git clone https://github.com/GuilhermeBezerra0212/Projetos.git
cd Projetos
python "Calculadora/main.py"
```

A calculadora usa `customtkinter`. Instale a dependência antes de executá-la:

```bash
pip install customtkinter
```

O projeto de perfil do investidor usa apenas bibliotecas da instalação padrão do Python.

## Contexto e limitações

Estes projetos são estudos de programação e preservam decisões tomadas durante o aprendizado. A calculadora avalia expressões construídas pela própria interface e ainda possui oportunidades de refatoração e testes.

O **Perfil do Investidor** é exclusivamente educacional. As carteiras e rentabilidades presentes no código são exemplos estáticos, não consideram o contexto individual do usuário e **não constituem recomendação de investimento**.

## Próximos passos

- adicionar testes automatizados;
- separar interface, regras de negócio e dados;
- documentar versões e requisitos;
- substituir exemplos financeiros estáticos por fontes verificáveis quando aplicável.

---

Construído por [Guilherme Bezerra](https://github.com/GuilhermeBezerra0212) como registro público de aprendizado contínuo.
