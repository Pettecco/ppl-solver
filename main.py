from solver import solve_lp

def main():
    print("=== Solucionador de PPL (Método Simplex via PuLP) ===\n")

    # Tipo de problema
    problem_type = input("Tipo de problema (max/min): ").strip().lower()
    if problem_type not in ["max", "min"]:
        print("Entrada inválida! Use 'max' ou 'min'.")
        return

    n_vars = int(input("Quantas variáveis? "))
    n_cons = int(input("Quantas restrições? "))

    # Função objetivo
    print("\nDigite os coeficientes da função objetivo:")
    objective_coeffs = []
    for i in range(n_vars):
        val = float(input(f"  Coeficiente c{i+1}: "))
        objective_coeffs.append(val)

    # Restrições
    print("\nDigite as restrições no formato:")
    print("  a1*x1 + a2*x2 + ... + an*xn (<=, >=, =) b")

    constraint_matrix = []
    rhs_values = []
    operators = []

    for i in range(n_cons):
        print(f"\nRestrição {i+1}:")
        row = []
        for j in range(n_vars):
            coef = float(input(f"  Coeficiente a{i+1}{j+1}: "))
            row.append(coef)
        op = input("  Operador (<=, >=, =): ").strip()
        rhs = float(input("  Valor b: "))
        constraint_matrix.append(row)
        operators.append(op)
        rhs_values.append(rhs)

    result = solve_lp(objective_coeffs, constraint_matrix, rhs_values, operators, sense=problem_type)

    print("\n=== RESULTADOS ===")
    print("Status da solução:", result["status"])

    if result["status"] == "Optimal":
        label = "Lucro máximo" if problem_type == "max" else "Custo mínimo"
        print(f"{label} (Z*) = {result['z_opt']:.4f}\n")

        print("Valores ótimos das variáveis:")
        for i, val in enumerate(result["x_opt"], start=1):
            print(f"  x{i} = {val:.4f}")

        print("\nPreços-sombra (valores duais):")
        for i, val in enumerate(result["sombra"], start=1):
            print(f"  Restrição {i}: {val:.4f}")

        print("\nFolgas das restrições:")
        for i, val in enumerate(result["folga"], start=1):
            print(f"  Restrição {i}: {val:.4f}")
    else:
        print("Não foi encontrada solução ótima.")

if __name__ == "__main__":
    main()
