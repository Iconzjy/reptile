import pynlpir  # 引入依赖包
from ctypes import c_char_p
pynlpir.open()  # 打开分词器
s = '曾境瑜是昆明理工大学软件161班的一名学生'
print("默认打开分词和词性标注功能:")
print(pynlpir.segment(s))  # 默认打开分词和词性标注功能
print("把词性标注语言变更为汉语:")
print(pynlpir.segment(s, pos_english=False)) # 把词性标注语言变更为汉语
print("使用pos_tagging来关闭词性标注:")
print(pynlpir.segment(s, pos_tagging=False))   # 使用pos_tagging来关闭词性标注

pynlpir.nlpir.AddUserWord(c_char_p("曾境瑜".encode()))#添加自定义词语：
pynlpir.nlpir.AddUserWord(c_char_p("昆明理工大学".encode()))
print("添加自定义词语:")
print(pynlpir.segment(s, pos_tagging=False))
pynlpir.close()