import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from models.car import Car
import os
from scraper import scrape

def extract_features_and_target(cars):
    features = []
    targets = []
    for car in cars:
        features.append([car.buildyear, car.mileage, car.power])
        targets.append(car.price)

    return features, targets

def train_model(features, targets):
    model = LinearRegression()
    model.fit(features, targets)
    return model

def predict_price(model, test_features):
    return model.predict(test_features)

def predict_car_price(brand, model, buildyear, mileage, power):
    # Read data from csv file
    cars = []

    csv_file = f'{brand}_{model}.csv'.lower()
    csv_file = os.path.join('cars', csv_file)

    #check if file exists
    if not os.path.isfile(csv_file):
        scrape(brand=brand, model=model)

    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:
            cars.append(Car(brand, model, row[0], row[1], row[2], row[3]))

    features, targets = extract_features_and_target(cars)

    model = train_model(features, targets)

    test_car = Car(brand=brand, model=model, buildyear=buildyear, mileage=mileage, price=0, power=power)

    test_features = [[test_car.buildyear, test_car.mileage, test_car.power]]

    predicted_price = predict_price(model, test_features)

    price = round(predicted_price[0], 2)

    print("Predicted Price:", price)

    return price