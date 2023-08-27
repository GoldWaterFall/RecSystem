#!/usr/bin/env python3


from base_user import cal_allSim
from user_cf import predict_click_baseUser
import os
import time


def main(uid,top_item=30):
    # 1.加载用户物品词典（可以放在hdfs中，hbase）
    if os.path.exists("result/user_item.txt"):
        with open("result/user_item.txt", "r+", encoding="utf-8") as f:
            user_item = eval(f.read())
    else:
        raise FileNotFoundError("please confirm your path")
    # 2.加载用户相似矩阵（内存，广播）
    if os.path.exists("result/user_sim.txt"):
       with open("result/user_sim.txt","r+",encoding="utf-8") as f:
            sim_dict = eval(f.read())
    else:
        sim_dict = cal_allSim(user_item, method="jaccard")
        with open("result/user_sim.txt", "w+", encoding="utf-8") as f:
            f.write(str(sim_dict))

    # 为基于用户的协同过滤 为用户推荐感兴趣的物品
    item = predict_click_baseUser(uid, user_item, sim_dict, top_item)
    return item


if __name__ == '__main__':
    uid = "1"
    top_item = 20
    start = time.time()
    print(main(uid, top_item))
    end = time.time()
    print((end-start))
