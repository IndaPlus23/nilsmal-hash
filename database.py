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


        print(database)

        self.database = database

        self.do_add("test1 1")
        self.do_add("test2 2")
        self.do_add("test3 3")
        self.do_add("test4 4")

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
        with open(SAVE_PATH, 'wb') as file:
            pickle.dump(self.database, file)


    def do_show(self, line):
        """"""

        values = self.database.get_all()
        print("----- DATABASE -----")
        for e in values:
            print(str(e[0]) + " --> " + str(e[1]))
        print("--------------------")


    def do_ping(self, line):
        """Play ping pong with my database! Very useful method!"""
        print("pong!", line)

    def do_exit(self, line):
        """Exit the CLI."""
        return True

    def do_quit(self, line):
        """Exit the CLI. But with quit instead of exit! Wooooow"""
        return True

class Database(object):
    def __init__(self, length=4):
        self.array = [None] * length
    
    def hash(self, key):
        length = len(self.array)
        return hash(key) % length
        
    def add(self, key, value):
        index = self.hash(key)
        if self.array[index] is not None:
            for kvp in self.array[index]:
                if kvp[0] == key:
                    kvp[1] = value
                    print("breaking ", key, kvp[0])
                    break
            else:
                self.array[index].append([key, value])
                print("Adding1: " + str(key) + " --> " + str(value) + " to the database")

        else:
            self.array[index] = []
            self.array[index].append([key, value])
            print("Adding2: " + str(key) + " --> " + str(value) + " to the database")
    
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
        print(self.array)
        for kvp in self.array:
            if kvp:
                if len(kvp) == 1:
                    return_arr.append([kvp[0][0], kvp[0][1]])
                if len(kvp) > 1:
                    for e in kvp:
                        return_arr.append([e[0], e[1]])
            else:
                print("REST: ", kvp)
        return return_arr 

if __name__ == "__main__":


    table = Database()

    CLI().cmdloop()

    # table.add("test1", 1)
    # table.add("test2", 2)
    # table.add("test3", 3)
    # table.add("test4", 4)
    # table.add("test5", 5)
    # table.add("test6", 6)
    # table.add("test7", 7)
    # table.add("test8", "Hejsan svejsan!")
    # table.add("test9", 9)

    # print(table.get("test4"))
    # print(table.get("test1"))
    # print(table.get("test3"))
    # print(table.get("test2"))