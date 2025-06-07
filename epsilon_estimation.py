import numpy as np
import matplotlib.pyplot as plt
import warnings
from matplotlib import MatplotlibDeprecationWarning

warnings.filterwarnings("ignore", category=MatplotlibDeprecationWarning, message=".*close_event.*")


# load A from stability_proof output
model_data = np.load('final_model_weights.npz')
A = model_data['A']

# load training data from interested_section output
# load training data from stability_proof
data = np.load('training_data_uav.npz')
e = data['e']
de = data['de']
e_interested = e[:, 0]
de_interested = e[:, 1]
dde_interested = de[:, 1]

lambda_val = 0.1

# match training structure from stability_proof.py
E_interested = np.column_stack((e_interested, de_interested))
dE_interested = np.column_stack((de_interested, dde_interested))

constraint_values = []

for t in range(len(e_interested)):
    e = E_interested[t, :].reshape(-1, 1)
    de = dE_interested[t, :].reshape(-1, 1)
    c = (de.T @ A @ e + e.T @ A @ de + lambda_val * e.T @ A @ e).item()
    constraint_values.append(c)

epsilon = max(constraint_values)
if epsilon < 0:
    epsilon = 0.0

import matplotlib
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.size'] = 12

# plot constraints
fig = plt.figure(figsize=(6.5, 2.8))
plt.plot(range(len(constraint_values)), constraint_values, linewidth=1.8, label=r"$\dot{V} + \lambda V$")
plt.xlabel('Training Sample Index')
plt.ylabel(r"$\dot{V} + \lambda V$")
plt.title('Constraints from Training Data')
plt.grid(True)

plt.axhline(y=epsilon, color='firebrick', linestyle='--', linewidth=1.5, label=r"$\epsilon$")

plt.ylim(bottom=min(constraint_values) - 0.05, top=epsilon + 0.05)

plt.text(len(constraint_values) * 0.82, epsilon + 0.005, rf"$\epsilon = {epsilon:.4f}$", color='firebrick')
plt.tight_layout()
plt.savefig('training_constraint_curve.pdf', format='pdf', bbox_inches='tight')
plt.close(fig)

print("Constraint plot saved as training_constraint_curve.pdf")

print(f"Final epsilon = {epsilon:.12f}")

with open('epsilon.txt', 'w') as f:
    f.write(str(epsilon))