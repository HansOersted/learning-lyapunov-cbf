import numpy as np
import re

# 读取 L 和 A
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

# 读取 epsilon
with open("epsilon.txt", "r") as f:
    epsilon_line = f.read().strip()
    epsilon_val = float(epsilon_line.split('=')[-1].strip())

lambda_val = 0.1
ineq_block = f"""dV + lambda * V <= epsilon
lambda = {lambda_val}, epsilon = {epsilon_val:.4f}"""

# 替换 LaTeX 文件内容
with open("lyapunov_training_report.tex", "r") as f:
    content = f.read()

# 替换矩阵部分
content = re.sub(r"L = [\s\S]+?A = L @ L\.T", latex_block.strip(), content)

# 替换不等式参数部分
content = re.sub(r"dV \+ lambda \* V <= epsilon\nlambda = .*?, epsilon = .*?",
                 ineq_block.strip(), content)

with open("lyapunov_training_report.tex", "w") as f:
    f.write(content)

print("✅ LaTeX 文件已成功更新：L、A 和 epsilon")
