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
from pockman.join_binding_sites import PocketJoin
from pockman.visualization import Visualizer

GRID_MIN, GRID_MAX   = 0.5, 3.0   # Å
BORDER_MIN, BORDER_MAX = 2.0, 10.0  # Å
DISTANCE_MIN, DISTANCE_MAX = 3, 8
CUTOFF_MIN, CUTOFF_MAX_DIAGONAL, CUTOFF_MAX_NON_DIAGONAL = 1, 12, 6

def _print_range_error(value, minimum, maximum, unit: str = ""):
    """
    Print a consistent “✘ … is outside the allowed range” message,
    followed by an optional explanation block.
    """
    unit_str = unit or ""
    print(f"\033[91m✘  {value}{unit_str} is outside the allowed range [{minimum}{unit_str}–{maximum}{unit_str}].\033[0m")
    print()


def ask_interactively() -> tuple[str, float, float, bool, float, float]:
    """Prompt the user until all parameters are valid, then return them."""
    # PDB path or ID
    while True:
        pdb_input = input(
            "➤ Enter the path to the input PDB file (or a 4‑character PDB ID): "
        ).strip()
        if not pdb_input:
            print("  ✘ Please type a path or a PDB ID.\n")
            continue
        if (len(pdb_input) == 4 and pdb_input.isalnum()) or os.path.exists(pdb_input):
            break
        print("  ✘ File not found and value is not a valid 4‑letter ID. Try again.\n")

     # Grid size
    while True:
        gs = input(f"➤ Enter grid size in Å (default 1.0, allowed {GRID_MIN} - {GRID_MAX}): ").strip()
        if not gs:
            grid_size = 1.0
        else:
            try:
                grid_size = float(gs)
            except ValueError:
                print("\033[91m  ✘ Please enter a number.\n\033[0m")
                continue
        if GRID_MIN <= grid_size <= GRID_MAX:
            break
        _print_range_error(grid_size, GRID_MIN, GRID_MAX, " Å")
        if grid_size < GRID_MIN:
            print(f"\033[93m ⚠️  The grid size must be at least {GRID_MIN} Å.\033[0m")
        if grid_size > GRID_MAX:
            print(f"\033[93m ⚠️  The grid size score must be at most {GRID_MAX} Å.\033[0m")



    # Border size
    while True:
        bs = input(f"➤ Enter border size in Å (default 5.0, allowed {BORDER_MIN}-{BORDER_MAX}): ").strip()
        if not bs:
            border = 5.0
        else:
            try:
                border = float(bs)
            except ValueError:
                print("\033[91m  ✘ Please enter a number.\n\033[0m")
                continue
        if BORDER_MIN <= border <= BORDER_MAX:
            break
        _print_range_error(border, BORDER_MIN, BORDER_MAX, " Å")
        if border < BORDER_MIN:
            print(f"\033[93m  ⚠️  The border size must be at least {BORDER_MIN} Å.\033[0m")
        if border > BORDER_MAX:
            print(f"\033[93m ⚠️  The border size score must be at most {BORDER_MAX} Å.\033[0m")

    # Planar diagonal search
    while True:
        diag = input("➤ Include planar diagonal PSP detection? (yes/no): ").strip().lower()
        if diag in {"", "no", "n"}:
            include_diagonals = False
            break
        if diag in {"yes", "y"}:
            include_diagonals = True
            break
        print("\033[91m  ✘ Please answer yes or no.\n\033[0m")

    # Voxel score cut-off
    while True:
        if include_diagonals:
            max_cutoff = CUTOFF_MAX_DIAGONAL
        else:
            max_cutoff = CUTOFF_MAX_NON_DIAGONAL
        vcf = input(f"➤ Enter the cut-off score desired to select voxels for the pocket clustering (default 4, allowed {CUTOFF_MIN}-{max_cutoff}): ").strip()
        if not vcf:
            cut_off = 4.0
            break
        else:
            try:
                cut_off = float(vcf)
            except ValueError:
                print("\033[91m  ✘ Please enter a number.\n\033[0m")
                continue
        if CUTOFF_MIN <= cut_off <= max_cutoff:
            break
        _print_range_error(cut_off, CUTOFF_MIN, max_cutoff)
        if cut_off < CUTOFF_MIN:
            print(f"\033[93m  ⚠️  The cut-off score must be at least {CUTOFF_MIN}.\033[0m")
        if cut_off > max_cutoff:
            print(f"\033[93m ⚠️  The cut-off score must be at most {max_cutoff}.\033[0m")

    # Distance threshold
    while True:
        dt = input(f"➤ Enter the distance threshold to determine closeness between voxel and atoms (default 4, allowed {DISTANCE_MIN}-{DISTANCE_MAX}): ").strip()
        if not dt:
            d_threshold = 4.0
            break
        else:
            try:
                d_threshold = float(dt)
            except ValueError:
                print("\033[91m  ✘ Please enter a number.\n\033[0m")
                continue
        if DISTANCE_MIN <= d_threshold <= DISTANCE_MAX:
            break
        _print_range_error(d_threshold, DISTANCE_MIN, DISTANCE_MAX)
        if d_threshold < DISTANCE_MIN:
            print(f"\033[93m  ⚠️  The distance score must be at least {DISTANCE_MIN}.\033[0m\n")
        if d_threshold > DISTANCE_MAX:
            print(f"\033[93m  ⚠️  The distance score must be at most {DISTANCE_MAX}.\033[0m\n")

    return pdb_input, grid_size, border, include_diagonals, cut_off, d_threshold

def main() -> None:
    print("╔════════════════════════════════╗")
    print("║    🔍  Welcome to PockMan      ║")
    print("╚════════════════════════════════╝")
    print("")
    print("— — — — —  INPUT PHASE — — — — — ")

    if len(sys.argv) == 1:
        pdb_input, grid_size, border, include_diagonals, cut_off, d_threshold = ask_interactively()

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
        parser.add_argument(
            "--voxel_score_cut_off",
            type=float,
            default=4.0,
            help="Cut-off used to determine which voxels to use to determine possible pockets, based on the voxel's score after PSP detection (default 4.0)",
        )
        parser.add_argument(
            "--distance_threshold",
            type=float,
            default=4.0,
            help="Maximum distance accepted between voxel and atom to assume that the atom is part of the predicted ligand binding site (default 4.0)",
        )
        args = parser.parse_args()
        pdb_input = args.pdb_input
        grid_size = args.grid_size
        border = args.border
        include_diagonals = args.diagonals
        cut_off = args.voxel_score_cut_off
        d_threshold = args.distance_threshold

    print("")
    print("— — — — —  PDB FETCH PHASE — — — — —")
    if os.path.exists(pdb_input):
        cleaned_filepath = os.path.join(
            os.path.dirname(pdb_input),
            os.path.splitext(os.path.basename(pdb_input))[0] + "_clean.pdb",
        )
        print(f"🧹Cleaning local PDB file: {pdb_input}")
        pdb_file = PDBHandler.clean_pdb(pdb_input, cleaned_filepath)
        if pdb_file is None:
            sys.exit("Failed to clean PDB file. Exiting.")
    else:
        print(f"📥 Assuming '{pdb_input}' is a PDB ID and attempting to download...")
        pdb_file = PDBHandler.download_pdb(pdb_input)
        if pdb_file is None:
            sys.exit("❌ Failed to obtain PDB file. Exiting.")

    pdb_id = os.path.splitext(os.path.basename(pdb_file))[0]

    protein   = ProteinStructure(pdb_id, pdb_file)

    grid      = ProteinGrid(protein, grid_size=grid_size, border=border)
    grid.print_grid_shapes()

    projector = ProteinProjector(protein, grid)
    projector.project_atoms()

    detector  = PSPDetector(grid)
    detector.search(diagonals=include_diagonals)

    cluster   = PocketCluster(grid, protein)
    cluster.detect_pockets(diagonals=include_diagonals, cutoff=cut_off)
    sorted_pockets, sorted_scores, original_scores = cluster.get_sorted_pockets()

    finder = NearbyAtomsFinder(protein, grid)
    nearby_atoms= finder.find_nearby_atoms(
        sorted_pockets, threshold=d_threshold, file_tag=pdb_id
    )

    joined_pockets = PocketJoin(pdb_id, nearby_atoms, original_scores)
    sorted_scores=joined_pockets.join_binding_sites()

    visualize=Visualizer(pdb_id, sorted_scores)
    visualize.save_chimera()
    visualize.save_pymol()

    Quote("pockman/quotes/quotes.json").get_quote()

if __name__ == "__main__":
    main()
