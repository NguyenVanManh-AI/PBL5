import cv2
import numpy as np
import face_recognition
import math
from skimage.feature import local_binary_pattern  # # pip install scikit-image
import skimage.feature          # Hog

class LBP(object):
    def __init__(self, radius=1, npoints=8, counter_clockwise=True, interpolation="bilinear"):
        self.radius = radius
        self.npoints = npoints
        self.interpolation = interpolation
        self.counter_clockwise = counter_clockwise
        assert self.radius > 0 and self.npoints > 0
        assert interpolation in ("bilinear", "nearest")
        self.get_pixel_func = self._get_pixel_nearest if self.interpolation == "nearest" else self._get_pixel_bilinear

        start_angle_radian = 0
        angle_radian = 2 * math.pi / npoints
        circle_direction = 1 if counter_clockwise else -1
        neighbor_positions = []
        for pos in range(self.npoints):
            # traverse on angles: 0, -1*angle_radian, -2*angle_radian, ...
            delta_x = math.cos(start_angle_radian + circle_direction * pos * angle_radian) * self.radius
            delta_y = -(math.sin(start_angle_radian + circle_direction * pos * angle_radian) * self.radius)
            neighbor_positions.append((delta_x, delta_y))
        neighbor_positions.reverse()
        self.neighbor_positions = neighbor_positions  # [(0.7071067811865474, 0.7071067811865477), (-1.8369701987210297e-16, 1.0), (-0.7071067811865477, 0.7071067811865475), (-1.0, -1.2246467991473532e-16), (-0.7071067811865475, -0.7071067811865476), (6.123233995736766e-17, -1.0), (0.7071067811865476, -0.7071067811865475), (1.0, -0.0)]
        assert len(self.neighbor_positions) == npoints
        pass

    def _get_pixel_nearest(self, image, x, y, w, h):
        xx = round(x)
        yy = round(y)
        if xx < 0 or yy < 0 or xx >= w or yy >= h:
            return 0
        else:
            return image[yy, xx]

    def _get_pixel_bilinear(self, image, x, y, w, h):
        """
            x: float. Eg: 0.3
            y: float. Eg: 0.7
        """
        xmin, xmax = math.floor(x), math.ceil(x)  # 0, 1
        ymin, ymax = math.floor(y), math.ceil(y)  # 0, 1

        intensity_top_left = 0 if xmin < 0 or ymin < 0 or xmin >= w or ymin >= h else image[ymin, xmin]
        intensity_top_right = 0 if xmax < 0 or ymin < 0 or xmax >= w or ymin >= h else image[ymin, xmax]
        intensity_bottom_left = 0 if xmin < 0 or ymax < 0 or xmin >= w or ymax >= h else image[ymax, xmin]
        intensity_bottom_right = 0 if xmax < 0 or ymax < 0 or xmax >= w or ymax >= h else image[ymax, xmax]

        weight_x = x - xmin
        weight_y = y - ymin

        intensity_at_top = (1 - weight_x) * intensity_top_left + weight_x * intensity_top_right
        intensity_at_bottom = (1 - weight_x) * intensity_bottom_left + weight_x * intensity_bottom_right

        final_intensity = (1 - weight_y) * intensity_at_top + weight_y * intensity_at_bottom
        return final_intensity

    def __call__(self, image):
        assert len(image.shape) == 2
        h, w = image.shape
        result = np.zeros([h, w])
        for y in range(h):
            for x in range(w):
                center_intensity = image[y, x]
                binary_vector = [0] * self.npoints  # [0, 0, 0, 0, 0, 0, 0, 0]
                for npos in range(self.npoints):
                    new_x = x + self.neighbor_positions[npos][0]
                    new_y = y + self.neighbor_positions[npos][1]

                    neighbor_intensity = self.get_pixel_func(image, new_x, new_y, w, h)

                    if center_intensity <= neighbor_intensity:
                        binary_vector[npos] = 1
                binary_str = "".join([str(e) for e in binary_vector])  # '00001001'
                decimal_value = int(binary_str, 2)  # convert binary string to decimal
                result[y, x] = decimal_value
        return result

img = cv2.imread(f"CSDLNew/HuanLuyenNew/HL_Tung_ (9).JPG", cv2.IMREAD_GRAYSCALE)
locationFace = face_recognition.face_locations(img)

y1, x2, y2, x1 = locationFace[0]
cropped_img = img[y1:y2, x1:x2]
down_points = (64, 64)

resize_down = cv2.resize(cropped_img, down_points, interpolation=cv2.INTER_LINEAR)

# # Load ảnh grayscale
# img = cv2.imread('cutImage/HL_Cuong_ (15).JPG', cv2.IMREAD_GRAYSCALE)


# # Loại bỏ nhiễu bằng phương pháp Gaussian Blur
# img_blur = cv2.GaussianBlur(img, (5, 5), 0)
# Loại bỏ nhiễu bằng phương pháp Median Blur
# img_blur = cv2.medianBlur(img, 5)
# Loại bỏ nhiễu bằng phương pháp Bilateral Filtering
img_blur = cv2.bilateralFilter(resize_down, 9, 75, 75)

# Chuẩn hóa dữ liệu
img_normalized = cv2.normalize(img_blur, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

# Hiển thị ảnh gốc, ảnh sau khi loại bỏ nhiễu và ảnh đã được chuẩn hóa
cv2.imshow('Original Image', img)
cv2.imwrite('anhOriginal.jpg', img)
cv2.imshow('Cropped Image', cropped_img)
cv2.imwrite('anhCropped.jpg', cropped_img)
cv2.imshow('Resized Image', resize_down)
cv2.imwrite('anhResized.jpg', resize_down)
cv2.imshow('Blur Image', img_blur)
cv2.imwrite('anhBlur.jpg', img_blur)
cv2.imshow('Normalized Image', img_normalized)
cv2.imwrite('anhNormalized.jpg', img_normalized)

# out_scikit = local_binary_pattern(image=img_normalized, P=8, R=1, method='default')
# cv2.imshow('LBP Lib Image', out_scikit)
# cv2.imwrite('anhLBPLib.jpg', out_scikit)
# lbp = LBP()
# out_our = lbp(img_normalized)
# cv2.imshow('my LBP Image', out_our)
# cv2.imwrite('anhLBPMy.jpg', out_our)

hog_feature = skimage.feature.hog(img_normalized, orientations=8, pixels_per_cell=(16, 16),
                                              cells_per_block=(1, 1), feature_vector=True)
out_scikit = local_binary_pattern(image=img_normalized, P=8, R=1, method='default')
cv2.imshow('LBP Lib Image', out_scikit)
cv2.imwrite('anhLBPLib.jpg', out_scikit)
lbp = LBP()
out_our = lbp(img_normalized)
cv2.imshow('my LBP Image', out_our)
cv2.imwrite('anhLBPMy.jpg', out_our)

cv2.waitKey(0)
cv2.destroyAllWindows()


