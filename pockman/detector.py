import numpy as np
from tqdm import tqdm

class PSPDetector:
    """
    Class to perform the Pocket Spherical Projection (PSP) detection on the grid.
    """
    def __init__(self, grid):
        """
        Initialize the PSPDetector.

        Args:
            grid (Grid): Grid object holding the protein and pocket grids.
        """
        self.grid = grid
        # Initial directions: axial directions and cubic diagonals.
        self.directions = [
            # Axial directions (6)
            np.array([1, 0, 0]), np.array([-1, 0, 0]),
            np.array([0, 1, 0]), np.array([0, -1, 0]),
            np.array([0, 0, 1]), np.array([0, 0, -1]),
            # Cubic diagonals (8)
            np.array([1, 1, 1]), np.array([1, 1, -1]), np.array([1, -1, 1]), np.array([1, -1, -1]),
            np.array([-1, 1, 1]), np.array([-1, 1, -1]), np.array([-1, -1, 1]), np.array([-1, -1, -1])
        ]

    def axial(self, grid_prot, grid_count, axis: str, i: int, j: int, k: int):
        """
        Process axial directions for voxel (i, j, k).
        """
        if axis == "x":
            dirs = self.directions[0:2]
            mod = 0
            top = self.grid.x_bins
        elif axis == "y":
            dirs = self.directions[2:4]
            mod = 1
            top = self.grid.y_bins
        elif axis == "z":
            dirs = self.directions[4:6]
            mod = 2
            top = self.grid.z_bins

        coord_pos = np.array([i, j, k])
        coord_neg = np.array([i, j, k])
        prot_found_pos = False
        prot_found_neg = False

        while not prot_found_pos and coord_pos[mod] < top - 1:
            coord_pos += dirs[0]
            if grid_prot[coord_pos[0], coord_pos[1], coord_pos[2]] == 1:
                prot_found_pos = True
                break
        while not prot_found_neg and coord_neg[mod] > 0:
            coord_neg += dirs[1]
            if grid_prot[coord_neg[0], coord_neg[1], coord_neg[2]] == 1:
                prot_found_neg = True
                break
        if prot_found_neg and prot_found_pos:
            grid_count[i, j, k] += 1

    def diagonal(self, grid_prot, grid_count, plane: str, i: int, j: int, k: int):
        """
        Process diagonal directions (in a plane) for voxel (i, j, k).
        """
        if plane == "xy":
            dirs = self.directions[14:18]
            mods = [0, 1]
            tops = [self.grid.x_bins, self.grid.y_bins]
        elif plane == "yz":
            dirs = self.directions[18:22]
            mods = [1, 2]
            tops = [self.grid.y_bins, self.grid.z_bins]
        elif plane == "xz":
            dirs = self.directions[22:]
            mods = [0, 2]
            tops = [self.grid.x_bins, self.grid.z_bins]

        same_sign_coord_pos = np.array([i, j, k])
        same_sign_coord_neg = np.array([i, j, k])
        diff_sign_coord1 = np.array([i, j, k])
        diff_sign_coord2 = np.array([i, j, k])
        pf_same_pos = pf_same_neg = pf_diff1 = pf_diff2 = False

        # Same sign
        while not pf_same_pos and same_sign_coord_pos[mods[0]] < tops[0] - 1 and same_sign_coord_pos[mods[1]] < tops[1] - 1:
            same_sign_coord_pos += dirs[0]
            if grid_prot[same_sign_coord_pos[0], same_sign_coord_pos[1], same_sign_coord_pos[2]] == 1:
                pf_same_pos = True
                break
        while not pf_same_neg and same_sign_coord_neg[mods[0]] > 0 and same_sign_coord_neg[mods[1]] > 0:
            same_sign_coord_neg += dirs[3]
            if grid_prot[same_sign_coord_neg[0], same_sign_coord_neg[1], same_sign_coord_neg[2]] == 1:
                pf_same_neg = True
                break
        if pf_same_neg and pf_same_pos:
            grid_count[i, j, k] += 1

        # Different sign
        while not pf_diff1 and diff_sign_coord1[mods[0]] < tops[0] - 1 and diff_sign_coord1[mods[1]] > 0:
            diff_sign_coord1 += dirs[1]
            if grid_prot[diff_sign_coord1[0], diff_sign_coord1[1], diff_sign_coord1[2]] == 1:
                pf_diff1 = True
                break
        while not pf_diff2 and diff_sign_coord2[mods[0]] > 0 and diff_sign_coord2[mods[1]] < tops[1] - 1:
            diff_sign_coord2 += dirs[2]
            if grid_prot[diff_sign_coord2[0], diff_sign_coord2[1], diff_sign_coord2[2]] == 1:
                pf_diff2 = True
                break
        if pf_diff1 and pf_diff2:
            grid_count[i, j, k] += 1

    def cubic_diagonals(self, grid_prot, grid_count, i: int, j: int, k: int):
        """
        Process cubic diagonal directions for voxel (i, j, k).
        """
        pos_pos_pos = np.array([i, j, k])
        neg_neg_neg = np.array([i, j, k])
        neg_pos_pos = np.array([i, j, k])
        pos_neg_neg = np.array([i, j, k])
        pos_neg_pos = np.array([i, j, k])
        neg_pos_neg = np.array([i, j, k])
        pos_pos_neg = np.array([i, j, k])
        neg_neg_pos = np.array([i, j, k])
        ppp = nnn = npp = pnn = pnp = npn = ppn = nnp = False

        # All positive and all negative
        while not ppp and pos_pos_pos[0] < self.grid.x_bins - 1 and pos_pos_pos[1] < self.grid.y_bins - 1 and pos_pos_pos[2] < self.grid.z_bins - 1:
            pos_pos_pos += self.directions[6]
            if grid_prot[pos_pos_pos[0], pos_pos_pos[1], pos_pos_pos[2]] == 1:
                ppp = True
                break
        while not nnn and neg_neg_neg[0] > 0 and neg_neg_neg[1] > 0 and neg_neg_neg[2] > 0:
            neg_neg_neg += self.directions[13]
            if grid_prot[neg_neg_neg[0], neg_neg_neg[1], neg_neg_neg[2]] == 1:
                nnn = True
                break
        if ppp and nnn:
            grid_count[i, j, k] += 1

        # x axis different
        while not npp and neg_pos_pos[0] > 0 and neg_pos_pos[1] < self.grid.y_bins - 1 and neg_pos_pos[2] < self.grid.z_bins - 1:
            neg_pos_pos += self.directions[10]
            if grid_prot[neg_pos_pos[0], neg_pos_pos[1], neg_pos_pos[2]] == 1:
                npp = True
                break
        while not pnn and pos_neg_neg[0] < self.grid.x_bins - 1 and pos_neg_neg[1] > 0 and pos_neg_neg[2] > 0:
            pos_neg_neg += self.directions[9]
            if grid_prot[pos_neg_neg[0], pos_neg_neg[1], pos_neg_neg[2]] == 1:
                pnn = True
                break
        if npp and pnn:
            grid_count[i, j, k] += 1

        # y axis different
        while not pnp and pos_neg_pos[0] < self.grid.x_bins - 1 and pos_neg_pos[1] > 0 and pos_neg_pos[2] < self.grid.z_bins - 1:
            pos_neg_pos += self.directions[8]
            if grid_prot[pos_neg_pos[0], pos_neg_pos[1], pos_neg_pos[2]] == 1:
                pnp = True
                break
        while not npn and neg_pos_neg[0] > 0 and neg_pos_neg[1] < self.grid.y_bins - 1 and neg_pos_neg[2] > 0:
            neg_pos_neg += self.directions[11]
            if grid_prot[neg_pos_neg[0], neg_pos_neg[1], neg_pos_neg[2]] == 1:
                npn = True
                break
        if pnp and npn:
            grid_count[i, j, k] += 1

        # z axis different
        while not ppn and pos_pos_neg[0] < self.grid.x_bins - 1 and pos_pos_neg[1] < self.grid.y_bins - 1 and pos_pos_neg[2] > 0:
            pos_pos_neg += self.directions[7]
            if grid_prot[pos_pos_neg[0], pos_pos_neg[1], pos_pos_neg[2]] == 1:
                ppn = True
                break
        while not nnp and neg_neg_pos[0] > 0 and neg_neg_pos[1] > 0 and neg_neg_pos[2] < self.grid.z_bins - 1:
            neg_neg_pos += self.directions[12]
            if grid_prot[neg_neg_pos[0], neg_neg_pos[1], neg_neg_pos[2]] == 1:
                nnp = True
                break
        if ppn and nnp:
            grid_count[i, j, k] += 1

    def search(self, diagonals: bool = False):
        """
        Perform the PSP search by iterating over the grid and updating the pocket grid.

        Args:
            diagonals (bool): Whether to include diagonal directions.
        """
        if diagonals:
            self.directions.extend([
                # XY plane (4)
                np.array([1, 1, 0]), np.array([1, -1, 0]),
                np.array([-1, 1, 0]), np.array([-1, -1, 0]),
                # YZ plane (4)
                np.array([0, 1, 1]), np.array([0, 1, -1]),
                np.array([0, -1, 1]), np.array([0, -1, -1]),
                # XZ plane (4)
                np.array([1, 0, 1]), np.array([1, 0, -1]),
                np.array([-1, 0, 1]), np.array([-1, 0, -1])
            ])
        total_voxels = self.grid.x_bins * self.grid.y_bins * self.grid.z_bins
        for i, j, k in tqdm(
            np.ndindex(self.grid.x_bins, self.grid.y_bins, self.grid.z_bins),
            total=total_voxels,
            desc="Detecting pockets",
            mininterval=0.3,
            dynamic_ncols=True,
            leave=True
        ):
            # Process only grid points not occupied by protein and not at the boundary.
            if (self.grid.prot_grid[i, j, k] == 0 and
                0 < i < self.grid.x_bins - 1 and
                0 < j < self.grid.y_bins - 1 and
                0 < k < self.grid.z_bins - 1):
                self.axial(self.grid.prot_grid, self.grid.pocket_grid, "x", i, j, k)
                self.axial(self.grid.prot_grid, self.grid.pocket_grid, "y", i, j, k)
                self.axial(self.grid.prot_grid, self.grid.pocket_grid, "z", i, j, k)
                if diagonals:
                    self.diagonal(self.grid.prot_grid, self.grid.pocket_grid, "xy", i, j, k)
                    self.diagonal(self.grid.prot_grid, self.grid.pocket_grid, "yz", i, j, k)
                    self.diagonal(self.grid.prot_grid, self.grid.pocket_grid, "xz", i, j, k)
                self.cubic_diagonals(self.grid.prot_grid, self.grid.pocket_grid, i, j, k)
        print(f"\033[92m✅ Protein detection completed.\033[0m")

class PocketCluster:
    """
    Class to cluster grid points into binding pockets and score them.
    """
    def __init__(self, grid, protein):
        """
        Initialize the PocketCluster.

        Args:
            grid (Grid): Grid object with computed pocket grid.
            protein (ProteinStructure): Protein structure.
        """
        self.grid = grid
        self.protein = protein
        self.pockets = []
        self.scores = []

    def detect_pockets(self, diagonals: bool = False, cutoff: int = 4):
        """
        Detect binding pockets by clustering grid points that exceed the cutoff.

        Args:
            diagonals (bool): Whether diagonal PSP values were used.
            cutoff (int): Minimum grid score for a voxel to be considered.
        """
        filtered_grid_points = []
        for i in range(self.grid.pocket_grid.shape[0]):
            for j in range(self.grid.pocket_grid.shape[1]):
                for k in range(self.grid.pocket_grid.shape[2]):
                    if self.grid.pocket_grid[i, j, k] > cutoff:
                        filtered_grid_points.append([i, j, k])
        top = 13 if diagonals else 7

        while filtered_grid_points:
            pocket = [filtered_grid_points[0]]
            score = [int(self.grid.pocket_grid[filtered_grid_points[0][0],
                                                   filtered_grid_points[0][1],
                                                   filtered_grid_points[0][2]])]
            for point in pocket:
                for gp in filtered_grid_points:
                    if ((point[0]-1 == gp[0] and point[1] == gp[1] and point[2] == gp[2]) or
                        (point[0]+1 == gp[0] and point[1] == gp[1] and point[2] == gp[2]) or
                        (point[0] == gp[0] and point[1]-1 == gp[1] and point[2] == gp[2]) or
                        (point[0] == gp[0] and point[1]+1 == gp[1] and point[2] == gp[2]) or
                        (point[0] == gp[0] and point[1] == gp[1] and point[2]-1 == gp[2]) or
                        (point[0] == gp[0] and point[1] == gp[1] and point[2]+1 == gp[2])):
                        if gp not in pocket:
                            pocket.append(gp)
                            score.append(int(self.grid.pocket_grid[gp[0], gp[1], gp[2]]))
            filtered_grid_points = [gpoint for gpoint in filtered_grid_points if gpoint not in pocket]
            if set(score) != {top}:
                self.pockets.append(pocket)
                self.scores.append(score)

    def get_sorted_pockets(self):
        """
        Score and sort the detected pockets by their average score.

        Returns:
            tuple: Sorted scores and sorted pockets.
        """
        pocket_scoring = [sum(s) / len(s) for s in self.scores]
        sorting = sorted(zip(pocket_scoring, self.pockets), reverse=True)
        sorted_scores, sorted_pockets = zip(*sorting) if sorting else ([], [])
        print("Sorted pocket scores:", sorted_scores)
        print(f"\033[92m✅ Pocket clustering and scoring completed.\033[0m")
        return sorted_pockets, sorted_scores
