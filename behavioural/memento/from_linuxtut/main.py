import time
from memento.gamer import Gamer


def startMain():
    gamer = Gamer(100)
    memento = gamer.createMemento()

    for i in range(100):
        print("==== {0}".format(i))
        print("Current status:{0}".format(gamer))
        gamer.bet()
        print(
            "The money you have{0}It became a circle".format(gamer.getMoney()))

        if gamer.getMoney() > memento.getMoney():
            print(
                "      (It has increased a lot, so let's save the current state)")
            memento = gamer.createMemento()
        elif gamer.getMoney() < memento.getMoney() / 2:
            print(
                "      (It has decreased a lot, so let's return to the previous state)")
            gamer.restoreMemento(memento)

        time.sleep(1)
        print("")


if __name__ == '__main__':
    startMain()
