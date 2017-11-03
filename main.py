# -*- coding: utf-8 -*-
import cv2
import numpy as np
from color_util import ColorUtil
from generator import Generator
from manager import Manager

if __name__ == '__main__':
    db = 'images.sqlite3'
    elem_list = ['test1.jpg', 'test2.jpg', 'test3.png', 'test4.jpg']
    target_img = cv2.imread('mario2.png')

    manager = Manager(db)
    manager.danger_drop()
    manager = Manager(db)

    for e in elem_list:
        img = cv2.imread(e)
        manager.add(img, e, 0)

    generator = Generator()
    generator.load(manager, 'output.png')
    generator.generate(target_img, (2, 2), (20, 20))
