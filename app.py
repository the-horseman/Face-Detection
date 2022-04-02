from flask import Flask, render_template, jsonify, request
import cv2
import base64
from mtcnn_cv2 import MTCNN
import numpy as np

app = Flask(__name__)


@app.route("/")
def start():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def ImgData():
    dict = {}
    if request.method == "POST":
        all_data = request.get_json(force=True)
        data_url = str(all_data["image"])

        # Decoding the base64 image to cv image
        data_url = data_url.replace("data:image/png;base64,", "")
        png_original = base64.b64decode(data_url)
        png_as_np = np.frombuffer(png_original, dtype=np.uint8)
        img = cv2.imdecode(png_as_np, flags=1)
        # Decoded the imgae

        img = ProcImage(img)
        string = base64.b64encode(cv2.imencode('.png', img)[1]).decode()
        dict['img'] = string
    return jsonify(dict)


def ProcImage(image):
    return image


if __name__ == "__main__":
    app.run()
