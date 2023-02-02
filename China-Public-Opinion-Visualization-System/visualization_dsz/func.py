# -*- codeing = utf-8 -*-
# @Time : 2021/3/24 14:14
# @Author : CBkozou
# @File : func.py
# @Software : PyCharm
import xlrd
# 读取数据
datapath=r"yq_data\topics.xls"
workbook = xlrd.open_workbook(datapath, formatting_info=True)
sheet = workbook.sheet_by_index(0)
yqlist=sheet.col_values(0) #舆情信息
del yqlist[0]
lylist=sheet.col_values(1) #来源
del lylist[0]
sjlist=sheet.col_values(2) #爬取时间
del sjlist[0]
qglist=sheet.col_values(3) #情感
del qglist[0]
idlist=sheet.col_values(4) #id
del idlist[0]

def getYQList():
    return yqlist
def getLYList():
    return lylist
def getSJList():
    return sjlist
def getQGList():
    return qglist
def getIDList():
    for i in range(len(idlist)): #转换成int
        idlist[i]=int(idlist[i])
    return idlist

def groupByElement(lst):
   #先取得不同元素起始的索引值，再按照这个索引值取切片
    index = []
    result = []
    for i, _ in enumerate(lst):
        if i < len(lst) - 1 and lst[i + 1] != lst[i]:
            index.append(i + 1)

    result.append(lst[:index[0]])
    for i, item in enumerate(index):
        if i < len(index) - 1:
            result.append(lst[index[i]:index[i + 1]])
    result.append(lst[item:])
    return result