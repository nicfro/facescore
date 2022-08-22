import os
import sys
import json

sys.path.insert(0, os.getcwd())

from fastapi.testclient import TestClient
from src.mock_data.users.user_data import UserData
from src.mock_data.images.image_data import ImageData
from src.main import app
from src.database.base import DBConnector


DB = DBConnector()
DB.drop_and_create_tables()
"""
client = TestClient(app)

# Create users from User mock data
insert_users = UserData()
for user in insert_users.data:
    client.post("/users", json=user)

# login with created user for JWT token & create header for future requests
form = {"username": user["name"], "password": user["password1"]}
bearer = client.post("/login", data=form)
token = json.loads(bearer.text)["access_token"]
header = {"Authorization": f"bearer {token}"}


# insert images from image mock data
insert_images = ImageData()

payload = json.dumps({"image": insert_images.verify1, "gesture": "ok"})
response = client.post("/users/verify/", data=payload, headers=header)

# payload = json.dumps({"image": insert_images.verify2, "gesture": "peace"})
# response = client.post("/users/verify/", data=payload, headers=header)

for image in insert_images.data:
    payload = json.dumps({"image": image})
    result = client.post("/images", headers=header, data=payload)

"""
