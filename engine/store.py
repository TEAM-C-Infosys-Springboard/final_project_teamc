# Import PersistenceManager to handle saving/loading data from disk
from engine.persistence import PersistenceManager



class PyKVStore:
    # Constructor: runs when store object is created
    def __init__(self):
        # Create persistence manager instance
        self.persistence = PersistenceManager()

        # Load existing data from file into memory
        self.data = self.persistence.load()

    # Store or update a key-value pair
    def put(self, key: str, value: str):
        self.data[key] = value             # Add/update value in memory
        self.persistence.save(self.data)   # Save updated data to disk
        return True

    # Retrieve value using key
    def get(self, key: str):
        # Return value if key exists, otherwise return None
        return self.data.get(key, None)

    # Delete a key-value pair
    def delete(self, key: str):
        # Check if key exists
        if key in self.data:
            del self.data[key]    # Remove key from memory
            self.persistence.save(self.data)   # Save updated data
            return True
        return False      # Return False if key not found


    # Return all stored key-value pairs
    def get_all(self):
        return self.data

    # Clear entire store
    def clear(self):
        self.data = {}            # Remove all data from memory
        self.persistence.save(self.data)  # Save empty store to disk
        return True
