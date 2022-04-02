import base64
import json
import cv2
import numpy as np

response = json.loads(open('js.json', 'r').read())
string = response['img']
data:image/jpg;base64,