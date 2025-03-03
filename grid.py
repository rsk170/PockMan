import numpy as np
from Bio import PDB

class Grid:
    def __init__(self, grid_size=1.0, border=5.0):
        """
        General Grid class that defines the voxel grid properties.

        Parameters:
            grid_size (float): Resolution in Angstroms.
            border (float): Extra space around the structure.
        """
        self.grid_size = grid_size
        self.border = border
        self.x_min, self.y_min, self.z_min = None, None, None
        self.x_bins, self.y_bins, self.z_bins = None, None, None
        self.grid = None

    def initialize_grid(self, coords):
        """Initialize the grid based on given atomic coordinates."""
        self.x_min, self.y_min, self.z_min = np.min(coords, axis=0) - self.border
        x_max, y_max, z_max = np.max(coords, axis=0) + self.border

        self.x_bins = int((x_max - self.x_min) / self.grid_size) + 1
        self.y_bins = int((y_max - self.y_min) / self.grid_size) + 1
        self.z_bins = int((z_max - self.z_min) / self.grid_size) + 1

        self.grid = np.zeros((self.x_bins, self.y_bins, self.z_bins))

    def get_grid_shape(self):
        """Return the shape of the grid."""
        return self.grid.shape if self.grid is not None else None


class ProteinGrid(Grid):
    VDW_RADII = {
        "H": 1.1,  # Hydrogen
        "C": 1.6,  # Carbon
        "N": 1.45, # Nitrogen
        "O": 1.42, # Oxygen
        "S": 1.7   # Sulfur (only in Cys & Met)
    }

    def __init__(self, pdb_file, grid_size=1.0, border=5.0):
        """
        Protein-specific grid that maps atomic positions.

        Parameters:
            pdb_file (str): Path to the input PDB file.
            grid_size (float): Resolution in Angstroms.
            border (float): Extra space around the protein.
        """
        super().__init__(grid_size, border)
        self.pdb_file = pdb_file
        self.structure = self._load_structure()
        self._initialize_protein_grid()
        self.project_protein()

    def _load_structure(self):
        """Load the PDB file using Biopython."""
        pdb_parser = PDB.PDBParser(QUIET=True)
        return pdb_parser.get_structure("protein", self.pdb_file)

    def _initialize_protein_grid(self):
        """Initialize the protein grid using atomic coordinates."""
        coords = np.array([atom.coord for atom in self.structure.get_atoms()])
        self.initialize_grid(coords)

    def _atom_range(self, x, y, z, radius):
        """Computes the voxel range occupied by an atom based on its radius."""
        neg_direction = [
            int(round((x - radius - self.x_min) / self.grid_size)),
            int(round((y - radius - self.y_min) / self.grid_size)),
            int(round((z - radius - self.z_min) / self.grid_size))
        ]
        pos_direction = [
            int(round((x + radius - self.x_min) / self.grid_size)),
            int(round((y + radius - self.y_min) / self.grid_size)),
            int(round((z + radius - self.z_min) / self.grid_size))
        ]

        neg_direction = [max(0, neg_direction[i]) for i in range(3)]
        pos_direction = [min((self.x_bins, self.y_bins, self.z_bins)[i] - 1, pos_direction[i]) for i in range(3)]

        return neg_direction, pos_direction

    def project_protein(self):
        """Mark the occupied voxels based on atomic positions and van der Waals radii."""
        for atom in self.structure.get_atoms():
            x, y, z = atom.coord
            radius = self.VDW_RADII.get(atom.element, 1.6)
            neg, pos = self._atom_range(x, y, z, radius)

            for i in range(neg[0], pos[0] + 1):
                for j in range(neg[1], pos[1] + 1):
                    for k in range(neg[2], pos[2] + 1):
                        self.grid[i, j, k] = 1  # Mark voxel as occupied