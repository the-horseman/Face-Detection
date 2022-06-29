from flask import Flask, render_template, jsonify, request
import cv2
import base64
from mtcnn_cv2 import MTCNN
import numpy as np
import tensorflow-cpu as tf

app = Flask(__name__)
cnn = tf.keras.models.load_model("static/FaceModel.h5")

@app.route("/")
def start():
    return render_template("index.html")

def cleanImg(frame=None):
    frame = cv2.resize(frame, (200, 200),
                       interpolation=cv2.INTER_NEAREST)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 1)
    th3 = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 2)
    _, res = cv2.threshold(
        th3, 70, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    print(np.shape(res))
    return res

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

        img, ans = ProcImage(img)
        string = base64.b64encode(cv2.imencode('.png', img)[1]).decode()
        dict['img'] = string
        dict['name'] = ans
    return jsonify(dict)


def ProcImage(frame):
    ls1 = ["Amaan", "Aryan", "Aviral", "Himanshu", "Kanika", "Kaustav", "Raja", "Rishika", "Shanky", "Tanishka", "Vijit", "None"]
    val = 11
    detector = MTCNN()
    ele = []
    ext = detector.detect_faces(frame)
    for i in ext:
        v = i["box"]
        ele.append(frame[v[1]:v[1]+v[3], v[0]:v[0]+v[2]])
        cv2.rectangle(frame, (v[0], v[1]), (v[0]+v[2],
                      v[1] + v[3]), (0, 155, 255), 4)
    for i in ext:
        v = i["box"]
    for i in ele:
        # img = cv2.resize(i, (200, 200))
        # cv2.imwrite("ext2.jpg", img)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # cv2.imwrite("ext.jpg", img)
        img = cleanImg(i)
        img = np.expand_dims(img, axis=0)
        result = cnn.predict(img)
        val = result[0].argmax()
        print(result)
        print(ls1[val])
    return (frame,ls1[val])


if __name__ == "__main__":
    app.run()
