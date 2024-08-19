from __future__ import annotations
from datetime import date
import numpy as np
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import ARRAY, FLOAT
from . import db

import numpy as np

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False) 
    password = db.Column(db.String(30), nullable = False)
    lands = db.relationship('Land', back_populates='owner')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class Land(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    x1 = db.Column(db.Float)
    y1 = db.Column(db.Float)
    x2 = db.Column(db.Float)
    y2 = db.Column(db.Float)
    x3 = db.Column(db.Float)
    y3 = db.Column(db.Float)
    x4 = db.Column(db.Float)
    y4 = db.Column(db.Float)
    name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', back_populates='lands')
    # points = db.Column(db.JSON, nullable=False)

    def __init__(self, name, user_id, x1, y1, x2, y2, x3, y3, x4, y4):
        self.name = name
        self.user_id = user_id
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.x4 = x4
        self.y4 = y4
        # self.points = self.__get_JSON_coords(first_point, second_point, third_point, fourth_point)

    # def __get_JSON_coords(self,
    #                       first_point: list[int],
    #                       second_point: list[int],
    #                       third_point: list[int],
    #                       fourth_point: list[int],
    #                       ) -> None:
         
    #     json_data = {}
    #     json_data["x1"] = first_point[0]
    #     json_data["y1"] = first_point[1]
    #     json_data["x2"] = second_point[0]
    #     json_data["y2"] = second_point[1]
    #     json_data["x3"] = third_point[0]
    #     json_data["y3"] = third_point[1]
    #     json_data["x4"] = fourth_point[0]
    #     json_data["y4"] = fourth_point[1]

    #     self.points = json_data        
    
    def sort_points(self) -> list[list[float]]:
        coordinates = [[self.x1, self.y1],  [self.x2, self.y2], [self.x3, self.y3], [self.x4, self.y4]]
        centroid = np.mean(coordinates, axis = 0)

        def angle_from_centroid(point):
            return np.arctan2(point[1] - centroid[1], point[0] - centroid[0])
        
        sorted_points = sorted(coordinates, key=angle_from_centroid)
        [[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = sorted_points
    
        return [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]

    def get_area_surface(self) -> float:
        [[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = self.sort_points() #nu stiu daca e legal ce am facut dar nu aveam alta idee pe moment
        #shoelace formula
        sum1 = x1 * y2 + x2 * y3 + x3 * y4 + x4 * y1
        sum2 = y1 * x2 + y2 * x3 + y3 * x4 + y4 * x1
        return round((abs(sum1 - sum2) / 2), 2)
    
    def get_limits(self) -> list[float]:

        coords_as_np = np.array([[self.x1, self.y1], 
                                 [self.x2, self.y2],
                                 [self.x3, self.y3],
                                 [self.x4, self.y4]])
        
        north = np.max(coords_as_np[:, 0])
        south = np.min(coords_as_np[:, 0])
        east = np.max(coords_as_np[:, 1])
        west = np.min(coords_as_np[:, 1])

        return [north, south, east, west]
    
    #info: un json cu 2-3 chestii random


class Result():
    input : str   #poate va fi un JSON
    result : str 
    statisfaction_level: int
    generated_date: date

    def _clear_result(self) -> None:
        # __del__ cred ca trebuie apelat
        pass

    def __del__(self) -> None:
        pass


   

