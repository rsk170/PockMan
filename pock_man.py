#!/usr/bin/env python3
"""
pock_man.py – command‑line entry point for PockMan
=================================================

When launched with **no** command‑line arguments the script switches to an
interactive wizard that keeps asking for sensible values.  When arguments
are supplied, it defers to argparse exactly as before.
"""

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
from pockman.visualization import Visualizer

GRID_MIN, GRID_MAX   = 0.5, 3.0   # Å
BORDER_MIN, BORDER_MAX = 2.0, 10.0  # Å


def _explain_grid_bounds() -> str:
    return (
        f"Grid spacing should be between {GRID_MIN} Å and {GRID_MAX} Å.\n"
        "  • <0.5 Å  → huge memory & runtime increase for marginal accuracy.\n"
        "  • >3 Å    → too coarse: cavities merge or disappear"
    )


def _explain_border_bounds() -> str:
    return (
        f"Border should be between {BORDER_MIN} Å and {BORDER_MAX} Å.\n"
        "  • <2 Å  → pockets at the surface may be truncated.\n"
        "  • >10 Å → adds empty space; grid grows needlessly"
    )

def ask_interactively() -> tuple[str, float, float, bool]:
    """Prompt the user until all parameters are valid, then return them."""
    # PDB path or ID
    while True:
        pdb_input = input(
            "Enter the path to the input PDB file (or a 4‑character PDB ID): "
        ).strip()
        if not pdb_input:
            print("  ✘ Please type a path or a PDB ID.\n")
            continue
        if (len(pdb_input) == 4 and pdb_input.isalnum()) or os.path.exists(pdb_input):
            break
        print("  ✘ File not found and value is not a valid 4‑letter ID. Try again.\n")

     # Grid size
    while True:
        gs = input(f"Enter grid size in Å (default 1.0, allowed {GRID_MIN}-{GRID_MAX}): ").strip()
        if not gs:
            grid_size = 1.0
        else:
            try:
                grid_size = float(gs)
            except ValueError:
                print("  ✘ Please enter a number.\n")
                continue
        if GRID_MIN <= grid_size <= GRID_MAX:
            break
        print(f"  ✘ {grid_size} Å is outside the accepted range.\n{_explain_grid_bounds()}\n")

    # Border size
    while True:
        bs = input(f"Enter border size in Å (default 5.0, allowed {BORDER_MIN}-{BORDER_MAX}): ").strip()
        if not bs:
            border = 5.0
        else:
            try:
                border = float(bs)
            except ValueError:
                print("  ✘ Please enter a number.\n")
                continue
        if BORDER_MIN <= border <= BORDER_MAX:
            break
        print(f"  ✘ {border} Å is outside the accepted range.\n{_explain_border_bounds()}\n")

    # Diagonal search
    while True:
        diag = input("Include diagonal pocket detection? (yes/no): ").strip().lower()
        if diag in {"", "no", "n"}:
            include_diagonals = False
            break
        if diag in {"yes", "y"}:
            include_diagonals = True
            break
        print("  ✘ Please answer yes or no.\n")

    return pdb_input, grid_size, border, include_diagonals

def main() -> None:
    if len(sys.argv) == 1:
        pdb_input, grid_size, border, include_diagonals = ask_interactively()

    else:
        parser = argparse.ArgumentParser(
            description=(
                "Identify putative ligand‑binding pockets in a protein "
                "and write visualisation scripts."
            )
        )
        parser.add_argument(
            "pdb_input",
            help="Path to a local PDB file or a valid 4‑character PDB ID",
        )
        parser.add_argument(
            "--grid_size",
            type=float,
            default=1.0,
            help="Voxel resolution in Å (default 1.0)",
        )
        parser.add_argument(
            "--border",
            type=float,
            default=5.0,
            help="Padding around the protein in Å (default 5.0)",
        )
        parser.add_argument(
            "--diagonals",
            action="store_true",
            help="Include diagonal pocket detection",
        )
        args = parser.parse_args()
        pdb_input = args.pdb_input
        grid_size = args.grid_size
        border = args.border
        include_diagonals = args.diagonals

    if os.path.exists(pdb_input):
        cleaned_filepath = os.path.join(
            os.path.dirname(pdb_input),
            os.path.splitext(os.path.basename(pdb_input))[0] + "_clean.pdb",
        )
        print(f"Cleaning local PDB file: {pdb_input}")
        pdb_file = PDBHandler.clean_pdb(pdb_input, cleaned_filepath)
        if pdb_file is None:
            sys.exit("Failed to clean PDB file. Exiting.")
    else:
        print(f"Local file not found. Assuming '{pdb_input}' is a PDB ID and attempting to download...")
        pdb_file = PDBHandler.download_pdb(pdb_input)
        if pdb_file is None:
            sys.exit("Failed to obtain PDB file. Exiting.")

    pdb_id = os.path.splitext(os.path.basename(pdb_file))[0]

    protein   = ProteinStructure(pdb_id, pdb_file)

    grid      = ProteinGrid(protein, grid_size=grid_size, border=border)
    grid.print_grid_shapes()

    projector = ProteinProjector(protein, grid)
    projector.project_atoms()

    detector  = PSPDetector(grid)
    detector.search(diagonals=include_diagonals)

    cluster   = PocketCluster(grid, protein)
    cluster.detect_pockets(diagonals=include_diagonals, cutoff=4)
    sorted_pockets = cluster.get_sorted_pockets()

    finder = NearbyAtomsFinder(protein, grid)
    finder.find_nearby_atoms(
        sorted_pockets, threshold=4.0, file_tag=pdb_id, include_het=False
    )

    Visualizer.save_chimera(sorted_pockets, grid, pdb_id)
    Visualizer.save_pymol(sorted_pockets, grid, pdb_id)

    Quote("pockman/quotes/quotes.json").get_quote()

if __name__ == "__main__":
    main()
