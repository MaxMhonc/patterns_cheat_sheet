# https://ru.wikipedia.org/wiki/%D0%9D%D0%B0%D0%B1%D0%BB%D1%8E%D0%B4%D0%B0%D1%82%D0%B5%D0%BB%D1%8C_(%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD_%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F)#Python

from abc import ABCMeta, abstractmethod


class Observer(metaclass=ABCMeta):
    """
    Абстрактный наблюдатель
    """

    @abstractmethod
    def update(self, message: str) -> None:
        """
        Получение нового сообщения
        """
        pass


class Observable(metaclass=ABCMeta):
    """
    Абстрактный наблюдаемый
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        self.observers = []  # инициализация списка наблюдателей

    def register(self, observer: Observer) -> None:
        """
        Регистрация нового наблюдателя на подписку
        """
        self.observers.append(observer)

    def notify_observers(self, message: str) -> None:
        """
        Передача сообщения всем наблюдателям, подписанным на события
        данного объекта наблюдаемого класса
        """
        for observer in self.observers:
            observer.update(message)


class Newspaper(Observable):
    """
    Газета, за новостями в которой следят тысячи людей
    """

    def add_news(self, news: str) -> None:
        """
        Выпуск очередной новости
        """
        self.notify_observers(news)


class Citizen(Observer):
    """
    Обычный гражданин, который любит читнуть с утра любимую газетку
    """

    def __init__(self, name: str) -> None:
        """
        Constructor.

        :param name: имя гражданина, чтоб не спутать его с кем-то другим
        """
        self.name = name

    def update(self, message: str) -> None:
        """
        Получение очередной новости
        """
        print(f'{self.name} узнал следующее: {message}')


if __name__ == '__main__':
    newspaper = Newspaper()  # создаем небольшую газету
    newspaper.register(Citizen('Иван'))  # добавляем двух человек, которые
    newspaper.register(Citizen('Василий'))  # ... ее регулярно выписывают
    # ... и вбрасываем очередную газетную утку
    newspaper.add_news('Наблюдатель - поведенческий шаблон проектирования')

'''
Иван узнал следующее: Наблюдатель - поведенческий шаблон проектирования
Василий узнал следующее: Наблюдатель - поведенческий шаблон проектирования
'''
