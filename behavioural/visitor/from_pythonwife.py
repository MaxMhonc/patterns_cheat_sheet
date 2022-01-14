# https://pythonwife.com/visitor-design-pattern-with-python/

from abc import abstractmethod


class Item():
    """Visitable class"""

    @abstractmethod
    def accept(self, visitor):
        pass


class Shirt(Item):
    def __init__(self, price, size):
        self.price = price
        self.size = size

    def get_price(self):
        return self.price

    def get_size(self):
        return self.size

    def accept(self, visitor):
        return visitor.visit(self)


class Book(Item):
    def __init__(self, cost, genre):
        self.price = cost
        self.genre = genre

    def get_price(self):
        return self.price

    def get_genre(self):
        return self.genre

    def accept(self, visitor):
        return visitor.visit(self)


class Visitor():
    """Abstract Vistor Class"""

    @abstractmethod
    def visit(self, item):
        pass


class CartVisitor(Visitor):
    def visit(self, item):
        if isinstance(item, Book):
            cost = item.get_price()
            print("Book Genre: {}, cost = ${}".format(item.get_genre(), cost))
            return cost
        elif isinstance(item, Shirt):
            cost = item.get_price()
            print("Shirt, size{} cost = ${}".format(item.get_size(), cost))
            return cost


def calculate_price(items):
    visitor = CartVisitor()
    sum = 0
    for item in items:
        sum = sum + item.accept(visitor)

    return sum


if __name__ == '__main__':
    items = [
        Shirt(10, "XL"),
        Shirt(15, "XXL"),
        Book(20, "Fiction"),
        Book(100, "Self Help"),
    ]

    total = calculate_price(items)
    print("Total Cost = ${}".format(total))
