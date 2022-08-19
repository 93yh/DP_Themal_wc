#!/usr/bin/env python
# import cv2
from re import A
import numpy as np
import matplotlib.pyplot as plt
# from PIL import Image
# import matplotlib
import numpy as np
import pandas as pd
# import csv
import os
import sys
import time
# from scipy import stats


# def text_arr(txt_path):
#     result = []
#     with open(txt_path) as f:
#         for line in f:
#             # a.append(b)：是将b原封不动的追加到a的末尾上，会改变a的值
#             result.append(line.strip().split('\n'))
#             # strip()用于移除字符串头尾指定的字符（默认为空格或者换行符）或字符序列
#         return result

def sleeptime(hour, min, sec):
    return hour * 3600 + min * 60 + sec
def analyse(img_ori,img_result,img_newest):


    # # 3.获取原始数据所有csv名称
    # filelist = os.listdir(img_ori)
    # filelist.remove('TestResultReport.csv')
    # filelist.remove('TestTimeReport.csv')
    # filelist.sort(key=lambda x: (int(x.split('_')[0]), int(x.split('_')[1])))
    # # 用lamdba函数指定排序的依据，如果需要多个关键字作为依据进行排序，可以用形如 lamdba x : (key1, key2, …) 的方式指定。在上面的代码中三个关键字是int(x.split(’’)[0])，int(x.split(’’)[1])，以第一个关键字为例进行解释。首先需要将标签根据"_“进行分割，即x.split(’_’)，然后先按第一个数字进行排序，取分割后的第一部分x.split(’_’)[0]，再按第二个数字进行排序，去掉‘.jpg’[:-4]
    # csv_names_ori = np.array([file for file in filelist if file.endswith('.csv')], dtype=object)

    # # 4.获取导出数据所有jpg名称
    # filelist2 = os.listdir(img_result)
    # filelist2.sort(key=lambda x: (int(x.split('_')[0]), int(x.split('_')[1])))
    # img_names_result = np.array([file for file in filelist2 if file.endswith('.png')], dtype=object)
    
    # 3.获取原始数据所有csv名称
    filelist = os.listdir(img_ori)
    try:
        filelist.remove('TestResultReport.csv')
        filelist.remove('TestTimeReport.csv')
        filelist.sort(key=lambda x: (int(x.split('_')[0]), int(x.split('_')[1])))
        # 用lamdba函数指定排序的依据，如果需要多个关键字作为依据进行排序，可以用形如 lamdba x : (key1, key2, …) 的方式指定。在上面的代码中三个关键字是int(x.split(’’)[0])，int(x.split(’’)[1])，以第一个关键字为例进行解释。首先需要将标签根据"_“进行分割，即x.split(’_’)，然后先按第一个数字进行排序，取分割后的第一部分x.split(’_’)[0]，再按第二个数字进行排序，去掉‘.jpg’[:-4]
        csv_names_ori = np.array(
           [file for file in filelist if file.endswith('.csv')], dtype=object)
    except:
        filelist.sort(key=lambda x: (int(x.split('_')[0]), int(x.split('_')[1])))
        # 用lamdba函数指定排序的依据，如果需要多个关键字作为依据进行排序，可以用形如 lamdba x : (key1, key2, …) 的方式指定。在上面的代码中三个关键字是int(x.split(’’)[0])，int(x.split(’’)[1])，以第一个关键字为例进行解释。首先需要将标签根据"_“进行分割，即x.split(’_’)，然后先按第一个数字进行排序，取分割后的第一部分x.split(’_’)[0]，再按第二个数字进行排序，去掉‘.jpg’[:-4]
        csv_names_ori = np.array(
            [file for file in filelist if file.endswith('.csv')], dtype=object)

    # 4.获取导出数据所有jpg名称
    filelist2 = os.listdir(img_result)
    try:
        filelist.remove('Analyse.jpg')
        filelist2.sort(key=lambda x: (
            int(x.split('_')[0]), int(x.split('_')[1])))
        img_names_result = np.array(
            [file for file in filelist2 if file.endswith('.jpg')], dtype=object)
    except:
        filelist2.sort(key=lambda x: (
            int(x.split('_')[0]), int(x.split('_')[1])))
        img_names_result = np.array(
            [file for file in filelist2 if file.endswith('.jpg')], dtype=object)

    # 5.待处理csv

    #5.待处理csv
    filelist_3=np.setdiff1d(csv_names_ori,img_names_result)

    # 6.判断是否有待处理数据

    if len(filelist_3)==0:      
        raise ValueError("没有待处理数据!")

    #7.处理数据
    for i in range(0,len(filelist_3)):
        filepath=img_ori+'/'+filelist_3[i]
        filepath2=img_result+filelist_3[i]  #filepath2输出目录
        with open(filepath, "r") as f:
            data = f.read()  # 读取文件
            data = data.replace('\x00', '')
        with open(filepath2, "w") as f2:
            f2.write(data)

        # f = open(filepath2)
        # val_list = f.readlines()
        # lists = []
        # for string in val_list:
        #     string = string.split(',')
        #     lists.append(string[0:256])
        #     a = np.array(lists)
        #     a = a.astype(float)
        # a = np.array(a).reshape(192, 256)
        df = pd.read_csv(filepath2, header=None)
        my_dataframe = df.dropna(axis=1, how='all')  # 删除一整列都是NaN的列
        #df转np
        a = my_dataframe.values    

        # 平均值
        # m = np.mean(a)    
        #           
        # 众数
        m =pd.Series(a.reshape(-1)).mode()[0] 
        val = 5
        a[a < m-val] = m-val
        a[a > m+val] = m+val
        plt.imshow(a, interpolation='None', cmap='jet')  # plt.cm.inferno

        # 温标  shrink=0.8
        plt.colorbar()
        plt.xticks(())
        plt.yticks(())
        plt.title(filelist_3[i][0:15])
        
        # 保存图片
        plt.savefig(img_result+filelist_3[i][0:-4]+".png")
        plt.savefig(img_newest+filelist_3[i][0:-4]+".png")
        # plt.show()
        plt.clf()
        plt.close()
        


        # matplotlib.image.imsave('test.png',a)

if __name__ == "__main__":

    Ti=input('请输入预处理时间间隔（小时）：')
    directory = os.path.split(os.path.realpath(sys.argv[0]))[0]  # 当前文件所在的目录，即父路径
    conf=pd.read_csv(directory+'/config.csv')
    ids=conf['ID']
    Address=conf['Address']
    while 1 == 1:
        for i in range(0,conf.shape[0]):
            img_ori = Address[i]
            ID=ids[i]
            # 2.导出数据目录
            isExists = os.path.exists(directory+'/'+'BF')
            # 判断结果，新建备份文件夹
            if not isExists:
                # 如果不存在则创建目录
                os.mkdir(directory+'/'+'BF')

            isExists = os.path.exists(directory+'/'+'BF/'+ID)
            # 判断结果
            if not isExists:
                # 如果不存在则创建目录
                os.mkdir(directory+'/'+'BF/'+ID)
            img_result = directory+'/'+'BF/'+ID+'/'  # 注意最后有'/'

            isExists = os.path.exists(directory+'/'+ID)
            # 判断结果
            if not isExists:
                # 如果不存在则创建目录
                os.mkdir(directory+'/'+ID)
            img_newest = directory+'/'+ID+'/'  # 注意最后有'/'
            second = sleeptime(int(Ti), 0, 0)
            analyse(img_ori,img_result,img_newest)
    
    # 每隔多久执行analyse
    second = sleeptime(int(Ti), 0, 0)
    time.sleep(second)
    
