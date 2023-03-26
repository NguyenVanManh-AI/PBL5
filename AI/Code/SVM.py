from sklearn import svm
import numpy as np

# X_train = np.load("rawData.npy")
# X_test = np.load("rawData_KT.npy")
# y_train = np.load("rawData_label.npy")

X_test = np.load("KT_new.npy")
y_train = np.load("HL_new_label.npy")
X_train = np.load("HL_new.npy")
y_test = np.load("KT_new_label.npy")
# Create and train SVM model
clf = svm.SVC(kernel='linear')
clf.fit(X_train, y_train)

# Predict test data
y_pred = clf.predict(X_test)
print(y_pred)

count = 0
for guess, correct in zip(y_pred, y_test ):
    guess = guess[guess.index('_'):]
    correct = correct[correct.index('_'):]
    count += 1 if guess.upper()==correct.upper() else 0

print("hieu suat: ", count/len(y_test)*100, "%")