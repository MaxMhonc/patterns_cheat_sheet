# https://stackabuse.com/the-bridge-design-pattern-in-python/
# Passenger & Cargo Carriers

class Carrier:
    def carry_military(self, items):
        pass

    def carry_commercial(self, items):
        pass


class Cargo(Carrier):
    def carry_military(self, items):
        print("The plane carries ", items, " military cargo goods")

    def carry_commercial(self, items):
        print("The plane carries ", items, " commercial cargo goods")


class Passenger(Carrier):
    def carry_military(self, passengers):
        print("The plane carries ", passengers, " military passengers")

    def carry_commercial(self, passengers):
        print("The plane carries ", passengers, " commercial passengers")


# Military & Commercial Planes
class Plane:
    def __init__(self, Carrier):
        self.carrier = Carrier

    def display_description(self):
        pass

    def add_objects(self):
        pass


class Commercial(Plane):
    def __init__(self, Carrier, objects):
        super().__init__(Carrier)
        self.objects = objects

    def display_description(self):
        self.carrier.carry_commercial(self.objects)

    def add_objects(self, new_objects):
        self.objects += new_objects


class Military(Plane):
    def __init__(self, Carrier, objects):
        super().__init__(Carrier)
        self.objects = objects

    def display_description(self):
        self.carrier.carry_military(self.objects)

    def add_objects(self, new_objects):
        self.objects += new_objects


if __name__ == '__main__':
    cargo = Cargo()
    passenger = Passenger()

    # Bridging Military and Cargo classes
    military1 = Military(cargo, 100)
    military1.display_description()
    military1.add_objects(25)
    military1.display_description()

    # Bridging Military and Passenger classes
    military2 = Military(passenger, 250)
    military2.display_description()
    military2.add_objects(10)
    military2.display_description()

    # Bridging Commercial and Passenger
    commercial1 = Commercial(passenger, 400)
    commercial1.display_description()
    commercial1.add_objects(50)
    commercial1.display_description()

    # Bridging Commercial and Cargo
    commercial2 = Commercial(cargo, 150)
    commercial2.display_description()
    commercial2.add_objects(15)
    commercial2.display_description()
