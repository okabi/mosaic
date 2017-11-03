# -*- coding: utf-8 -*-
import copy
import cv2
import numpy as np
from color_util import ColorUtil


class Generator:
    """ モザイクアート生成クラス """

    def load(self, manager, path):
        """ 画像集合を読み込む """
        self.infos = manager.get()
        self.images = []
        for info in self.infos:
            self.images.append(cv2.imread(info[1]))
        self.path = path


    def generate(self, target_img, in_elem_size, out_elem_size):
        """ 読み込んだ画像から目標っぽいモザイク画像を生成する """
        print 'target labs...'
        target_labs = self.__target_labs(target_img, in_elem_size)
        print 'distances...'
        distances = self.__distances(target_labs)
        print 'adopts...'
        adopts = self.__adopt(distances)
        print 'generating...'
        self.__generate(target_labs, adopts, out_elem_size)


    def __target_labs(self, target_img, elem_size):
        """ ターゲットの画素の平均 L*a*b* 値を計算 """
        shape = np.shape(target_img)
        size_x = shape[0] / elem_size[0]
        size_y = shape[1] / elem_size[1]
        ret = np.zeros((size_x, size_y, 3))
        for i in xrange(size_x):
            for j in xrange(size_y):
                ret[i, j] = ColorUtil.mean_lab(
                    target_img[
                        (elem_size[0] * i):(elem_size[0] * (i + 1)),
                        (elem_size[1] * j):(elem_size[1] * (j + 1))])
        return ret


    def __distances(self, target_labs):
        """ 各画素色について各素材画像との距離を計算 """
        shape = np.shape(target_labs)
        n = len(self.infos)
        ret = np.zeros((shape[0], shape[1], n, 2))
        for i in xrange(shape[0]):
            for j in xrange(shape[1]):
                l, a, b = target_labs[i, j]
                for k in xrange(n):
                    l2, a2, b2 = self.infos[k][2:5]
                    ret[i, j, k] = [
                        k,
                        ColorUtil.lab_euclid_distance(
                            l, a, b, l2, a2, b2)[0]]
                s = copy.deepcopy(ret[i, j].tolist())
                s.sort(key=lambda x:x[1])
                ret[i, j] = s
        return ret


    def __adopt(self, distances):
        """ ターゲットの各画素にどの画像を割り当てるか決定する """
        shape = np.shape(distances)
        ret = np.zeros((shape[0], shape[1]))
        for i in xrange(shape[0]):
            for j in xrange(shape[1]):
                # とりあえず最も近い画像を割り当てていく
                # 本当は割当て回数を平等にすべき
                ret[i, j] = distances[i, j, 0, 0]
        return ret


    def __generate(self, target_labs, adopts, out_elem_size):
        """ 割り当て情報からモザイクアートを生成する """
        shape = np.shape(adopts)
        img = np.zeros(
            (shape[0] * out_elem_size[0],
             shape[1] * out_elem_size[1],
             3))
        for i in xrange(shape[0]):
            for j in xrange(shape[1]):
                # 色の補正
                n = int(adopts[i, j])
                l, a, b = self.infos[n][2:5]
                l2, a2, b2 = target_labs[i, j]
                elem = cv2.resize(self.images[n], out_elem_size)
                rgbs = ColorUtil.revise(elem, l, a, b, l2, a2, b2)
                # 出力画像の画素割り当て
                for i2 in xrange(out_elem_size[0]):
                    for j2 in xrange(out_elem_size[1]):
                        r, g, b = rgbs[i2, j2]
                        img[out_elem_size[0] * i + i2, out_elem_size[1] * j + j2] = [r, b, g]
        # 画像出力
        cv2.imwrite(self.path, img)
