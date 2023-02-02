# -*- codeing = utf-8 -*-
# @Time : 2021/1/10 16:25
# @Author : CBkozou
# @File : spider.py
# @Software : PyCharm

import re
import requests
import time
from bs4 import BeautifulSoup #网页解析，获取数据
import xlwt #进行excel操作
import xlrd
from xlutils.copy import copy

def main():
    Baidu()
    Weibo()

def Baidu():
    baiduURL = "http://top.baidu.com/buzz?b=1&fr=20811"
    baiduHTML = askURL(baiduURL)
    baiduDatalist = getBaiduData(baiduHTML)
    saveBaiduData(baiduDatalist)

def Weibo():
    weiboURL="https://tophub.today/n/KqndgxeLl9"
    weiboHTML=askURL(weiboURL)
    weiboDatalist=getWeiboData(weiboHTML)
    saveWeiboData(weiboDatalist)

def askURL(url):
    my_header = {'User-Agent':'Mozilla/5.0'}
    response=requests.get(url,headers=my_header)
    print(response)
    response.encoding = response.apparent_encoding
    return response.text

def getBaiduData(html):
    # https://www.cnblogs.com/TobuTobu/p/10008867.html
    datalist=[]
    topic_names = []
    topic_froms=[]
    topic_time=[]
    soup = BeautifulSoup(html,'html.parser')
    all_topics=soup.find_all('tr')[1:]

    for each_topic in all_topics:
        data=[]
        #print(each_topic)
        topic_rank = each_topic.find('td',class_='first')#排名
        topic_name = each_topic.find('td',class_='keyword')#标题目
        topic_times = each_topic.find('td',class_='last')#搜索指数
        # print(topic_rank)
        if topic_rank != None and topic_name!=None and topic_times!=None:
            topic_rank = each_topic.find('td',class_='first').get_text().replace(' ','').replace('\n','')
            data.append(topic_rank)
            topic_name = each_topic.find('td',class_='keyword').get_text().replace(' ','').replace('\n','').replace('search','')
            data.append(topic_name)
            topic_names.append(topic_name)
            topic_froms.append("百度")
            topic_time.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            topic_times = each_topic.find('td',class_='last').get_text().replace(' ','').replace('\n','')
            data.append(topic_times)
            datalist.append(data)

    saveTopics(topic_names,topic_froms,topic_time)
    # print(datalist)
    return datalist

def getWeiboData(html):
    # https://www.cnblogs.com/fxc0210/p/12749287.html
    titles = re.findall('<a href=".*?">.*?(.*?)</a>', html)[4:24]
    heat = re.findall('<td>(.*?)</td>', html)[:20]
    for i in range(len(heat)):
        heat[i]=str(int(float(heat[i].replace('万', ''))*10000))
    # 创建空列表
    datalist = []
    topic_names = []
    topic_froms=[]
    topic_time=[]
    for i in range(20):
        # 拷贝数据
        datalist.append([i+1,titles[i], heat[i][:]])
        topic_names.append(titles[i])
        topic_froms.append("微博")
        topic_time.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # print(datalist)
    saveTopics(topic_names,topic_froms,topic_time)
    return datalist

def saveBaiduData(datalist):
    localtime1 = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
    localtime2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # savepath = "%s爬取百度热榜.xls" % localtime1
    savepath="baidu_data/%s爬取百度热榜.xls"%localtime1
    # print(savepath)
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('百度热榜', cell_overwrite_ok=True)  # cell_overwrite_ok在往上写可以覆盖以前的内容
    row = ("爬取时间", localtime2)

    for i in range(0, 2):
        sheet.write(0, i, row[i])
    col=("排名","热搜事件","热度")
    for i in range(0, 3):
        sheet.write(1, i, col[i])
    for i in range(0,20):
        # print("第%d条"%(i+1))
        data=datalist[i]
        for j in range(0,3):
            sheet.write(i+2,j,data[j])#i+1从第二行开始写数据

    book.save(savepath)

def saveWeiboData(datalist):
    localtime1 = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
    localtime2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # savepath="%s爬取微博热榜.xls"%localtime1
    savepath=r"weibo_data/%s爬取微博热榜.xls"%localtime1
    # print(savepath)
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('微博热榜', cell_overwrite_ok=True)  # cell_overwrite_ok在往上写可以覆盖以前的内容
    row = ("爬取时间", localtime2)

    for i in range(0, 2):
        sheet.write(0, i, row[i])
    col=("排名","热搜事件","热度")
    for i in range(0, 3):
        sheet.write(1, i, col[i])
    for i in range(0,20):
        # print("第%d条"%(i+1))
        data=datalist[i]
        for j in range(0,3):
            sheet.write(i+2,j,data[j])#i+1从第二行开始写数据

    book.save(savepath)

def saveTopics(topicNames, topicFrom, topicTime):
    filename = r'yq_data\topics.xls'

    # 遍历sheet1中所有行row
    workbook = xlrd.open_workbook(filename, formatting_info=True)
    sheet = workbook.sheet_by_index(0)
    num_rows = sheet.nrows
    rows = []
    for curr_row in range(num_rows):
        row = sheet.row_values(curr_row)
        rows.append(row)

    tag = 0
    # 在末尾增加新行
    for i in topicNames:
        for j in range(len(rows)):
            temp=rows[j][0]
            # print(temp)
            # temp = "".join(str(rows[j]))
            if i == temp:
                tag = 1
        if tag == 0:
            workbook = xlrd.open_workbook(filename, formatting_info=True)
            sheet = workbook.sheet_by_index(0)
            rowNum = sheet.nrows
            # colNum = sheet.ncols
            book = copy(workbook)
            sheet = book.get_sheet(0)
            sheet.write(rowNum, 0, i)
            sheet.write(rowNum, 1, topicFrom[topicNames.index(i)])
            sheet.write(rowNum, 2, topicTime[topicNames.index(i)])
            book.save(filename)
        tag = 0


def sleeptime(hour,min,sec): #定时启动
    return hour*3600 + min*60 + sec;

if __name__=="__main__":#当程序执行时
#调用函数
    second = sleeptime(1,0,0);
    S_time=1 #爬取次数
    main()
    print("第%d次爬取完毕"%S_time)
    # while True:
    #     time.sleep(second)
    #     main()
    #     S_time+=1
    #     print("第%d次爬取完毕"%S_time)