import os
import numpy as np

class PocketJoin:
    """
    Class to join predicted ligand binding sites if they share residues and they centers are close.
    """
    def __init__(self, pdb_id, atoms, scores):
        """
        Initialize the NearbyAtomsFinder.

        Args:
            atoms: a list of lists with the atoms found nearby per pocket by the function find_nearby_atoms of the package "atoms_finder".
            scores: original scores of the filtered voxels, without doing the average, obtained from the method get_sorted_pockets in the package "detector".
        """
        self.id = pdb_id
        self.atoms = atoms
        self.scores = scores
        self.overlaps=[]
        self.joined_atoms=[]
        self.joined_scores=[]
        self.sorted_atoms=[]

    def detect_overlaps(self):
        """
        Detect overlaps between pockets based on shared residues and proximity.
        """
        for pocket_1 in range(len(self.atoms)):
            residues_1=set(((atom[22:26].strip(), atom[20]) for atom in self.atoms[pocket_1]))
            coordinates_1= [[float(atom[26:37]), float(atom[37:45]), float(atom[45:53])] for atom in self.atoms[pocket_1]]
            counter="no" #counter to know if the first pocket is involved in an overlap
            for pocket_2 in range(pocket_1+1, len(self.atoms)):
                residues_2=set(((atom[22:26].strip(), atom[20]) for atom in self.atoms[pocket_2]))
                intersection= residues_1 & residues_2
                union= residues_1 | residues_2
                if not union:
                    continue
                if len(intersection)/len(union) > 0.2:
                    coordinates_2= [[float(atom[26:37]), float(atom[37:45]), float(atom[45:53])] for atom in self.atoms[pocket_2]]
                    center_1= [np.average([coord[0] for coord in coordinates_1]),
                               np.average([coord[1] for coord in coordinates_1]),
                               np.average([coord[2] for coord in coordinates_1])]
                    center_2= [np.average([coord[0] for coord in coordinates_2]),
                               np.average([coord[1] for coord in coordinates_2]),
                               np.average([coord[2] for coord in coordinates_2])]
                    distance= (((center_1[0] - center_2[0]) ** 2) +
                               ((center_1[1] - center_2[1]) ** 2) +
                               ((center_1[2] - center_2[2]) ** 2)) ** 0.5
                    if distance < 8:
                        self.overlaps.append(set([pocket_1, pocket_2]))
                        counter="yes"
            if counter =="no":
                self.overlaps.append(set([pocket_1]))

    def join_overlaps(self):
        """
        Join overlapping pockets into a single pocket.
        """
        changed = True
        while changed:
            changed = False
            new_overlaps = []
            while self.overlaps:
                first = self.overlaps.pop(0)
                merged = False
                for i, other in enumerate(self.overlaps):
                    if first & other:
                        self.overlaps[i] = first | other
                        merged = True
                        changed = True
                        break
                if not merged:
                    new_overlaps.append(first)
            self.overlaps = new_overlaps

    def joined_data(self):
        """
        Join the data of the overlapping pockets.
        """
        for overlap in self.overlaps:
            join_atoms=[]
            join_scores=[]
            for pocket in overlap:
                join_atoms.extend(self.atoms[pocket])
                join_scores.extend(self.scores[pocket])
            self.joined_atoms.append(join_atoms)
            self.joined_scores.append(join_scores)

    def sort_sites(self):
        """
        Score and sort the detected pockets by their average score.

        Returns:
            tuple: Sorted scores and sorted pockets.
        """
        pocket_scoring = [sum(s) / len(s) for s in self.joined_scores]
        sorting = sorted(zip(pocket_scoring, self.joined_atoms), reverse=True)
        sorted_scores, sorted_pockets = zip(*sorting) if sorting else ([], [])
        self.sorted_atoms= sorted_pockets

        return sorted_scores

    def print_results(self):
        """
        Print the results of the binding sites.
        """
        output_dir = os.path.join("results", self.id, "binding_sites")
        os.makedirs(output_dir, exist_ok=True)
        result=""
        for bin_site in range(len(self.sorted_atoms)):
            ind_result= f"Predicted ligand-binding site number {bin_site+1}\n"
            ind_result+= "".join(self.sorted_atoms[bin_site])
            file_path = os.path.join(output_dir, f"Ligand_binding_site_{self.id}_{bin_site+1}.txt")
            with open (file_path, "w") as f:
                f.write(ind_result)
            result+=ind_result+"\n"
        general_file = os.path.join(output_dir, f"Ligand_binding_site_{self.id}.txt")
        with open (general_file, "w") as f:
            f.write(result)

    def join_binding_sites(self):
        """
        Main function to join binding sites.
        """
        self.detect_overlaps()
        self.join_overlaps()
        self.joined_data()
        sorted_scores = self.sort_sites()
        self.print_results()

        print("")
        print("— — — — —  OUTPUT PHASE — — — — —")
        print(f"\033[92m✅ Pocket overlaps solved.\033[0m")
        print(f"\033[38;5;208m📂 Individual binding sites files saved to: results/{self.id}/binding_sites/\033[0m")
        print(f"\033[38;5;208m📄 General binding sites file saved to: results/{self.id}/binding_sites/Ligand_binding_site_{self.id}.txt\033[0m")

        return sorted_scores