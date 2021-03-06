# -*- coding: utf-8 -*-
# Rails から渡される ID に紐付いた画像情報を計算し、DB に格納する。

import cv2
import sys
from color_util import ColorUtil
from manager import Manager

if __name__ == '__main__':
    args = sys.argv

    manager = Manager()
    infos = manager.get(id=args[1])[0]
    path = "/home/okabi/Projects/mosaic/web/public/images/{:}".format(infos[1])
    image = cv2.imread(path)
    h, s, v = ColorUtil.mean_hsv(image)
    manager.update_hsv(args[1], h, s, v)
