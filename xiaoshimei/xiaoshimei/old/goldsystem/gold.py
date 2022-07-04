
import pymysql
from xiaoshimei.plugins.goldsystem.globals import EXTRA_MODULES,EXTRA_MODULES3
OK = 0
ERROR = 1
ITEM_PRICE = {
    0: 20,
    1: 20,
    2: 10,
    3: 13,
    4: 100,
    5: 100,
    6: 50,
    7: 65,
    8: 2000,
    9: 2000,
    10: 2000,
    11: 2000,
    12: 2,
    13: 10,
    14: 160,
    15: 4,
    16: 20,
    17: 220,
    18: 20,
    19: 1,
    30: 6000,
    31: 35000,
    32: 5000,
    33: 5000,
    34: 5000,
    35: 5000,
    36: 9999999,
    37: 50,
    38: 75,
    39: 100,
    40: 150,
    41: 200,
    42: 500,



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


def shop_limit(user_id, group_id,item_id):
    """
    阿瑞斯购买记录
    :param item_id: 物品编号
    :param user_id:QQ number
    :param group_id:QQ group number
    :return:是否购买过。购买过返回True,否则False
    """
    conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
    cursor = conn.cursor()
    sql = f'SELECT item_num FROM shop_limit WHERE user_id = {user_id} AND group_id = {group_id} AND item_id = {item_id}'
    cursor.execute(sql)
    data = cursor.fetchone()
    conn.close()
    if data is None:
        return False
    else:
        return data[0]


def add_shop_limit(user_id, group_id,item_id,num=1):
    conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
    cursor = conn.cursor()
    sql = f'SELECT item_num FROM shop_limit WHERE user_id = {user_id} AND group_id = {group_id} AND item_id = {item_id}'
    sql2 = f'UPDATE shop_limit SET item_num = item_num + {num} WHERE user_id = {user_id} ' \
           f'AND group_id = {group_id} AND item_id = {item_id}'
    sql3 = f'INSERT INTO shop_limit (user_id,group_id,item_id,item_num) VALUES ({user_id},{group_id},{item_id},{num})'
    cursor.execute(sql)
    result = cursor.fetchone()
    if result is None:
        cursor.execute(sql3)
        conn.commit()
    else:
        cursor.execute(sql2)
        conn.commit()
    conn.close()


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
        conn.commit()
    else:
        cursor.execute(sql3)
        conn.commit()
    conn.close()


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
        return 2
    elif data[0] < num:
        return 1
    else:
        cursor.execute(sql3)
        conn.commit()
        conn.close()
        return OK


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
    sql = f"SELECT * FROM user_package WHERE user_id = {user_id} AND group_id = {group_id} AND item_id = {item_id}"
    sql2 = f'UPDATE user_package SET item_num = item_num - {num} WHERE user_id = {user_id} ' \
           f'AND group_id = {group_id} AND item_id = {item_id}'
    cursor.execute(sql)
    result = cursor.fetchone()
    if result:
        uni_id = result[4]
        item_num = result[3]
        if item_num == num:
            sql3 = f'DELETE FROM user_package WHERE item_uni_id = {uni_id}'
            cursor= conn.cursor()
            cursor.execute(sql3)
            conn.commit()
        elif item_num > num:
            cursor= conn.cursor()
            cursor.execute(sql2)
            conn.commit()
        else:
            return ERROR
    else:
        return ERROR
    conn.close()
    return OK


def cost_weapon(weapon_id):
    sql = f"SELECT item_uni_id FROM strength WHERE weapon_id = {weapon_id}"
    sql2 = f'DELETE FROM strength WHERE weapon_id = {weapon_id}'
    conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    uni_id = result[0]
    cursor = conn.cursor()
    cursor.execute(sql2)
    conn.commit()
    sql3 = f"UPDATE user_package SET item_num = item_num - 1 WHERE item_uni_id = {uni_id}"
    cursor = conn.cursor()
    cursor.execute(sql3)
    conn.commit()
    conn.close()


def sell(user_id: int, group_id: int, item_id: int, num: int = 1):
    """
    出售物品给商店
    :param num: 出售数量
    :param user_id: QQ号
    :param group_id: 群号
    :param item_id: 物品id
    """
    if not cost_item(user_id, group_id, item_id, num):
        get_gold(user_id, group_id, ITEM_PRICE[item_id] * num)
        return 0
    else:
        return 1


def query(user_id:int,group_id:int,item_id_list=None):
    if not item_id_list:
        area = ""
    else:
        area = f" AND item_id in ({','.join([str(i) for i in item_id_list])})"
    sql2 = f'SELECT * FROM user_package WHERE user_id = {user_id} AND group_id = {group_id}{area}'
    conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute(sql2)
    result = cursor.fetchall()
    list_of_pack = [0]*100
    for items in result:
        if items[3]:
            list_of_pack[items[2]] = items[3]
    return list_of_pack


def get_permit_group(group_id):
    sql2 = f'SELECT permission FROM permit_group WHERE group_id = {group_id}'
    conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute(sql2)
    result = cursor.fetchone()
    conn.close()
    if result is None:
        return None
    elif result[0] == 0:
        return False
    else:
        return True


def set_permit_group(group_id,permit=1):
    permission = get_permit_group(group_id)
    sql = f"INSERT INTO permit_group (group_id,permission) VALUES ({group_id},{permit})"
    sql2 = f"UPDATE permit_group SET permission = {permit} WHERE group_id = group_id"
    conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
    cursor = conn.cursor()
    if permission is None:
        cursor.execute(sql)
        conn.commit()
    else:
        cursor.execute(sql2)
        conn.commit()
    conn.close()
    return 1


def authority(group_id):
    """
    查询权限
    :param group_id: 群号
    :return: 权限列表 0：未开启；1：开启；2：限时开启
    """
    sql2 = f'SELECT * FROM extra WHERE group_id = {group_id}'
    conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute(sql2)
    result = cursor.fetchone()
    if not result:
        cursor = conn.cursor()
        sql = f"INSERT INTO extra (group_id) VALUES ({group_id})"
        cursor.execute(sql)
        conn.commit()
        return [0]*(len(EXTRA_MODULES))
    return result


def change_authority(group_id,module_list,status_list):
    """
    变更权限
    :param group_id: 群号
    :param module_list: 模块列表
    :param status_list: 状态列表 0：未开启；1：开启；2：限时开启
    :return:
    """
    conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
    cursor = conn.cursor()
    sql3 = ','.join([f"{module_list[i]}={status_list[i]}" for i in range(len(module_list))])
    sql2 = f'UPDATE extra SET {sql3} WHERE group_id = {group_id}'
    cursor.execute(sql2)
    conn.commit()
    conn.close()


def authority2(group_id):
    """
    查询权限
    :param group_id: 群号
    :return: 权限列表 0：未开启；1：开启；2：限时开启
    """
    field = [EXTRA_MODULES[i[0]] for i in EXTRA_MODULES3]
    sql2 = f'SELECT {",".join(field)} FROM extra WHERE group_id = {group_id}'
    conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute(sql2)
    result = cursor.fetchone()
    if not result:
        cursor = conn.cursor()
        sql = f"INSERT INTO extra (group_id) VALUES ({group_id})"
        cursor.execute(sql)
        conn.commit()
        return [0]*(len(EXTRA_MODULES3))
    return result


def superuser(user_id,group_id):
    conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
    cursor = conn.cursor()
    sql2 = f'SELECT user_id FROM superuser WHERE user_id = {user_id} AND group_id = {group_id}'
    cursor.execute(sql2)
    result = cursor.fetchone()
    conn.close()
    if result:
        return True
    else:
        return False


def add_superuser(user_id,group_id):
    conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
    cursor = conn.cursor()
    sql2 = f'SELECT user_id FROM superuser WHERE user_id = {user_id} AND group_id = {group_id}'
    cursor.execute(sql2)
    result = cursor.fetchone()
    conn.close()
    if result:
        return 0
    else:
        conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
        cursor = conn.cursor()
        sql = f'INSERT INTO superuser (user_id,group_id) VALUES ({user_id},{group_id})'
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return 1


def remove_superuser(user_id,group_id):
    conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
    cursor = conn.cursor()
    sql2 = f'SELECT user_id FROM superuser WHERE user_id = {user_id} AND group_id = {group_id}'
    cursor.execute(sql2)
    result = cursor.fetchone()
    conn.close()
    if not result:
        return 0
    else:
        conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
        cursor = conn.cursor()
        sql = f'DELETE FROM superuser WHERE user_id = {user_id} AND group_id = {group_id}'
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return 1


def baozhu_query(user_id,group_id):
    conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
    cursor = conn.cursor()
    sql2 = f'SELECT * FROM baozhu WHERE user_id = {user_id} AND group_id = {group_id}'
    cursor.execute(sql2)
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[2:]
    else:
        conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
        cursor = conn.cursor()
        sql = f'INSERT INTO baozhu (user_id,group_id) VALUES ({user_id},{group_id})'
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return [0] * 56


baozhu_name_list = ['bs4','qj4','js4','cj4','cf4','rh4','xx4','bj4','hbao4','hbing4','fengy4','lj4','zs4','zshang4','yd4',
               'xs4','jshang4','hf4','jn4','jr4','mk4','shif4',
               'shangh4','hj4','gj4','fy4','mj4','xy4']
sbaozhu_name_list = ["s"+i for i in baozhu_name_list]
baozhu_name_list = baozhu_name_list + sbaozhu_name_list


def get_baozhu(user_id,group_id,baozhu_num_list:list):
    baozhu_query(user_id,group_id)
    conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
    cursor = conn.cursor()
    sql2 = []
    for i,num in enumerate(baozhu_num_list):
        if num:
            sql2 = sql2.append(f'{baozhu_num_list[i]} = {baozhu_num_list[i]} + {num}')
    sql = f'UPDATE baozhu SET {",".join(sql2)} WHERE user_id = {user_id} AND group_id = {group_id}'
    cursor.execute(sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    pass
