import cmd
import pickle
import os

from database import Database

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
        Use syntax: add <key> <value1> <value2> ...
        """
        values = line.split(" ")

        self.database.add(values[0], values[1:])
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

        longest_key = 0
        for e in values:
            longest_key = max(len(str(e[0])), longest_key)

        for e in values:
            values = ""
            for value in e[1]:
                values += " | " + str(value)
            print(str(e[0]) + " ", end="")
            for e in range(longest_key - len(str(e[0]))):
                print(" ", end="")
            print(values + " |")
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

if __name__ == "__main__":

    CLI().cmdloop()
