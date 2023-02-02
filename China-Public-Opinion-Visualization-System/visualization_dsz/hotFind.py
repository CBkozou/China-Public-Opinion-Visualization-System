# -*- codeing = utf-8 -*-
# @Time : 2021/1/16 15:03
# @Author : CBkozou
# @File : hotFind.py
# @Software : PyCharm

import xlwt
from matplotlib import pyplot as plt #绘图，数据可视化
from wordcloud import WordCloud #词云
from PIL import Image #图片处理
import numpy as np #矩阵运算
import jieba
import func

# 1. 配置热点关键字和信息数量阈值，从中来提取针对性的，预置好的热点内容
#把所有舆情信息转换成列表
yqlist=func.getYQList()
lylist=func.getLYList()
sjlist=func.getSJList()
qglist=func.getQGList()

yuzhi=2 #阈值
hotKeyList=["河北", "疫情", "特朗普","新疆","印度","特斯拉"] #预设热点关键词

#=====================================================================================
# 2. 创建excel和表
savepath=r"yq_data/hots.xls"
book = xlwt.Workbook(encoding="utf-8", style_compression=0)

#传给app.py
hotCount=0 #统计超过阈值的热点数量
topicsCount=0 #统计热点相关舆情的数量
saveHotKeyList=[] # 超过阈值的热点关键词
countList=[]
positiveCountList=[]
negativeCountList=[]
warningLevelList=[]
negativeRateList=[]

for hot in hotKeyList:
    saveHotList = []  # 超过阈值的热点

    #统计某个舆情关键词包含的舆情数量
    count=0
    for j in yqlist:
        if (hot in j) == True:
            count+=1
    # print(count)


    # 如果舆情数量大于阈值，判断为这是一个热点，为其创建sheet进行储存
    if count>yuzhi:
        countList.append(count)
        hotCount+=1
        topicsCount+=count
        saveHotKeyList.append(hot)
        sheet = book.add_sheet(hot, cell_overwrite_ok=True)
        sheet.write(0, 0, hot)
        # 寻找包含舆情热点关键词的舆情，储存在对应的表中
        temp = 1
        hot_qglist = [] #某个热点的情感列表
        for j in yqlist:
            if (hot in j) == True:
                # print(hot, j)
                sheet.write(temp, 0, j)
                sheet.write(temp, 1, lylist[yqlist.index(j)])
                sheet.write(temp, 2, sjlist[yqlist.index(j)])
                sheet.write(temp, 3, qglist[yqlist.index(j)])
                temp += 1
                saveHotList.append(j)
                hot_qglist.append(qglist[yqlist.index(j)])

        # 统计该热点中包含的积极和消极舆情数目
        positiveCount = hot_qglist.count("positive")
        positiveCountList.append(positiveCount)
        negativeCount = hot_qglist.count("negative")
        negativeCountList.append(negativeCount)

        #计算预警等级
        warningLevel=0
        negativeRate=negativeCount/count
        negativeRateList.append(negativeRate)
        if negativeRate>=0.1 and negativeRate<0.33:
            warningLevel=1
        elif negativeRate>=0.33 and negativeRate<0.5:
            warningLevel = 2
        elif negativeRate>=0.5 and negativeRate<0.7:
            warningLevel = 3
        elif negativeRate>=0.7:
            warningLevel=4
        warningLevelList.append(warningLevel)

        # 写入热点各项统计数据
        sheet.write(temp, 0, "舆情总数")
        sheet.write(temp+1, 0, "积极舆情数")
        sheet.write(temp+2, 0, "消极舆情数")
        sheet.write(temp+3, 0, "预警等级")
        sheet.write(temp, 1, count)
        sheet.write(temp+1, 1, positiveCount)
        sheet.write(temp+2, 1, negativeCount)
        sheet.write(temp+3, 1, warningLevel)

        # =====================================================================================
        # 3. 绘制每一个热点的词云图
        # 把所有包含热点词的舆情信息连成一个字符串
        text = ""
        for i in saveHotList:
            text = text + i
        # 分词
        cut = jieba.cut(text)
        # print(cut)
        string = ' '.join(cut)
        # print(string)
        img = Image.open(r'static/img/cloud.png') #作为轮廓的图片
        img_array = np.array(img)  # 将图片转换为数组
        wc = WordCloud(
            background_color='white',
            mask=img_array,
            font_path="STKAITI.TTF"
        )
        wc.generate_from_text(string)

        # 绘制图片
        # fig = plt.figure(1)
        plt.imshow(wc)
        plt.axis('off')  # 是否显示坐标轴

        # plt.show()#显示图片
        # 保存图片
        plt.savefig(r'static/img/hot%d.jpg'%hotCount, dpi=500)  # dpi 清晰度


book.save(savepath)
# print(saveHotList)
# print(countlist)

#=====================================================================================
# 4. 传给app.py的数据
print(hotCount)
print(topicsCount)
print(saveHotKeyList)
print(countList)
print(positiveCountList)
print(negativeCountList)
print(warningLevelList)
print(negativeRateList)