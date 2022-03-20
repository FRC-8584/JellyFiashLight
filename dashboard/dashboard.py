from flask import Flask, make_response, redirect, render_template, request, url_for, Request
from modules import json
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

class Web_UI():
    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        request_type = request.headers.get("Request-type")
        if request_type != None:
            return deal_requeste(request_type, request.get_data(), request)
        return render_template("index.html")

    def run(
        self,
        host: typing.Optional[str] = None,
        port: typing.Optional[int] = None,
        **options: typing.Any,
    ):
        self.app.run(host=host, port=port, debug=True, use_reloader=False, **options)
