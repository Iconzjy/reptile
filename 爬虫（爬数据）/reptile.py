
import sys, re
from pyquery import PyQuery as pq
import os

import random
import importlib, sys
import time

import openpyxl
import xlrd
import xlwt
importlib.reload(sys)
from xlutils.copy import copy
logfile="log.txt"
def write_excel(key,english,miandian,time):
    path="v20.xls"
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格

    new_worksheet.write(rows_old, 0, key)  # 追加写入数据，注意是从rows_old行开始写入
    new_worksheet.write(rows_old, 1, english)
    new_worksheet.write(rows_old, 2, miandian)
    new_worksheet.write(rows_old, 3, time)
    new_workbook.save(path)



def get_next_page(page_url,after_url,keyword="",NUM=0):
    english = ""
    miandian = ""
    urlLog = open(logfile, 'r', encoding=u'utf-8', errors='ignore')
    urlLog.write(page_url+after_url)
    urlLog.close()
    d = pq(url=page_url+after_url)
    objs = d('#translationExamples')('#tmTable')('.span6')
    if objs:
        for i in range(0, len(objs)):
            print(i)
            if i % 2 == 0:
                rm_str = objs.eq(i).remove('sup')
                english = rm_str.find('span').text()
                print(english)
            else:
                rm_str = objs.eq(i).remove('sup')
                rm_str = rm_str.remove('aside')
                miandian = rm_str.find('span').text()
                print(miandian)
                write_excel(keyword, english, miandian, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    obj_next = d('#translationExamples')('div')('ul')('li')('a')
    if obj_next:
        NUM=NUM+1
        print(obj_next.eq(len(obj_next)-1).attr('href'))
        if obj_next.eq(len(obj_next)-1).attr('rel').find('nofollow'):
            if NUM < 3:
                time.sleep(random.randint(6, 19) * 7)
                get_next_page(page_url, obj_next.eq(len(obj_next)-1).attr('href'),keyword)



def get_page_content(page_url,keyword="",NUM=0):
    english=""
    miandian=""
    urlLog = open(logfile, 'r', encoding=u'utf-8', errors='ignore')
    urlLog.write(page_url)
    urlLog.close()
    d = pq(url=page_url)
    objs = d('#translationExamples')('#tmTable')('.span6')
    if objs:
        for i in range(0, len(objs)):
            print(i)
            if i%2==0:
                rm_str=objs.eq(i).remove('sup')
                english=rm_str.find('span').text()
                print(english)
            else:
                rm_str = objs.eq(i).remove('sup')
                rm_str = rm_str.remove('aside')
                miandian=rm_str.find('span').text()
                print(miandian)
                write_excel(keyword,english,miandian,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

    obj_next = d('#translationExamples')('div')('ul')('li')('a')
    if obj_next:
        NUM=NUM+1
        print(obj_next.eq(len(obj_next)-1).attr('href'))
        time.sleep(random.randint(6,19)*7)
        get_next_page(page_url,obj_next.eq(len(obj_next)-1).attr('href'),keyword,NUM)


if __name__ == '__main__':
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    else:
        file_object = open('en_Dic_v1.0_20.txt')
        count = 0
        line = 0
        index = 0
        if os.path.exists('record.txt'):
            line_record = open("record.txt", 'r', encoding=u'utf-8', errors='ignore')
            get_line = line_record.readlines()
            if get_line:
                get_line = get_line
                print(get_line)
                for v in get_line:
                    line = int(v)
            line_record.close()
        print(line)

        try:
            words = file_object.readlines()
            words = words[:-1]
        finally:
            file_object.close()
        for word in words:
            if index < line:
                index = index + 1
                continue
            if count == 10:
                time.sleep(random.randint(6, 19) * 10)
                count = 0
            count = count + 1
            word = word[:-1]
            url = "https://glosbe.com/en/my/" + word
            url.replace("\r\n", "")
            print(url)
            try:
                get_page_content(url, word,0)
                line_record = open("record.txt", 'w', encoding=u'utf-8', errors='ignore')
                line = line+1
                line_record.write(str(line))
                line_record.close()
                time.sleep(random.randint(6, 19) * 10)
            except IOError as e:
                print(e)
        file_object.close()


