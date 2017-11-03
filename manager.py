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
                  mean_l real not null,
                  mean_a real not null,
                  mean_b real not null,
                  fav_count integer not null);
              """
        self.__db.execute(sql)


    def __del__(self):
        self.__db.close()


    def add(self, img, path, fav_count):
        """ 画像情報を DB に追加する """
        l, a, b = ColorUtil.mean_lab(img)
        sql = """
              insert into images(path, mean_l, mean_a, mean_b, fav_count)
              values (?, ?, ?, ?, ?)
              """
        self.__db.execute(sql, (path, l, a, b, fav_count))


    def get(self):
        """ 画像情報を DB から取得する """
        sql = """ select * from images """
        return [x for x in self.__db.execute(sql)]


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
