# Import json module to read/write data in JSON format
import json

# Import os module to handle file paths and directories
import os


class PersistenceManager:
    """
    PersistenceManager handles saving and loading key-value data
    to and from disk using a JSON file.
 
    This ensures that in-memory data is persisted across
    application restarts and enables crash-safe recovery.
    """

    # Constructor method runs when object is created
    def __init__(self, file_path="data/store.json"):

        # Path where data will be stored
        self.file_path = file_path

        # Create data folder if it doesn't exist
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    # Method to save dictionary data into file
    def save(self, data: dict):
        """Save key-value data to file"""

        # Open file in write mode
        with open(self.file_path, "w") as file:
            # Convert dictionary to JSON and write to file
            json.dump(data, file)

    # Method to load data from file
    def load(self):
        """Load key-value data from file"""

        # If file does not exist, return empty dictionary
        if not os.path.exists(self.file_path):
            return {}

        # Open file in read mode
        with open(self.file_path, "r") as file:
            # Read JSON data and convert it back to dictionary
            return json.load(file)
