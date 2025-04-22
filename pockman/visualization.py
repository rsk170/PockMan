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
    def set_color_chimera(norm_scores):
        """
        Setting the color of the pocket depending on its normalized score
        """
        r = norm_scores
        g = 0
        b = 1 - norm_scores
        return f"{r:.2f} {g:.2f} {b:.2f}"
    
    @staticmethod
    def set_color_pymol(norm_scores):
        """
        Setting the color of the pocket depending on its normalized score
        """
        r = norm_scores
        g = 0
        b = 1 - norm_scores
        return f"{r:.2f}, {g:.2f}, {b:.2f}"

    def save_chimera(self):
        """
        Generate a command script for visualizing pockets.
        """
        output_dir = os.path.join("results", self.id, "chimera")
        os.makedirs(output_dir, exist_ok=True)

        norm_scores = self.normalize_scores()

        all_pocket_vis=f"open ../../../pdb_files/{self.id}.pdb\nsurface\n\n"

        for pocket in range(len(norm_scores)):
            binding_sites_dir = os.path.join("results", self.id, "binding_sites")
            pattern = os.path.join(binding_sites_dir, f"Ligand_binding_site_{self.id}_{pocket+1}.txt")
            files_found = glob.glob(pattern)
            if files_found:
                with open(files_found[0]) as f:
                    pocket_content = f.readlines()[1:]
            else:
                print(f"File not found: {pattern}")
                continue
            residues=set(((atom[22:26].strip(), atom[20]) for atom in pocket_content))

            pocket_color=self.set_color_chimera(norm_scores[pocket])
            label = f"pocket_{pocket+1}"
            ind_pocket_vis=(f"colordef {label} {pocket_color}\n")
            for atom in residues:
                ind_pocket_vis+=f"color {label} :{atom[0]}.{atom[1]}\n"
            ind_pocket_vis+="\n"

            cmd_file = os.path.join(output_dir, f"{self.id}_{pocket+1}_chimera.cmd")
            with open(cmd_file, "w") as f:
                f.write(f"open ../../../pdb_files/{self.id}.pdb\n")
                f.write("surface\n\n")
                f.write(ind_pocket_vis)
            all_pocket_vis+=ind_pocket_vis

        print(f"\033[96m📂 Chimera command scripts for  individual pockets saved to: {output_dir}/\033[0m")
        cmd_file = os.path.join(output_dir, f"{self.id}_chimera.cmd")

        with open(cmd_file, 'w') as f:
            f.write(all_pocket_vis)
        print(f"\033[96m📄 Chimera combined command script saved to: {cmd_file}\033[0m")

    def save_pymol(self):
        """
        Generate a PyMOL script for visualizing pockets.
        Creates one script per pocket + a combined one.
        """
        output_dir = os.path.join("results", self.id, "pymol")
        os.makedirs(output_dir, exist_ok=True)

        norm_scores = self.normalize_scores()

        all_pocket_vis = f"load ../../../pdb_files/{self.id}.pdb\nhide everything\nshow surface\ncolor grey80\nbg_color black\n\n"

        for pocket in range(len(norm_scores)):
            binding_sites_dir = os.path.join("results", self.id, "binding_sites")
            pattern = os.path.join(binding_sites_dir, f"Ligand_binding_site_{self.id}_{pocket+1}.txt")
            files_found = glob.glob(pattern)
            if files_found:
                with open(files_found[0]) as f:
                    pocket_content = f.readlines()[1:]
            else:
                print(f"File not found: {pattern}")
                continue
            residues = set(((atom[22:26].strip(), atom[20]) for atom in pocket_content))
            pocket_color = self.set_color_pymol(norm_scores[pocket])  # "r g b"
            label = f"pocket_{pocket+1}"
            color_name = f"{label}_color"

            selectors = []
            for resnum, chain in residues:
                selectors.append(f"(resi {resnum} and chain {chain})")
            selection_str = " or ".join(selectors)

            # Per-pocket script content
            ind_pocket_vis = f"load ../../pdb_files/{self.id}.pdb\nhide everything\nshow surface\ncolor grey80\nbg_color black\n"
            ind_pocket_vis += f"# {label} — score {norm_scores[pocket]:.2f}\n"
            ind_pocket_vis += f"set_color {color_name}, [{pocket_color}]\n"
            ind_pocket_vis += f"select {label}, {selection_str}\n"
            ind_pocket_vis += f"show surface, {label}\n"
            ind_pocket_vis += f"set transparency, 0.0, {label}\n"
            ind_pocket_vis += f"color {color_name}, {label}\n\n"

            # Save per-pocket script
            cmd_file = os.path.join(output_dir, f"{self.id}_{pocket+1}_pymol.pml")
            with open(cmd_file, "w") as f:
                f.write(ind_pocket_vis)

            # Add to combined script
            all_pocket_vis += f"# {label}\n"
            all_pocket_vis += f"set_color {color_name}, [{pocket_color}]\n"
            all_pocket_vis += f"select {label}, {selection_str}\n"
            all_pocket_vis += f"show surface, {label}\n"
            all_pocket_vis += f"set transparency, 0.0, {label}\n"
            all_pocket_vis += f"color {color_name}, {label}\n\n"

        print(f"\033[95m📂 PyMOL command scripts for individual pockets saved to: {output_dir}/\033[0m")
        # Save combined script
        cmd_file = os.path.join(output_dir, f"{self.id}_pymol.pml")
        with open(cmd_file, "w") as f:
            f.write(all_pocket_vis)
        print(f"\033[95m📄 PyMOL combined script saved to: {cmd_file}\033[0m")

