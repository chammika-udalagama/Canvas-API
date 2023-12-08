class CComm:
    def __init__(self, parent_name, verbosity=True) -> None:
        self.parent_name = parent_name
        self.verbosity = verbosity

    def print(self, msg):
        msg = f'{self.parent_name}: {msg}'
        print(msg)
