from enum import Enum

class Car:
    def __init__(self, brand, model, buildyear, mileage, price, power):
        self.brand = brand
        self.model = model
        self.buildyear = int(buildyear)
        try:
            self.mileage = float(mileage)
        except:
            self.mileage = 0
        self.price = float(price)
        self.power = int(power)