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
            camera_id = int(data.get("camera-id", -1))
            config_id = int(data.get("config-id", -1))
            if camera_id in range(5) and config_id in range(10):
                origin_data = json.load(f"data/camera_{camera_id}.json")
                origin_data["config_id"] = config_id
                json.dump(f"data/camera_{camera_id}.json", origin_data)

                response = make_response()
                response.set_data(
                    json.dumps(
                        {
                            "camera-id": camera_id,
                            "config": origin_data["config_list"][config_id]
                        }
                    )
                )

                camera_list[camera_id].reload()
                camera_list[camera_id].load_config()

                return response
        except:
            pass
    
    elif type_of == "send_camera":
        try:
            data = raw_requests.get_json()
            camera_id = int(data.get("camera-id", -1))
            config_id = int(data.get("config-id", -1))
            if camera_id in range(5) and config_id in range(10):
                origin_data = json.load(f"data/camera_{camera_id}.json")
                origin_data["config_id"] = config_id
                origin_data["config_list"][config_id] = data["config"]
                json.dump(f"data/camera_{camera_id}.json", origin_data)

                camera_list[camera_id].reload()
                camera_list[camera_id].load_config()
        except:
            pass

    elif type_of == "request_code":
        try:
            data = raw_requests.get_json()
            camera_id = int(data.get("camera-id", -1))
            config_id = int(data.get("config-id", -1))
            if camera_id in range(5) and config_id in range(10):
                origin_data = json.load(f"data/camera_{camera_id}.json")
                origin_data["config_id"] = config_id
                json.dump(f"data/camera_{camera_id}.json", origin_data)

                response = make_response()
                with open(f"camera/camera_{camera_id}/config_{config_id}.py") as code_file:
                    response.set_data(
                        json.dumps(
                            {
                                "code": code_file.read(),
                                "enable": origin_data["config_list"][config_id]["code"]
                            }
                        )
                    )
                    code_file.close()

                camera_list[camera_id].reload()
                camera_list[camera_id].load_config()

                return response
        except:
            pass
    
    elif type_of == "send_code":
        try:
            data = raw_requests.get_json()
            camera_id = int(data.get("camera-id", -1))
            config_id = int(data.get("config-id", -1))
            if camera_id in range(5) and config_id in range(10):
                code = data["code"]
                enable = data["enable"]
                with open(f"camera/camera_{camera_id}/config_{config_id}.py", mode="w") as code_file:
                    code_file.write(code)
                    code_file.close()

                origin_data = json.load(f"data/camera_{camera_id}.json")
                origin_data["config_id"] = config_id
                origin_data["config_list"][config_id]["code"] = enable
                json.dump(f"data/camera_{camera_id}.json", origin_data)

                camera_list[camera_id].reload()
                camera_list[camera_id].load_config()
        except:
            pass
    return ("", 204)

camera_list = []
for i in range(5):
    camera_list.append(Camera(i))

class Web_UI():
    app = Flask(__name__)

    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

    @app.route('/', methods=['GET', 'POST'])
    def index():
        request_type = request.headers.get("Request-type")
        if request_type != None:
            response = deal_requeste(request_type, request.get_data(), request)
            try:
                print("Response:" + response.data)
            except:
                pass
            return response
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
        self.app.run(host=host, port=port, debug=True, use_reloader=False, threaded=True, **options)
