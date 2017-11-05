# -*- coding: utf-8 -*-
import copy
import cv2
import subprocess
import numpy as np
from color_util import ColorUtil
from manager import Manager


class Generator:
    """ モザイクアート生成クラス """

    def load(self, manager, path):
        """ 画像集合を読み込む """
        self.infos = manager.get()
        self.images = []
        for info in self.infos:
            pa = "/home/okabi/Projects/mosaic/web/public/images/{:}".format(info[1])
            self.images.append(cv2.imread(pa))
        self.out_path = path


    def generate(self, target_img, in_elem_size, out_elem_size):
        """ 読み込んだ画像から目標っぽいモザイク画像を生成する """
        # output.jpg の削除
        print 'target hsvs...'
        target_hsvs = self.__target_hsvs(target_img, in_elem_size)
        print 'distances...'
        distances = self.__distances(target_hsvs)
        print 'adopts...'
        adopts = self.__adopt(distances)
        print 'generating...'
        self.__generate(target_hsvs, adopts, out_elem_size)
        print 'end'


    def __target_hsvs(self, target_img, elem_size):
        """ ターゲットの画素の平均 HSV 値を計算 """
        shape = np.shape(target_img)
        size_x = shape[0] / elem_size[0]
        size_y = shape[1] / elem_size[1]
        ret = np.zeros((size_x, size_y, 3))
        for i in xrange(size_x):
            for j in xrange(size_y):
                ret[i, j] = ColorUtil.mean_hsv(
                    target_img[
                        (elem_size[0] * i):(elem_size[0] * (i + 1)),
                        (elem_size[1] * j):(elem_size[1] * (j + 1))])
        return ret


    def __distances(self, target_hsvs):
        """ 各画素色について各素材画像との距離を計算 """
        shape = np.shape(target_hsvs)
        n = len(self.infos)
        ret = np.zeros((shape[0], shape[1], n, 2))
        for i in xrange(shape[0]):
            for j in xrange(shape[1]):
                h, s, v = target_hsvs[i, j]
                for k in xrange(n):
                    h2, s2, v2 = self.infos[k][2:5]
                    ret[i, j, k] = [
                        k,
                        ColorUtil.hsv_distance(
                            h, s, v, h2, s2, v2)[0]]
                s = copy.deepcopy(ret[i, j].tolist())
                s.sort(key=lambda x:x[1])
                ret[i, j] = s
        return ret


    def __adopt(self, distances):
        """ ターゲットの各画素にどの画像を割り当てるか決定する """
        shape = np.shape(distances)
        ret = np.zeros((shape[0], shape[1]))
        n = len(self.infos)
        adoptable = np.zeros(n) + 1
        for i in xrange(shape[0]):
            for j in xrange(shape[1]):
                # 最も近い画像を、割り当て回数を平等にして割り当てていく
                ans = -1
                for k in xrange(n):
                    id = int(distances[i, j, k, 0])
                    if adoptable[id] > 0:
                        ans = id
                        adoptable[id] -= 1
                        break
                if ans == -1:
                    adoptable += 1
                    ans = int(distances[i, j, 0, 0])
                    adoptable[id] -= 1
                ret[i, j] = distances[i, j, ans, 0]
        return ret


    def __generate(self, target_hsvs, adopts, out_elem_size):
        """ 割り当て情報からモザイクアートを生成する """
        shape = np.shape(adopts)
        img = np.zeros(
            (shape[0] * out_elem_size[0],
             shape[1] * out_elem_size[1],
             3))
        before_progress = -1
        for i in xrange(shape[0]):
            for j in xrange(shape[1]):
                # 進捗表示
                progress = int(100.0 * (shape[1] * i + j) / (shape[0] * shape[1]))
                if progress > before_progress and progress % 5 == 0:
                    print "{:} % 完了".format(progress)
                before_progress = progress
                # 色の補正
                n = int(adopts[i, j])
                h, s, v = self.infos[n][2:5]
                h2, s2, v2 = target_hsvs[i, j]
                elem = cv2.resize(self.images[n], out_elem_size)
                rgbs = ColorUtil.revise_hsv(elem, h, s, v, h2, s2, v2)
                # 出力画像の画素割り当て
                for i2 in xrange(out_elem_size[0]):
                    for j2 in xrange(out_elem_size[1]):
                        r, g, b = rgbs[i2, j2]
                        img[out_elem_size[0] * i + i2, out_elem_size[1] * j + j2] = [b, g, r]
        # 画像出力
        cv2.imwrite(self.out_path, img)

