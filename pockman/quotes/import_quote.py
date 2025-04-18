import random
import json

class Quote:
    """
    Class to obtain a random quote at the end of each run of the program.
    """
    def __init__(self, quote_file):
        """
        Initialize the Quote.

        Args:
            quote_file: file where the quotes are stored
        """
        with open (quote_file) as f:
            self.quotes= json.load(f)
    
    def get_quote(self):
        """
        Obtain a random quote from the list of quotes
        """
        r_quote = random.choice(self.quotes)
        print(f'💬 "{r_quote["text"]}"\n  — {r_quote["author"]}')