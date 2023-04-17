import face_recognition
import numpy as np
from datetime import datetime
import pandas as pd

# read encodeListKnow + classnames
df = pd.read_csv('../LBPLearning/SaveDir/know_face_encode.csv')
encodeListKnow = list(np.array(df))
dfname = pd.read_csv('../LBPLearning/SaveDir/know_face_classnames.csv')
classnames = list(map( lambda x: x[0],  list(np.array(dfname))))
# print(encodeListKnow)
print(classnames)
# read encodeListUnKnow + classnames
dfUnknow = pd.read_csv('../LBPLearning/SaveDir/unknow_face_encode.csv')
encodeListUnknow = list(np.array(dfUnknow))
dfnameCorrect = pd.read_csv('../LBPLearning/SaveDir/unknow_face_classnames.csv')
classnamesCorrect = list(map( lambda x: x[0],  list(np.array(dfnameCorrect))))
print(classnamesCorrect)

def thamdu(name):
    with open("../LBPLearning/SaveDir/thamdu.csv", "r+") as f:
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
            with open("../LBPLearning/SaveDir/thamdu.csv", "w") as f1:
                for name1, time in zip(nameList, timeList):
                    f1.writelines(f"{name1},{time}")

names = np.unique(classnames)
print(names)
dict_name_index = {}
for name in names:
    indexs = [vt for vt in range(len(classnames)) if classnames[vt]==name]
    dict_name_index[name] = indexs

print(dict_name_index)

encodeListKnowNew = []
feature_means = {}
for name in names:
    encodes = [encodeListKnow[i] for i in dict_name_index[name]]
    feature_data = [[float(i) for i in row] for row in encodes]
    encodeListKnowNew.append(np.mean(feature_data, axis=0))

print(encodeListKnowNew)

classnames_guess = []

for encodeFaceNotKnow in encodeListUnknow:
    # matches = face_recognition.compare_faces(encodeListKnow, encodeFaceNotKnow)
    # print(matches)
    # faceDis = face_recognition.face_distance(encodeListKnow, encodeFaceNotKnow)
    faceDis = face_recognition.face_distance(encodeListKnowNew, encodeFaceNotKnow)
    print(faceDis)
    matchIndex = np.argmin(faceDis)
    if faceDis[matchIndex] < 1.85:
        print(matchIndex)
        name = names[matchIndex].upper()
        # name = classnames[matchIndex].upper()
        thamdu(name)
    else:
        name = "UNKNOW"
    classnames_guess.append(name)

dfname_guess = pd.DataFrame(classnames_guess)

# Save the DataFrame to a CSV file
dfname_guess.to_csv("../LBPLearning/SaveDir/unknow_classnames_guess.csv", index=False)

# calc hiệu suất của thuật toán
exactly = 0
for correct, guess in zip(classnamesCorrect, classnames_guess):
    print(correct, guess)
    if guess!='UNKNOW':
        guess = guess[guess.index('_'):]
    correct = correct[correct.index('_'):]
    exactly += 1 if guess.upper()==correct.upper() else 0
efficiency = exactly/len(classnamesCorrect) *100
print("efficiency: ", efficiency, "%")