
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

I'll help you integrate the GRASS GIS environment activation into your project setup. Here's how to properly organize this:

### Recommended Approach: Create an Environment Setup Script

1. **Create a new file called `activate_grass.sh` in your `scripts/` directory**:
```bash
#!/bin/bash

# Activate Conda environment
conda activate Geogis

# Set GRASS GIS environment variables
export GISBASE="/Applications/GRASS-8.4.app/Contents/Resources"
export PATH="$GISBASE/bin:$GISBASE/scripts:$PATH"
export PYTHONPATH="$GISBASE/etc/python:$PYTHONPATH"
export GISDBASE="$HOME/grassdata"
export LOCATION_NAME="mediterranean"  # Changed to match your project
export MAPSET="PERMANENT"
export GRASS_PYTHON=python3
export GRASS_SKIP_MAPSET_OWNER_CHECK=1

# Initialize GRASS session
/Applications/GRASS-8.4.app/Contents/Resources/bin/grass "$GISDBASE/$LOCATION_NAME/$MAPSET" --exec python3 -c "import grass.script as gs; print(gs.read_command('g.version'))"

echo "GRASS GIS environment is ready"
```

2. **Make it executable**:
```bash
chmod +x scripts/activate_grass.sh
```

3. **Create a Python version (`grass_env.py`) for use in Jupyter notebooks**:
```python
import os
import subprocess

def setup_grass():
    """Setup GRASS GIS environment variables"""
    os.environ['GISBASE'] = "/Applications/GRASS-8.4.app/Contents/Resources"
    os.environ['PATH'] = f"{os.environ['GISBASE']}/bin:{os.environ['GISBASE']}/scripts:{os.environ['PATH']}"
    os.environ['PYTHONPATH'] = f"{os.environ['GISBASE']}/etc/python:{os.environ['PYTHONPATH']}"
    os.environ['GISDBASE'] = os.path.expanduser("~/grassdata")
    os.environ['LOCATION_NAME'] = "mediterranean"
    os.environ['MAPSET'] = "PERMANENT"
    os.environ['GRASS_PYTHON'] = "python3"
    os.environ['GRASS_SKIP_MAPSET_OWNER_CHECK'] = "1"
    
    # Test the setup
    try:
        import grass.script as gs
        print(gs.read_command('g.version'))
    except Exception as e:
        print(f"GRASS setup failed: {str(e)}")

if __name__ == "__main__":
    setup_grass()
```

### How to Use This:

1. **From terminal**:
```bash
source scripts/activate_grass.sh
```

2. **In Jupyter notebooks**:
```python
from grass_env import setup_grass
setup_grass()

# Now you can use GRASS Python bindings
import grass.script as gs
gs.run_command('g.list', type='raster')
```

### Recommended Repository Structure:
```
Thesis_project/
├── scripts/
│   ├── activate_grass.sh
│   ├── grass_env.py
│   └── utilities.py
├── notebooks/
│   └── 01_grass_setup.ipynb
├── environment.yml
└── README.md
```

### Update Your README.md:
Add these instructions to your README:

```markdown
## GRASS GIS Setup

1. Activate the environment:
```bash
conda activate Geogis
source scripts/activate_grass.sh
```

2. For Jupyter notebooks:
```python
from scripts.grass_env import setup_grass
setup_grass()
```

Would you like me to:
1. Add error handling to the activation script?
2. Provide a sample Jupyter notebook using this setup?
3. Explain how to create the GRASS location "mediterranean"?

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
