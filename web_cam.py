from flask import Flask, Response, url_for
from threading import Thread
from time import sleep
import cv2
from simplejpeg import encode_jpeg

app = Flask(__name__)
camera = cv2.VideoCapture(0)

new_frame = ""
def camara_thread_job():
    global new_frame
    while True:
        success, frame = camera.read()
        try:
            if not success:
                break
            else:
                # _, buffer = cv2.imencode('.jpg', frame.copy())
                # new_frame = buffer.tobytes()
                cv2.BGR
                new_frame = encode_jpeg(frame.copy(), colorspace="bgr")
        except:
            pass

camara_thread = Thread(target=camara_thread_job)
camara_thread.start()

def gen_frames():
    while True:
        yield (b'--frame\r\nContent-Type:image/jpeg\r\nContent-Length: ' + f"{len(new_frame)}".encode() + b'\r\n\r\n' + new_frame + b'\r\n')
        sleep(1/80)

@app.route('/')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001)