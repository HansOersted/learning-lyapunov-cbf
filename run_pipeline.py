import subprocess
import os

def run_step(description, command):
    print(f"\n=== {description} ===")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed during: {description}")
        print(e)
        exit(1)

if __name__ == "__main__":
    # Step 1: Run controller_evaluator.py
    run_step("Step 1: Running controller_evaluator.py", ["python3", "controller_evaluator.py"])

    # Step 2: Run plot_tracking_error.py
    run_step("Step 2: Running plot_tracking_error.py", ["python3", "plot_tracking_error.py"])

    # Step 3: Run epsilon_estimation.py
    run_step("Step 3: Running epsilon_estimation.py", ["python3", "epsilon_estimation.py"])

    # Step 4: Run update_latex.py
    run_step("Step 4: Running update_latex.py", ["python3", "update_latex.py"])