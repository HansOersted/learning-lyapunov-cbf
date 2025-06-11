# Learning Lyapunov Functions from Data

> “My professor asked me to find a Lyapunov candidate.  
> I spent the whole afternoon and missed my date at Tivoli (amusement park in Denmark).  
> Now she says we’re over 💔.”  
> — Thomas, heartbroken but now stable

What used to take a heartbreak 💔 — now takes one command in this repository.

<img src="https://github.com/user-attachments/assets/fbbd9abd-ead4-4227-80d2-64125da81efc" alt="Lyapunov Banner" width="80%">

## 💡 What It Does


Given the tracking result, this repository automates the search for Lyapunov candidate.  
And it even gives us a PDF report automatically!

<div>&nbsp;&nbsp;&nbsp;&nbsp;🧼 Whiteboard math?  
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Gone.</div>

<div>&nbsp;&nbsp;&nbsp;&nbsp;🎯 Blind guessing?  
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Gone.</div>

<div>&nbsp;&nbsp;&nbsp;&nbsp;💔 Romantic tragedy?  
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Completely avoidable.</div>

## 🧪 Environment

To run this project successfully, make sure you have the following:

### Python

- Python 3.8 or later
- Install dependencies with:

```bash
pip install -r requirements.txt
```

### LaTeX

To compile the final report, you need a LaTeX engine and required packages:

```bash
sudo apt install -y texlive-full
```

Alternatively, run 

```
sudo apt update && sudo apt install -y texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra cm-super dvipng latexmk lmodern texlive-lang-cjk texlive-xetex texlive-luatex
```

## 🚀 Quick Start

Once your environment is set up, find the Lyapunov candidate in 3 steps:

---

### *(Optional)* Step 1. Load the tracking result

*To beginners:*  
**Skip this step!** The default tracking result is collected from the flight of a UAV simulator.

*To advanced users:*  
Replace with the interested tracking result for analysis.

---

### Step 2. Find the Lyapunov candidate

Simply run and wait:

```bash
python3 run_pipeline.py
```

This will generate `lyapunov_training_report.tex` for the next step.

---

### Step 3. Generate the PDF report

Compile `lyapunov_training_report.tex`:

```bash
latexmk -pdf lyapunov_training_report.tex
```

Finally, a Lyapunov candidate is found with a training report `lyapunov_training_report.pdf`.


## 📸 Output Preview

At the end of the pipeline, you'll get a beautiful auto-generated PDF report:

👉 [lyapunov_training_report.pdf](https://github.com/user-attachments/files/20640749/lyapunov_training_report.pdf)

<img src="https://github.com/user-attachments/assets/0ffeb331-cdf4-4c98-8448-808e62c272b8" width="30%"> <img src="https://github.com/user-attachments/assets/458dded4-a22e-4bf5-aa20-d2f7b4b0acf9" width="30%"> <img src="https://github.com/user-attachments/assets/4346b0da-e85b-494b-8a54-7a1ab9400154" width="30%">

It includes:
- Tracking error history (input data)
- Training loss curve
- Final Lyapunov function form
- 3D Lyapunov surface plot
- Final constraint inequality


No manual math. No stress. Just data → Lyapunov candidate.


## 📚 Related Paper

This repository accompanies our IROS 2025 submission:

**[Towards Data-Driven Model-Free Safety-Critical Control](https://arxiv.org/abs/2506.06931)**  
_Zhe Shen, Yitaek Kim, Christoffer Sloth, 2025_

If you found this repository useful, consider citing our paper.


### 📖 BibTeX

```bibtex
@article{lyapunov2025towards,
  title={Towards Data-Driven Model-Free Safety-Critical Control},
  author={Shen, Zhe and Kim, Yitaek and Sloth, Christoffer},
  journal={arXiv preprint arXiv:2506.06931},
  year={2025}
}
