import os

class Loader:
    def __init__(self, filename):
        self.filename = filename

    def fileexists(self):
        if os.path.isfile(self.filename):
            return True
        else:
            return False

    def load(self):
        data = list()
        try:
            with open(self.filename) as f:
                data = f.read()
        except IOError as e:
            print("Unable to load file")
        return data