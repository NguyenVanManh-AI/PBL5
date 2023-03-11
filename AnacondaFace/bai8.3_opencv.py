import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime

path = r"C:\Users\ADMIN\Downloads\PBL5\AnacondaFace\train"
images = []
classnames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(os.path.join(path, cl))
    if curImg is not None:
        images.append(curImg)
        classnames.append(os.path.splitext(cl)[0])
print(len(images))
print(classnames)

#step encoding
def Mahoa (images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnow = Mahoa(images)
print("ma hoa thanh cong")
print(len(encodeListKnow))

def thamdu(name):
    with open(r"C:\Users\ADMIN\Downloads\PBL5\AnacondaFace\thamdu.csv","a+") as f:
        myDatalist = f.readlines()
        nameList = []
        timeList = []
        for line in myDatalist:
            entry = line.split(",")
            nameList.append(entry[0])
            timeList.append(entry[1])

        if name not in nameList:
            now = datetime.now()
            dtstring = now.strftime("%H:%M:%S")
            f.writelines(f"\n{name},{dtstring}")
        else:
            # thay doi thoi gian truoc do thanh thoi gian sau
            indexSearch = nameList.index(name)
            timeList[indexSearch] = datetime.now().strftime("%H:%M:%S")
            if indexSearch != len(timeList)-1:
                timeList[indexSearch] += "\n"
            with open(r"C:\Users\ADMIN\Downloads\PBL5\AnacondaFace\thamdu.csv", "w", encoding="utf-8") as f1:
                for name1, time in zip(nameList, timeList):
                    f1.writelines(f"{name1},{time}")

# Khởi động webcam
# cap = cv2.VideoCapture("videotest2s.mp4")
cap = cv2.VideoCapture(0)
dem = 0

while(True):
    # trả về boolean và khung hình (false , none) hoặc (true, image)
    ret, frame = cap.read()
    # if dem < 3:
    #     dem += 1
    #     continue
    # else:
    #     dem = 0
    framS = cv2.resize(frame, (0, 0), None, fx=0.5, fy=0.5)
    framS = cv2.cvtColor(framS, cv2.COLOR_BGR2RGB)

    facecurFrame = face_recognition.face_locations(framS) #danh sach cac khuon mat tren khung hinh hien tai
    encodecurFrame = face_recognition.face_encodings(framS)

    for encodeFace, faceLoc in zip(encodecurFrame, facecurFrame):
        matches = face_recognition.compare_faces(encodeListKnow, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnow, encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)
        if faceDis[matchIndex]<0.50 :
            name = classnames[matchIndex].upper()
            thamdu(name)
        else:
            name = "UNKNOW"
        #print ten len frame
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1*2, x2*2, y2*2, x1*2
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
        cv2.putText(frame, name, (x2, y2), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)

    cv2.imshow("Face detection - PBL5", frame)
    if cv2.waitKey(1)==ord("q"): #độ trễ 1/1000s, nếu bấm q sẽ thoát
        break
cap.release() #giai phong camera
cv2.destroyAllWindows() #thoat tat ca cua so


