import math
import cv2
import numpy as np
from skimage.feature import local_binary_pattern  # # pip install scikit-image

KERNEL_WIDTH = 7
KERNEL_HEIGHT = 7
SIGMA_X = 3
SIGMA_Y = 3


def main():
    img = cv2.imread('girl_xinh.jpg', cv2.IMREAD_GRAYSCALE)

    # LBP
    out = local_binary_pattern(image=img, P=8, R=1, method='default')
    cv2.imwrite('lbp.jpg', out)
    print("Saved image @ lbp.jpg")

    # Gaussian blur + LBP
    blur_img = cv2.GaussianBlur(img, ksize=(KERNEL_WIDTH, KERNEL_HEIGHT), sigmaX=SIGMA_X, sigmaY=SIGMA_Y)
    down_points = (64, 64)

    resize_down = cv2.resize(blur_img, down_points, interpolation=cv2.INTER_LINEAR)
    blur_out = local_binary_pattern(image=resize_down, P=8, R=1, method='default')
    cv2.imwrite('blur.jpg', blur_img)
    cv2.imwrite('blur_lbp.jpg', blur_out)
    print("Saved image @ blur.jpg")
    print("Saved image @ blur_lbp.jpg")


if __name__ == "__main__":
    main()
    print('---------')
    print('* Follow me @ ' + "\x1b[1;%dm" % (34) + ' https://www.facebook.com/kyznano/' + "\x1b[0m")
    print('* Minh fanpage @ ' + "\x1b[1;%dm" % (34) + ' https://www.facebook.com/minhng.info/' + "\x1b[0m")
    print('* Join GVGroup @ ' + "\x1b[1;%dm" % (34) + 'https://www.facebook.com/groups/ip.gvgroup/' + "\x1b[0m")
    print('* Thank you ^^~')