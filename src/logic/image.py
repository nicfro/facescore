import argparse
from src.schemas.images import ImageSchema
from src.database.crud import create, read

class Image:
    def __init__(**kwargs):
        self.kwargs = vars(kwargs) if type(kwargs) is argparse.Namespace else kwargs
        self.image = ImageSchema(kwargs)

    def upload_image(image_binary):
        create(self.image)

    def get_image(image_id):
        return read(self.image, "id", image_id).file
