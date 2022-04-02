from flask import Flask, Response, render_template, request, Request, make_response
from modules import json
from camera import Camera
import typing

def deal_requeste(type_of: str, data, raw_requests: Request):
    print(f"Get Request Type:{type_of}")
    try:
        print(f"Data:{data.decode('utf-8')}")
    except:
        print(f"Data:{data}")
    if type_of == "include":
        return render_template(json.loads(data).get("file_name"))
    elif type_of == "request_camera":
        try:
            data = raw_requests.get_json()
            camera_id = int(data.get("camera-id", False))
            if camera_id in range(5):
                data = json.load(f"data/camera_{camera_id}.json")
                response = make_response()
                response.set_data(json.dumps({"camera-id": camera_id, "config": data}))
                return response
        except:
            pass
    elif type_of == "send_camera":
        try:
            data = raw_requests.get_json()
            camera_id = int(data.get("camera-id", False))
            camera_config = data["config"]
            if camera_id in range(5):
                json.dump(f"data/camera_{camera_id}.json", camera_config)
                camera_list[camera_id].load_config()
        except:
            pass
    elif type_of == "request_code":
        try:
            data = raw_requests.get_json()
            camera_id = data.get("camera-id", False)
            if camera_id in range(5):
                response = make_response()
                with open(f"camera/camera_{camera_id}.py", mode="r") as code_file:
                    response.set_data(code_file.read())
                    code_file.close()
                return response
        except:
            pass
    elif type_of == "send_code":
        try:
            data = raw_requests.get_json()
            camera_id = data.get("camera-id", False)
            code = data["code"]
            if camera_id in range(5):
                with open(f"camera/camera_{camera_id}.py", mode="w") as code_file:
                    code_file.write(code)
                    code_file.close()
        except:
            pass
    return ("", 204)

camera_list = []
for i in range(5):
    camera_list.append(Camera(i))

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
        return Response(camera_list[0].output(), mimetype='multipart/x-mixed-replace; boundary=frame')
    @app.route("/camera_1")
    def camera_1_r():
        return Response(camera_list[1].output(), mimetype='multipart/x-mixed-replace; boundary=frame')
    @app.route("/camera_2")
    def camera_2_r():
        return Response(camera_list[2].output(), mimetype='multipart/x-mixed-replace; boundary=frame')
    @app.route("/camera_3")
    def camera_3_r():
        return Response(camera_list[3].output(), mimetype='multipart/x-mixed-replace; boundary=frame')
    @app.route("/camera_4")
    def camera_4_r():
        return Response(camera_list[4].output(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def run(
        self,
        host: typing.Optional[str] = None,
        port: typing.Optional[int] = None,
        **options: typing.Any,
    ):
        self.app.run(host=host, port=port, debug=True, use_reloader=False, **options)
