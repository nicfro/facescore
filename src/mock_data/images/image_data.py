import os
import glob
import base64


class ImageData:
    def __init__(self):
        self.data = []
        paths = glob.glob(os.path.dirname(__file__) + "\\nic*.PNG")
        for path in paths:
            with open(path, "rb") as f:
                im_bytes = f.read()
            self.data.append(base64.b64encode(im_bytes).decode("utf8"))

        with open(os.path.dirname(__file__) + "\\ok1.jpg", "rb") as f:
            im_bytes = f.read()
        self.verify1 = base64.b64encode(im_bytes).decode("utf8")

        with open(
            os.path.dirname(__file__) + "\\peace.jpg",
            "rb",
        ) as f:
            im_bytes = f.read()
        self.verify2 = base64.b64encode(im_bytes).decode("utf8")
