import subprocess
import os
import sys
import matplotlib
matplotlib.use('Agg')

TRIAL_TIMES = 100
STABILITY_SCRIPT = 'stability_proof.py'
NPZ_FILE = 'training_data_uav.npz'

if not os.path.exists(NPZ_FILE):
    print(f"❌ Required training data '{NPZ_FILE}' not found.")
    sys.exit(1)
else:
    print(f"📁 Found training data file: {NPZ_FILE}")

    OUTPUT_FILES = [
        'constraint_first_epoch.png',
        'constraint_last_epoch.png',
        'lyapunov_surface.png',
        'loss_history.png',
        'final_model_weights.npz'
    ]

    for fname in OUTPUT_FILES:
        if os.path.exists(fname):
            os.remove(fname)
            print(f"🗑️  Removed old file: {fname}")

for trial in range(1, TRIAL_TIMES + 1):
    print(f"\n🔁 Trial {trial}/{TRIAL_TIMES} for stability_proof.py")

    result = subprocess.run(
        [sys.executable, STABILITY_SCRIPT],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env={**os.environ, "MPLBACKEND": "Agg"}  # for matplotlib
    )

    print(result.stdout)

    if result.stderr:
        print("⚠️  Warnings detected:")
        print(result.stderr)
    else:
        print("✅ No warnings. Training succeeded.")
        break
else:
    print(f"❌ {STABILITY_SCRIPT} gave warnings {TRIAL_TIMES} times. Aborting.")
