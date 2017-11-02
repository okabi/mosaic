# -*- coding: utf-8 -*-
import cv2
import numpy as np
from color_util import ColorUtil



if __name__ == '__main__':
    img1 = cv2.imread('test4.jpg')
    l1, a1, b1 = ColorUtil.mean_lab(img1)
    print [l1, a1, b1]

    img2 = cv2.imread('test3.png')
    l2, a2, b2 = ColorUtil.mean_lab(img2)
    print [l2, a2, b2]

    d, dl, da, db = ColorUtil.lab_euclid_distance(l1, a1, b1, l2, a2, b2)
    print [d, dl, da, db]

    revised = ColorUtil.revise(img1, l1, a1, b1, l2, a2, b2)
    cv2.imwrite('output4.png', revised)
