import warnings
import matplotlib
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.size'] = 12
import matplotlib.pyplot as plt
import os

if os.path.exists("loss_history.npy"):
    os.remove("loss_history.npy")

warnings.filterwarnings("ignore", category=matplotlib.MatplotlibDeprecationWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

import numpy as np


data = np.load('training_data_uav.npz')
e = data['e']
de = data['de']
e_interested = e[:, 0]
de_interested = e[:, 1]
dde_interested = de[:, 1]
length = len(e)

# important parameters
lambda_val = 0.1
num_epochs = 100
learning_rate = 1e-2
gamma = 1e-4

dimension = 2
h = 32  # hidden layer width

E_interested = np.column_stack((e_interested, de_interested))
dE_interested = np.column_stack((de_interested, dde_interested))

# initialization
L1 = np.random.randn(h, dimension)
b1 = np.zeros((h, 1))

L2 = np.random.randn(h, h)
b2 = np.zeros((h, 1))

L_out = np.random.randn(int(dimension * (dimension + 1) / 2), h)
b_out = np.zeros((int(dimension * (dimension + 1) / 2), 1))

loss_history = np.zeros(num_epochs)
constraint_history = np.zeros(num_epochs)
constraint_first_epoch = []
constraint_last_epoch = []
A_history = []
L_history = []

for epoch in range(num_epochs):
    total_loss_clean = 0

    dL1 = np.zeros_like(L1)
    db1 = np.zeros_like(b1)
    dL2 = np.zeros_like(L2)
    db2 = np.zeros_like(b2)
    dL_out = np.zeros_like(L_out)
    db_out = np.zeros_like(b_out)

    for t in range(length):
        e = E_interested[t, :].reshape(-1, 1)
        de = dE_interested[t, :].reshape(-1, 1)

        hidden1 = np.maximum(0, L1 @ e + b1)
        hidden2 = np.maximum(0, L2 @ hidden1 + b2)

        L_flat = L_out @ hidden2 + b_out
        L_pred = np.zeros((dimension, dimension))
        tril_indices = np.tril_indices(dimension)
        L_pred[tril_indices] = L_flat.flatten()
        diag_idx = np.diag_indices(dimension)
        L_pred[diag_idx] = np.log(1 + np.exp(L_pred[diag_idx]))

        if np.isinf(L_pred).any():
            warnings.warn("L_pred contains Inf values!")
        if np.isnan(L_pred).any():
            warnings.warn("L_pred contains NaN values!")

        A = L_pred @ L_pred.T

        if np.isinf(A).any():
            warnings.warn("A contains Inf values!")
        if np.isnan(A).any():
            warnings.warn("A contains NaN values!")

        constraint = de.T @ A @ e + e.T @ A @ de + lambda_val * e.T @ A @ e + gamma
        constraint_clean = constraint - gamma

        if epoch == 0:
            constraint_first_epoch.append(constraint_clean.item())
        if epoch == num_epochs - 1:
            constraint_last_epoch.append(constraint_clean.item())

        constraint_violation = max(0, constraint)
        loss_clean = max(0, constraint_clean)
        total_loss_clean += loss_clean

        if constraint_violation > 0:
            A1, B1 = de.T, e
            A2, B2 = e.T, de
            A3, B3 = e.T, e

            grad_constraint = (A1.T @ B1.T + B1 @ A1) @ L_pred \
                            + (A2.T @ B2.T + B2 @ A2) @ L_pred \
                            + lambda_val * (A3.T @ B3.T + B3 @ A3) @ L_pred

            softplus_derivative = 1 / (1 + np.exp(-L_pred))
            grad_constraint[diag_idx] *= softplus_derivative[diag_idx]
        else:
            grad_constraint = np.zeros_like(L_pred)

        grad_L_flat = grad_constraint[tril_indices].reshape(-1, 1)
        dL_out += grad_L_flat @ hidden2.T
        db_out += grad_L_flat

        grad_hidden2 = (L_out.T @ grad_L_flat) * (hidden2 > 0)
        dL2 += grad_hidden2 @ hidden1.T
        db2 += grad_hidden2

        grad_hidden1 = (L2.T @ grad_hidden2) * (hidden1 > 0)
        dL1 += grad_hidden1 @ e.T
        db1 += grad_hidden1

    # update the gradients except for the last epoch
    scale = length
    if epoch <= num_epochs - 2:
        L1 -= learning_rate * dL1 / scale
        b1 -= learning_rate * db1 / scale
        L2 -= learning_rate * dL2 / scale
        b2 -= learning_rate * db2 / scale
        L_out -= learning_rate * dL_out / scale
        b_out -= learning_rate * db_out / scale

    loss_history[epoch] = float(total_loss_clean)
    constraint_history[epoch] = constraint.item()
    A_history.append(A)
    L_history.append(L_pred)

    np.savez('final_model_weights.npz', A=A_history[-1], L=L_history[-1])

    if (epoch + 1) % 50 == 0:
        print(f"Epoch {epoch+1}/{num_epochs} - Loss: {float(total_loss_clean):.4f}", flush=True)
        print("L_pred =\n", L_pred, flush=True)
        print("A =\n", A, flush=True)
        print("Eigenvalues of A:", np.linalg.eigvals(A), flush=True)

fig = plt.figure(figsize=(5.5, 2.5))
plt.plot(loss_history, linewidth=1.5)
plt.xlabel(r"Epoch")
plt.ylabel(r"Loss")
plt.title(r"Training Loss History")
plt.grid(True)
plt.tight_layout(pad=0.5)
plt.savefig("loss_history.pdf", format="pdf", bbox_inches='tight')
plt.close(fig)

fig = plt.figure()
plt.plot(constraint_first_epoch, linewidth=2)
plt.xlabel('Training Sample Index')
plt.ylabel('Constraint Value')
plt.title('Constraints in the First Epoch (Clean)')
plt.grid()
plt.savefig("constraint_first_epoch.png")
plt.close(fig)

fig = plt.figure()
plt.plot(constraint_last_epoch, linewidth=2)
plt.xlabel('Training Sample Index')
plt.ylabel('Constraint Value')
plt.title('Constraints in the Last Epoch (Clean)')
plt.grid()
plt.savefig("constraint_last_epoch.png")
plt.close(fig)

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable

e, de = np.meshgrid(np.arange(-20, 21, 1), np.arange(-20, 21, 1))
Lyap = np.zeros_like(e, dtype=float)
A_plot = A_history[-1]

for i in range(e.shape[0]):
    for j in range(e.shape[1]):
        vec = np.array([[e[i, j]], [de[i, j]]])
        Lyap[i, j] = (vec.T @ A_plot @ vec).item()

fig = plt.figure(figsize=(8, 5.5))
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(
    e, de, Lyap,
    cmap='inferno',      # viridis, plasma, cividis
    edgecolor='none',
    antialiased=True
)

ax.set_xlabel(r"$e$")
ax.set_ylabel(r"$\dot{e}$")
ax.set_zlabel(r"$V(e, \dot{e})$")
ax.set_title(r"Lyapunov Function Surface $(\lambda = {:.2f})$".format(lambda_val), fontsize=13)

cbar = fig.colorbar(surf, ax=ax, shrink=0.7, pad=0.15, aspect=20)
cbar.set_label(r"$V(e, \dot{e})$")

fig.subplots_adjust(left=0.05, right=0.88, top=0.95, bottom=0.05)

plt.savefig("lyapunov_surface.pdf", format="pdf", bbox_inches='tight')
plt.close(fig)

np.save("loss_history.npy", loss_history)
