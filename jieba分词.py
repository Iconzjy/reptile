import jieba
seg_list = jieba.cut("我是一只小小鸟", cut_all = True)
print("全模式:", ' '.join(seg_list))

seg_list = jieba.cut("我是一只小小鸟")
print("精确模式:", ' '.join(seg_list))

seg_list = jieba.cut_for_search("我是一只小小鸟")
print("搜索模式:", ' '.join(seg_list))