# -*- coding: utf-8 -*-
import math
import numpy as np

class ColorUtil:
    """ 色変換の便利関数群 """

    @staticmethod
    def rgb_to_srgb(r, g, b, maxValue=255):
        """ RGB を 0-1 に正規化する """
        return map(lambda x: float(x) / maxValue, [r, g, b])


    @staticmethod
    def srgb_to_rgb(r, g, b, maxValue=255):
        """ 正規化 RGB を RGB にスケールする """
        return map(lambda x: x * maxValue, [r, g, b])


    @staticmethod
    def srgb_to_xyz(r, g, b):
        """ 正規化 RGB を XYZ に変換する """
        m = np.array([[0.4124, 0.3576, 0.1805],
                      [0.2126, 0.7152, 0.0722],
                      [0.0193, 0.1192, 0.9505]])
        l = map(lambda x: x / 12.92 if x <= 0.04045
                else ((x + 0.055) / 1.055) ** 2.4,
                [r, g, b])
        return (m.dot(l)).tolist()


    @staticmethod
    def xyz_to_srgb(x, y, z):
        """ XYZ を正規化 RGB に変換する """
        m = np.array([[3.2406, -1.5372, -0.4986],
                      [-0.9689, 1.8758, 0.0415],
                      [0.0557, -0.2040, 1.0570]])
        l = m.dot([x, y, z]).tolist()
        return map(lambda w: w * 12.92 if w <= 0.0031308
                   else (math.e ** (math.log(w) / 2.4)) * 1.055 - 0.055,
                   l)


    @staticmethod
    def xyz_to_lab(x, y, z):
        """ XYZ を L*a*b* に変換する """
        s = 6.0 / 29
        f = lambda w: w ** (1.0 / 3) if w > s ** 3 else (w / 3.0 / s ** 2) + 4.0 / 29
        fy = f(y / 100.000)
        l = 116 * fy - 16
        a = 500 * (f(x / 95.047) - fy)
        b = 200 * (fy - f(z / 108.883))
        return [l, a, b]


    @staticmethod
    def lab_to_xyz(l, a, b):
        """ L*a*b* を XYZ に変換する """
        s = 6.0 / 29
        f = lambda x: math.e ** (3 * math.log(x)) if x > s else 3 * (s ** 2) * (x - 4.0 / 29)
        fy = (l + 16) / 116.0
        x = f(a / 500.0 + fy) * 95.047
        y = f(fy) * 100.000
        z = f(fy - b / 200.0) * 108.883
        return [x, y, z]


    @staticmethod
    def lab_euclid_distance(l1, a1, b1, l2, a2, b2):
        """ 色同士の距離を L*a*b* 空間上で計算して返す """
        dl = l2 - l1
        da = a2 - a1
        db = b2 - b1
        d = math.sqrt(dl ** 2 + da ** 2 + db ** 2)
        return [d, dl, da, db]


# テスト用
# c = [255, 100, 0]
# print c
# sc = ColorUtil.rgb_to_srgb(c[0], c[1], c[2])
# print sc
# xyz = ColorUtil.srgb_to_xyz(sc[0], sc[1], sc[2])
# print xyz
# lab = ColorUtil.xyz_to_lab(xyz[0], xyz[1], xyz[2])
# print lab
# xyz = ColorUtil.lab_to_xyz(lab[0], lab[1], lab[2])
# print xyz
# sc = ColorUtil.xyz_to_srgb(xyz[0], xyz[1], xyz[2])
# print sc
# c = ColorUtil.srgb_to_rgb(sc[0], sc[1], sc[2])
# print c
