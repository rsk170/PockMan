from pockman.constants import VDW_RADII

class NearbyAtomsFinder:
    """
    Class to obtain the nearby atoms for each detected binding pocket and output a result file.
    """
    def __init__(self, protein, grid):
        """
        Initialize the NearbyAtomsFinder.

        Args:
            protein (ProteinStructure): Protein structure object.
            grid (Grid): Grid object containing grid parameters.
        """
        self.protein = protein
        self.grid = grid

    def find_nearby_atoms(self, sorted_pockets, threshold: float, file_tag: str):
        """
        Look for atoms near each pocket and write the results to a file.

        Args:
            sorted_pockets (list): List of pockets (each pocket is a list of grid coordinates).
            threshold (float): Distance threshold for nearby atoms.
            file_tag (str): Tag to include in the output file name.
        """
        result = []
        for pocket_idx, pocket in enumerate(sorted_pockets):
            ind_pocket = []
            atoms = []
            for grid_point in pocket:
                x = self.grid.x_min + grid_point[0] * self.grid.grid_size
                y = self.grid.y_min + grid_point[1] * self.grid.grid_size
                z = self.grid.z_min + grid_point[2] * self.grid.grid_size
                for atom in self.protein.get_atoms():
                    residue = atom.get_parent()
                    if residue.id[0] == " ":
                        distance = (((x - atom.coord[0]) ** 2) +
                                    ((y - atom.coord[1]) ** 2) +
                                    ((z - atom.coord[2]) ** 2)) ** 0.5 - VDW_RADII.get(atom.element, 1.6)
                        if distance <= threshold:
                            if [atom.coord[0], atom.coord[1], atom.coord[2]] not in atoms:
                                atoms.append([atom.coord[0], atom.coord[1], atom.coord[2]])
                                res = atom.get_parent()
                                chain = res.get_parent()
                                icode = res.id[2].strip() or ""
                                resnum = f"{res.id[1]}{icode}"
                                ind_pocket.append(f"ATOM {atom.serial_number:5d}  {atom.name:<4}{res.resname:>3} {chain.id}{resnum:>4}    {atom.coord[0]:8.3f}{atom.coord[1]:8.3f}{atom.coord[2]:8.3f}  1.00 {atom.bfactor:6.2f}           {atom.element:>2}\n")
            result.append(ind_pocket)
        print(f"\033[92m✅ Nearby atom detection completed.\033[0m")
        return result
