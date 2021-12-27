# https://dev.to/erikwhiting88/implementing-the-decorator-pattern-in-python-1fdm

# Leashed dog with decoration
class Dog:
    def __init__(self, name):
        self.name = name

    def bark(self):
        print("RUFF!")


class LeashedDogDecorator:
    def __init__(self, model):
        self.model = model
        self.model_attributes = [attribute for attribute in
                                 self.model.__dict__.keys()]
        self.model_methods = [m for m in dir(self.model) if not m.startswith(
            '_') and m not in self.model_attributes]

    def __getattr__(self, func):
        if func in self.model_methods:
            def method(*args):
                return getattr(self.model, func)(*args)

            return method
        elif func in self.model_attributes:
            return getattr(self.model, func)
        else:
            raise AttributeError

    def tug_on_leash(self):
        print("Let's go!!")


dog = Dog('Jeff')
dog = LeashedDogDecorator(dog)
dog.bark()
dog.tug_on_leash()
print(dog.name)
