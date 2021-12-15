# https://ru.wikipedia.org/wiki/%D0%9F%D1%80%D0%BE%D1%82%D0%BE%D1%82%D0%B8%D0%BF_(%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD_%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F)
import copy


class Prototype:

    def __init__(self):
        self._objects = {}

    def register_object(self, name, obj):
        """Register an object"""
        self._objects[name] = obj

    def unregister_object(self, name):
        """Unregister an object"""
        del self._objects[name]

    def clone(self, name, **attr):
        """Clone a registered object and update inner attributes dictionary"""
        obj = copy.deepcopy(self._objects.get(name))
        obj.__dict__.update(attr)
        return obj


class A:
    def __init__(self):
        self.x = 3
        self.y = 8
        self.z = 15
        self.garbage = [38, 11, 19]

    def __str__(self):
        return '{} {} {} {}'.format(self.x, self.y, self.z, self.garbage)


def main():
    a = A()
    prototype = Prototype()
    prototype.register_object('objecta', a)
    b = prototype.clone('objecta')
    c = prototype.clone('objecta', x=1, y=2, garbage=[88, 1])
    print([str(i) for i in (a, b, c)])


if __name__ == '__main__':
    main()
