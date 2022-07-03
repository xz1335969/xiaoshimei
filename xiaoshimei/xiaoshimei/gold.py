import pymysql
import random
ITEM_PRICE = {
    0: 100,
    1: 100,
    2: 55,
    3: 65,

}


def gold_query(user_id: int, group_id: int):
    """
    查询金币数
    :param user_id: QQ号
    :param group_id: 群号
    :return: 该群中此QQ号拥有的金币
    """
    conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
    cursor = conn.cursor()
    sql = f'SELECT gold FROM gold WHERE user_id = {user_id} AND group_id = {group_id}'
    cursor.execute(sql)
    data = cursor.fetchone()
    conn.close()
    if data is None:
        return 0
    else:
        return data[0]


def get_gold(user_id: int, group_id: int, num: int):
    """
    获取金币
    :param user_id: QQ号
    :param group_id: 群号
    :param num: 获取金币数
    """
    conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
    cursor = conn.cursor()
    sql = f'SELECT gold FROM gold WHERE user_id = {user_id} AND group_id = {group_id}'
    sql2 = f'INSERT INTO gold (user_id, group_id, gold) VALUES ({user_id},{group_id},{num})'
    sql3 = f'UPDATE gold SET gold = gold + {num} WHERE user_id = {user_id} AND group_id = {group_id}'
    cursor.execute(sql)
    data = cursor.fetchone()
    if data is None:
        cursor.execute(sql2)
    else:
        cursor.execute(sql3)


def cost_gold(user_id: int, group_id: int, num: int):
    """
    花费金币
    :param user_id: QQ号
    :param group_id: 群号
    :param num: 花费金币数
    :return: 返回结果
    """
    conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
    cursor = conn.cursor()
    sql = f'SELECT gold FROM gold WHERE user_id = {user_id} AND group_id = {group_id}'
    sql3 = f'UPDATE gold SET gold = gold - {num} WHERE user_id = {user_id} AND group_id = {group_id}'
    cursor.execute(sql)
    data = cursor.fetchone()
    if data is None:
        raise Exception(f"[CQ:at,qq={user_id}]您没有金币！")
    elif data[0] < num:
        raise Exception(f"[CQ:at,qq={user_id}]您的金币不足！")
    else:
        cursor.execute(sql3)
        conn.commit()
        return 0


def signin(user_id: int, group_id: int):
    """
    签到
    :param user_id: QQ号
    :param group_id: 群号
    """
    _min = 10
    _max = 30
    num = random.randint(_min, _max)
    get_gold(user_id, group_id, num)


def get_item(user_id: int, group_id: int, item_id: int, num: int = 1):
    conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
    cursor = conn.cursor()
    sql = f'SELECT item_num FROM user_package WHERE user_id = {user_id} AND group_id = {group_id} AND item_id = {item_id}'
    sql2 = f'UPDATE  user_package SET item_num = item_num + {num} WHERE user_id = {user_id} ' \
           f'AND group_id = {group_id} AND item_id = {item_id}'
    sql3 = f'INSERT INTO user_package (user_id,group_id,item_id,item_num) VALUES ({user_id},{group_id},{item_id},{num})'
    cursor.execute(sql)
    result = cursor.fetchone()
    if result is None:
        cursor.execute(sql3)
        conn.commit()
    else:
        cursor.execute(sql2)
        conn.commit()
    conn.close()


def cost_item(user_id: int, group_id: int, item_id: int, num: int = 1):
    conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
    cursor = conn.cursor()
    sql = f'SELECT item_num FROM user_package WHERE user_id = {user_id} AND group_id = {group_id} AND item_id = {item_id}'
    sql2 = f'UPDATE  user_package SET item_num = item_num - {num} WHERE user_id = {user_id} ' \
           f'AND group_id = {group_id} AND item_id = {item_id}'
    cursor.execute(sql)
    result = cursor.fetchone()
    if result is None or result[0] < num:
        raise Exception('可交易物品不足！')
    else:
        cursor.execute(sql2)
        conn.commit()
    conn.close()


def trade(from_id: int, to_id: int, group_id: int, item_id: int, gold_num: int, num: int = 1):
    """
    交易物品
    :param gold_num: 交易金额
    :param num: 交易数量
    :param item_id: 交易物品编号
    :param from_id:卖家QQ
    :param to_id: 买家QQ
    :param group_id: 群号
    """
    cost_item(from_id, group_id, item_id, num)
    cost_gold(to_id, group_id, gold_num)
    get_item(to_id, group_id, num)
    get_gold(from_id, group_id, gold_num)


def sell(user_id: int, group_id: int, item_id: int, num: int = 1):
    """
    出售物品给商店
    :param num: 出售数量
    :param user_id: QQ号
    :param group_id: 群号
    :param item_id: 物品id
    """
    cost_item(user_id, group_id, item_id, num)
    get_gold(user_id, group_id, ITEM_PRICE[item_id] * num)


if __name__ == '__main__':
    pass
