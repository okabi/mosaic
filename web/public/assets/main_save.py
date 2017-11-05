# -*- coding: utf-8 -*-
# Rails から渡される ID に紐付いた画像情報を計算し、DB に格納する。

import cv2
import sys
from color_util import ColorUtil
from manager import Manager

if __name__ == '__main__':
    db = 'web/db/production.sqlite3'
    args = sys.argv

    manager = Manager(db)
    infos = manager.get(id=args[1])
    path = "web/public/images/{:}".format(infos[1])
    h, s, v = ColorUtil.mean_hsv(cv2.imread(path))
    manager.update_hsv(args[1], h, s, v)
