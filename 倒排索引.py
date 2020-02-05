#  建索引
from doc import Doc
import jieba
import codecs
import math

stop_words = 'stopwords.txt'
stopwords = codecs.open(stop_words,'r',encoding='utf8').readlines()
stopwords = [ w.strip() for w in stopwords ]

stop_flag = ['x', 'c', 'u','d', 'p', 't', 'uj', 'm', 'f', 'r']

class Indexer:
    daopai = {} #用来存储检索词和文档对象
    daopai_word={"123","123"}
    daopai_num={}

    def __init__(self, file_path):
        self.doc_list = []
        self.index_writer(file_path)

    def index_writer(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                word, English, miandian,time = line.strip().split('///')
                doc = Doc()
                doc.add('word', word)
                doc.add('English', English)
                doc.add('miandian', miandian)
                # doc.add('time', time)
                self.doc_list.append(doc)
        self.index()

    def index(self):
        doc_num = len(self.doc_list)  # 文档总数
        for doc in self.doc_list:
            word = doc.get('word')

            # 倒排
            term_list = list(jieba.cut_for_search(doc.get('English')))  # 分词
            for t in term_list:
                if t not in self.daopai_num and t not in stopwords:
                    self.daopai_num[t] = {}
                if t in self.daopai_word:
                    if t.isalpha() == False:
                        continue
                    if doc in self.daopai[t]:
                        if doc not in self.daopai_num[t]:
                            self.daopai_num[t] = {doc:0}
                        self.daopai_num[t][doc] += 1
                        continue
                    self.daopai[t].append(doc)
                else:
                    if t.isalpha() == False:
                        continue
                    self.daopai_word.add(t)
                    daopaiobj=[]
                    daopaiobj.append(doc)
                    self.daopai[t]=daopaiobj
                    self.daopai_num[t] = {doc:0}
                    self.daopai_num[t][doc] += 1
        for key in self.daopai.keys():
            print(key+": ",end=" ")
            for value in self.daopai[key]:
                print(value,end=" ")
            print()
        print("index done")



if __name__ == '__main__':
    ind=0
    # with open("v20.txt", 'r', encoding='utf-8') as f:
    #     for line in f.readlines():
    #         word, English, miandian,time = line.strip().split('///')
    #         doc = Doc()
    #         doc.add('word', word)
    #         doc.add('English', English)
    #         doc.add('miandian', miandian)
    #         str="lines/%d"%ind+".txt"
    #         file=open(str,'w',encoding='utf-8')
    #         file.write(word+" " + English + " " +miandian)
    #         file.close()
    #         ind=ind+1
    #         print(str)
    #        # file = open("")
    print("index")
    Indexer(file_path="v20.txt")