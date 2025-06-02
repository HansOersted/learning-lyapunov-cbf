import numpy as np
import os

expected_ratio = 0.2  # Expected ratio of final loss to initial loss
N_check = 10          # Number of evenly spaced points to check
final_threshold = 8.0 # Maximum acceptable final loss

# Load loss history
if os.path.exists('loss_history.npy'):
    loss_history = np.load('loss_history.npy')
elif os.path.exists('loss_history.txt'):
    loss_history = np.loadtxt('loss_history.txt')
else:
    raise FileNotFoundError("Neither 'loss_history.npy' nor 'loss_history.txt' was found.")

loss_history = loss_history.flatten()
T = len(loss_history)

check_N = min(N_check, T)
check_indices = np.linspace(0, T - 1, num=check_N, dtype=int)
selected_losses = loss_history[check_indices]

# Condition 1: Overall drop is sufficient
ratio = loss_history[-1] / loss_history[0]
satisfies_ratio = ratio <= expected_ratio

# Condition 2: First N_check points are non-increasing
non_increasing = all(x >= y for x, y in zip(selected_losses[:-1], selected_losses[1:]))

# Condition 3: Final loss below absolute threshold
satisfies_final_threshold = loss_history[-1] <= final_threshold

# Output results
# print(f"Initial loss: {loss_history[0]:.6f}")
# print(f"Final loss:   {loss_history[-1]:.6f}")
# print(f"Check indices: {check_indices}")
# print(f"Selected losses: {selected_losses}")
print(f"Final/Initial ratio: {ratio:.6f} (threshold: {expected_ratio})")
print(f"Is non-increasing over selected {check_N} points? {'Yes' if non_increasing else 'No'}")
print(f"Is final loss below threshold {final_threshold}? {'Yes' if satisfies_final_threshold else 'No'}")

if satisfies_ratio and non_increasing and satisfies_final_threshold:
    print("✅ Training judged successful.")
else:
    print("❌ Training judged unsuccessful.")
