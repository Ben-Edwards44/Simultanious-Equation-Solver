import matrix


class Equation:
    def __init__(self, equation_str):
        self.coeffs, self.constant = self.parse_equation(equation_str)

    def seperate_coeff(self, token):
        coeff = ""
        variable = ""

        for i in token:
            if i in "012345678.":
                coeff += i
            else:
                variable += i

        if coeff == "":
            coeff = 1

        return float(coeff), variable


    def parse_equation(self, equation_str):
        tokens = equation_str.split(" ")

        coeffs = {}
        constant = 0

        prev_mult = 1
        equals_mult = 1

        for i in tokens:
            if i == "+":
                prev_mult = 1
            elif i == "-":
                prev_mult = -1
            elif i == "=":
                equals_mult = -1
            else:
                coeff, var = self.seperate_coeff(i)

                coeff *= prev_mult * equals_mult

                if var != "":
                    if var in coeffs:
                        coeffs[var] += coeff
                    else:
                        coeffs[var] = coeff
                else:
                    constant += coeff

                prev_mult = 1

        sorted_coeffs = self.sort_coeffs(coeffs)

        return sorted_coeffs, constant

    def sort_coeffs(self, coeffs):
        sorted_coeffs = {}

        for var in sorted(coeffs.keys()):
            sorted_coeffs[var] = coeffs[var]

        return sorted_coeffs        


def solve(coeff_matrix, constant_matrix):
    inv_coeff = coeff_matrix.inverse()
    result_matrix = matrix.Matrix.mat_mul(inv_coeff, constant_matrix)

    return result_matrix


def build_matrices(equations):
    coeff_matrix = []
    constant_matrix = []

    for i in equations:
        coeff_matrix.append([x for x in i.coeffs.values()])
        constant_matrix.append([-i.constant])  #use - here because the parsed equation is in the form ax + ... + c = 0

    if len(equations) <= 1 or len(coeff_matrix[0]) != len(equations):
        raise Exception("Invalid number of equations: ensure the number of equations matches the number of unknowns.")
    
    return matrix.SquareMatrix(coeff_matrix), matrix.Matrix(constant_matrix)


def output_solution(result_matrix, eq_coeffs):
    var_names = eq_coeffs.keys()

    for i, x in zip(result_matrix.mat, var_names):
        print(f"{x} = {i[0]}")


def main():
    equations = []

    while True:
        inp = input("Enter equation: ")

        if inp == "":
            break
            
        equations.append(Equation(inp))

    coeff_matrix, constant_matrix = build_matrices(equations)
    result_matrix = solve(coeff_matrix, constant_matrix)

    output_solution(result_matrix, equations[0].coeffs)


if __name__ == "__main__":
    main()