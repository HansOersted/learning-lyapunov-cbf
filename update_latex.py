import numpy as np

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

with open("lyapunov_training_report.tex", "r") as f:
    content = f.read()

import re
pattern = r"L = [\s\S]+?A = L @ L\.T"
content = re.sub(pattern, latex_block.strip(), content)

with open("lyapunov_training_report.tex", "w") as f:
    f.write(content)

print("LaTeX updated")
