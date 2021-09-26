class car:
    xang=None
    def __init__(self, name):
        self.name = name
    def set(self):
        self.xang = 100

car = car('honda')
car.set()
print(car.xang)