import os
os.environ["OPENCV_LOG_LEVEL"]="FATAL"
from modules import json, Thread
from importlib import reload
from time import sleep
import cv2, math, numpy as np
from simplejpeg import encode_jpeg

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
        self.camera_read_thread = Thread(target=self.camera_read, name=f"camera_{id}")
        self.load_config()
        self.camera_read_thread.start()

    def load_config(self):
        image_config: dict = json.load(f"data/camera_{self.id}.json").get("image", False)
        camera_config: dict = json.load(f"data/camera_{self.id}.json").get("camera", False)
        if image_config:
            self.config = image_config
        if camera_config:
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
            print(f"Camera {self.id} load config")
            print(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
            print(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
            print(self.camera.get(cv2.CAP_PROP_FPS))
            print(self.camera.get(cv2.CAP_PROP_BRIGHTNESS))
            print(self.camera.get(cv2.CAP_PROP_CONTRAST))
            print(self.camera.get(cv2.CAP_PROP_SATURATION))
            print(self.camera.get(cv2.CAP_PROP_HUE))
            print(self.camera.get(cv2.CAP_PROP_GAIN))
            print(self.camera.get(cv2.CAP_PROP_EXPOSURE))
            # if self.camera_read_thread.is_alive():
            #     self.camera_read_thread.stop()
            #     self.camera_read_thread.join()
            #     self.camera_read_thread = Thread(target=self.camera_read, name=f"camera_{id}")
            #     self.camera_read_thread.start()

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
            try:
                success, raw_img = self.camera.read()
                if success:
                    img = raw_img.copy()
                    if self.config.get("enable", 0) == 1:
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
            except:
                sleep(5)

    # 調整亮度
    def brightness(self, r_img):
        value = self.config.get("brightness", 0) / 255
        if value > 0:
            increase_img = r_img.copy()
            increase_img = 255 * (increase_img/255) ** (1 - value)
            return np.array(increase_img, dtype=np.uint8)
        elif value < 0:
            decrease_img = r_img.copy()
            if value == -1:
                decrease_img = 0 * decrease_img
            else:
                decrease_img = 255 * (decrease_img/255) ** (1 + -20 * value)
            return np.array(decrease_img, dtype=np.uint8)
        else:
            return r_img

    # 調整飽和度
    def saturation(self, r_img):
        value = self.config.get("saturation", 0) / 255
        if value != 0:
            value = 9 * value / 255
            img = r_img.astype(np.float32)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            if value != 0:
                img[:, :, 1] *= max((1 + value), 0)
                img[:, :, 1][img[:, :, 1] > 255] = 255
            img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
            return np.array(img, dtype=np.uint8)
        return r_img

    # 調整對比度
    def contrast(self, r_img):
        c = self.config.get("contrast", 0) / 255.0 
        if c != 0:
            k = math.tan((45 + 44 * c) / 180 * math.pi)

            img = (r_img - 127.5) * k + 127.5

            return np.clip(img, 0, 255).astype(np.uint8)
        return r_img

    # 調整紅藍平衡
    def modify_color_temperature(self, r_img):
        blue_blance = 50 * self.config.get("blue-blance", 0) / 255
        red_blance = 50 * self.config.get("red-blance", 0) / 255
        if blue_blance != 0 or red_blance != 0:
            imgB = r_img[:, :, 0] 
            imgG = r_img[:, :, 1]
            imgR = r_img[:, :, 2] 

            bAve = cv2.mean(imgB)[0] - blue_blance + red_blance
            gAve = cv2.mean(imgG)[0] + blue_blance + red_blance
            rAve = cv2.mean(imgR)[0] + blue_blance - red_blance
            aveGray = (int)(bAve + gAve + rAve) / 3

            bCoef = aveGray / bAve
            gCoef = aveGray / gAve
            rCoef = aveGray / rAve
            imgB = np.floor((imgB * bCoef))
            imgG = np.floor((imgG * gCoef))
            imgR = np.floor((imgR * rCoef))

            imgb = imgB
            imgb[imgb > 255] = 255
            
            imgg = imgG
            imgg[imgg > 255] = 255
            
            imgr = imgR
            imgr[imgr > 255] = 255
                
            return np.dstack((imgb, imgg, imgr)).astype(np.uint8)
        return r_img

    # 修正高光
    def highlight(self, r_img):
        value = self.config.get("reduce-highlight", 0)
        if value != 0:
            img_gray = cv2.cvtColor(r_img, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(img_gray, 255 - value, 255, 0)
            contours, _  = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            img_zero = np.zeros(r_img.shape, dtype=np.uint8)

            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                img_zero[y:y+h, x:x+w] = 255
                mask = img_zero

            return cv2.illuminationChange(r_img, mask, alpha=0.2, beta=0.2) 
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
