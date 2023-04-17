import face_recognition
import os
import pandas as pd
import math
import cv2
import numpy as np
# from skimage.feature import local_binary_pattern  # # pip install scikit-image
import skimage.feature
# ----------------method HoG for extracting feature vector HoG---------------------------
def hog(image, orientations=8, pixels_per_cell=(8, 8), cells_per_block=(3, 3), visualize=False):
    # Chuyển ảnh sang màu xám
    print("shape before grayscale: ", image.shape)
    if (len(image.shape)==3):
        image = grayscale(image)
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print("shape after grayscale: ", image.shape)

    # Tính độ lớn và hướng của gradient
    gx, gy = gradient(image)

    # Tính độ lớn và hướng của gradient trung bình trong mỗi ô pixel
    magnitude, angle = magnitude_orientation(gx, gy)

    # Tính histogram của hướng gradient trong mỗi ô pixel
    histogram = orientation_histogram(magnitude, angle, orientations, pixels_per_cell, cells_per_block)
    # print(histogram)
    # Tính đặc trưng HOG
    hog_feature = histogram.ravel()
    # print(hog_feature)
    return hog_feature

def grayscale(image):
    print("gray scale")
    # Chuyển ảnh sang màu xám
    return np.dot(image[..., :3], [0.299, 0.587, 0.114])

def gradient(image):
    # Apply a filter to the grayscale image
    # kernel = np.ones((5, 5), np.float32) / 25
    # img_filtered = cv2.filter2D(image, -1, kernel)
    # Tính gradient theo trục x và trục y
    gx = np.gradient(image, axis=1)
    gy = np.gradient(image, axis=0)
    # gx = cv2.Sobel(img_filtered, cv2.CV_32F, 1, 0)
    # gy = cv2.Sobel(img_filtered, cv2.CV_32F, 0, 1)
    # print("gradient image")
    return gx, gy

def magnitude_orientation(gx, gy):
    # Tính độ lớn và hướng của gradient
    magnitude = np.sqrt(gx ** 2 + gy ** 2)
    angle = np.arctan2(gy, gx) * 180 / np.pi
    # print("toa do theo R và góc")
    return magnitude, angle

def orientation_histogram(magnitude, angle, orientations, pixels_per_cell, cells_per_block):
    # Tính histogram của hướng gradient trong mỗi ô pixel
    height, width = magnitude.shape
    cy, cx = pixels_per_cell    # 16 * 16
    nbins = orientations        # 8
    histogram = np.zeros((height // cy, width // cx, nbins))
    # array 64//16   *  64//16    *   8
    # array  4 * 4 * 8
    # print(magnitude)
    # print(angle)
    for y in range(height // cy):   # for y in range(4)
        for x in range(width // cx):    # for x in range(4)
            for i in range(cy):             # for i in range(16)
                for j in range(cx):             # for j in range(16)
                    pixel_y = y * cy + i
                    pixel_x = x * cx + j    # tọa độ pixel trên ảnh 64*64
                    pixel_magnitude = magnitude[pixel_y, pixel_x]  # lấy R
                    pixel_angle = angle[pixel_y, pixel_x]   # lấy góc       # 45
                    orientation = int((pixel_angle * nbins) / 180)          # 35 * 8 / 180 = 2    # 60 * 8 / 180 = 2,66
                    # print(orientation)
                    histogram[y, x, orientation-1] += pixel_magnitude
    # print(histogram)
    # print(np.sum(histogram))
    # Chuẩn hóa các khối ô pixel
    by, bx = cells_per_block    # 1 * 1
    normalized_histogram = np.zeros((height // cy - by + 1, width // cx - bx + 1, by * bx * nbins))
    for y in range(height // cy - by + 1):          # for y in range(64//8 - 3 + 1)     #6
        for x in range(width // cx - bx + 1):           # for x in range(6)
            block = histogram[y:y+by, x:x+bx, :].ravel()    #  his[0:3, 0:3, 0:8]   #72
            normalized_histogram[y, x, :] = block / np.sqrt(np.sum(block ** 2) + 1e-5)
    # print(normalized_histogram)
    return normalized_histogram

# ----------------class LBP for extracting feature vector LBP---------------------------
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

pathTest= "../LBPLearning/CSDLNew/KiemThuNew/"
images = []
classnames = []
myList = os.listdir(pathTest)
print(myList)
for cl in myList:
    print(cl)
    curImg = cv2.imread(f"{pathTest}/{cl}", cv2.IMREAD_GRAYSCALE)
    images.append(curImg)
    str1 = os.path.splitext(cl)[0]
    str1 = str1[:str1.rindex('_')]
    classnames.append(str1)
    #splitext sẽ tách chuỗi ra làm 2 phần tên và phần mở rộng
print(len(images))
print(classnames)

#step encoding
def Mahoa (images):
    LBP_List = []
    for img, index in zip(images, range(len(images))):
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        locationFace = face_recognition.face_locations(img)
        if len(locationFace) != 0:
            y1, x2, y2, x1 = locationFace[0]
            cropped_img = img[y1:y2, x1:x2]
            down_points = (64, 64)

            resize_down = cv2.resize(cropped_img, down_points, interpolation=cv2.INTER_LINEAR)
            cv2.imwrite(f"../LBPLearning/cutImageTest/{myList[index]}", resize_down)
            lbp = LBP()
            out_our = lbp(resize_down)
            # # out_scikit = local_binary_pattern(image=resize_down, P=8, R=1, method='default')q
            print("Scikit output:", out_our)
            cv2.imwrite(f"../LBPLearning/LBPImageTest/{myList[index]}", out_our)

            # đã có LBP_img
            hist, _ = np.histogram(out_our, bins=256)
            # chuan hoa
            hist = np.float32(hist) / np.sum(hist)
            LBP_List.append(hist)
        else:
            classnames.pop(index)
    return LBP_List

#step encoding
def MahoaHoG (images):
    HoG_List = []
    for img, index in zip(images, range(len(images))):
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        locationFace = face_recognition.face_locations(img)
        if len(locationFace) != 0:
            y1, x2, y2, x1 = locationFace[0]
            cropped_img = img[y1:y2, x1:x2]
            down_points = (64, 64)

            resize_down = cv2.resize(cropped_img, down_points, interpolation=cv2.INTER_LINEAR)
            cv2.imwrite(f"../LBPLearning/cutImage/{myList[index]}", resize_down)
            hog_feature = hog(resize_down, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(3, 3))
            # hog_feature = skimage.feature.hog(resize_down, orientations=8, pixels_per_cell=(16, 16),
            #                                   cells_per_block=(3, 3), feature_vector=True)
            HoG_List.append(hog_feature)
        else:
            classnames.pop(index)
    return HoG_List

encodeListKnow = MahoaHoG(images)
print("ma hoa thanh cong")
# print(len(encodeListKnow))

# save encodeListKnow + classnames in file know_face_encode.csv
# Create a DataFrame to store the face encodings
df = pd.DataFrame(encodeListKnow)
dfname = pd.DataFrame(classnames)

# Save the DataFrame to a CSV file
df.to_csv("../LBPLearning/SaveDir/unknow_face_encode.csv", index=False)
dfname.to_csv("../LBPLearning/SaveDir/unknow_face_classnames.csv", index=False)