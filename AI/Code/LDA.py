from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import numpy as np
import pandas as pd

# read encodeListKnow + classnames
dfKnow = pd.read_csv('SaveDir/know_face_encode.csv')
encodeListKnow = list(np.array(dfKnow))
dfname = pd.read_csv('SaveDir/know_face_classnames.csv')
classnames = list(map( lambda x: x[0],  list(np.array(dfname))))
print(classnames)
# read encodeListUnKnow + classnames
dfUnknow = pd.read_csv('SaveDir/not_know_face_encode.csv')
encodeListUnknow = list(np.array(dfUnknow))
dfnameCorrect = pd.read_csv('SaveDir/not_know_classnames_correct.csv')
classnamesCorrect = list(map( lambda x: x[0],  list(np.array(dfnameCorrect))))
print(classnamesCorrect)


# Các vector đặc trưng của các khuôn mặt đã biết
known_faces = np.array(encodeListKnow)

# Nhãn của các khuôn mặt đã biết
known_labels = np.array(classnames)

# Các vector đặc trưng của các khuôn mặt chưa biết
unknown_faces = np.array(encodeListUnknow)

# Khởi tạo mô hình LDA
lda = LinearDiscriminantAnalysis()

# Huấn luyện mô hình LDA với các vector đặc trưng đã biết và nhãn tương ứng
lda.fit(known_faces, known_labels)

# Dự đoán nhãn của các khuôn mặt chưa biết bằng cách sử dụng mô hình LDA đã huấn luyện
predicted_labels = lda.predict(unknown_faces)

# Save guess classnames
dfnameGuess = pd.DataFrame(predicted_labels)
dfnameGuess.to_csv("SaveDir/not_know_classnames_guess.csv", index=False)

# In ra các nhãn được dự đoán
print("guess:", predicted_labels)
# In ra các nhãn được chính xác
print("correct:", classnamesCorrect)

# Tinh hieu suat
count = 0
for guess, correct in zip(predicted_labels, classnamesCorrect):
    guess = guess[guess.index('_'):]
    correct = correct[correct.index('_'):]
    count += 1 if guess.upper()==correct.upper() else 0

print("hieu suat: ", count/len(classnamesCorrect)*100, "%")