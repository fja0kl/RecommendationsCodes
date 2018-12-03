#!/usr/bin/python3
import sys
from models.cf import UserCF
from preprocess import Channel
import time
import pandas as pd


PATH = './data/'
TOPN = 10

def getNames(movies):
    moviesDF = pd.read_csv('./data/movies.csv')
    moviesNames = [moviesDF[moviesDF['MovieID'] == k]['Title'].values for k, _ in movies]
    result = zip(movies, moviesNames)
    return result

def manage():
    param = sys.argv[1] #0:文件名
    if param == 'preprocess':
        Channel().process()
    elif param == 'cf':
        start = time.time()
        movies = UserCF().recommend(2,10)
        result = getNames(movies)
        for movie in result:
            print(movie[1][0], movie[0][1])
        print('Cost time:%f' % (time.time() - start))
    else:
        print('Args must in ["preprocess", "cf", "lfm"，"prank"].')
    sys.exit()

if __name__ == '__main__':
    manage()