import pulp

def solve_lp(c, A, b, signs, sense="max"):
    """
    Resolve um problema de Programação Linear usando o método Simplex (CBC via PuLP).

    Args:
        c (list[float]): Coeficientes da função objetivo.
        A (list[list[float]]): Matriz de coeficientes das restrições.
        b (list[float]): Lados direitos das restrições.
        signs (list[str]): Operadores das restrições ('<=', '>=', '=').
        sense (str): 'max' para maximização, 'min' para minimização.

    Returns:
        dict: Contendo status, solução ótima, valor ótimo,
              preços-sombra e folgas das restrições.
    """

    n_vars = len(c)
    n_cons = len(A)

    # Cria variáveis de decisão
    x = [pulp.LpVariable(f"x{i+1}", lowBound=0) for i in range(n_vars)]

    # Define o tipo do problema
    if sense == "max":
        model = pulp.LpProblem("Linear_Program", pulp.LpMaximize)
    elif sense == "min":
        model = pulp.LpProblem("Linear_Program", pulp.LpMinimize)
    else:
        raise ValueError("sense deve ser 'max' ou 'min'")

    # Função objetivo
    model += pulp.lpDot(c, x), "Objective_Function"

    # Restrições
    for i in range(n_cons):
        expr = pulp.lpDot(A[i], x)
        op = signs[i]
        rhs = b[i]

        if op == "<=":
            model += expr <= rhs, f"Constraint_{i+1}"
        elif op == ">=":
            model += expr >= rhs, f"Constraint_{i+1}"
        elif op == "=":
            model += expr == rhs, f"Constraint_{i+1}"
        else:
            raise ValueError(f"Operador inválido na restrição {i+1}: {op}")

    # Resolver via CBC
    solver = pulp.PULP_CBC_CMD(msg=False)
    model.solve(solver)

    # Coleta dos resultados
    status = pulp.LpStatus[model.status]
    z_opt = pulp.value(model.objective)
    x_opt = [var.value() for var in x]

    # Preços-sombra (pi) e folgas (slack)
    shadow_prices = []
    slacks = []
    for cons in model.constraints.values():
        shadow_prices.append(cons.pi)
        slacks.append(cons.slack)

    return {
        "status": status,
        "z_opt": z_opt,
        "x_opt": x_opt,
        "sombra": shadow_prices,
        "folga": slacks
    }