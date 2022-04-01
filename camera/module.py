from modules import json
from cv2 import VideoCapture
cap = VideoCapture()


class Camera():
    def __init__(self, id: int) -> None:
        self.id = id
        self.load_config()

    def load_config(self):
        self.config = json.load(f"camera_{self.id}.json")