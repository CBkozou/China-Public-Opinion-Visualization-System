# -*- codeing = utf-8 -*-
# @Time : 2021/3/16 15:35
# @Author : CBkozou
# @File : eventFind.py
# @Software : PyCharm

import jieba
import sys
import func

#保存控制台输出
class Logger(object):
    def __init__(self, fileN="Default.log"):
        self.terminal = sys.stdout
        self.log = open(fileN, "a",encoding='utf8')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass
sys.stdout = Logger("yq_data/events.txt")  # 保存

#1. 收集舆情信息
#所有舆情转换成一个列表
yqlist=func.getYQList()
sjlist=func.getSJList()

#=====================================================================================

#2.将舆情信息按照时间进行分组
#只截取日期
for yuqing in range(len(sjlist)):
    str=sjlist[yuqing]
    sjlist[yuqing]= str[0:10]

groupByTime = func.groupByElement(sjlist)#将相同日期的舆情进行分组

#存储所有的爬取日期
Times=[]
for i in range(len(groupByTime)):
    Times.append(groupByTime[i][0])
#将日期转换为舆情
id=0
for yuqing in groupByTime:
    for j in range(len(yuqing)):
        yuqing[j]=yqlist[id]
        id+=1

# print(groupByTime)
#=====================================================================================

#3. 统计每一天舆情的高频关键词，若大于阈值，则判定为一个舆情事件
event_yz=3 #设置事件阈值
#yuqing:某一天的全部舆情
timeCount=0

#传给app.py
eventKeywordCount=0 #超过阈值的关键词总数
eventsCount=0 #舆情相关事件个数
eventKeywordCountList=[]#每日关键词数列表
eventsCountList=[]#每日舆情数列表
eventKeywordList=[]#每日关键词列表
eventsList=[]#每日舆情列表


for yuqing in groupByTime:
    yqtext=""
    for j in yuqing:
        yqtext+=j
    # print(yqtext)
    words = jieba.lcut(yqtext)  # 使用精确模式对文本进行分词
    counts = {}  # 通过键值对的形式存储词语及其出现的次数
    for word in words:
        if len(word) == 1:  # 单个词语不计算在内
            continue
        else:
            counts[word] = counts.get(word, 0) + 1  # 遍历所有词语，每出现一次其对应的值加 1
    items = list(counts.items())  # 将键值对转换成列表
    items.sort(key=lambda x: x[1], reverse=True)  # 根据词语出现的次数进行从大到小排序
    # print(items)

    eventKeyword=[]
    for j in items:
        if j[1]>=event_yz: #如果某天的某个关键词大于阈值，确定为是一个事件
            eventKeyword.append(j[0])

    events=[]
    for j in eventKeyword:
        for k in yuqing:
            if j in k:
                events.append(k)
    events=sorted(set(events), key=events.index)#每个元素按照原顺序只保留一次

    if len(eventKeyword)==0:
        print("今日无突发舆情事件")
    else:
        print("事件关键词:",end="")
        print(eventKeyword)
        print("与事件相关的舆情:",end="")
        print(events)

    eventKeywordCount+=len(eventKeyword)
    eventsCount+=len(events)
    eventKeywordCountList.append(len(eventKeyword))
    eventsCountList.append(len(events))
    eventKeywordList.append(eventKeyword)
    eventsList.append(events)

    # print(eventKeywordCount)
    # print(eventsCount)
    # print(eventKeywordCountList)
    # print(eventsCountList)

    print("%s事件提取结束\n" % Times[timeCount])
    timeCount+=1

