from enum import Enum

class Car:
    def __init__(self, brand, model, buildyear, mileage, price, power):
        self.brand = brand
        self.model = model
        self.buildyear = int(buildyear)
        self.mileage = float(mileage)
        self.price = float(price)
        self.power = int(power)