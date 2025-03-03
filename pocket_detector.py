import numpy as np

class PocketDetector:
    def __init__(self, protein_grid, include_diagonals=False):
        """Initialize pocket detection based on protein grid."""
        self.protein_grid = protein_grid
        self.include_diagonals = include_diagonals
        self.pocket_grid = np.zeros_like(protein_grid.grid)

    def detect_pockets(self):
        """Detect pocket sites using geometric analysis."""
        x_bins, y_bins, z_bins = self.protein_grid.grid.shape
        for i in range(1, x_bins - 1):
            for j in range(1, y_bins - 1):
                for k in range(1, z_bins - 1):
                    if self.protein_grid.grid[i, j, k] == 0:
                        self.pocket_grid[i, j, k] = 1  # Simplified pocket detection

    def save_pockets_to_pdb(self, filename="pockets.pdb"):
        """Save detected pocket sites to a PDB file."""
        with open(filename, "w") as f:
            atom_id = 1
            for i in range(self.pocket_grid.shape[0]):
                for j in range(self.pocket_grid.shape[1]):
                    for k in range(self.pocket_grid.shape[2]):
                        if self.pocket_grid[i, j, k] > 0:
                            x = i * self.protein_grid.grid_size + self.protein_grid.x_min
                            y = j * self.protein_grid.grid_size + self.protein_grid.y_min
                            z = k * self.protein_grid.grid_size + self.protein_grid.z_min
                            f.write(f"HETATM{atom_id:5d}  POCK  POCK    1    {x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           C\n")
                            atom_id += 1
        print(f"Pocket atoms saved in {filename}")

    def find_nearby_residues(self, cutoff=4.0):
        """Identify residues near pocket sites."""
        nearby_residues = set()
        for model in self.protein_grid.structure:
            for chain in model:
                for residue in chain:
                    for atom in residue:
                        atom_coord = atom.coord
                        i, j, k = [
                            int(round((atom_coord[axis] - self.protein_grid.x_min) / self.protein_grid.grid_size))
                            for axis in range(3)
                        ]
                        if 0 <= i < self.pocket_grid.shape[0] and 0 <= j < self.pocket_grid.shape[1] and 0 <= k < self.pocket_grid.shape[2]:
                            if self.pocket_grid[i, j, k] > 0:
                                nearby_residues.add(residue)
        return nearby_residues

    def save_binding_sites(self, residues, filename="binding_site.txt"):
        """Save detected ligand binding site residues to a text file."""
        if residues is None or len(residues) == 0:
            print("No binding sites detected. Skipping file creation.")
            return
        try:
            with open(filename, "w") as f:
                for residue in residues:
                    res_name = residue.resname
                    chain_id = residue.parent.id
                    res_id = residue.id[1]
                    f.write(f"{res_name} Chain {chain_id} Residue {res_id}\n")
            print(f"Binding site saved in {filename}")
        except Exception as e:
            print(f"⚠️ Error saving {filename}: {e}")