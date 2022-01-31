from model import MinesweeperModel
from controller import MinesweeperController
from view import MinesweeperView

model = MinesweeperModel()
controller = MinesweeperController(model)
view = MinesweeperView(model, controller)
view.pack()
view.mainloop()
