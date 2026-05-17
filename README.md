# CAB-Internship-tool

> Automated detection and statistical analysis of molecules in interstellar molecular clouds.

This repository collects all files developed during an internship at CAB (Centro de Astrobiología, CSIC-INTA) for automating the detection of molecules in one of the chemically richest zones of our Galaxy, G+0.693-0.027. The pipeline consists of two tools that must be run in sequence:

1. `madcuba_STARS` tool — runs inside MADCUBA and generates synthetic (simulated) spectra for all molecules present in the reference spectrum.
2. `python_STARS` tool — takes the output of the previous step and performs visualization and statistical analysis.

---

## Table of Contents

- [Requirements](#requirements)
- [Repository Structure](#repository-structure)
- [Workflow Overview](#workflow-overview)
- [Important Notes](#important-notes)
- [Contact](#contact)

---

## Requirements

**For the MADCUBA STARS tool:**
- [MADCUBA](https://cab.inta-csic.es/madcuba/) with Jython support (downloaded on first run). Check out the guide `How_to_use_MADCUBA_STARS_tool.pdf`.

**For the Python tool:**
- Python 3.x
- NumPy
- Matplotlib
- SciPy

For installing them, please put in your command window this prompt:
```bash
pip install numpy matplotlib scipy
```
You can check out all the features of the Python STARS tool in the guide `How_to_use_Python_STARS_tool.pdf`.

---

## Repository Structure

```
CAB-Internship-tool/
├── How_to_use_MADCUBA_STARS_tool.pdf           # Guide: running the MADCUBA STARS tool
├── How_to_use_Python_STARS_tool.pdf            # Guide: running the Python STARS tool
├── INPUT_moleculardata_Barahona2026_sample.txt # Sample molecular data input file
├── MADCUBA_STARS_Tool_sample.py                # MADCUBA macro (Jython) — Step 1
├── MADCUBA_STARS_pythoncode_Barahona2026.ipynb # Jupyter notebook — Step 2
├── SAMPLESPECTRUM.spec                         # Reference spectrum (30–50 GHz)
└── README.md
```

---

## Workflow Overview

```
SAMPLESPECTRUM.spec  +  INPUT_moleculardata_Barahona2026_sample.txt
        │
        ▼
[ Step 1 — MADCUBA_STARS_Tool_sample.py ]     ← run inside MADCUBA via Macros → Run
        │
        │  outputs:  molecular_gooddata.txt
        │            simulate_generate_<molecule>.*   (~120 files)
        ▼
[ Step 2 — MADCUBA_STARS_pythoncode_Barahona2026.ipynb ]   ← JupyterLab 
        │
        ▼
  Plots or .txt files
```

## Important Notes

> [!WARNING]
> **Spectral range limitation — read before use.**
>
> The tool currently operates only within the 30–50 GHz frequency range. The bundled reference spectrum (`SAMPLESPECTRUM.spec`) covers exclusively this window.
>
> If you need to work with a different frequency range, you must supply your own reference spectrum covering that range and update the paths in both files:
> - `MADCUBA_STARS_Tool_sample.py` — lines **23, 50, 53, 56**
> - `MADCUBA_STARS_pythoncode_Barahona2026.ipynb` — lines **151–154**
>
> Make sure your reference spectrum fulfills the following points:
> - Covers the full frequency range of your molecular data.
> - Has compatible frequency resolution and units.
> - Follows the same format as [`SAMPLESPECTRUM.spec`](SAMPLESPECTRUM.spec) (use it as a template).

---

## Contact

If you find any issues with any command of the tool, please reach out:

- **Author:** Borja Barahona Gómez — [bbarahon@ucm.es](mailto:bbarahon@ucm.es)
- **Supervisors:**
  - Miguel Sanz Novo — [msanz@cab.inta-csic.es](mailto:msanz@cab.inta-csic.es)
  - Víctor M. Rivilla Rodríguez — [vrivilla@cab.inta-csic.es](mailto:vrivilla@cab.inta-csic.es)
