# -*- codeing = utf-8 -*-
# @Time : 2021/3/18 10:42
# @Author : CBkozou
# @File : sentaLSTM.py
# @Software : PyCharm

import xlrd
import xlutils.copy
import paddlehub as hub
import warnings

warnings.filterwarnings("ignore",category=DeprecationWarning)
#所有舆情转换成一个列表，把要测试的短文本以str格式放到这个列表里
datapath=r"yq_data\topics.xls"
workbook = xlrd.open_workbook(datapath, formatting_info=True)
sheet = workbook.sheet_by_index(0)
yqlist=sheet.col_values(0)
del yqlist[0]
# print(yqlist)

sentimentList=[]

# 加载senta LSTM模型
senta = hub.Module(name="senta_bilstm")
# 指定模型输入
input_dict = {"text": yqlist}
# 把数据喂给senta模型的文本分类函数
results = senta.sentiment_classify(data=input_dict)
# 遍历分析每个短文本
for index, result in enumerate(results):
    print(result)
    sentimentList.append(result['sentiment_key'])
    print(yqlist[index], result['sentiment_key'])
print(sentimentList)

#将情感结果写入excel
filename = r'yq_data\topics.xls'
read_book = xlrd.open_workbook(filename, formatting_info=True)
write_book = xlutils.copy.copy(read_book)   # 复制
sheet = write_book.get_sheet(0)
for i in range(len(sentimentList)):
    sheet.write(1+i,3,sentimentList[i]) #写入预测情感结果
    sheet.write(1+i, 4, i+1) #写入编号
    print("第%d条预测成功"%(i+1))
write_book.save(filename)

