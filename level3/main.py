import json, os
from datetime import datetime

class Cars:
    def __init__(self, id, price_per_day, price_per_km):
        self.id = id
        self.price_per_day = price_per_day
        self.price_per_km = price_per_km
    
    @classmethod
    def from_json(cls, json_string):
        return cls(**json_string)
    
    def __repr__(self):
        return f'<Cars id => {self.id}, price_per_day => {self.price_per_day}, price_per_km => {self.price_per_km}>'
        
class Rentals(object):
    def __init__(self, id, car_id, start_date, end_date, distance):
        self.id = id
        self.car_id = car_id
        self.start_date = start_date
        self.end_date = end_date
        self.distance = distance
        
    @classmethod
    def from_json(cls, json_string):
        return cls(**json_string)
    
    def __repr__(self):
        return f'<Rentals {self.id}, car_id => {self.car_id}, start_date => {self.start_date}, end_date => {self.end_date}, distance => {self.distance}>'
    
def create_rentals(rent):
    list = []
    for i in range(0,len(rent)):
        list.append(Rentals.from_json(rent[i]))
    return list

def create_cars(car):
    list = []
    for i in range(0,len(car)):
        list.append(Cars.from_json(cars[i]))
    return list

def listToDict(lst):
    op = dict(lst)
    return op

def nb_days(start_date, end_date):
    d1 = datetime.strptime(start_date, "%Y-%m-%d")
    d2 = datetime.strptime(end_date, "%Y-%m-%d")
    return abs((d2 - d1).days) + 1

def calculate_price_km(price_km, distance):
    result = price_km * distance
    return result

def total_price(a, b):
    val = a + b
    return (val)

def commission(price, days):
    com = price * 30 / 100
    insurance = com / 2
    assistance = days * 100
    drivy = com - insurance - assistance
    res = {
        "insurance_fee" : int(insurance),
        "assistance_fee" : int(assistance),
        "drivy_fee" : int(drivy)
    }
    return res

def calculate_price_day(day, price):
    days_left = day
    result = 0
    while (days_left > 0):
        if (days_left == 1):
            result = result + price
        if (days_left > 1 and days_left <= 4):
            new_price = (price - (price * 10 / 100))
            result = result + new_price   
        if (days_left > 4 and days_left <= 10):
            new_price = (price - (price * 30 / 100))
            result = result + new_price
        if (days_left > 10):
            new_price = (price - (price * 50 / 100))
            result = result + new_price
        days_left = days_left - 1  
    return int(result)

def main(rentals, cars):
    json_res = { "rentals" : []
                }
    
    for i in range(0,len(rentals)):
        for j in range(0, len(cars)):
            if(cars[j].id == rentals[i].car_id):
                days = nb_days(rentals[i].start_date,rentals[i].end_date)
                price_km = calculate_price_km(cars[j].price_per_km,rentals[i].distance)
                price_day = calculate_price_day(days, cars[j].price_per_day)
                price = total_price(price_day,price_km)
                com = commission(price, days)
                hash = {
                    "id" : rentals[i].id,
                    "price" : price,
                    "commission" : com
                }
                json_res["rentals"].append(hash)
    return json_res

def write_json(fi):
    path = os.getcwd() + "/data/output.json"
    f = open (path, 'w')
    new = fi
    f.write(json.dumps(new, indent=2))
    f.close()
    

if __name__ == "__main__": 
    file_path = os.getcwd() + "/data/input.json"
    with open(file_path, 'r') as f:
        datas = json.load(f)

    json_dict = listToDict(datas)
    rentals = json_dict['rentals']
    cars = json_dict['cars']
    all_cars = create_cars(cars)
    all_rentals = create_rentals(rentals)

    final_file = main(all_rentals, all_cars)
    write_json(final_file)

