#!/usr/bin/env python3
import argparse
import os
import sys
from pockman.protein import ProteinStructure
from pockman.protein_grid import ProteinGrid
from pockman.projector import ProteinProjector
from pockman.detector import PSPDetector, PocketCluster
from pockman.atoms_finder import NearbyAtomsFinder
from pockman.quotes.import_quote import Quote

from pockman.pdb_handler import PDBHandler
from pockman.visualization import save_chimera, save_pymol

def main():
    # If no command-line arguments are provided, ask the user interactively.
    if len(sys.argv) == 1:
        pdb_input = input("Enter the path to the input PDB file (or a PDB ID to use): ")
        grid_size_input = input("Enter grid size in Angstroms (default: 1.0): ")
        border_input = input("Enter border size in Angstroms (default: 5.0): ")
        diagonals_input = input("Would you like to include diagonal pocket detection? (yes/no): ")

        grid_size = float(grid_size_input) if grid_size_input.strip() != "" else 1.0
        border = float(border_input) if border_input.strip() != "" else 5.0
        include_diagonals = diagonals_input.lower() == "yes"
    else:
        # Use argparse if command-line arguments are provided.
        parser = argparse.ArgumentParser(
            description="Calculate grid attributes for a given PDB file and detect ligand binding sites."
        )
        parser.add_argument("pdb_input", help="Path to the input PDB file or a valid PDB ID")
        parser.add_argument("--grid_size", type=float, default=1.0, help="Resolution in Angstroms (default: 1.0)")
        parser.add_argument("--border", type=float, default=5.0, help="Extra space around the protein (default: 5.0)")
        parser.add_argument("--diagonals", action="store_true", help="Include diagonal pocket detection")
        args = parser.parse_args()
        pdb_input = args.pdb_input
        grid_size = args.grid_size
        border = args.border
        include_diagonals = args.diagonals

    if not os.path.exists(pdb_input):
        print(f"Local file not found. Assuming '{pdb_input}' is a PDB ID and attempting to download...")
        downloaded_path = PDBHandler.download_pdb(pdb_input)
        if downloaded_path is None:
            print("Failed to obtain PDB file. Exiting.")
            sys.exit(1)
        pdb_file = downloaded_path
    else:
        cleaned_filepath = os.path.join(
        os.path.dirname(pdb_input),
        os.path.splitext(os.path.basename(pdb_input))[0] + "_clean.pdb"
        )
        print(f"Cleaning local PDB file: {pdb_input}")
        pdb_file = PDBHandler.clean_pdb(pdb_input, cleaned_filepath)
        if pdb_file is None:
            print("Failed to clean PDB file. Exiting.")
            sys.exit(1)

    pdb_id = os.path.splitext(os.path.basename(pdb_file))[0]

    # Load the protein structure
    protein = ProteinStructure(pdb_id, pdb_file)

    # Initialize the grid parameters based on the provided grid size and border
    grid = ProteinGrid(protein, grid_size=grid_size, border=border)
    grid.print_grid_shapes()

    # Project protein atoms onto the grid
    projector = ProteinProjector(protein, grid)
    projector.project_atoms()

    # Perform PSP pocket detection; include diagonals if requested.
    detector = PSPDetector(grid)
    detector.search(diagonals=include_diagonals)

    # Cluster the detected pockets and compute their scores.
    cluster = PocketCluster(grid, protein)
    cluster.detect_pockets(diagonals=include_diagonals, cutoff=4)
    sorted_pockets = cluster.get_sorted_pockets()

    # Find nearby atoms (residues) around the binding pockets and save to a file.
    finder = NearbyAtomsFinder(protein, grid)
    finder.find_nearby_atoms(sorted_pockets, threshold=4.0, file_tag=pdb_id, include_het=False)

    # Print a final quote, for aesthetics, to make it more beautiful
    quoting=Quote("pockman/quotes/quotes.json")
    quoting.get_quote()

    # Save visualization scripts
    save_chimera(sorted_pockets, grid, pdb_id)
    save_pymol(sorted_pockets, grid, pdb_id)

if __name__ == "__main__":
    main()
