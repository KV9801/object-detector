import os
import torch


class Model:
    def __init__(self):
        # Model
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

    def getphoto(self, dir_photo):
        # Inference
        results = self.model(dir_photo)
        return results

class Config(object):
    SECRET_KEY = os.urandom(24)
    MAX_CONTENT_LENGTH = 1024 * 1024 * 16  # for 16MB max-limit.
