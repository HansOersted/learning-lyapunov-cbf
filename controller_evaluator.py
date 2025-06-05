import subprocess
import os
import sys
import matplotlib
matplotlib.use('Agg')

TRIAL_TIMES = 100
STABILITY_SCRIPT = 'stability_proof.py'
VERIFY_LOSS_SCRIPT = 'verify_loss_drop.py'
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
        'lyapunov_training_report.aux',
        'lyapunov_training_report.fdb_latexmk',
        'lyapunov_training_report.fls',
        'lyapunov_training_report.log',
        'lyapunov_training_report.pdf',
        'tracking_error_history.pdf',
        'lyapunov_surface.pdf',
        'training_constraint_curve.pdf',
        'loss_history.pdf',
        'lyapunov_training_report.synctex.gz',
        'epsilon.txt'
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

    # Check for warning output
    has_warning = bool(stderr_output.strip())
    if has_warning:
        print("⚠️  Warnings or errors detected:")
        print(stderr_output)
        print("🔁 Skipping verification. Retrying...")
        continue
    else:
        print("✅ No warnings.")

    # 🧪 Run verify_loss_drop.py to check convergence
    print("🔍 Verifying loss convergence...")
    result = subprocess.run(
        [sys.executable, VERIFY_LOSS_SCRIPT],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr.strip():
        print("⚠️ Error during verification:", result.stderr.strip())

    success = (
        not has_warning and
        "Training judged successful." in result.stdout
    )

    if success:
        print("🎉 Training accepted. Exiting loop.")
        # Run epsilon_estimation.py
        print("📐 Estimating epsilon using epsilon_estimation.py...")
        epsilon_result = subprocess.run(
            [sys.executable, "epsilon_estimation.py"],
            capture_output=True,
            text=True
        )
        print(epsilon_result.stdout)
        break
    else:
        print("🔁 Training not accepted. Trying again...")

else:
    print(f"❌ {STABILITY_SCRIPT} failed all {TRIAL_TIMES} attempts.")
