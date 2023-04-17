import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Load dữ liệu iris
iris = datasets.load_iris()
X = iris.data
y = iris.target

# Chia tập dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print('y_train = ', y_train)
y_unique = np.unique(y_train)
print(y_unique)

# Khởi tạo mô hình SVM với kernel là linear
clf = SVC(kernel='linear', C=1)

# Huấn luyện mô hình với tập huấn luyện
clf.fit(X_train, y_train)
# Dự đoán nhãn của các điểm dữ liệu trong tập kiểm tra
y_pred = clf.predict(X_test)

# Lấy giá trị số liệu thực thể của các điểm dữ liệu trong tập kiểm tra
confidence_scores = clf.decision_function(X_test)

# In kết quả dự đoán và giá trị số liệu thực thể của mô hình
for i in range(len(X_test)):
    print("Dự đoán: ", y_pred[i], " - Giá trị số liệu thực thể: ", confidence_scores[i])

# Tính độ chính xác của mô hình
accuracy = accuracy_score(y_test, y_pred)
print("Độ chính xác của mô hình: ", accuracy)