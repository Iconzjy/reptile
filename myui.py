# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import jieba.posseg as pseg
import codecs
from gensim import corpora
from gensim.summarization import bm25
import os


#停用词
stop_words = 'stopwords.txt'
stopwords = codecs.open(stop_words,'r',encoding='utf8').readlines()
stopwords = [ w.strip() for w in stopwords ]

stop_flag = ['x', 'c', 'u','d', 'p', 't', 'uj', 'm', 'f', 'r']

#分词，根据输入文件的文件名（单个文件），读取文件，然后进行分词（结巴分词）
#并存入result中，然后返回
def tokenization(filename):
    result = []
    with open("lines/"+filename, 'r',encoding='utf-8') as f:
        text = f.read()
        words = pseg.cut(text)
    for word, flag in words:
        if flag not in stop_flag and word not in stopwords:
            result.append(word)
    return result

#用于记录每个文档的分词后的容器，[[...,...],.....,[],[]]类型
corpus = []
#文件夹路径
dirname = 'lines'
#用来存储文件名，文件名的位置和corpus是相对应的
filenames = []
#查询语句
query_str = ""


#记录txt文档的内容，看是否有重复
filetxt=""

#获取文件名和词典
def getFilesNameAndCorpus():
    for root, dirs, files in os.walk(dirname):
        for f in files:
            corpus.append(tokenization(f))
            filenames.append(f)
    dictionary = corpora.Dictionary(corpus)
    print("dictionary lenth: ",len(dictionary))
    return dictionary


#建立词袋模型
#根据查询短语，用于获取BM25得分
def getScores(dictionary):
    bm25Model = bm25.BM25(corpus)
    query = []
    #对查询词分词
    for word in query_str.strip().split():
        query.append(word)
    scores = bm25Model.get_scores(query)
    return scores

#排序
def getSort(scores):
    # print(scores)
    list.sort(scores,reverse=True)

#获取文件的内容
def getFileContent(score,scores,beg=0,i=0):
    global filetxt
    str=""
    idx = scores.index(score,beg,len(scores))
    fname = filenames[idx]
    with open("lines/"+fname,'r',encoding='utf-8') as f:
        fread=f.read()
        fread=fread.strip()
        if filetxt == fread:
            i=i-1
        else:
            print("得分：", score)
            print("所在文本：", fname)
            print(fread)
            str += "得分：%.7f"%score+"   所在文本："+ fname + "\n"+fread+"\r\n"
        filetxt = fread
        f.close()
    return idx,i,str

dictionary = getFilesNameAndCorpus()#通过corpora库建立词典模型

#查询
def getSearch(str):
    global query_str
    query_str=str#查询短语
    scores = getScores(dictionary)
    scores_copy = scores.copy()
    getSort(scores)
    i = 0
    last_value = 0.0
    begin = 0
    rtnValue=""
    #只查询前10个
    for s in scores:
        if last_value != s:
            begin = 0
        last_value = s
        i = i + 1
        if i > 10:
            break
        begin, i,str = getFileContent(s, scores_copy, begin, i)
        rtnValue+=str
        begin = begin + 1
    return rtnValue

#界面
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("大报告")
        Form.resize(800, 600)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(20, 22, 522, 40))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(544, 20, 150, 46))
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(20, 78, 682, 502))
        self.textEdit.setObjectName("textEdit")

        self.pushButton.clicked.connect(lambda: self.sure_click())

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "大报告"))
        self.pushButton.setText(_translate("Form", "查找"))

    def getConent(self):
        return self.lineEdit.text()

    def setResult(self, value):
        self.textEdit.setText(value)

    def sure_click(self):
        str = self.getConent()
        self.textEdit.clear()
        self.textEdit.setText(getSearch(str))