import cv2
import face_recognition
import os
import pandas as pd
import numpy as np
from datetime import datetime

pathTrain = "HL_new"
images = []
classnames = []
myList = os.listdir(pathTrain)
print(myList)
for cl in myList:
    print(cl)
    curImg = cv2.imread(f"{pathTrain}/{cl}")
    images.append(curImg)
    str1 = os.path.splitext(cl)[0]
    str1 = str1[:str1.rindex('_')]
    classnames.append(str1)
    #splitext sẽ tách chuỗi ra làm 2 phần tên và phần mở rộng
print(len(images))
print(classnames)

#step encoding
def Mahoa (images):
    encodeList = []
    count = 0
    for img, index in zip(images, range(len(images))):
        print(count)
        count+=1
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)
        if len(encode)!=0:
            encode = encode[0]
            encodeList.append(encode)
        else:
            classnames.pop(index)
    return encodeList

encodeListKnow = Mahoa(images)

print("ma hoa thanh cong")
np.save("HL_new.npy" , encodeListKnow)
np.save("HL_new_label.npy" , classnames)


print(len(encodeListKnow))

# save encodeListKnow + classnames in file know_face_encode.csv
# Create a DataFrame to store the face encodings
# df = pd.DataFrame(encodeListKnow)
# dfname = pd.DataFrame(classnames)

# Save the DataFrame to a CSV file
# df.to_csv("SaveDir/know_face_encode.csv", index=False)
# dfname.to_csv("SaveDir/know_face_classnames.csv", index=False)