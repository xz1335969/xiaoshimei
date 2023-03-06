import random
# 这里是我之前写的加权随机函数，直接抄过来用了。
def overrandom(items: list[tuple | list] | dict):
    """
    对于输入的值与权重组成的字典或元组列表，求加权平均。
    :param items: 求加权平均的字典或元组列表
    :return: 加权随机出的键
    """
    if type(items) == list:
        keys = [i[0] for i in items]
        rates = [i[1] for i in items]
    else:
        keys = [i for i in items]
        rates = [items[i] for i in keys]
    rate_all = sum(rates)
    rand = random.randint(1, rate_all)
    i = 0
    for j in range(len(keys)):
        rand -= rates[j]
        if rand <= 0:
            i = int(j)
            break
    return keys[i]

# 检查问题是否回答正确的函数，自己写
def test_answer(answer):
    if answer >= 0:
        return True
    else:
        return False

# 问题的权重，这里可以读取文件或者读取数据库得到
question_weight = {
    "题型一": 10,
    "题型二": 10,
    "题型三": 10,
}
def test():
    question = overrandom(question_weight)
    answer = input("请输入回答")
    try:
        answer = int(answer)
    except:
        print("输入有误！")
        return
    if test_answer(answer):
        question_weight[question] += 2
        print("回答正确")
        return True
    else:
        question_weight[question] -= 2
        print("回答错误")
        return False

