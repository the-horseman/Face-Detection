import numpy as np
import cv2
import os


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

path = "D:\\Face-Data"
new_path = "D:\\Proc-Face-Data"
dirs = os.listdir(path)
for i in dirs:
    cur_dir = path + "\\" + i
    fle = os.listdir(cur_dir)
    for j in fle:
        cur_fle = cur_dir + "\\" + j
        new_fle = new_path + "\\" + i + "\\" + j
        old_img = cv2.imread(cur_fle)
        new_img = cleanImg(old_img)
        print(new_fle)
        cv2.imwrite(new_fle, new_img)

        