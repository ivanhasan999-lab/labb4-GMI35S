from flask import Blueprint, jsonify, request
import json
import os

car_bp = Blueprint('car_bp', __name__)
DATA_FILE = "cars.json"

def load_cars():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            content = file.read()
            return json.loads(content) if content else []
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_cars(cars):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(cars, file, indent=4, ensure_ascii=False)

# GET - Hämta alla bilar
@car_bp.route("/cars", methods=["GET"])
def get_cars():
    return jsonify(load_cars()), 200

# POST - Lägg till en bil
@car_bp.route("/cars", methods=["POST"])
def add_car():
    new_car = request.get_json(silent=True)
    if not new_car or "regnr" not in new_car:
        return jsonify({"error": "Data saknas"}), 400
    
    cars = load_cars()
    # Hindra dubbletter
    if any(c['regnr'].upper() == new_car['regnr'].upper() for c in cars):
        return jsonify({"error": "Bilen finns redan"}), 400

    cars.append(new_car)
    save_cars(cars)
    return jsonify({"message": "Bil tillagd!", "car": new_car}), 201

# PUT - Uppdatera via regnr
@car_bp.route("/cars/<string:regnr>", methods=["PUT"])
def update_car(regnr):
    data = request.get_json(silent=True)
    cars = load_cars()
    for car in cars:
        if car['regnr'].upper() == regnr.upper():
            car.update(data)
            save_cars(cars)
            return jsonify({"message": "Uppdaterad", "car": car}), 200
    return jsonify({"error": "Hittades ej"}), 404

# DELETE - Ta bort via regnr
@car_bp.route("/cars/<string:regnr>", methods=["DELETE"])
def delete_car(regnr):
    cars = load_cars()
    new_list = [c for c in cars if c['regnr'].upper() != regnr.upper()]
    if len(new_list) == len(cars):
        return jsonify({"error": "Hittades ej"}), 404
    save_cars(new_list)
    return jsonify({"message": f"Bil {regnr} raderad"}), 200