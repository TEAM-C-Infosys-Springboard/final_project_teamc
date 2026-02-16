# Import the PyKVStore class
from store import PyKVStore

# Create an instance of the key-value store
kv = PyKVStore()

# Store a key-value pair
kv.put("name", "Divi")

# Retrieve and print the value for key "name"
print(kv.get("name"))    # Output: Divi

# Delete the key "name" from the store
kv.delete("name")

# Try retrieving the deleted key
print(kv.get("name"))      # Output: None (since key was deleted)
