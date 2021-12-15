# Делегирование (англ. Delegation) — основной шаблон проектирования, в котором
# объект внешне выражает некоторое поведение, но в реальности передаёт
# ответственность за выполнение этого поведения связанному объекту.
# Шаблон делегирования является фундаментальной абстракцией, на основе которой
# реализованы другие шаблоны - композиция (также называемая агрегацией),
# примеси (mixins) и аспекты (aspects).


class A:
    def f(self):
        print('A : вызываем метод f')

    def g(self):
        print('A : вызываем метод g')


class C:
    def __init__(self):
        self.A = A()

    def f(self):
        return self.A.f()

    def g(self):
        return self.A.g()


c = C()
c.f()  # A: вызываем метод f
c.g()  # A: вызываем метод g
