#  建索引
from doc import Doc
import jieba
import jieba.posseg as pseg
import codecs
import 空间向量模型 as vsm

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
                if t in stopwords:#去停用词
                    continue
                if t not in self.daopai_num:
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
        # for key in self.daopai.keys():
        #     print(key+": ",end=" ")
        #     for value in self.daopai[key]:
        #         print(value,end=" ")
        #     print()
        print("index done")
        return self.daopai



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
    dictionalry = Indexer(file_path="test_v20.txt").index()
    # for key in dictionalry:
    #     print(key+": ",end=" ")
    #     for value in dictionalry[key]:
    #         print(value,end=" ")
    #     print()
    # sqr=input("请输入查询文本：")
    sqr="In 1979, that Court reversed the lower court’s decision, stating: “Said punishment [expulsion] contradicts the constitutional"
    words = pseg.cut(sqr)
    sqr_words=[]
    for word, flag in words:
        if flag not in stop_flag and word not in stopwords:
            sqr_words.append(word)

    resultIndex=[]#用来存放查询的相似度值
    resultContent=[]#用来存放DOC对象，与resultIndex一一对应
    for key in dictionalry.keys():
        if key in sqr_words:
            for value in dictionalry[key]:#value是文本对象，就是词库里的句子
                sim = vsm.vsm(sqr,value.get("English"))
                if value not in resultContent:#判断文件是否重复出现过
                    resultIndex.append(sim)
                    resultContent.append(value)


    IndexCopy=resultIndex.copy()
    list.sort(IndexCopy,reverse=True)
    for ind in IndexCopy:
        pos = resultIndex.index(ind)
        print(ind,resultContent[pos].get("English"))

