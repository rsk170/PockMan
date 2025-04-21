import os
import glob

class Visualizer:

    def __init__(self, prot_id, scores):
        self.id=prot_id
        self.scores=scores
        
    def normalize_scores(self):
        """
        Normalize the sorted_scores to be between 0 and 1, making them suitable for coloring in Chimera.
        """
        if max(self.scores) == min(self.scores):
            return [0.5 for score in self.scores]
        return [(score - min(self.scores))/( max(self.scores)- min(self.scores)) for score in self.scores]
    
    @staticmethod
    def set_color(norm_scores):
        """
        Setting the color of the pocket depending on its normalized score
        """
        r = norm_scores
        g = 0
        b = 1 - norm_scores
        return f"{r:.2f} {g:.2f} {b:.2f}"

    def save_chimera(self):
        """
        Generate a command script for visualizing pockets.
        """
        output_dir = "results"
        os.makedirs(output_dir, exist_ok=True)
        
        norm_scores = self.normalize_scores()
        
        all_pocket_vis=f"open {self.id}.pdb\nsurface\n\n"
        for pocket in range(len(norm_scores)): 
            file = f"Ligand_binding_site_{self.id}_{pocket+1}.txt"
            with open(glob.glob(file)[0]) as f:
                pocket_content = f.readlines()[1:]
            residues=set(((int(atom[22:26]), atom[20]) for atom in pocket_content))
            
            pocket_color=self.set_color(norm_scores[pocket])
            label = f"pocket_{pocket+1}"
            ind_pocket_vis=(f"colordef {label} {pocket_color}\n")
            for atom in residues:
                ind_pocket_vis+=f"color {label} :{atom[0]}.{atom[1]}\n"
            ind_pocket_vis+="\n"
            
            cmd_file = os.path.join(output_dir, f"{self.id}_{pocket+1}_chimera.cmd")
            with open(cmd_file, "w") as f:
                f.write(f"open {self.id}.pdb\n")
                f.write("surface\n\n")
                f.write(ind_pocket_vis)
            print(f"\033[96m📄 Chimera commandscript for pocket {pocket+1} saved to: {cmd_file}\033[0m")
            all_pocket_vis+=ind_pocket_vis
            
        cmd_file = os.path.join(output_dir, f"{self.id}_chimera.cmd")

        with open(cmd_file, 'w') as f:
            f.write(all_pocket_vis)
        print(f"\033[96m📄 Chimera command script saved to: {cmd_file}\033[0m")

    @staticmethod
    def save_pymol(pockets, grid, output_prefix):
        """
        Generate a PyMOL script that visualizes the pocket centers and predicted atoms.

        Parameters
        ----------
        pockets : list of voxel index lists
            Each pocket is a list of (i, j, k) grid indices.
        grid : ProteinGrid
            Grid object with spacing and origin.
        output_prefix : str
            Prefix for output files.
        """
        output_dir = "results"
        os.makedirs(output_dir, exist_ok=True)

        script_path = os.path.join(output_dir, f"{output_prefix}_pymol.pml")

        with open(script_path, 'w') as f:
            f.write("bg_color white\n")
            f.write(f"load Ligand_binding_sites2_{output_prefix}.txt\n")
            f.write("hide everything\n")
            f.write("show spheres\n")
            f.write("set sphere_scale, 0.3\n")
            f.write("color red\n")
            f.write("zoom\n")

            for i, pocket in enumerate(pockets, 1):
                x, y, z = Visualizer.compute_center(pocket, grid)
                f.write(f"pseudoatom pocket_center_{i}, pos=[{x:.2f}, {y:.2f}, {z:.2f}]\n")
                f.write(f"color orange, pocket_center_{i}\n")
                f.write(f"set sphere_scale, 0.5, pocket_center_{i}\n")
                f.write(f"label pocket_center_{i}, \"Pocket {i}\"\n")

        print(f"\033[94m🧬 PyMOL visualization script saved to: {script_path}\033[0m")