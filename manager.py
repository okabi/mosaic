# -*- coding: utf-8 -*-
import sqlite3
import cv2
import numpy as np
from color_util import ColorUtil


class Manager:
    """ モザイクアートのための画像管理クラス """

    def __init__(self, db_path):
        self.__db = sqlite3.connect(db_path)
        sql = """
              create table if not exists images(
                  id integer primary key,
                  path text unique not null,
                  mean_h real,
                  mean_s real,
                  mean_v real,
                  fav_count integer not null);
              """
        self.__db.execute(sql)


    def __del__(self):
        self.__db.commit()
        self.__db.close()


    def add(self, img, path, fav_count):
        """ 画像情報を DB に追加する """
        h, s, v = ColorUtil.mean_hsv(img)
        sql = """
              insert into images(path, mean_h, mean_s, mean_v, fav_count)
              values (?, ?, ?, ?, ?)
              """
        self.__db.execute(sql, (path, h, s, v, fav_count))


    def get(self, id=None):
        """ 画像情報を DB から取得する """
        if id is None:
            sql = """ select * from images """
            return [x for x in self.__db.execute(sql)]
        else:
            sql = """ select * from images where id = ? """
            return [x for x in self.__db.execute(sql, (id))]


    def update_hsv(self, id, h, s, v):
        """ 画像の HSV を更新する """
        sql = """
              update images set
              mean_h = ?, mean_s = ?, mean_v = ?
              where id = ?
              """
        self.__db.execute(sql, (h, s, v, id))


    def update_fav_count(self, id, new_fav_count):
        """ 画像のいいね数を更新する """
        sql = """
              update images set fav_count = ? where id = ?
              """
        self.__db.execute(sql, (new_fav_count, id))


    def danger_drop(self):
        """ DB を初期化する """
        sql = """ drop table images """
        self.__db.execute(sql)
