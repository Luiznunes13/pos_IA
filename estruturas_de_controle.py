# Situação-Problema: Classificação de Peças na Esteira de Produção Automatizada
# •Uma fábrica que opera com tecnologias de manufatura inteligente deseja implementar um sistema básico de
# classificação de peças. Para isso, após a leitura de sensores, o operador deve informar:
# •A temperatura da peça (em °C)
# •O peso da peça (em kg)
# •A espessura da peça (em mm)
# •O sistema deve, com base nesses dados:
# •Verificar se a peça está superaquecida (temperatura acima de 80°C) ou com temperatura baixa (abaixo de
# 60°C).
# •Se a temperatura estiver adequada (entre 60 e 80°C, inclusive), o sistema deve analisar se peso e espessura
# estão dentro do padrão (peso entre 9 e 11 kg e espessura entre 1.8 e 2.2 mm).
# •Por fim, o sistema deve exibir uma mensagem indicando se a peça foi aprovada ou rejeitada, junto ao motivo
# da rejeição (temperatura inadequada ou dimensão fora do padrão).

# Entrada dos dados
temperatura = float(input("Informe a temperatura da peça (°C): "))
peso = float(input("Informe o peso da peça (kg): "))
esspessura = float(input("Informe a espessura da peça (mm): "))

# Lista para armazenar erros
erros = []

# Verificação da temperatura
if temperatura > 80:
    erros.append("temperatura superaquecida")
elif temperatura < 60:
    erros.append("temperatura baixa")

# Verificação de peso
if not (9 <= peso <= 11):
    erros.append("peso fora do padrão")

# Verificação de espessura
if not (1.8 <= esspessura <= 2.2):
    erros.append("espessura fora do padrão")

# Resultado final
if erros:
    print("Peça rejeitada pelos seguintes motivos:")
    for erro in erros:
        print(f"- {erro}")
else:
    print("Peça aprovada!")