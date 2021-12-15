# https://titanwolf.org/Network/Articles/Article?AID=439e5138-64ee-4bd5-9de7-e879de1233ff

class lazy(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        val = self.func(instance)
        setattr(instance, self.func.__name__, val)
        return val


class Circle(object):

    def __init__(self, radius):
        self.radius = radius

    @lazy
    def area(self):
        print('evalute')
        return 3.14 * self.radius ** 2


c = Circle(4)
print(c.radius)
print(c.area)
print(c.area)
print(c.area)
