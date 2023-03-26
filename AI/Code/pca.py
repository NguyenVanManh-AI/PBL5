from sklearn.decomposition import PCA
import numpy as np
# Load dữ liệu Iris
X = np.load("data.npy")
y = ["cuong", "cuong",  "cuong",\
     "nguyen",  "nguyen", "nguyen", "nguyen",\
     "phuc",  "phuc",
     "trinh", "trinh", "trinh", "trinh", "trinh", \
     "luyt", "luyt", "luyt", "luyt", "luyt", "luyt", \
     "chu", "chu", "chu", "chu", "chu", \
     "ban",  \
     "manh", "manh", "manh", "manh", "manh", \
     "duy", "duy", "duy", "duy", "duy", "duy", "duy", "duy", "duy", "duy", "duy",
    ]

print(len(X[0]))

# Khởi tạo PCA với số chiều mới là 70
pca = PCA(n_components=70)


# Áp dụng PCA lên dữ liệu Iris
X_pca = pca.fit_transform(X)

print(len(X_pca[0]))
# In ra số lượng các thành phần chính
print(pca.n_components_)

# In ra tỷ lệ phương sai được giải thích bởi các thành phần chính
# print(pca.explained_variance_ratio_)

# In ra kết quả sau khi áp dụng PCA
# print(X_pca)
