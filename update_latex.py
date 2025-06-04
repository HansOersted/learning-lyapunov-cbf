import numpy as np
import re

data = np.load("final_model_weights.npz")
L = data["L"]
A = data["A"]

def matrix_to_bmatrix(name, mat):
    lines = [f"{name} &= \\begin{{bmatrix}}"]
    for row in mat:
        row_str = ' & '.join(f"{v:.2f}" for v in row)
        lines.append(f"{row_str} \\\\")
    lines.append("\\end{bmatrix}")
    return '\n'.join(lines)

latex_block = (
    "\\begin{align}\n"
    f"{matrix_to_bmatrix('L', L)}, \\\\\n"
    f"{matrix_to_bmatrix('A', A)}.\n"
    "\\end{align}"
)

with open("epsilon.txt", "r") as f:
    epsilon_val = float(f.read().strip())

lambda_val = 0.1
ineq_block = f"""dV + lambda * V <= epsilon
lambda = {lambda_val}, epsilon = {epsilon_val:.4f}"""

with open("lyapunov_training_report.tex", "r") as f:
    content = f.read()

content = re.sub(r"\\begin{align}[\s\S]+?\\end{align}", lambda _: latex_block, content)

ineq_pattern = r"dV \+ lambda \* V <= epsilon\nlambda = .*?(?=\\end\{verbatim\})"
content = re.sub(ineq_pattern, ineq_block, content, flags=re.DOTALL)

with open("lyapunov_training_report.tex", "w") as f:
    f.write(content)

print("LaTeX report updated successfully.")
