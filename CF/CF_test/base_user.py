import numpy as np
from load_data import *

#计算两个用户的相似性
def sim_cos(u1_id,u2_id,user_item):
    '''

    :param u1_id: 第一个用户uid
    :param u2_id: 第二个用户uid
    :param user_item: 用户-物品字典
    :return: 余弦相似度
    '''
    u1 = user_item[u1_id]
    u2 = user_item[u2_id]
    cor_index=set(u1.keys()) & set(u2.keys()) #找到两个用户共同评价过的物品的索引
    cross = 0  #初始化余弦相似度的分子部分
    u1_score = 0
    u2_score = 0
    for iid in cor_index:
        cross += u1[iid]*u1[iid]# 计算余弦相似度的分子部分
        u1_score += u1[iid] * u1[iid] # 计算用户u1的评分平方和
        u2_score += u2[iid] * u2[iid] # 计算用户u2的评分平方和
    m = cross # 分子部分
    s = (np.sqrt(u1_score) * np.sqrt(u2_score))# 分母部分，即两个用户评分向量的模的乘积
    if s == 0:
        return 0
    sim = m / s # 计算余弦相似度
    return np.around(sim,2)

def sim_jaccard(u1_id, u2_id, user_item):
    '''

    :param u1_id: 第一个用户uid
    :param u2_id: 第二个用户uid
    :param user_item: 用户-物品字典
    :return: jaccard相似度
    '''
    # 拿出u1 u2的集合，做交集，做并集，用交集的长度除以并集的长度得到jaccard距离
    # 注意分母为0.
    u1_item = user_item[u1_id]
    u2_item = user_item[u2_id]
    m = len(u1_item & u2_item) # 计算两个集合的交集的长度
    n = len(u1_item | u2_item) # 计算两个集合的并集的长度
    if n == 0:
        return 0
    else:
        return np.around(m/n, 2)# 计算 Jaccard 相似度并返回，保留两位小数

#计算用户两两相似字典
def cal_allSim(user_item,method="cosin"):
    '''
    :param user_item: 用户-物品字典
    :param method: 相似度计算方式 cosin or jaccard
    :return:返回用户相似字典
    '''
    #初始一个用户相似字典
    sim_dict={}
    #遍历用户去计算用户的两两相似
    for u1 in user_item.keys():
        for u2 in user_item.keys():
            #如果用户id一样，意味着用户是同一个，因此，不用计算，直接跳过。
            if u1==u2:
                continue
            #如果用户id不一样，那么计算用户相似
            else:
            # 如果sim_dict字典中没有u1的key，那么基于get进行初始化，然后计算u1 和u2 的相似度
                if sim_dict.get(u1, -1) == -1:
                    # 用cos 夹角余弦方法
                    if method == "cosin":
                        # 此处自己实现了一个sim_cos的方法
                        sim_dict[u1] = {u2: sim_cos(u1, u2, user_item)}
                    # 用jaccard方法
                    elif method == "jaccard":
                        # 此处自己实现了一个sim_jaccard的方法
                        sim_dict[u1] = {u2: sim_jaccard(u1, u2, user_item)}
                    else:
                        raise ("请输入正确相似度计算方法")
                # 如果sim_dict字典中有u1的key，那么直接计算相似度
                else:
                    if method == "cosin":
                        sim_dict[u1].update({u2: sim_cos(u1, u2, user_item)})
                    elif method == "jaccard":
                        sim_dict[u1].update({u2: sim_jaccard(u1, u2, user_item)})
                    else:
                        raise ("请输入正确相似度计算方法")
    # 最终返回用户相似词典 {"u1":{"u2":0.5，"u3":0.04}}
    return sim_dict

if __name__ == '__main__':
    #显示矩阵
    user_item,item_set= create_user_item_score("data/ua.base")
    sim_dict= cal_allSim(user_item,"cosin")
    with open("result/user_sim.txt",'w') as file:
        # 将字典转换为字符串格式，并写入文件
        file.write(str(sim_dict))

    #隐式矩阵
    #user_item= create_user_item_click("data/ua.base")
    #sim_dict= cal_allSim(user_item,"jaccard")
    #with open("result/user_sim.txt",'w') as file:
        # 将字典转换为字符串格式，并写入文件
        #file.write(str(sim_dict))