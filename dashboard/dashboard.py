from flask import Flask, url_for, render_template

class Web_UI():
    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        return render_template("index.html")

if __name__ == "__main__":
    web = Web_UI()
    web.app.run("0.0.0.0")