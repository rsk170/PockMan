from Bio import PDB

class ProteinStructure:
    """
    Class to handle the loading and representation of a protein structure from a PDB file.
    """
    def __init__(self, pdb_id: str, pdb_file: str):
        """
        Initialize the ProteinStructure.

        Args:
            pdb_id (str): Identifier for the protein.
            pdb_file (str): Path to the PDB file.
        """
        self.pdb_id = pdb_id
        parser = PDB.PDBParser(QUIET=True)
        self.structure = parser.get_structure(pdb_id, pdb_file)

    def get_atoms(self):
        """
        Return all atoms in the protein structure.

        Returns:
            Iterator of atom objects.
        """
        return self.structure.get_atoms()
