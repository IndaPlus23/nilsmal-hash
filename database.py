import cmd
import pickle
import os

SAVE_PATH = "./persistant_save.pickle"

class CLI(cmd.Cmd):
    prompt = '>> '
    intro = 'Welcome to my database. Type "help" for available commands.'

    def __init__(self, database=None, completekey='tab', stdin=None, stdout=None):
        super().__init__(completekey=completekey, stdin=stdin, stdout=stdout)
        if os.path.exists(SAVE_PATH):
            print("Loading database")
            with open(SAVE_PATH, 'rb') as file:
                database = pickle.load(file)
        else:
            if not database: 
                print("Creating new database")
                database = Database()

        self.database = database


    def update_pickle(self, database):
        with open(SAVE_PATH, 'wb') as file:
            pickle.dump(database, file)

    def do_add(self, line):
        """
        Add a key value to the database.
        Use syntax: add <key> <value> 
        """
        values = line.split(" ")
        if len(values) > 2: 
            print("Please only pass two values to the add method!")
            pass

        self.database.add(values[0], values[1])
        self.update_pickle(self.database)

    def do_delete(self, line):
        """
        Delete one element from the database
        Use syntax: delete <key>
        """
        if len(line.split(" ")) > 1:
            print("Please only pass one key to the delete method!")
            pass
        self.database.delete(line)
        self.update_pickle(self.database)


    def do_show(self, line):
        """
        Display the entire database
        """

        values = self.database.get_all()
        print("----- DATABASE -----")
        for e in values:
            print(str(e[0]) + " --> " + str(e[1]))
        print("--------------------")

    def do_get(self, line):
        """
        Get one element from database based on key.
        Use synax: get <key>
        """
        if len(line.split(" ")) > 1:
            print("Please only pass one key to the get method!")
            pass

        print(self.database.get(line))


    def do_clear(self, line):
        """
        Simple command to clear the screen
        """
        os.system('cls')

    def do_ping(self, line):
        """
        Play ping pong with my database! Very useful method!
        """
        print("pong!", line)

    def do_exit(self, line):
        """
        Exit the CLI.
        """
        return True

    def do_quit(self, line):
        """
        Exit the CLI. But with quit instead of exit! Wooooow
        """
        return True

class Database(object):
    def __init__(self, length=4):
        self.array = [None] * length
    
    def hash(self, key):
        hash_value = 0
        for char in key:
            hash_value = (hash_value * 31 + ord(char)) % len(self.array)
        return hash_value
        
    def add(self, key, value):
        index = self.hash(key)
        if self.array[index] is not None:
            for kvp in self.array[index]:
                if kvp[0] == key:
                    kvp[1] = value
                    print("Updating key: ", kvp[0])
                    break
            else:
                print(f"Adding value {key} --> {value}")
                self.array[index].append([key, value])
        else:
            print(f"Adding value {key} --> {value}")
            self.array[index] = []
            self.array[index].append([key, value])
    
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

if __name__ == "__main__":

    CLI().cmdloop()
