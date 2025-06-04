import numpy as np
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['text.usetex'] = True
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 12

data = np.load("training_data_uav.npz")
e = data["e"]

dt = 0.05
time = np.arange(len(e)) * dt
tracking_error = e[:, 0]

plt.figure(figsize=(5.5, 2.5), dpi=300)
plt.plot(time, tracking_error, linewidth=1.5)

plt.xlabel(r"Time (s)")
plt.ylabel(r"Tracking Error")
plt.title(r"Tracking Error History", fontsize=13)
plt.grid(True)
plt.tight_layout(pad=0.5)

plt.savefig("tracking_error_history.pdf", format="pdf", bbox_inches='tight')
plt.close()

print("tracking_error_history.pdf saved.")
