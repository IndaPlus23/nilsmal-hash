class Database(object):
    def __init__(self, length=4):
        self.array = [None] * length
    
    def hash(self, key):
        hash_value = 0
        for char in key:
            hash_value = (hash_value * 31 + ord(char)) % len(self.array)
        return hash_value
        
    def add(self, key, values):
        index = self.hash(key)
        if self.array[index] is not None:
            for kvp in self.array[index]:
                if kvp[0] == key:
                    kvp[1] = values
                    print("Updating key: ", kvp[0])
                    break
            else:
                print(f"Adding value {key} --> {values}")
                self.array[index].append([key, values])
        else:
            print(f"Adding value {key} --> {values}")
            self.array[index] = []
            self.array[index].append([key, values])
    
    def delete(self, key):
        index = self.hash(key)
        if self.array[index] is not None:
            print(f"Deleting key: {key}")
            self.array[index] = []

    def get(self, key):
        index = self.hash(key)
        if self.array[index] is None:
            raise KeyError()
        else:
            for kvp in self.array[index]:
                if kvp[0] == key:
                    return kvp[1]
            raise KeyError()
    
    def get_all(self):
        return_arr = []
        for kvp in self.array:
            if kvp:
                if len(kvp) == 1:
                    return_arr.append([kvp[0][0], kvp[0][1]])
                if len(kvp) > 1:
                    for e in kvp:
                        return_arr.append([e[0], e[1]])
        return return_arr 
