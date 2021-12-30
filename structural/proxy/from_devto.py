# https://dev.to/jemaloqiu/design-pattern-in-python-5-proxy-pattern-44mf

from abc import ABCMeta, abstractmethod


class Subject(metaclass=ABCMeta):
    """ Subject class """

    def __init__(self, name):
        self.__name = name

    def getName(self):
        return self.__name

    @abstractmethod
    def request(self, content=''):
        pass


class RealSubject(Subject):
    """RealSubject class"""

    def request(self, content):
        print("RealSubject todo something...")


class ProxySubject(Subject):
    """ ProxySubject Class"""

    def __init__(self, name, subject):
        super().__init__(name)
        self._realSubject = subject

    def request(self, content=''):
        self.preRequest()
        if (self._realSubject is not None):
            self._realSubject.request(content)
        self.afterRequest()

    def preRequest(self):
        print("preRequest")

    def afterRequest(self):
        print("afterRequest")


class RomeoGiving(Subject):
    """Romeo gives gift"""

    def __init__(self, name, wishMsg, receiver):
        super().__init__(name)
        self.__message = wishMsg
        self.__receiver = receiver

    def getMsg(self):
        return self.__message

    def getReceiver(self):
        return self.__receiver

    def request(self, content):
        print("  {} sends gift to {} with a wish Message：\"{}\"".format(
            self.getName(), self.getReceiver(), self.getMsg()))
        print("  Gift is {}".format(str(content)))


class JackGiving(ProxySubject):
    """Jack gives gift instead"""

    def __init__(self, name, GivingTask):
        super().__init__(name, GivingTask)

    def preRequest(self):
        print(" [Proxy] {} saying: I give you the gift on behalf of {}".format(
            self.getName(), self._realSubject.getName()))

    def afterRequest(self):
        print(
            " [Proxy] {} saying: I have given gift to {} on behalf of {}".format(
                self.getName(), self._realSubject.getReceiver(),
                self._realSubject.getName()))


if __name__ == '__main__':
    print("=================")
    Romeo = RomeoGiving("Romeo",
                        "I loved you, I love you and I will love you forever.",
                        "Julia")
    print("Romeo gives gift: ")
    Romeo.request("Rose")

    print("=================")

    print("Jack gives gift instead")
    Jack = JackGiving("Jack", Romeo)
    Jack.request("Chocolate")
