# https://programming.vip/docs/python-design-pattern-mediator-pattern.html

class Consumer:
    """Consumer class"""

    def __init__(self, product, price):
        self.name = "Consumer"

        self.product = product

        self.price = price

    def shopping(self, name):
        """Shopping"""

        print(
            "towards{} purchase {}In price {}product".format(name, self.price,
                                                             self.product))


class Producer:
    """Producer class"""

    def __init__(self, product, price):
        self.name = "Producer"

        self.product = product

        self.price = price

    def sale(self, name):
        """Selling goods"""

        print("towards{} Sale {}Price {}product".format(name, self.price,
                                                        self.product))


class Mediator:
    """Intermediaries"""

    def __init__(self):
        self.name = "tertium quid"

        self.consumer = None

        self.producer = None

    def sale(self):
        """Stock purchase"""

        self.consumer.shopping(self.producer.name)

    def shopping(self):
        """Shipment"""

        self.producer.sale(self.consumer.name)

    def profit(self):
        """profit"""

        print('Intermediary net income:{}'.format(
            (self.consumer.price - self.producer.price)))

    def complete(self):
        self.sale()

        self.shopping()

        self.profit()


if __name__ == '__main__':
    consumer = Consumer('Mobile phone', 3000)

    producer = Producer("Mobile phone", 2500)

    mediator = Mediator()

    mediator.consumer = consumer

    mediator.producer = producer

    mediator.complete()
