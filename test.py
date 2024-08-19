from website.models import Land, User
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import numpy as np
from flask import Flask

db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db.init_app(app)

# Example coordinate storage (in-memory)
land_coordinates = {
    1: [[0, 0], [0, 1], [1, 1], [1, 0]],  # Coordinates for Land ID 1
    2: [[1, 0], [1, 1], [2, 1], [2, 0]],  # Coordinates for Land ID 2
    3: [[2, 0], [2, 1], [3, 1], [3, 0]]   # Coordinates for Land ID 3
}

with app.app_context():
    # Create the database and tables
    db.create_all()

    # Create a new user
    new_user = User(username='Alice', email='alice@example.com', password='password123')

    # Create and assign three lands to the new user
    land1 = Land(owner=new_user)
    land2 = Land(owner=new_user)
    land3 = Land(owner=new_user)

    # Add the user and lands to the session
    db.session.add(new_user)
    db.session.add(land1)
    db.session.add(land2)
    db.session.add(land3)

    # Commit the changes
    db.session.commit()

    # Access lands for the user
    all_lands = new_user.lands

    # Print the list of all lands and their computed areas
    print("List of all lands with areas:")
    for land in all_lands:
        land_id = land.id
        coords = land_coordinates.get(land_id, [])
        if coords:
            area = Land.get_area_surface(coords)
            print(f'Land ID: {land_id}, Area: {area}')
        else:
            print(f'Land ID: {land_id} has no coordinates stored.')
