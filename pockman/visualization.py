import os
import numpy as np

class Visualizer:

    @staticmethod
    def compute_center(pocket_voxels, grid):
        """Compute the geometric center of a pocket given grid voxel indices."""
        coords = []
        for gx, gy, gz in pocket_voxels:
            x = grid.x_min + gx * grid.grid_size
            y = grid.y_min + gy * grid.grid_size
            z = grid.z_min + gz * grid.grid_size
            coords.append((x, y, z))
        return np.mean(coords, axis=0)

    @staticmethod
    def save_chimera(pockets, grid, output_prefix):
        """
        Generate Chimera-compatible BILD and command script for visualizing pockets.

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

        bild_file = os.path.join(output_dir, f"{output_prefix}_chimera_spheres.bild")
        cmd_file = os.path.join(output_dir, f"{output_prefix}_chimera.cmd")

        with open(bild_file, 'w') as bf:
            bf.write(".transparency 0.0\n")  # Make spheres solid

            for i, pocket in enumerate(pockets, 1):
                center = Visualizer.compute_center(pocket, grid)
                x, y, z = center

                # Color rotation: red, orange, green
                if i % 3 == 1:
                    r, g, b = 1.0, 0.0, 0.0  # red
                elif i % 3 == 2:
                    r, g, b = 1.0, 0.65, 0.0  # orange
                else:
                    r, g, b = 0.13, 0.55, 0.13  # green

                bf.write(f".comment Pocket {i}\n")
                bf.write(f".color {r:.2f} {g:.2f} {b:.2f}\n")
                bf.write(f".sphere {x:.2f} {y:.2f} {z:.2f} 2.0\n\n")

        with open(cmd_file, 'w') as f:
            f.write("# Chimera command script for visualizing PockMan binding pockets\n")
            f.write("background solid white\n")
            f.write(f"open {os.path.basename(bild_file)}\n")
            f.write("focus\n")

        print(f"\033[92m✅ Chimera BILD file saved to: {bild_file}\033[0m")
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