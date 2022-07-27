import os
import sys

sys.path.insert(0, os.getcwd())

from fastapi.testclient import TestClient
from src.mock_data.users.user_data import UserData
from src.mock_data.images.image_data import ImageData
from src.main import app
from src.database.base import DBConnector


DB = DBConnector()
DB.drop_and_create_tables()

client = TestClient(app)

insert_users = UserData()
insert_images = ImageData()

for user in insert_users.data:
    client.post("/users", json=user)


form = {"user_id": "1", "gender": "female"}
for image in insert_images.data:
    files = {"image": (f"{image}", open(image, "rb").read())}
    header = {
        "Content-Type": "multipart/form-data",
    }
    result = client.post("/images", params=form, files=files)

