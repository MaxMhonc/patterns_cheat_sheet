# https://ru.wikipedia.org/wiki/%D0%90%D0%B4%D0%B0%D0%BF%D1%82%D0%B5%D1%80_(%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD_%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F)#Python
class GameConsole:
    def create_game_picture(self):
        return 'picture from console'


class Antenna:
    def create_wave_picture(self):
        return 'picture from wave'


class SourceGameConsole(GameConsole):
    def get_picture(self):
        return self.create_game_picture()


class SourceAntenna(Antenna):
    def get_picture(self):
        return self.create_wave_picture()


class TV:
    def __init__(self, source):
        self.source = source

    def show_picture(self):
        return self.source.get_picture()


g = SourceGameConsole()
a = SourceAntenna()
game_tv = TV(g)
cabel_tv = TV(a)
print(game_tv.show_picture())
print(cabel_tv.show_picture())
