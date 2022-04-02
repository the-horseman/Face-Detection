import cv2
from mtcnn_cv2 import MTCNN

detector = MTCNN()
cap = cv2.VideoCapture(0)
cnt = 0
limit = 150
flag = 0
val = 1
text = "Press to start"
while(cap.isOpened()):
    ret, frame = cap.read()
    if cnt == limit or ret == False:
        break
    frame = cv2.flip(frame, 1)
    cv2.putText(frame, text, (30,30), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0))
    ele = []
    ext = detector.detect_faces(frame)
    for i in ext:
        v = i["box"]
        ele.append(frame[v[1]-5:v[1]+v[3]+10, v[0]-5:v[0]+v[2]+10])
    
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        text = "Started"
        flag = 1
    if cv2.waitKey(1) & 0xFF == ord('p'):
        break
    if flag == 1:
        for j in ele:
            print(j)
            cv2.imwrite('Aryan-'+str(cnt)+'.jpg', j)
            cnt += 1

cap.release()
cv2.destroyAllWindows()
