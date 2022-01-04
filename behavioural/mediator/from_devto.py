# https://dev.to/jemaloqiu/design-pattern-in-python-6-mediator-pattern-b7d

# Basket of Too good to go
class BasketInfo:
    """Food Basket info"""

    def __init__(self, location, price, address, Shop):
        self.__location = location
        self.__price = price
        self.__address = address
        self.__Shop = Shop

    def getLocation(self):
        return self.__location

    def getAddress(self):
        return self.__address

    def getShopName(self):
        return self.__Shop.getName()

    def showInfo(self, isShowShop=True):
        print(" ++ Location: {}".format(self.__location))
        print(" ++ Price: {}".format(str(self.__price) + " euros"))
        print(" ++ Address: {}".format(self.__address))
        print(" ++ Shop: " + self.getShopName() if isShowShop else "")
        print()


import difflib


# Check the similarity of two strings
def get_equal_rate(str1, str2):
    return difflib.SequenceMatcher(None, str1, str2).quick_ratio()


class BasketPlatformApp:
    """Too Good To Go platform"""

    def __init__(self, name):
        self.__BasketInfos = []
        self.__name = name

    def getName(self):
        return self.__name

    def addBasketInfo(self, BasketInfo):
        self.__BasketInfos.append(BasketInfo)

    def removeBasketInfo(self, BasketInfo):
        for info in self.__BasketInfos:
            if (info == BasketInfo):
                self.__BasketInfos.remove(info)

    def getSearchCondition(self, description):
        return description

    def getMatchInfos(self, searchCondition):
        print(self.getName(), " shows suitable baskets for you：")
        suitables = []
        for info in self.__BasketInfos:
            if get_equal_rate(searchCondition, info.getLocation()) > 0.9:
                info.showInfo(False)
                suitables.append(info)
        return suitables

    def addBasket(self, BasketInfo):
        print(self.getName(), " has a new avaible Basket \n  -- Provided by ",
              BasketInfo.getShopName(), ",\n  -- Located at: ",
              BasketInfo.getAddress())

    def addBaskets(self):
        for info in self.__BasketInfos:
            self.addBasket(info)


class BasketShop:
    """ BasketShop class """

    def __init__(self, name):
        self.__name = name
        self.__BasketInfo = None

    def getName(self):
        return self.__name

    def setBasketInfo(self, address, location, price):
        self.__BasketInfo = BasketInfo(location, price, address, self)

    def publishBasketInfo(self, App):
        App.addBasketInfo(self.__BasketInfo)
        print(self.getName() + " pushes a Basket on ", App.getName(), ": ")
        self.__BasketInfo.showInfo()


class Customer:
    """User of TooGoodToGO"""

    def __init__(self, name):
        self.__name = name

    def getName(self):
        return self.__name

    def findBasket(self, description, App):
        print(
            "User " + self.getName() + ", searching a backet with info: " + description)
        print()
        return App.getMatchInfos(App.getSearchCondition(description))

    def viewBasket(self, BasketInfos):
        size = len(BasketInfos)
        return BasketInfos[size - 1]

    def buyBasket(self, BasketInfo, App):
        """ command Basket on App """
        print(self.getName(), " made a new command on ", App.getName(),
              " for a basket in ", BasketInfo.getShopName())


if __name__ == "__main__":
    myAPP = BasketPlatformApp("Too Good To Go")
    Paul = BasketShop("Paul")
    Paul.setBasketInfo("La Defense Parvis 15, 92000, Haut-Seine",
                       "4 temps commercial center", 3.99)
    Paul.publishBasketInfo(myAPP)
    Auchan = BasketShop("Auchan")
    Auchan.setBasketInfo("22 Rue Alma, 92240, Courbevoie",
                         "Supermarcket A2Pas", 4.0)
    Auchan.publishBasketInfo(myAPP)
    Sushi = BasketShop("Sushi Shop")
    Sushi.setBasketInfo("La Defense Parvis 15, 92000, Haut-Seine",
                        "4 temps commercial center", 6.99)
    Sushi.publishBasketInfo(myAPP)
    print()

    myAPP.addBaskets()
    print()

    jemaloQ = Customer("jemaloQ")
    BasketInfos = jemaloQ.findBasket("4 temps commercial center", myAPP)
    print()
    print("Searching available baskets for you ……")
    print()
    AppropriateBasket = jemaloQ.viewBasket(BasketInfos)
    jemaloQ.buyBasket(AppropriateBasket, myAPP)
