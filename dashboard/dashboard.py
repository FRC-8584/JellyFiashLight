from flask import Flask, Response, render_template, request, Request
from modules import json
from camera import Camera
import typing

def deal_requeste(type_of: str, data: str | bytes, raw_requests: Request):
    print(f"Get Request Type:{type_of}")
    try:
        print(f"Data:{data.decode('utf-8')}")
    except:
        print(f"Data:{data}")
    if type_of == "include":
        return render_template(json.loads(data).get("file_name"))
    return ("", 204)

camera_0 = Camera(0)

class Web_UI():
    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        request_type = request.headers.get("Request-type")
        if request_type != None:
            return deal_requeste(request_type, request.get_data(), request)
        return render_template("index.html")

    @app.route("/camera_0")
    def camera_0_r():
        return Response(camera_0.output(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def run(
        self,
        host: typing.Optional[str] = None,
        port: typing.Optional[int] = None,
        **options: typing.Any,
    ):
        self.app.run(host=host, port=port, debug=True, use_reloader=False, **options)
