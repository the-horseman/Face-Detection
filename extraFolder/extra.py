import base64
import json
import cv2

img = cv2.imread('test.jpg')
string = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
dict = {
    'img': string
}
with open('js.json', 'w') as outfile:
    json.dump(dict, outfile, ensure_ascii=False, indent=4)
