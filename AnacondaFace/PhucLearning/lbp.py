import math
import cv2
import numpy as np
from skimage.feature import local_binary_pattern  # # pip install scikit-image


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


def main():
    pattern = np.array([
        [234, 34, 67, 93, 165, 256, 96, 32],
        [74, 32, 1, 56, 93, 20, 200, 93, ],
        [72, 145, 83, 94, 145, 241, 176, 82],
        [94, 83, 135, 185, 252, 187, 33, 58],
        [99, 76, 92, 32, 56, 128, 194, 92],
        [232, 155, 222, 94, 22, 185, 25, 65],
        [87, 24, 43, 129, 32, 39, 74, 91],
        [243, 97, 215, 36, 184, 92, 4, 9],
    ])
    out_scikit = local_binary_pattern(image=pattern, P=8, R=1, method='default')
    print("Scikit output:", out_scikit)

    lbp = LBP()
    out_our = lbp(pattern)
    print("Our output:", out_our)
    print("Same output:", (out_our == out_scikit).all())


if __name__ == "__main__":
    main()
    print('---------')
    print('* Follow me @ ' + "\x1b[1;%dm" % (34) + ' https://www.facebook.com/kyznano/' + "\x1b[0m")
    print('* Minh fanpage @ ' + "\x1b[1;%dm" % (34) + ' https://www.facebook.com/minhng.info/' + "\x1b[0m")
    print('* Join GVGroup @ ' + "\x1b[1;%dm" % (34) + 'https://www.facebook.com/groups/ip.gvgroup/' + "\x1b[0m")
    print('* Thank you ^^~')