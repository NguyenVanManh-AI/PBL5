import cv2
import face_recognition
import os
import pandas as pd
import numpy as np
from datetime import datetime

pathCheck = "KT_new"
images = []
classnames = []
myList = os.listdir(pathCheck)
print(myList)
for cl in myList:
    print(cl)
    curImg = cv2.imread(f"{pathCheck}/{cl}")
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
    count=0
    for img in images:
        print(count)
        count += 1
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)
        if len(encode)!=0:
            encode = encode[0]
        else:
            encode = np.zeros(128)
        encodeList.append(encode)
    return encodeList

encodeListKnow = Mahoa(images)
print("ma hoa thanh cong")
print(len(encodeListKnow))
np.save("KT_new.npy" , encodeListKnow)
np.save("KT_new_label.npy" , classnames)

# save encodeListKnow + classnames in file know_face_encode.csv
# Create a DataFrame to store the face encodings
# df = pd.DataFrame(encodeListKnow)
# dfname = pd.DataFrame(classnames)

# Save the DataFrame to a CSV file
# df.to_csv("SaveDir/not_know_face_encode.csv", index=False)
# dfname.to_csv("SaveDir/not_know_classnames_correct.csv", index=False)