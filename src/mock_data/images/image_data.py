import os
import glob


class ImageData:
    def __init__(self):
        self.data = glob.glob(os.path.dirname(__file__) + "\\*.PNG")
