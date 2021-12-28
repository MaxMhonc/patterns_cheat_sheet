# https://github.com/faif/python-patterns/blob/master/patterns/structural/facade.py
# Complex computer parts
class CPU:
    """
    Simple CPU representation.
    """

    def freeze(self):
        print("Freezing processor.")

    def jump(self, position):
        print("Jumping to:", position)

    def execute(self):
        print("Executing.")


class Memory:
    """
    Simple memory representation.
    """

    def load(self, position, data):
        print(f"Loading from {position} data: '{data}'.")


class SolidStateDrive:
    """
    Simple solid state drive representation.
    """

    def read(self, lba, size):
        return f"Some data from sector {lba} with size {size}"


class ComputerFacade:
    """
    Represents a facade for various computer parts.
    """

    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.ssd = SolidStateDrive()

    def start(self):
        self.cpu.freeze()
        self.memory.load("0x00", self.ssd.read("100", "1024"))
        self.cpu.jump("0x00")
        self.cpu.execute()


def main():
    """
    >>> computer_facade = ComputerFacade()
    >>> computer_facade.start()
    Freezing processor.
    Loading from 0x00 data: 'Some data from sector 100 with size 1024'.
    Jumping to: 0x00
    Executing.
    """


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
