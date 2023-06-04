import uvicorn
from fastapi import FastAPI
from predict import predict_car_price
import json
from scraper import scrape

app = FastAPI()

#fix for CORS error
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins
)


@app.get("/predict")
def predict_car(brand: str, model: str, buildyear: int, mileage: int, power: int):
    price = predict_car_price(brand, model, buildyear, mileage, power)

    return {
        "price": price
    }

@app.get("/cars")
def get_cars():
    file = open('cars.json', 'r')

    cars = json.load(file)

    return {
        "cars": cars
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)