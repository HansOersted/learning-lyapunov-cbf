import numpy as np
import matplotlib.pyplot as plt

data = np.load("training_data_uav.npz")
e = data["e"]  # tracking error over time

dt = 0.05  # time step in seconds
time = np.arange(len(e)) * dt

tracking_error = e[:, 0]

plt.figure()
plt.plot(time, tracking_error, linewidth=2)
plt.xlabel("Time (s)")
plt.ylabel("Tracking Error")
plt.title("Tracking Error History")
plt.grid(True)
plt.tight_layout()
plt.savefig("tracking_error_history.png")
plt.close()

print("tracking_error_history.png saved.")
