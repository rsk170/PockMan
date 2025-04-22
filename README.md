# PockMan 🔎

![Logo](img/logo.jpeg)

## Overview 🎯

PockMan is a bioinformatics tool designed to detect potential ligand-binding pockets in protein structures. It uses a voxel-based grid projection system to analyze protein surface features and detect potential binding sites. PockMan supports both local .pdb files and automatic downloads from the RCSB Protein Data Bank. Output includes binding site coordinates and ready-to-use visualization scripts for Chimera and PyMOL.

## Features 🔬

- **Protein Grid Projection**: Maps protein atoms onto a 3D grid.
- **Pocket Detection**: Identifies cavities using axial and optional diagonal searches.
- **Residue Clustering**: Scores and clusters likely ligand-binding sites.
- **PDB File Support**: Accepts local PDB files or downloads structures from RCSB PDB.
- **Output Visualization**: Generates Chimera & PyMOL command scripts per pocket and globally.
- **Interactive Mode**: A user-friendly wizard guides parameter selection.

## Installation 📦

### Prerequisites 🐍

Ensure you have Python 3 installed. You also need the following dependencies:

```bash
pip install numpy biopython tqdm requests setuptools
```

### Installing the Package ⚙️

#### **Standard Installation (Recommended for Users) 💻**
1. Clone the repository:
   ```bash
   git clone https://github.com/rsk170/PockMan.git
   cd PockMan
   ```
2. Install the package from the local source:
   ```bash
   pip install -e .
   ```

### Upgrading the Package 🔄

To update to the latest version after making changes:
```bash
pip install --upgrade .
```

### Uninstalling the Package ❌

If you need to remove the package:
```bash
pip uninstall PockMan
```

## Arguments ⚙️
```bash
usage: pockman [-h] [--grid_size GRID_SIZE] [--border BORDER] [--diagonals]
               [--voxel_score_cut_off CUTOFF] [--distance_threshold DIST]
               pdb_input

positional arguments:
  pdb_input             Path to the input PDB file or a valid PDB ID

optional arguments:
  -h, --help            Show this help message and exit
  --grid_size GRID_SIZE
                        Resolution in Angstroms (default: 1.0)
  --border BORDER       Extra space around the protein (default: 5.0)
  --diagonals           Include diagonal pocket detection for a more comprehensive search.
  --voxel_score_cut_off Voxel score threshold (default: 4.0)
  --distance_threshold  Voxel-to-atom proximity threshold (default: 4.0 Å)
```

## Usage 🖥️

### Interactive Mode 📝
Just type pockman with no arguments:

```bash
$ pockman
```

You'll be prompted step-by-step to input or confirm parameters like grid size, cut-off scores, and detection options — with validation and suggestions provided along the way.
```bash
➤ Enter the path to the input PDB file (or a 4‑character PDB ID): 1e28
➤ Enter grid size in Å (default 1.0, allowed 0.5 - 3.0):
➤ Enter border size in Å (default 5.0, allowed 2.0-10.0):
➤ Include planar diagonal PSP detection? (yes/no):
➤ Enter the cut-off score desired to select voxels for the pocket clustering (default 4, allowed 1-6):
➤ Enter the distance threshold to determine closeness between voxel and atoms (default 4, allowed 3-8):
```

### Command Line Execution
Run the program from the terminal with a local PDB file:
```bash
pockman 1e28.pdb --grid_size 1.0 --border 5.0
```

To use a PDB ID and download it automatically:
```bash
pockman 1e28 --grid_size 1.0 --border 5.0
```

To enable diagonal pocket detection, add the `--diagonals` flag:
```bash
pockman 1e28.pdb --grid_size 1.0 --border 5.0 --diagonals
```

Additionally, you can set the voxel score cutoff and distance threshold:
```bash
pockman 1e28 --grid_size 1.0 --border 5.0 --diagonals --voxel_score_cut_off 4 --distance_threshold 4
```

## Output Files 📂📊
Results are saved under results/{pdb_id}/, with the following structure:

```bash
results/
└── 1a28/
    ├── binding_sites/
    │   ├── Ligand_binding_site_1a28.txt
    │   ├── Ligand_binding_site_1a28_1.txt
    │   └── ...
    ├── chimera/
    │   ├── 1a28_1_chimera.cmd
    │   └── 1a28_chimera.cmd
    └── pymol/
        ├── 1a28_1_pymol.pml
        └── 1a28_pymol.pml
```

- **Ligand_binding_site_X.txt**: Residue list per pocket.
- **Ligand_binding_site_1a28.txt**: Combined binding site report.

### Chimera & PyMOL Visualization Scripts

Each predicted pocket is accompanied by ready-to-run scripts that highlight residues and atoms in that binding site, enabling fast, clear 3D visualization in popular molecular viewers:

- **1a28_X_chimera.cmd**: Visualizes pocket #X with coloring, surface display, and labels.
- **1a28_chimera.cmd**: Combined script to visualize all pockets at once.

- **1a28_X_pymol.pml**: Loads and colors pocket #X.
- **1a28_pymol.pml**:  Loads all pockets, shows surface, and labels residues.

## Example Output 💡
```bash
— — — — —  PDB FETCH PHASE — — — — —
📥 Assuming '1e28' is a PDB ID and attempting to download...
🗄  PDB file already exists: pdb_files/1e28.pdb

— — — — —  ANALYSIS PHASE — — — — —
🔬 Starting analysis...
Protein grid shape: (72, 66, 83)
✅ Protein grid projection completed.
🔍 Detecting pockets: 100%|█████████████████████████████████████████████████████████████████████| 394416/394416 [00:43<00:00, 9076.69it/s]
✅ Protein detection completed.
✅ Pocket clustering and scoring completed.
✅ Nearby atom detection completed.

— — — — —  OUTPUT PHASE — — — — —
✅ Pocket overlaps solved.
📂 Individual binding sites files saved to: results/1e28/binding_sites/
📄 General binding sites file saved to: results/1e28/binding_sites/Ligand_binding_site_1e28.txt
📂 Chimera command scripts for  individual pockets saved to: results/1e28/chimera/
📄 Chimera combined command script saved to: results/1e28/chimera/1e28_chimera.cmd
📂 PyMOL command scripts for individual pockets saved to: results/1e28/pymol/
📄 PyMOL combined script saved to: results/1e28/pymol/1e28_pymol.pml
💬 "You cannot find peace by avoiding life."
  — Virginia Woolf
```

## Contributors 👥
- Narine Fischer, Radostina Kisleva, Wael Badr

## Acknowledgments 🎖️
This tool uses **Biopython** for PDB processing, **NumPy** for grid computations, **tqdm** for progress bars
and **requests** for fetching remote files.

Special thanks to **Universitat Pompeu Fabra** and the Structural Bioinformatics and Python courses for the foundation of this project.