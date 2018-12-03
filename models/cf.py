#!/usr/bin/python3
#coding:utf-8
import pandas as pd
import math

class UserCF:
    def __init__(self):
        self.file_path = './data/ratings.csv'
        self.dframe = pd.read_csv(self.file_path)
    
    @staticmethod
    def _cosine_sim(target, other):
        union_items = set(target) & set(other)
        if len(union_items) == 0:
            return 0.0
        target = [i**2 for i in target]; other = [i**2 for i in other]
        tarLen = sum(target); othLen = sum(other)
        cosine = len(union_items)/math.sqrt(tarLen * othLen)

        return cosine

    def _get_top_n_users(self, targetUserId, topN):
        # 通过计算用户之间的相似度,返回topN相似的用户列表   
        # 获取目标用户的观影记录
        target = self.dframe[self.dframe['UserID'] == targetUserId]['MovieID']
        # 获取其他用户的用户Id
        others_userId = [i for i in set(self.dframe['UserID']) if i != targetUserId]
        # 根据用户Id获取用户的观影记录
        others_movies = [self.dframe[self.dframe['UserID'] == i]['MovieID'] for i in others_userId]

        # 根据观影记录计算用户之间的相似度
        sim_list = [self._cosine_sim(target, other) for other in others_movies]
        # 将用户Id和相似度绑定,并根据相似度降序排序
        sim_list = sorted(zip(others_userId, sim_list), key=lambda a: a[1], reverse=True)
        # 返回topN用户列表
        return sim_list[:topN]
    
    def _get_candidates_items(self, targetUserId):
        # 获取目标用户没看过的所有电影
        # 其他用户看过的电影记录
        otherSeenMoives = set(self.dframe[self.dframe['UserID'] != targetUserId]['MovieID'])
        # 获取用户看过的电影
        tarSeenMovies = set(self.dframe[self.dframe['UserID'] == targetUserId]['MovieID'])
        # 两个集合筛选:选出目标用户没看过的所有电影
        candidates = list(otherSeenMoives - tarSeenMovies)

        return candidates
    
    def _get_topN_items(self, topNusers, candidates, topN):
        """获取topN推荐列表
        计算候选列表中topN相似用户的加权兴趣[评价]作为最终的推荐力度
        """
        # 获取topN相似用户Id的观影记录:记录中有电影评分
        topN_user_data = [self.dframe[self.dframe['UserID'] == k] for k, _ in topNusers]
        # 保存候选电影的推荐力度
        interest_list = []
        for movie in candidates:
            # topN用户的评分
            tmp = []
            for user_data in topN_user_data:
                # print(user_data)
                if movie in user_data['MovieID'].values:
                    # to print
                    score = user_data[user_data['MovieID'] == movie]['Rating'].values[0]/5.0
                    tmp.append(score)
                else:
                    tmp.append(0.0)
            interest = sum([topNusers[i][1] * tmp[i] for i in range(topN)])
            interest_list.append((movie, interest))
        interest_list = sorted(interest_list, key=lambda a:a[1], reverse=True)
        return interest_list[:topN]
    
    def recommend(self, target_userId=1, topN=10):
        """
        给目标用户推荐topN items.
        """
        topN_users = self._get_top_n_users(target_userId, topN)
        candidates = self._get_candidates_items(target_userId)
        topN_items = self._get_topN_items(topN_users,candidates,topN)

        return topN_items


