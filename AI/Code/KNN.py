from sklearn.neighbors import KNeighborsClassifier
import cv2
import face_recognition
import os
import numpy as np

# step 1 load ảnh từ kho ảnh nhận dạng

import cv2
import face_recognition
import os
import pandas as pd
import numpy as np
from datetime import datetime

pathTrain = "image"
y_train =[]
name =[]
err =[]
images = []
myList = os.listdir(pathTrain)
for cl in myList:
    curImg = cv2.imread(f"{pathTrain}/{cl}")
    str1 = os.path.splitext(cl)[0]
    name.append(str1)
    str1 = str1[:str1.index(' (')]
    print(str1)
    y_train.append(str1)
    images.append(curImg)

#step encoding
def Mahoa (images):
    encodeList = []
    count=0
    for img, index in zip(images, range(len(images))):

        print(count)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)
        if len(encode)!=0:
            encode = encode[0]
            encodeList.append(encode)
        else:
            print("err at "+ str(count) + "Name "+name[count])
        count += 1
    return encodeList

# x_load = np.load("rawData.npy")
# #
# x_train = Mahoa(images)
# np.save("rawData.npy",x_train)
# np.save("rawData_label.npy",y_train)


x_train = np.load("HL_new.npy")
y_train = np.load("HL_new_label.npy")

# x_train = np.load('rawData.npy')
print("ma hoa thanh cong")
print(x_train)


# Dữ liệu kiểm tra

path = "Image2"
images = []
classNames = []
myList = os.listdir(path)
print(myList) # ['Donal Trump.jpg', 'elon musk .jpg', 'Joker.jpg', 'tokuda.jpg']
for cl in myList:
    print(cl)
    curImg = cv2.imread(f"{path}/{cl}") # pic2/Donal Trump.jpg
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
    # splitext sẽ tách path ra thành 2 phần, phần trước đuôi mở rộng và phần mở rộng
print(len(images))
print(classNames)
#
# x_test = Mahoa(images)
# np.save("rawData_KT.npy", x_test)

# x_test = np.load("rawData_KT.npy")
x_test = np.load("KT_new.npy")
print(len(x_test))
y_test = np.load("KT_new_label.npy")
print(len(y_test))
# Tạo mô hình KNN với k=3
knn = KNeighborsClassifier(n_neighbors=3)

# Huấn luyện mô hình
knn.fit(x_train, y_train)

# Phân loại dữ liệu kiểm tra
predictions = knn.predict(x_test)

# In kết quả phân loại
print(predictions)

count = 0
for guess, correct in zip(predictions, y_test ):
    guess = guess[guess.index('_'):]
    correct = correct[correct.index('_'):]
    count += 1 if guess.upper()==correct.upper() else 0

print("hieu suat: ", count/len(y_test)*100, "%")




