from engine.persistence import PersistenceManager



class PyKVStore:
    def __init__(self):
        self.persistence = PersistenceManager()
        self.data = self.persistence.load()

    def put(self, key: str, value: str):
        self.data[key] = value
        self.persistence.save(self.data)
        return True

    def get(self, key: str):
        return self.data.get(key, None)

    def delete(self, key: str):
        if key in self.data:
            del self.data[key]
            self.persistence.save(self.data)
            return True
        return False

    def get_all(self):
        return self.data

    def clear(self):
        self.data = {}
        self.persistence.save(self.data)
        return True
