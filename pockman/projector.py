import numpy as np
from pockman.constants import VDW_RADII

class ProteinProjector:
    """
    Class responsible for projecting the atoms of a protein onto a 3D grid.
    """
    def __init__(self, protein, grid):
        """
        Initialize the ProteinProjector.

        Args:
            protein (ProteinStructure): Loaded protein structure.
            grid (Grid): Grid object created based on the protein.
        """
        self.protein = protein
        self.grid = grid

    def _atom_range(self, x: float, y: float, z: float, radius: float):
        """
        Compute the voxel range occupied by an atom based on its radius.

        Args:
            x (float): x-coordinate of the atom.
            y (float): y-coordinate of the atom.
            z (float): z-coordinate of the atom.
            radius (float): Van der Waals radius of the atom.

        Returns:
            tuple: Two lists (neg_direction, pos_direction) representing the min and max voxel indices.
        """
        neg_direction = [
            int(round((x - radius - self.grid.x_min) / self.grid.grid_size)),
            int(round((y - radius - self.grid.y_min) / self.grid.grid_size)),
            int(round((z - radius - self.grid.z_min) / self.grid.grid_size))
        ]
        pos_direction = [
            int(round((x + radius - self.grid.x_min) / self.grid.grid_size)),
            int(round((y + radius - self.grid.y_min) / self.grid.grid_size)),
            int(round((z + radius - self.grid.z_min) / self.grid.grid_size))
        ]
        # Ensure indices are within grid bounds
        neg_direction = [max(0, neg_direction[i]) for i in range(3)]
        pos_direction = [
            min((self.grid.x_bins, self.grid.y_bins, self.grid.z_bins)[i] - 1, pos_direction[i])
            for i in range(3)
        ]
        return neg_direction, pos_direction

    def project_atoms(self):
        """
        Mark grid voxels as occupied where protein atoms are located.
        """
        for atom in self.protein.get_atoms():
            residue = atom.get_parent()
            # Process only atoms that belong to the protein (i.e. residue id " ")
            if residue.id[0] == " ":
                x, y, z = atom.coord
                radius = VDW_RADII.get(atom.element, 1.6)
                neg, pos = self._atom_range(x, y, z, radius)
                for i in range(neg[0], pos[0] + 1):
                    for j in range(neg[1], pos[1] + 1):
                        for k in range(neg[2], pos[2] + 1):
                            self.grid.prot_grid[i, j, k] = 1 # Mark as occupied
        print("\033[92m✅ Protein grid projection completed.\033[0m")
        print("Protein grid shape:", self.grid.prot_grid.shape)
