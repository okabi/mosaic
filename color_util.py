# -*- coding: utf-8 -*-
import copy
import cv2
import math
import numpy as np


class ColorUtil:
    """ 色変換の便利関数群 """

    # 正規化 RGB 関連
    @staticmethod
    def rgb_to_srgb(r, g, b, maxValue=255):
        """ RGB を 0-1 に正規化する """
        return map(lambda x: float(x) / maxValue, [r, g, b])


    @staticmethod
    def srgb_to_rgb(r, g, b, maxValue=255):
        """ 正規化 RGB を RGB にスケールする """
        return map(lambda x: x * maxValue, [r, g, b])


    # L*a*b* 関連
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
        ret = map(lambda w: w * 12.92 if w <= 0.0031308
                  else (math.e ** (math.log(w) / 2.4)) * 1.055 - 0.055,
                  l)
        return map(lambda w: min(1.0, max(0.0, w)), ret)


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


    # HSV 関連
    @staticmethod
    def srgb_to_hsv(r, g, b):
        """ 正規化 RGB を HSV に変換する """
        ma = max([r, g, b])
        mi = min([r, g, b])
        if ma == mi:
            return [0.0, 0.0, ma]
        else:
            d = ma - mi
            h = 0.0
            if mi == b:
                h = (g - r) / d + 1
            elif mi == r:
                h = (b - g) / d + 3
            else:
                h = (r - b) / d + 5
            h /= 6.0
            s = d / ma
            v = ma
            return [h, s, v]


    @staticmethod
    def hsv_to_srgb(h, s, v):
        """ HSV を正規化 RGB に変換する """
        c  = v * s
        hd = h * 6.0
        x = c * (1 - abs((hd % 2) - 1))
        ret = np.array([v - c, v - c, v - c])
        if 0 <= hd and hd < 1:
            ret += [c, x, 0]
        elif 1 <= hd and hd < 2:
            ret += [x, c, 0]
        elif 2 <= hd and hd < 3:
            ret += [0, c, x]
        elif 3 <= hd and hd < 4:
            ret += [0, x, c]
        elif 4 <= hd and hd < 5:
            ret += [x, 0, c]
        else:
            ret += [c, 0, x]
        return map(lambda w: max(0.0, min(1.0, w)), ret)


    @staticmethod
    def hsv_distance(h1, s1, v1, h2, s2, v2):
        """ 色同士の距離を HSV 空間上で計算して返す """
        r1 = 2 * math.pi * h1
        p1 = [s1 * math.cos(r1), s1 * math.sin(r1), v1]
        r2 = 2 * math.pi * h2
        p2 = [s2 * math.cos(r2), s2 * math.sin(r2), v2]
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        dz = p1[2] - p2[2]
        d = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
        return [d, dx, dy, dz]


    # 平均色関連
    @staticmethod
    def mean_rgb(img):
        """ 画像の RGB 平均値を返す """
        return img.mean(axis=(0, 1)).astype(np.int16).tolist()[::-1]


    @staticmethod
    def mean_lab(img):
        """ 画像の L*a*b* 平均値を返す """
        shape = np.shape(img)
        labs = np.zeros((shape[0] * shape[1], 3))
        for i in xrange(shape[0]):
            for j in xrange(shape[1]):
                n = shape[0] * i + j
                rgb = img[i, j].tolist()[::-1]
                sr, sg, sb = ColorUtil.rgb_to_srgb(rgb[0], rgb[1], rgb[2])
                x, y, z = ColorUtil.srgb_to_xyz(sr, sg, sb)
                labs[n] = ColorUtil.xyz_to_lab(x, y, z)
        return labs.mean(axis=0).tolist()


    @staticmethod
    def mean_hsv(img):
        """ 画像の HSV 平均値を返す """
        shape = np.shape(img)
        hsvs = np.zeros((shape[0] * shape[1], 3))
        for i in xrange(shape[0]):
            for j in xrange(shape[1]):
                n = shape[1] * i + j
                rgb = img[i, j].tolist()[::-1]
                sr, sg, sb = ColorUtil.rgb_to_srgb(rgb[0], rgb[1], rgb[2])
                hsvs[n] = ColorUtil.srgb_to_hsv(sr, sg, sb)
        # return np.median(hsvs, axis=0).tolist()
        return hsvs.mean(axis=0).tolist()


    # 補正関連
    @staticmethod
    def revise_lab(img1, l1, a1, b1, l2, a2, b2):
        """ 平均 L*a*b* から、img1 を img2 の色に補正する。 """
        pl = l2 / l1
        pa = a2 / a1
        pb = b2 / b1
        shape = np.shape(img1)
        ret = copy.deepcopy(img1)
        for i in xrange(shape[0]):
            for j in xrange(shape[1]):
                r, g, b = ret[i, j]
                sr, sg, sb = ColorUtil.rgb_to_srgb(r, g, b)
                x, y, z = ColorUtil.srgb_to_xyz(sr, sg, sb)
                l, a, b = ColorUtil.xyz_to_lab(x, y, z)
                l *= pl
                a *= pa
                b *= pb
                x, y, z = ColorUtil.lab_to_xyz(l, a, b)
                sr, sg, sb = ColorUtil.xyz_to_srgb(x, y, z)
                r, g, b = ColorUtil.srgb_to_rgb(sr, sg, sb)
                ret[i, j] = [r, g, b]
        return ret


    @staticmethod
    def revise_hsv(img1, h1, s1, v1, h2, s2, v2):
        """ 平均 HSV から、img1 を img2 の色に補正する。 """
        ph = 1 if h1 == 0 else h2 / h1
        ps = 1 if s1 == 0 else s2 / s1
        pv = 1 if v1 == 0 else v2 / v1
        shape = np.shape(img1)
        ret = copy.deepcopy(img1)
        for i in xrange(shape[0]):
            for j in xrange(shape[1]):
                r, g, b = ret[i, j]
                sr, sg, sb = ColorUtil.rgb_to_srgb(r, g, b)
                h, s, v = ColorUtil.srgb_to_hsv(sr, sg, sb)
                h = h2
                s *= ps
                v *= pv
                sr, sg, sb = ColorUtil.hsv_to_srgb(h, s, v)
                r, g, b = ColorUtil.srgb_to_rgb(sr, sg, sb)
                ret[i, j] = [r, g, b]
        return ret


if __name__ == '__main__':
    c = [255, 100, 0]
    print c
    sc = ColorUtil.rgb_to_srgb(c[0], c[1], c[2])
    print sc
    hsv = ColorUtil.srgb_to_hsv(sc[0], sc[1], sc[2])
    print hsv
    sc = ColorUtil.hsv_to_srgb(hsv[0], hsv[1], hsv[2])
    print sc
    c = ColorUtil.srgb_to_rgb(sc[0], sc[1], sc[2])
    print c
