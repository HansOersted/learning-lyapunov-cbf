import numpy as np
import re

data = np.load("final_model_weights.npz")
L = data['L']
A = data['A']

def format_matrix(mat):
    return '\n'.join(
        ['    [' + '  '.join(f"{v:.2f}" for v in row) + ']' for row in mat]
    )

latex_block = f"""L = 
{format_matrix(L)}

A = 
{format_matrix(A)}

A = L @ L.T
"""

with open("epsilon.txt", "r") as f:
    epsilon_line = f.read().strip()
    epsilon_val = float(epsilon_line)

lambda_val = 0.1
ineq_block = f"""dV + lambda * V <= epsilon
lambda = {lambda_val}, epsilon = {epsilon_val:.4f}"""

with open("lyapunov_training_report.tex", "r") as f:
    content = f.read()

content = re.sub(r"L = [\s\S]+?A = L @ L\.T", latex_block.strip(), content)

ineq_pattern = r"dV \+ lambda \* V <= epsilon\nlambda = .*?(?=\\end\{verbatim\})"
content = re.sub(ineq_pattern, ineq_block, content, flags=re.DOTALL)

with open("lyapunov_training_report.tex", "w") as f:
    f.write(content)

print("LaTeX updated")
