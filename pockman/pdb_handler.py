import os
import re
import requests

class PDBHandler:
    @staticmethod
    def is_valid_pdb_id(pdb_id):
        """Check if the given PDB ID is valid (four alphanumeric characters, first is a digit)."""
        return bool(re.fullmatch(r'^[1-9][A-Za-z0-9]{3}$', pdb_id))

    @staticmethod
    def clean_pdb(raw_pdb_path, cleaned_pdb_path, verbose=True):
        """
        Clean the raw PDB file by removing water molecules and non-protein atoms.
        This implementation keeps only lines starting with "ATOM".
        """
        try:
            with open(raw_pdb_path, "r") as infile, open(cleaned_pdb_path, "w") as outfile:
                for line in infile:
                    if line.startswith("ATOM"):
                        outfile.write(line)
            if verbose:
                print(f"✅ Cleaned PDB file saved to: {cleaned_pdb_path}")
            return cleaned_pdb_path
        except Exception as e:
            if verbose:
                print(f"❌ Error cleaning PDB file: {e}")
            return None

    @classmethod
    def download_pdb(cls, pdb_id, save_dir="pdb_files", overwrite=False, verbose=True):
        """
        Download and clean a PDB file:
          - Validates the pdb_id.
          - Downloads the raw PDB file from RCSB.
          - Cleans the file (removes water and non-protein atoms).
          - Saves and returns the path to the cleaned PDB file.
        """
        if not cls.is_valid_pdb_id(pdb_id):
            print(f"❌ Invalid PDB ID: {pdb_id}.")
            return None

        os.makedirs(save_dir, exist_ok=True)
        pdb_filepath = os.path.join(save_dir, f"{pdb_id}.pdb")

        if os.path.exists(pdb_filepath) and not overwrite:
            if verbose:
                print(f"🗄  PDB file already exists: {pdb_filepath}")
            return pdb_filepath

        # Download the PDB file
        url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching PDB {pdb_id}: {e}")
            return None

        # Save the raw PDB file
        raw_pdb_path = os.path.join(save_dir, f"{pdb_id}_raw.pdb")
        with open(raw_pdb_path, "wb") as f:
            f.write(response.content)

        if verbose:
            print(f"\033[92m✅ Downloaded PDB {pdb_id} → {raw_pdb_path}\033[0m")

        # Clean the PDB file and save as final pdb_filepath
        print(f"🧹Cleaning local PDB file: {pdb_filepath}")
        return cls.clean_pdb(raw_pdb_path, pdb_filepath, verbose)
