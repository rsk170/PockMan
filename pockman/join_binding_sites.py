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
        for pocket_1 in range(len(self.atoms)):
            residues_1=set(((int(atom[22:26]), atom[20]) for atom in self.atoms[pocket_1]))
            coordinates_1= [[float(atom[26:37]), float(atom[37:45]), float(atom[45:53])] for atom in self.atoms[pocket_1]]
            counter="no" #counter to know if the first pocket is involved in an overlap
            for pocket_2 in range(pocket_1+1, len(self.atoms)):
                residues_2=set(((int(atom[22:26]), atom[20]) for atom in self.atoms[pocket_2]))
                intersection= residues_1 & residues_2
                union= residues_1 | residues_2
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
        result=""
        for bin_site in range(len(self.sorted_atoms)):
            ind_result= f"Predicted ligand-binding site number {bin_site}\n"
            ind_result+= "".join(self.sorted_atoms[bin_site])
            with open (f"Ligand_binding_site_{self.id}_{bin_site+1}.txt", "w") as f:
                f.write(ind_result)
            result+=ind_result+"\n"
        with open (f"Ligand_binding_site_{self.id}.txt", "w") as f:
            f.write(result)
            
    def join_binding_sites(self):
        self.detect_overlaps()
        self.join_overlaps()
        self.joined_data()
        sorted_scores = self.sort_sites()
        self.print_results()
        
        return sorted_scores