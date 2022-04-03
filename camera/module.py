import os
os.environ["OPENCV_LOG_LEVEL"]="FATAL"
from modules import json, Thread
from importlib import reload
from time import sleep
import cv2, math, numpy as np
from simplejpeg import encode_jpeg
from queue import Queue

import camera.camera_0 as camera_0
import camera.camera_1 as camera_1
import camera.camera_2 as camera_2
import camera.camera_3 as camera_3
import camera.camera_4 as camera_4

class Camera():
    def __init__(self, id: int) -> None:
        self.id = id
        self.reload()
        self.img = np.zeros((640, 480, 3), dtype=np.uint8)
        self.frame = encode_jpeg(self.img.copy(), colorspace="bgr")
        self.camera = cv2.VideoCapture(id)
        self.camera_queue = Queue()
        self.camera_read_thread = Thread(target=self.camera_read, name=f"camera_{id}")
        self.load_config()
        self.camera_read_thread.start()

    def load_config(self, image_config=None, camera_config=None):
        if image_config == None:
            image_config: dict = json.load(f"data/camera_{self.id}.json").get("image", False)
        if camera_config == None:
            camera_config: dict = json.load(f"data/camera_{self.id}.json").get("camera", False)
        if image_config:
            self.config = image_config
        if camera_config:
            self.camera_queue.put(camera_config)

    def reload(self):
        if self.id == 0:
            reload(camera_0)
            self.camera_module = camera_0
        elif self.id == 1:
            reload(camera_1)
            self.camera_module = camera_1
        elif self.id == 2:
            reload(camera_2)
            self.camera_module = camera_2
        elif self.id == 3:
            reload(camera_3)
            self.camera_module = camera_3
        elif self.id == 4:
            reload(camera_4)
            self.camera_module = camera_4

    # 讀取鏡頭
    def camera_read(self):
        while True:
            if not self.camera_queue.empty():
                camera_config: dict = self.camera_queue.get()
                self.camera.release()
                self.camera = cv2.VideoCapture(self.id)
                self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, camera_config.get("width", 0))
                self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_config.get("height", 0))
                self.camera.set(cv2.CAP_PROP_FPS, camera_config.get("fps", 0))
                self.camera.set(cv2.CAP_PROP_BRIGHTNESS, camera_config.get("brightness", 0))
                self.camera.set(cv2.CAP_PROP_CONTRAST, camera_config.get("contrast", 0))
                self.camera.set(cv2.CAP_PROP_SATURATION, camera_config.get("saturation", 0))
                self.camera.set(cv2.CAP_PROP_HUE, camera_config.get("hue", 0))
                self.camera.set(cv2.CAP_PROP_GAIN, camera_config.get("gain", 0))
                self.camera.set(cv2.CAP_PROP_EXPOSURE, camera_config.get("exposure", 0))
            success, raw_img = self.camera.read()
            if success:
                img = raw_img.copy()
                img = self.highlight(img)
                img = self.brightness(img)
                img = self.contrast(img)
                img = self.modify_color_temperature(img)
                img = self.saturation(img)
                try:
                    img = self.camera_module.runPipeline(img)
                except:
                    pass
                self.img = img.copy()
                self.frame = encode_jpeg(img.copy(), colorspace="bgr")
            else:
                try:
                    self.camera = cv2.VideoCapture(self.id)
                except:
                    sleep(5)

    # 調整亮度
    def brightness(self, r_img):
        value = self.config.get("brightness", 0)
        if value != 0:
            r_img = r_img.astype(np.float64)
            if value > 0:
                r_img += (255 - np.min(r_img)) * value / 255
            else:
                r_img -= (0 - np.max(r_img)) * value / 255
            r_img += value
            r_img[r_img > 255] = 255
            r_img[r_img < 0] = 0
            return r_img.astype(np.uint8)
        return r_img

    # 調整飽和度
    def saturation(self, r_img):
        value = self.config.get("saturation", 0)
        if value != 0:
            img = cv2.cvtColor(r_img, cv2.COLOR_BGR2HSV).astype(np.float64)
            if value > 0:
                img[:, :, 1] += (255 - np.min(img[:, :, 1])) * value / 255
            else:
                img[:, :, 1] -= (0 - np.max(img[:, :, 1])) * value / 255
            img[img[:, :, 1] > 255, 1] = 255
            img[img[:, :, 1] < 0, 1] = 0
            img = img.astype(np.uint8)
            img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
            return img
        return r_img

    # 調整對比度
    def contrast(self, r_img):
        c = self.config.get("contrast", 0)
        if c != 0:
            img_gray = cv2.cvtColor(r_img, cv2.COLOR_BGR2GRAY)
            med = np.median(img_gray)
            r_img = r_img.astype(np.float64)
            r_img += (r_img - med) * c / 255
            r_img[r_img > 255] = 255
            r_img[r_img < 0] = 0
            return r_img.astype(np.uint8)
        return r_img

    # 調整紅藍平衡
    def modify_color_temperature(self, r_img):
        blue_blance = self.config.get("blue-blance", 0)
        red_blance = self.config.get("red-blance", 0)
        if blue_blance != 0 or red_blance != 0:
            r_img = r_img.astype(np.float64)
            r_img[:, :, 0] += blue_blance - red_blance
            r_img[:, :, 1] -= (blue_blance + red_blance) / 2
            r_img[:, :, 2] += red_blance - blue_blance
            r_img[r_img > 255] = 255
            r_img[r_img < 0] = 0
            return r_img.astype(np.uint8)
        return r_img

    # 修正高光
    def highlight(self, r_img):
        value = self.config.get("reduce-highlight", 0)
        if value != 0:
            img_gray = cv2.cvtColor(r_img, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(img_gray, 255 - value, 255, 0)
            r_img = r_img.astype(np.float64)
            r_img[thresh == 255] *= 1 - (np.stack((img_gray,)*3, axis=-1)[thresh == 255] / 255) * 2 *value / 255
            r_img[r_img < 0] = 0
            r_img = r_img.astype(np.uint8)
        return r_img

    def output(self):
        while True:
            yield (b"--frame\r\nContent-Type:image/jpeg\r\n\r\n" + self.frame + b"\r\n")

def show(img):
    cv2.imshow("", img)
    while True:
        if cv2.waitKey() == 27:
            cv2.destroyAllWindows()
            break

def brightness_0(r_img, value):
    if value != 0:
        r_img = r_img.astype(np.float64)
        if value > 0:
            r_img += (255 - np.min(r_img)) * value / 255
        else:
            r_img -= (0 - np.max(r_img)) * value / 255
        r_img += value
        r_img[r_img > 255] = 255
        r_img[r_img < 0] = 0
        return r_img.astype(np.uint8)
    return r_img