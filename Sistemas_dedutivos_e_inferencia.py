#-------------------------------------------------------------------
# Simulação do Motor de Inferência usando Modus Ponens
#-------------------------------------------------------------------

# A: "O Robô_12 está parado." (Verdadeiro)
# B: "A luz de energia do Robô_12 está apagada." (Verdadeiro)


# 1. Base de Conhecimento (Regras que o sistema conhece)
base_de_conhecimento = {
    "Regra_1": "B → C",  # Se a luz de energia está apagada, então há uma falha de energia.
    "Regra_2": "B ∧ C → D",   # Se o robô está parado E há uma falha de energia, então o problema é elétrico.
    "Regra_3": "D → E"  # Se o problema é elétrico, então o robô precisa de elétrica.
}

# 2. Base de Fatos (O que os sensores estão dizendo AGORA)
#    Inicialmente, só temos a leitura do sensor de temperatura.
base_de_fatos = {
    'A': True,   # O Robô_12 está parado.
    'B': True,   # A luz de energia do Robô_12 está apagada.
    'C': False,  # Há uma falha de energia.
    'D': False,  # O problema é elétrico.
    'E': False   # Notificar a equipe de elétrica.
}

print("--- Ciclo de Inferência ---")
print(f"Estado Inicial dos Fatos: {base_de_fatos}")

# O MOTOR DE INFERÊNCIA COMEÇA A TRABALHAR
print("\n... Motor de Inferência procurando regras aplicáveis ...")

# Tentativa de aplicar Regra_1: B → C
# O motor verifica se o antecedente ('B') da regra está na base de fatos como 'True'.
if base_de_fatos.get('B') is True:
    print("\n[Passo 1]: Modus Ponens aplicado!")
    print(f"  - Fato 'B' é Verdadeiro.")
    print(f"  - Regra 'B → C' existe.")
    print(f"  - Conclusão: Inferimos que 'C' também é Verdadeiro.")

    # A conclusão é adicionada à base de fatos.
    base_de_fatos['C'] = True
    print(f"  - Novo Estado dos Fatos: {base_de_fatos}")
else:
    print("\n[Passo 1]: Antecedente de 'B → C' não encontrado como Verdadeiro.")

# O motor faz outra varredura com a base de fatos atualizada.
print("\n... Motor de Inferência procurando regras aplicáveis novamente ...")

# Tentativa de aplicar Regra_2: B ∧ C → D
# O motor verifica se o antecedente ('B' e 'C') da regra está na base de fatos como 'True'.
if base_de_fatos.get('B') is True and base_de_fatos.get('C') is True:
    print("\n[Passo 2]: Modus Ponens aplicado!")
    print(f"  - Fatos 'B' e 'C' são Verdadeiros.")
    print(f"  - Regra 'B ∧ C → D' existe.")
    print(f"  - Conclusão: Inferimos que 'D' também é Verdadeiro.")

    # A conclusão final é adicionada à base de fatos.
    base_de_fatos['D'] = True
    print(f"  - Estado Final dos Fatos: {base_de_fatos}")
else:
    print("\n[Passo 2]: Antecedente de 'B ∧ C → D' não encontrado como Verdadeiro.")

# O motor faz outra varredura com a base de fatos atualizada.
print("\n... Motor de Inferência procurando regras aplicáveis novamente ...")

# Tentativa de aplicar Regra_3: D → E
# O motor verifica se o antecedente ('D') da regra está na base de fatos como 'True'.
if base_de_fatos.get('D') is True:
    print("\n[Passo 3]: Modus Ponens aplicado!")
    print(f"  - Fato 'D' (inferido no passo anterior) é Verdadeiro.")
    print(f"  - Regra 'D → E' existe.")
    print(f"  - Conclusão: Inferimos que 'E' também é Verdadeiro.")

    # A conclusão final é adicionada à base de fatos.
    base_de_fatos['E'] = True
    print(f"  - Estado Final dos Fatos: {base_de_fatos}")

    # Uma ação no mundo real seria executada.
    print("\n[AÇÃO FINAL]: Sistema notifica a equipe de elétrica para verificar o Robô_12!")
else:
    print("\n[Passo 3]: Antecedente de 'D → E' não encontrado como Verdadeiro.")
