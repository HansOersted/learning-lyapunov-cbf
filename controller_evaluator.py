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
        'final_model_weights.npz',
        'training_constraint_curve.png',
        'final_model_weights.npz'
    ]

    for fname in OUTPUT_FILES:
        if os.path.exists(fname):
            os.remove(fname)
            print(f"🗑️  Removed old file: {fname}")

for trial in range(1, TRIAL_TIMES + 1):
    print(f"\n🔁 Trial {trial}/{TRIAL_TIMES} for {STABILITY_SCRIPT}")

    process = subprocess.Popen(
        [sys.executable, STABILITY_SCRIPT],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
        universal_newlines=True,
        env={**os.environ, "MPLBACKEND": "Agg"}
    )

    for line in process.stdout:
        print(line, end='')

    process.wait()
    stderr_output = process.stderr.read()

    if stderr_output.strip():
        print("⚠️  Warnings or errors detected:")
        print(stderr_output)
    else:
        print("✅ No warnings. Training succeeded.")
        break
else:
    print(f"❌ {STABILITY_SCRIPT} gave warnings {TRIAL_TIMES} times. Aborting.")
