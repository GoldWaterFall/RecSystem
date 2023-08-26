def create_user_item_click(path):
    """
    :param path: 构建点击数据，输入数据路径
    :return:  输出为用户-物品字典
    """
    #初始化用户物品字段为空
    user_item=dict()
    #打开文件，做一个buffer
    with open(path,"r",encoding="utf-8")as f:
        #死循环，一行一行读数据，直到读取完毕
        while True:
            #读数据 1	1	5	874965758
            line=f.readline()
            #如果line不为空，则对line基于\t进行切分，得到[1,1,5,874965758]
            if line:
                lines=line.strip().split("\t")
                uid=lines[0]
                iid=lines[1]
                #初始化字典，get到uid则更新，如果uid不在字典中，初始化uid为key,value为set(iid)
                #user_item.get(uid, -1) 这一部分是在尝试从字典 user_item 中获取键为 uid 的值。
                # 如果该键存在，则会返回与其相关联的值；如果键不存在，则会返回 -1。
                if user_item.get(uid,-1)==-1:
                    user_item[uid]={iid}
                else:
                    user_item[uid].add(iid)
            #如果line为空，表示读取完毕，跳出死循环
            else:
                print("已经读完")
                break
    return user_item

def create_user_item_score(path):
    """
    :param path:输入数据路径
    :return: 输出为 key为用户，item为{iid : score}的一个字典 和一个物品集
    """
    #初始化用户物品字典为空
    user_item=dict()
    #为保证物品唯一，所以构建了set集合
    item_set=set()

    with open(path,"r",encoding="utf-8")as f:
        while True:
            line=f.readline()
            if line:
                lines=line.strip().split("\t")
                uid=lines[0]
                iid=lines[1]
                score=int(lines[2])
                item_set.add(iid)
                #初始化字典
                if user_item.get(uid, -1) == -1:
                    user_item[uid] = {iid: score}
                else:
                    #add() 用于将单个元素添加到集合中，而 update() 用于将一个集合合并到另一个集合中。
                    user_item[uid].update({iid: score})
            else:
                print("已经读完")
                break
    return user_item,item_set

if __name__ == '__main__':
    user_item= create_user_item_click("data/ua.base")
    with open("result/user_item.txt",'w') as file:
        # 将字典转换为字符串格式，并写入文件
        file.write(str(user_item))