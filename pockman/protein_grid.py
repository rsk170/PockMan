import numpy as np
import copy as cp

class ProteinGrid:
    """
    Class to generate and store the 3D grid (voxel) representation for the protein and potential binding pockets.
    """
    def __init__(self, protein, grid_size: float = 1.0, border: float = 5.0):
        """
        Initialize the Grid based on a given protein structure.

        Args:
            protein (ProteinStructure): Loaded protein structure.
            grid_size (float): Resolution in Angstroms.
            border (float): Extra space around the protein.
        """
        self.protein = protein
        self.grid_size = grid_size
        self.border = border
        self._calculate_bounds()
        self._initialize_grids()

    def _calculate_bounds(self):
        """
        Calculate the spatial boundaries and the number of bins (voxels) along each axis.
        """
        atoms = list(self.protein.get_atoms())
        coords = np.array([atom.coord for atom in atoms])
        self.x_min, self.y_min, self.z_min = np.min(coords, axis=0) - self.border
        self.x_max, self.y_max, self.z_max = np.max(coords, axis=0) + self.border

        self.x_bins = int((self.x_max - self.x_min) / self.grid_size) + 1
        self.y_bins = int((self.y_max - self.y_min) / self.grid_size) + 1
        self.z_bins = int((self.z_max - self.z_min) / self.grid_size) + 1

    def _initialize_grids(self):
        """
        Initialize the protein grid and pocket grid as 3D numpy arrays.
        """
        self.prot_grid = np.zeros((self.x_bins, self.y_bins, self.z_bins))
        self.pocket_grid = cp.deepcopy(self.prot_grid)

    def print_grid_shapes(self):
        """
        Print the shapes of the protein grid and pocket grid.
        """
        print("Protein grid shape:", self.prot_grid.shape)
        print("Pocket grid shape:", self.pocket_grid.shape)
