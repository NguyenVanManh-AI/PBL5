import cv2

# Load ảnh grayscale
img = cv2.imread('girl_xinh.jpg', cv2.IMREAD_GRAYSCALE)

# # Loại bỏ nhiễu bằng phương pháp Gaussian Blur
# img_blur = cv2.GaussianBlur(img, (5, 5), 0)
# # Loại bỏ nhiễu bằng phương pháp Median Blur
# img_blur = cv2.medianBlur(img, 5)
# Loại bỏ nhiễu bằng phương pháp Bilateral Filtering
img_blur = cv2.bilateralFilter(img, 9, 75, 75)

# Hiển thị ảnh gốc và ảnh sau khi loại bỏ nhiễu
cv2.imshow('Original Image', img)
cv2.imshow('Blur Image', img_blur)
cv2.waitKey(0)
cv2.destroyAllWindows()