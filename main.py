# -*- coding: utf-8 -*-
# Rails から渡される ID に紐付いたターゲットのモザイクアートを作る。
import cv2
import sqlite3
import sys
import traceback
import numpy as np
from color_util import ColorUtil
from generator import Generator
from manager import Manager

if __name__ == '__main__':
    try:
        db = '/home/okabi/Projects/mosaic/web/db/production.sqlite3'
        args = sys.argv
        conn = sqlite3.connect(db)
        infos = [x for x in conn.execute(""" select * from targets where id = ? """, (args[1],))]
        t = infos[0][1]
        conn.close()

        path = "/home/okabi/Projects/mosaic/web/public/targets/{:}".format(t)
        target_img = cv2.imread(path)

        manager = Manager()
        generator = Generator()
        generator.load(manager, '/home/okabi/Projects/mosaic/web/public/output.jpg')
        generator.generate(target_img, (1, 1), (10, 10))
    except:
        print traceback.format_exc()
        print 'end'
