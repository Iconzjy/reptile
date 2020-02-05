

from math import sqrt
import jieba


# 合并标签集
def create_vocabulary(tag_list1, tag_list2):
    return list(set(jieba.cut_for_search(tag_list1+tag_list2)))


# 统计词频  tf
def calc_tag_frequency(tag_list):
    tag_frequency = {}
    tag_set = set(jieba.cut_for_search(tag_list))
    while ' ' in tag_set:
        tag_set.remove(' ')
    for tag in tag_set:
        tag_frequency[tag] = tag_list.count(tag)
    return tag_frequency


# 建立词频向量， 每个文本中的[次数，次数，......]
def create_vector(tag_frequency, vocabulary):
    vector = []
    tag_set = tag_frequency.keys()
    for tag in vocabulary:
        if tag in tag_set:
            vector.append(tag_frequency[tag])
        else:
            vector.append(0)
    return vector


# 计算词频向量相似度
def calc_similar(vector1, vector2, tag_count):
    x = 0.0 # 分子
    y1 = 0.0 # 分母1
    y2 = 0.0 # 分母2
    tag_count = float(tag_count)
    for i in range(0, len(vector1)): # same length
        t1 = vector1[i] / tag_count
        t2 = vector2[i] / tag_count
        x = x + (t1 * t2)
        y1 += pow(t1, 2)
        y2 += pow(t2, 2)
    return x / sqrt(y1 * y2)


# VSM模型实现
def vsm(tag_list1, tag_list2):
    count = len(tag_list1) + len(tag_list2)
    vocabulary = create_vocabulary(tag_list1, tag_list2)
    vector1 = create_vector(calc_tag_frequency(tag_list1), vocabulary)
    vector2 = create_vector(calc_tag_frequency(tag_list2), vocabulary)
    similar = calc_similar(vector1, vector2, count)
    return similar


if __name__ == '__main__':
    # 1. 文章分词
    # 2. TF-IDF 提取关键词作为文章标签
    # 3. 计算VSM模型相似度
    s1="The person’s expulsion results in the destruction, or the removal, of the corrupting element from the congregation and in the preservation of its spirit, or dominant attitude. —2 Tim. The person’s expulsion results in the destruction, or the removal, of the corrupting element from the congregation and in the preservation of its spirit, or dominant attitude. —2 Tim. The person’s expulsion results in the destruction, or the removal, of the corrupting element from the congregation and in the preservation of its spirit, or dominant attitude."
    s2="Just after the expulsion of August Riedmueller, the first full-time minister to work in the country, ten Luxembourgers were baptized on September 25, 1932. Just after the expulsion of August Riedmueller, the first full-time minister to work in the country, ten Luxembourgers were baptized on September 25, 1932. Just after the expulsion of August Riedmueller, the first full-time minister to work in the country, ten Luxembourgers were baptized on September 25, 1932."
    s3="expulsion"
    print("vsm(s1,s1):", vsm(s1, s1))
    print("vsm(s1,s2):",vsm(s1,s2))
    print("vsm(s1, s3):",vsm(s1, s3))
    print("vsm(s2, s3)",vsm(s2, s3))
    print("other: ",vsm("in in expulsion results in the destruction","in"))
    pass