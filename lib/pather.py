class Pather():
    def __init__(self, name, parent="root"):
        self.name = name
        self.parent = [parent]
        self.children = []

    def __repr__(self):
        return  self.name

    