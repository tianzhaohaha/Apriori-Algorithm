import pandas as pd
import numpy as np
import itertools
import utils


upgrade = True
data = pd.read_csv('Groceries.csv')
basket = []

for i in range(len(data)):
    basket.append(data['items'][i].strip('}').strip('{').split(','))


goods = set(itertools.chain(*basket))#不同的商品

num_to_item = {}
item_to_num = {}

for index,item in enumerate(goods):#做映射
    num_to_item[index] = item
    item_to_num[item] = index


#在basket做映射
basket = utils.to_num(basket,item_to_num)

if upgrade==False:
    #计算所有频繁项集
    L_all = utils.get_L_all(0.005,basket)
    #生成关联规则
    result = utils.rule_from_Lall(L_all,0.5)


    #存储
    def back(item):
        li = list(item)
        for i in range(len(li)):
            li[i] = num_to_item[li[i]]
        return li

    df = pd.DataFrame(result)
    df = df.reindex(['left','right','left|right'],axis =1)
    df['left'] = df['left'].apply(back)
    df['right'] = df['right'].apply(back)
    df.to_csv('result.csv')
else:
    #计算所有频繁项集
    L_all = utils.get_L_all_upgrade(0.005,basket)


    #生成关联规则
    result = utils.rule_from_Lall(L_all,0.5)


    #存储
    def back(item):
        li = list(item)
        for i in range(len(li)):
            li[i] = num_to_item[li[i]]
        return li

    df = pd.DataFrame(result)
    df = df.reindex(['left','right','left|right'],axis =1)
    df['left'] = df['left'].apply(back)
    df['right'] = df['right'].apply(back)
    df.to_csv('result.csv')








