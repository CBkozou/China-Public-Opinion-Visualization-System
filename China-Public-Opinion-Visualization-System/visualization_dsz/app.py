# -*- codeing = utf-8 -*-
# @Time : 2021/3/23 9:42
# @Author : CBkozou
# @File : app.py
# @Software : PyCharm

from flask import Flask,render_template

import hotFind
import eventFind
import func

app=Flask(__name__)

yqlist=func.getYQList()
lylist=func.getLYList()
sjlist=func.getSJList()
qglist=func.getQGList()
idlist=func.getIDList()

positiveCountList=[]
negativeCountList=[]
groupByTime = func.groupByElement(sjlist)#将相同日期的舆情进行分组
#存储所有的爬取日期
Times=[]
for i in range(len(groupByTime)):
    Times.append(groupByTime[i][0])
#将日期转换为情感
id=0
for yuqing in groupByTime:
    for j in range(len(yuqing)):
        yuqing[j]=qglist[id]
        id+=1
for i in groupByTime:
    positiveCountList.append(i.count("positive"))
    negativeCountList.append(i.count("negative"))



yqCount=len(yqlist)#爬取舆情总数
# 统计来源数
baiduCount=lylist.count("百度")
weiboCount=lylist.count("微博")

# 统计该热点中包含的积极和消极舆情数目
positiveCount = qglist.count("positive")
negativeCount = qglist.count("negative")

# 统计进行爬取操作的日期列表
sjlistCut=[]#只截取日期的时间列表
for yuqing in range(len(sjlist)):
    temp=sjlist[yuqing]
    sjlistCut.append(temp[0:10])
sjlistCut=sorted(set(sjlistCut),key = sjlistCut.index) #每种只留一个
timeCount=len(sjlistCut)

#创建全部舆情字典
yqAllDataDic=[]
for i in range(len(yqlist)):
    temp={'id':idlist[i],'yq':yqlist[i],'ly':lylist[i],'sj':sjlist[i],'qg':qglist[i]}
    yqAllDataDic.append(temp)

#创建正面舆情字典
yqPosiDataDic=[]
for i in range(len(yqlist)):
    if qglist[i]=='positive':
        temp={'id':idlist[i],'yq':yqlist[i],'ly':lylist[i],'sj':sjlist[i],'qg':qglist[i]}
        yqPosiDataDic.append(temp)

#创建负面舆情字典
yqNegaDataDic=[]
for i in range(len(yqlist)):
    if qglist[i]=='negative':
        temp={'id':idlist[i],'yq':yqlist[i],'ly':lylist[i],'sj':sjlist[i],'qg':qglist[i]}
        yqNegaDataDic.append(temp)

#创建舆情事件字典
eventsDic=[]
for i in range(len(sjlistCut)):
    temp={'data':sjlistCut[i],'keywords':'，'.join(eventFind.eventKeywordList[i]),'events':'，'.join(eventFind.eventsList[i]),
          'id1':r'#collapseCard%d'%i,'id2':r'collapseCard%d'%i}
    eventsDic.append(temp)

@app.route('/')
def index():
    return render_template("index.html",yqCount=yqCount,
                           positiveCount=positiveCount,negativeCount=negativeCount,
                           hotCount=hotFind.hotCount,timeCount=timeCount,
                           sjlistCut=sjlistCut,
                           positiveCountList=positiveCountList,negativeCountList=negativeCountList,
                           eventKeywordCount=eventFind.eventKeywordCount)

@app.route('/hots')
def hots():
    return render_template("hots.html",countList=hotFind.countList,positiveCountList=hotFind.positiveCountList,
                           negativeCountList=hotFind.negativeCountList,warningLevelList=hotFind.warningLevelList,
                           negativeRateList=hotFind.negativeRateList,
                           hotCount=hotFind.hotCount,topicsCount=hotFind.topicsCount)

@app.route('/events')
def events():
    return render_template("events.html",eventKeywordCount=eventFind.eventKeywordCount,
                           eventsCount=eventFind.eventsCount,eventKeywordCountList=eventFind.eventKeywordCountList,
                           eventsCountList=eventFind.eventsCountList,sjlistCut=sjlistCut,
                           eventsDic=eventsDic)

@app.route('/website')
def website():
    return render_template("tables1.html",weiboCount=weiboCount,baiduCount=baiduCount)

@app.route('/yqAllData')
def yqAllData():
    return render_template("tables2.html",yqAllDataDic=yqAllDataDic)

@app.route('/yqPosiData')
def yqPosiData():
    return render_template("tables3.html",yqPosiDataDic=yqPosiDataDic)

@app.route('/yqNegaData')
def yqNegaData():
    return render_template("tables4.html",yqNegaDataDic=yqNegaDataDic)

if __name__=='__main__':
    app.run(debug=True) #开debug，随时写网页上随时改
