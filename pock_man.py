#!/usr/bin/env python3
import argparse
import os
import sys
from grid import ProteinGrid
from pocket_detector import PocketDetector

from pdb_handler import PDBHandler

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
        pdb_input = downloaded_path
    else:
        pdb_input = pdb_input

    # Initialize and project the protein grid
    protein_grid = ProteinGrid(pdb_input, grid_size=grid_size, border=border)
    print("Protein grid shape:", protein_grid.get_grid_shape())

    # Perform pocket detection
    pocket_detector = PocketDetector(protein_grid, include_diagonals=include_diagonals)
    pocket_detector.detect_pockets()
    pocket_detector.save_pockets_to_pdb()

    # Find nearby residues
    residues = pocket_detector.find_nearby_residues()
    if residues:
        print(f"Found {len(residues)} residues near binding pockets.")
    else:
        print("No binding site residues detected.")

    # Save binding site residues to a text file
    pocket_detector.save_binding_sites(residues)

if __name__ == "__main__":
    main()
