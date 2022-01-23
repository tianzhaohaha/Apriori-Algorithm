import pandas as pd
import numpy as np
import itertools


def to_num(basket,item_to_num):
    for i in range(len(basket)):
        for j in range(len(basket[i])):
            basket[i][j] = item_to_num[basket[i][j]]


    return basket




def buildC1(basket):
    item1 = set(itertools.chain(*basket))
    return [frozenset([i]) for i in item1]


def ck_to_lk(dataset, ck, min_support):
    """

    :param dataset:
    :param ck:
    :param min_support:
    :return:
    """
    support = {}

    for row in dataset:
        for items in ck:
            if items.issubset(row):
                support[items] = support.get(items, 0) + 1
    total = len(dataset)

    return {k: v / total for k, v in support.items() if v / total >= min_support}


def lk_to_ckset(lk_list):
    """
    由频繁1项集组合形成频繁k+1项集
    :param lk_list:
    :return:
    """
    ckset = set()
    lk_size = len(lk_list)
    if lk_size > 1:  # 如果lk只有一个的话，说明无法再向上取候选集了
        k = len(lk_list[0])
        for i, j in itertools.combinations(range(lk_size), 2):
            t = lk_list[i] | lk_list[j]
            if len(t) == (k + 1):
                ckset.add(t)

    return ckset

def lk_to_ckset_PCY(lk_list):
    """
    由频繁1项集组合形成频繁k+1项集
    :param lk_list:
    :return:
    """
    ckset = set()
    lk_size = len(lk_list)
    if lk_size > 1:  # 如果lk只有一个的话，说明无法再向上取候选集了
        k = len(lk_list[0])
        for i, j in itertools.combinations(range(lk_size), 2):
            t = lk_list[i] | lk_list[j]
            if len(t) == (k + 1):
                ckset.add(t)

    return ckset



def get_L_all(min_support,basket):
    """
    生成所有的频繁项集
    :param dataset:
    :param min_support:
    :return:
    """
    c1 = buildC1(basket)
    L1 = ck_to_lk(basket, c1, min_support)
    L_all = L1
    Lk = L1
    i = 1
    print(len(Lk))
    while len(Lk) > 1:
        lk_list = list(Lk.keys())

        ck = lk_to_ckset(lk_list)

        Lk = ck_to_lk(basket, ck, min_support)
        print(len(Lk))
        if len(Lk) > 0:
            L_all.update(Lk)
        else:
            break
        print(i)
        i += 1
    return L_all

def rule_from_item(item):
    left = []
    for i in range(1,len(item)):
        left.extend(itertools.combinations(item,i))
    return [(frozenset(le),frozenset(item.difference(le))) for le in left]


# 生成关联规则
def rule_from_Lall(L_all, min_confidence):
    rules = []
    for Lk in L_all:
        if len(Lk) > 1:
            rules.extend(rule_from_item(Lk))

    result = []
    for left, right in rules:
        support = L_all[left | right]
        confidence = support / L_all[left]
        if confidence >= min_confidence:
            result.append({'left': left, 'right': right, 'left|right': confidence})

    return result


def get_L_all_upgrade(min_support,basket):
    """
    生成所有的频繁项集
    :param dataset:
    :param min_support:
    :return:
    """
    c1 = buildC1(basket)
    L1 = ck_to_lk(basket, c1, min_support)

    L_all = L1

    Lk = L1
    i = 1
    print(len(Lk))
    while len(Lk) > 1:
        if i ==1:
            lk_list = list(Lk.keys())
            ck = lk_to_ckset(lk_list)
            Lk = PCY(ck,basket,min_support)
        else:
            lk_list = list(Lk.keys())
            ck = lk_to_ckset(lk_list)
            Lk = ck_to_lk(basket, ck, min_support)
        print(len(Lk))
        if len(Lk) > 0:
            L_all.update(Lk)
        else:
            break
        print(i)
        i += 1
    return L_all


def hash(x, y):
    '''
    返回hash值
    '''
    return int(str(x)+str(y))%1000







def PCY(ck, dataset, min_support):
    '''
    计算2阶频繁项及支持度(经过PCY算法改进)
    '''
    cnt = [0] * 1000
    bitmap = [0] * 1000
    pairs = []
    pairs2hash = {}

    for row in dataset:
        for items in ck:
            if items.issubset(row):
                g = items
                f = hash(list(items)[0], list(items)[1])
                cnt[f] += 1
                if g not in pairs:
                    pairs.append(g)
                    pairs2hash[g] = f

    data_num = len(dataset)
    bitmap = [1 if cnt[i]/data_num >= min_support else 0 for i in range(1000)]

    candidateFreq = []
    for i in range(len(pairs)):
        g = pairs[i]
        if bitmap[pairs2hash[g]] == 1:
            candidateFreq.append(pairs[i])

    support = {}
    candidateFreq_num = len(candidateFreq)
    for i in range(candidateFreq_num):
        for j in range(data_num):
            if set(candidateFreq[i]).issubset(set(dataset[j])):
                support[candidateFreq[i]] = support.get(candidateFreq[i],0)+1


    return {k: v / data_num for k, v in support.items() if v / data_num >= min_support}


