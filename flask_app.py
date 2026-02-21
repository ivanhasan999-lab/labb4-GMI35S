from flask import Flask
from car_routes import car_bp

app = Flask(__name__)

# --- ROUTES ---

# 1. Den här routen fixar "404 Not Found" på huvudsidan.
@app.route('/')
def home():
    return """
    <h1>Bil-API är igång!</h1>
    <p>För att se alla bilar, gå till: <a href="/cars">/cars</a></p>
    """

# 2. Registrera din Blueprint från car_routes.py
# Detta gör att alla routes som @car_bp.route("/cars") blir aktiva.
app.register_blueprint(car_bp)

# --- STARTA SERVERN ---

if __name__ == "__main__":
    # debug=True gör att servern laddar om automatiskt när du ändrar i koden.
    # port=5000 är standard för Flask.
    app.run(debug=True, port=5000)