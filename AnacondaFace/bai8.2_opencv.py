import cv2
import face_recognition
import os
import numpy as np

path = "train"
images = []
classnames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    print(cl)
    curImg = cv2.imread(f"{path}/{cl}")
    images.append(curImg)
    classnames.append(os.path.splitext(cl)[0])
    #splitext sẽ tách chuỗi ra làm 2 phần tên và phần mở rộng
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

# Khởi động webcam
cap = cv2.VideoCapture("videotest2s.mp4")
dem = 0
while(True):
    # trả về boolean và khung hình (false , none) hoặc (true, image)
    ret, frame = cap.read()
    if dem < 3:
        dem += 1
        continue
    else:
        dem = 0
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
        else:
            name = "UNKNOW"
        #print ten len frame
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1*2, x2*2, y2*2, x1*2
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
        cv2.putText(frame, name, (x2, y2), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)

    cv2.imshow("Phuc lap trinh", frame)
    if cv2.waitKey(1)==ord("q"): #độ trễ 1/1000s, nếu bấm q sẽ thoát
        break
cap.release() #giai phong camera
cv2.destroyAllWindows() #thoat tat ca cua so


