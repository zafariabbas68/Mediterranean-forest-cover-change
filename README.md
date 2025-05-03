
# Forest Cover Change Analysis in the Mediterranean Basin

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![GRASS GIS](https://img.shields.io/badge/GRASS%20GIS-8.4-green)](https://grass.osgeo.org/)

This repository contains the computational workflow for analyzing multi-temporal forest cover changes in the Mediterranean region using ESA CCI and GLC_FCS30D datasets, implemented through GRASS GIS and Python in Jupyter notebooks.

## 📌 Project Overview

- **Objective**: Quantify and visualize forest cover dynamics (1992-2020)
- **Datasets**:
  - ESA Climate Change Initiative (CCI) Land Cover
  - GLC_FCS30D Annual Global Land Cover Maps
- **Study Area**: Mediterranean basin (Lat: 28°-46°N, Lon: 10°W-36°E)
- **Methodology**: Transition matrix analysis, Change detection metrics, Spatial pattern analysis

## 🛠️ Technical Setup

### Prerequisites
- Conda/Mamba package manager
- GRASS GIS 8.4+
- Python 3.8+

### Installation
```bash
# Clone repository
git clone  https://github.com/zafariabbas68/Mediterranean-forest-cover-change
cd mediterranean-forest-cover-change

# Create conda environment
conda env create -f environment.yml
conda activate forest-change

# Initialize GRASS location (one-time setup)
python scripts/initialize_grass_location.py
```

### Configuration
Set paths in `config.yaml`:
```yaml
data_dir: ./data/input  # Raw LC datasets
output_dir: ./results   # Analysis outputs
grassdb: ~/grassdata/mediterranean_analysis
```

## 📂 Repository Structure
```
.
├── notebooks/           # Analysis workflows
│   ├── 01_data_preprocessing.ipynb
│   ├── 02_change_detection.ipynb
│   └── 03_visualization.ipynb
├── scripts/             # Reusable modules
│   ├── grass_utils.py   # GRASS GIS helpers
│   └── change_metrics.py
├── data/                # Input datasets (git-ignored)
├── results/             # Outputs (git-ignored)
└── environment.yml      # Conda environment
```

## 🚀 Workflow
1. **Preprocessing**:
   - Dataset harmonization (300m → 30m resolution)
   - Mediterranean basin masking
2. **Change Analysis**:
   ```python
   import grass.script as gs
   from scripts.change_metrics import compute_transition_matrix
   
   compute_transition_matrix(1992, 2020, 'forest')
   ```
3. **Visualization**:
   - Sankey diagrams of land cover transitions
   - Spatial hot-spot maps



## 🤝 How to Cite
If you use this code in your research, please cite:
```
Your Name (2024). Forest Cover Change Analysis in Mediterranean. [GitHub]. https://github.com/yourusername/mediterranean-forest-cover-change
```

## 📜 License
MIT License - See [LICENSE](LICENSE) for details.

## 🆘 Support
For technical issues, please open a 
