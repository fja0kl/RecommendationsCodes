#!/usr/bin/python3
#coding:utf-8
# 数据集路径: http://grouplens.org/datasets/movielens/1m
import pandas as pd
import os

class Channel:
    def __init__(self, dataDir):
        self.path = dataDir
    
    def _process_user_data(self, file='users.dat'):
        fullpath = os.path.join(self.path, file)
        # 读取dat文件,转换成csv格式
        f = pd.read_table(fullpath, sep='::', engine='python',names=['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code'])
        f.to_csv(os.path.join(self.path, 'users.csv'), index=False)
    
    def _process_ratings_data(self, file='ratings.dat'):
        fullpath = os.path.join(self.path, file)
        f = pd.read_table(fullpath, sep="::", engine='python',names=['UserID','MovieID','Rating','Timestamp'])
        f.to_csv(os.path.join(self.path, 'ratings.csv'), index=False)
    
    def _process_movies_data(self, file='movies.dat'):
        fullpath = os.path.join(self.path, file)
        f = pd.read_table(fullpath, sep="::", engine='python',names=['MovieID','Title','Genres'])
        f.to_csv(os.path.join(self.path, 'movies.csv'), index=False)
    
    def process(self):
        print("Process Movies Data...")
        self._process_movies_data()
        print("Moives Done!")
        
        print("Process Ratings Data...")
        self._process_ratings_data()
        print("Ratings Done!")

        print("Process Users Data...")
        self._process_user_data()
        print("Users Done!")
        print("Done")

if __name__ == '__main__':
    ch = Channel('./data')
    ch.process()