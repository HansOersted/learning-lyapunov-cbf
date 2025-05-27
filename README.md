# Learning Lyapunov Functions from Data

This repository demonstrates how to learn a candidate Lyapunov function from trajectory data. The system adopts the UAV dynamics simulated in Simulink for the data collection.

With the collected date, a Lyapunov function is trained using a Python script based on a parameterized neural representation.

---

## 🧠 System Model

The system under consideration is a UAV stabilized by a closed-loop PD controller:

![System Model](system_model.png)

Simulink is used to simulate the system and export tracking errors $e\$, $e = r - x\$:

```math
e(t), \\
\dot{e}(t), \\
\ddot{e}(t)
```

These collected tracking errors are for the training purpose in this repository.

---

## 💻 Repository Contents


| File                                  | Description                                                                                            |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `controller_evaluator.py`             | Automatically runs training with retries if warnings occur; removes old result files before each trial |
| `stability_proof.py`                  | Core script that trains a positive-definite Lyapunov function\( V(x) = x^\top A x \)                   |
| `training_data_uav.npz`               | Pre-collected trajectory data from Simulink (contains ($e\$, $\dot{e}\$, $\ddot{e}\$)                  |
| `final_model_weights.npz` [output]    | Output file containing the learned matrix$\( A \)$                                                     |
| `loss_history.png` [output]           | Training loss plot                                                                                     |
| `constraint_first_epoch.png` [output] | Constraint violations at first epoch                                                                   |
| `constraint_last_epoch.png` [output]  | Constraint violations at final epoch                                                                   |
| `lyapunov_surface.png` [output]       | 3D surface of the learned Lyapunov function                                                            |

> **Note**: `epsilon_estimation.py` is included and will be later updated.

---

## 🔁 Reproducibility

To ensure full reproducibility:

1. All result files are automatically deleted at the beginning of each trial.
2. The script `controller_evaluator.py` runs training up to 100 times if necessary until no numerical warnings occur.
3. All plotting is non-interactive (`matplotlib.use("Agg")`) and safe for headless environments.

---

## 🚀 How to Run

1. Make sure you have:

   - Python 3.8+
   - `numpy`, `matplotlib`, `scipy`
2. Run the training process:

```bash
python controller_evaluator.py
```
