---

# Project Name
Test Program for Atypical Inventive Problem Solving Based on the Integration of Large Language Models and TRIZ

## Introduction
Aiming at the complexity and steep learning curve of solving atypical inventive problems, this work combines the text reasoning and generation capabilities of large language models with TRIZ to construct an automated problem-solving framework.
The system supports six sequential steps: input of original problem text, structured information extraction from problem descriptions, formulation of physical contradictions, causal chain expansion and causal condition analysis, generation of solving strategies using separation principles, and recommendation of solutions. Among these steps, only the initial problem input requires manual participation; all other modules are executed automatically. The system can be applied in scientific research experiments, engineering innovation assistance, teaching demonstrations, and similar scenarios.

Five preset cases are stored in `clscaseset.py`, and users only need to set the corresponding index in `main.py` to run them. New cases can be added to the list within the `clscaseset` class. The test system records intermediate reasoning data, which is saved in `experiments/source`. It supports clustering of system outputs; clustering results are stored in `experiments/cluster`, and radar charts generated from clustering results are saved in `experiments/visualdata`.

## Environment Setup
### Dependencies
python 3.11–3.14
langchain_core==1.2.7
langchain_community==0.4.1
langchain_deepseek==1.0.1

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Running Instructions
### Clone Repository
```bash
git clone https://github.com/j2202ason/NTCS-paper-experiment-2026.git
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configuration
1. Set the DeepSeek environment variable and API key.
2. In `main.py`, assign the DeepSeek API key to the `api_key` variable, for example:
   ```python
   api_key = "DEEPSEEK_API_KEY"  # set deepseek api key
   ```

### Run Main Program
```bash
python main.py
```

## Project Structure
- `main.py` — main program entry
- `*.py` — core code modules
- `experiments/` — experimental data
  - `source/` — core runtime data
  - `extractor/` — analysis process data
  - `cluster/` — clustering results
  - `visualdata/` — radar chart outputs
- `requirements.txt` — dependency list

## Citation
```bibtex
@article{your_paper,
  title={Solving non-typical Inventive Problems Based on TRIZ with Large Language Model Integration},
  author={Shang Liu and others},
  journal={...},
  year={2026}
}
```

---
