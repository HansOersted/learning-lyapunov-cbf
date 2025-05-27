import warnings
import matplotlib
import matplotlib.pyplot as plt

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
num_epochs = 600
learning_rate = 1e-2
gamma = 1e-4

n1 = 1
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

    for i in range(n1):
        for t in range(length):
            de = E_interested[t, :].reshape(-1, 1)
            dde = dE_interested[t, :].reshape(-1, 1)

            hidden1 = np.maximum(0, L1 @ de + b1)
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

            constraint = dde.T @ A @ de + de.T @ A @ dde + lambda_val * de.T @ A @ de + gamma
            constraint_clean = constraint - gamma

            if epoch == 0:
                constraint_first_epoch.append(constraint_clean.item())
            if epoch == num_epochs - 1:
                constraint_last_epoch.append(constraint_clean.item())

            constraint_violation = max(0, constraint)
            loss_clean = max(0, constraint_clean)
            total_loss_clean += loss_clean

            if constraint_violation > 0:
                A1, B1 = dde.T, de
                A2, B2 = de.T, dde
                A3, B3 = de.T, de

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
            dL1 += grad_hidden1 @ de.T
            db1 += grad_hidden1

    # update the gradients
    scale = n1 * length
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

    np.savez('final_model_weights.npz', A=A_history[-1])

    if epoch % 50 == 0:
        print(f"Epoch {epoch+1}/{num_epochs} - Loss: {total_loss_clean.item():.4f}", flush=True)
        print("L_pred =\n", L_pred, flush=True)
        print("A =\n", A, flush=True)
        print("Eigenvalues of A:", np.linalg.eigvals(A), flush=True)

fig = plt.figure()
plt.plot(loss_history, linewidth=2)
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training Loss (Clean)')
plt.grid()
plt.savefig("loss_history.png")
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

e, de = np.meshgrid(np.arange(-20, 21, 1), np.arange(-20, 21, 1))
Lyap = np.zeros_like(e, dtype=float)
A_plot = A_history[-1]

for i in range(e.shape[0]):
    for j in range(e.shape[1]):
        vec = np.array([[e[i, j]], [de[i, j]]])
        Lyap[i, j] = (vec.T @ A_plot @ vec).item()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(e, de, Lyap)
ax.set_xlabel('e')
ax.set_ylabel('de')
ax.set_zlabel('V(e, de)')
ax.set_title(f'Lyapunov Function (lambda = {lambda_val})')
plt.savefig("lyapunov_surface.png")
plt.close(fig)

