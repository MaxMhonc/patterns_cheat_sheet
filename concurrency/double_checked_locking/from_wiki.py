# https://ru.wikipedia.org/wiki/%D0%91%D0%BB%D0%BE%D0%BA%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B0_%D1%81_%D0%B4%D0%B2%D0%BE%D0%B9%D0%BD%D0%BE%D0%B9_%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%BE%D0%B9#%D0%9F%D1%80%D0%B8%D0%BC%D0%B5%D1%80_%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F_%D0%B2_Python

import threading


class SimpleLazyProxy:
    '''ленивая инициализация объекта

    безопасная для многонитевого использования'''

    def __init__(self, factory):
        self.__lock = threading.RLock()
        self.__obj = None
        self.__factory = factory

    def __call__(self):
        '''функция для доступа к настоящему объекту

        если объект не создан, то он создастся'''

        # пробуем получить "быстрый" доступ к объекту:
        obj = self.__obj

        if obj is not None:
            # получилось!

            return obj
        else:
            # объект, возможно, ещё не создан

            with self.__lock:
                # получаем доступ к объекту в эксклюзивном режиме:
                obj = self.__obj

                if obj is not None:
                    # оказалось, объект уже создан.
                    # 	не будем повторно его создавать

                    return obj
                else:
                    # объект действительно ещё не создан.
                    # 	создадим же его!

                    obj = self.__factory()

                    self.__obj = obj

                    return obj

    __getattr__ = lambda self, name: \
        getattr(self(), name)


def lazy(proxy_cls=SimpleLazyProxy):
    '''декоратор, превращающий класс в класс с ленивой инициализацией

    средствами Proxy-класса'''

    class ClassDecorator:
        def __init__(self, cls):
            # инициализация декоратора,
            # 	но не декорируемого класса и не Proxy-класса

            self.cls = cls

        def __call__(self, *args, **kwargs):
            # запрос инициализации Proxy-класса

            # передадим Proxy-классу нужные параметры
            # 	для инициализации декорируемого класса

            return proxy_cls(lambda: self.cls(*args, **kwargs))

    return ClassDecorator


# простая проверка:

def test_0():
    print('\t\t\t*** Начало теста ***')

    import time

    @lazy()  # экземпляры этого класса будут с ленивой инициализацией
    class TestType:
        def __init__(self, name):
            print('%s: Создаётся...' % name)
            # искусственно увеличим время создания объекта
            # 	для нагнетения конкуренции потоков
            time.sleep(3)

            self.name = name

            print('%s: Создался!' % name)

        def test(self):
            print('%s: Проверка' % self.name)

    # один такой экземпляр будет взаимодействовать с несколькими потоками
    test_obj = TestType('Межнитевый тестовый объект')

    target_event = threading.Event()

    def threads_target():
        # функция, которую будут выполнять потоки:

        # ждём наступления специального события
        target_event.wait()

        # как только это событие наступит -
        # 	все 10 потоков одновременно обратятся к тестовому объекту
        # 	и в этот момент он инициализируется в одном из потоков
        test_obj.test()

    # создадим эти 10 потоков с вышеописанным алгоритмом threads_target()
    threads = []
    for thread in range(10):
        thread = threading.Thread(target=threads_target)

        thread.start()
        threads.append(thread)

    print('До этого момента обращений к объекту не было')

    # подождём немного времени...
    time.sleep(3)

    # ...и запустим test_obj.test() одновременно во всех потоках
    print('Активируем событие для использования тестового объекта!')
    target_event.set()

    # завершение
    for thread in threads:
        thread.join()

    print('\t\t\t*** Конец теста ***')
