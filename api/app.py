# Import fastAPI framework and HTTPException for error handling
from fastapi import FastAPI, HTTPException

# Import Custom key-value store class
from engine.store import PyKVStore

# Create FastAPI app with title shown in Swagger docs
app = FastAPI(title="PyKV - In-Memory Key Value Store")

# Create one global store instance to hold data in memory
kv_store = PyKVStore()

# Route to store a key-value pair
@app.post("/put")
def put_value(key: str, value: str):
    kv_store.put(key, value) # Save key and value
    return {"message": "Key stored successfully"}


# Route to get value using key
@app.get("/get/{key}")
def get_value(key: str):
    value = kv_store.get(key)  # Retrieve value from store

    # If key does not exist
    if value is None:
        return {"error": "Key not found"}
    
    return {"key": key, "value": value}


# Route to delete a key
@app.delete("/delete/{key}")
def delete_value(key: str):
    success = kv_store.delete(key) # Attempt deletion

    # If key was not found
    if not success:
        raise HTTPException(status_code=404, detail="Key not found")
    
    return {"message": "Key deleted successfully"}

# Route to return all stored key-value pairs
@app.get("/all")
def get_all_values():
    return kv_store.get_all()


# Route to clear entire store
@app.delete("/clear")
def clear_data():
    kv_store.clear() # Remove all data
    return {"message": "Store cleared successfully"}
