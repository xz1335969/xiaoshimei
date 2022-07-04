import random
import datetime
import time
import re
import pymysql
from nonebot import on_command, CommandSession, MessageSegment
import xiaoshimei.plugins.goldsystem.createImage as createImage

TYPELIST = {
    "weapon": 0,
    "shield": 1,
    "item": 2,
}

EXTRA_MODULES = [
    'group_id',  # 0
    'setujinyan',  # 1
    'help',  # 2
    'ipackage',  # 3
    'legend_box',  # 4
    'fake_rl',  # 5
    'sell',  # 6
    'drillshop',  # 7
    'danwang',  # 8
    'chaoshen',  # 9
    'Sboomerang',  # 10
    'strength',  # 11
    'monijinglian',  # 12
    'signin',  # 13
    'gold_query',  # 14
    'gold_present',  # 15
    'gold_shop',  # 16
    'rob',  # 17
    'gamble',  # 18
    'guess_coin',  # 19
    'wawale',  # 20
    'heisi',  # 21
    'leavemsg',  # 22
    'leave_private_msg',  # 23
    'left_msg',  # 24
    'left_msg_all',  # 25
    'love',  # 26
    'kiss',  # 27
    'away',  # 28
    'sleep_time',  # 29
    'sleep_list',  # 30
    'group_release_all',  # 31
    'blessing',

]

EXTRA_MODULES2 = [
    '涩图禁言',  # 1
    '仓库',  # 3
    '神器盒子',  # 4
    '模拟熔炼',  # 5
    '出售物品',  # 6
    '钻头商城',  # 7
    '弹王兑换',  # 8 9 10
    '模拟强化',  # 11
    '模拟精炼',  # 12
    '签到',  # 13 14 15 16
    '抢劫',  # 17
    '金币小游戏',  # 18 19 20
    '留言',  # 22 23 24 25
    '小师妹交流',  # 26 27 28 21
    '睡眠套餐',  # 29 30 31

]

EXTRA_MODULES3 = [[1], [3], [4], [5], [6], [7], [8, 9, 10], [11], [12], [13, 14, 15, 16], [17], [18, 19, 20],
                  [22, 23, 24, 25], [28, 27, 28, 21], [29, 30, 31]]


def authority(group_id):
    """
    查询权限
    :param group_id: 群号
    :return: 权限列表 0：未开启；1：开启；2：限时开启
    """
    sql2 = f'SELECT * FROM extra WHERE group_id = {group_id}'
    conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei', charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute(sql2)
    result = cursor.fetchone()
    if not result:
        cursor = conn.cursor()
        sql = f"INSERT INTO extra (group_id) VALUES ({group_id})"
        cursor.execute(sql)
        conn.commit()
        return [0] * (len(EXTRA_MODULES))
    return result


def change_authority(group_id, module_list, status_list):
    """
    变更权限
    :param group_id: 群号
    :param module_list: 模块列表
    :param status_list: 状态列表 0：未开启；1：开启；2：限时开启
    :return:
    """
    conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei', charset='utf8mb4')
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
    conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei', charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute(sql2)
    result = cursor.fetchone()
    if not result:
        cursor = conn.cursor()
        sql = f"INSERT INTO extra (group_id) VALUES ({group_id})"
        cursor.execute(sql)
        conn.commit()
        return [0] * (len(EXTRA_MODULES3))
    return result


def num_list_to_str(num_list: list):
    return [f"{i}" for i in num_list]


def randomlist(list1: list):
    """
    将list打乱顺序后返回
    :param list1: 输入list
    :return: 打乱顺序的list
    """
    for i in range(len(list1) - 1):
        num = random.randint(i, len(list1) - 1)
        _ = list1[num]
        list1[num] = list1[i]
        list1[i] = _
    return list1


def overrandom(box: dict):
    """
    加权随机函数：
    从box中的所有物品进行加权随机
    :param box:键为要进行随机选取的物品名称，值为所占的权重
    :return: 随机结果
    """
    sum0 = sum(box.values())
    randomnum = random.randint(0, sum0 - 1)
    for items in box:
        if randomnum < box[items]:
            return items
        else:
            randomnum -= box[items]


def get_qq(cq_msg):
    res = re.findall(r'[Qq]{2}=(\w+)]', cq_msg)
    if len(res):
        return res[0]
    else:
        return None


# user_package
# uni_id  player_id  item_id  count  type


# user_detail
# player_id  user_id  group_id  gold  rob_ban  is_superuser
#
# group_permission
# 不变
#
# item_details
# item_id name type  property1 property2 fusion_id  fusion_probability

# (201,"1级强化石",2,75,0,202,89),(202,"2级强化石",2,300,0,203,89),(203,"3级强化石",2,1200,0,204,89),
# (204,"4级强化石",2,4800,0,205,100),205,"5级强化石",2,24000,0,0,0),(206,"神恩符",2,0,0,0,0),(207,"幸运符15%",2,15,0,0,0),
# (208,"幸运符25%",2,25,0,0,0),(211,"攻击祝福宝珠",2,20,0,0,0)(299,"护身符",2,0,0,0,0)

# (220,"真·爱心回力标初级碎片",2,0,0,230,89),
# (221,"真·牛头怪初级碎片",2,0,0,231,89),
# (222,"真·远古竹枪初级碎片",2,0,0,232,89),
# (223,"真·小鸡初级碎片",2,0,0,233,89),
# (224,"真·天使之赐初级碎片",2,0,0,234,89),
# (225,"巴罗夫的盾牌初级碎片",2,0,0,235,89),
# (230,"真·爱心回力标高级碎片",2,0,0,0,2),
# (231,"真·牛头怪高级碎片",2,0,0,0,2),
# (232,"真·远古竹枪高级碎片",2,0,0,0,2),
# (233,"真·小鸡高级碎片",2,0,0,0,2),
# (234,"真·天使之赐高级碎片",2,0,0,0,6),
# (235,"巴罗夫的盾牌高级碎片",2,0,0,0,6)

# (1,"真·牛头怪",0,242,5,0,0)
# (2,"真·远古竹枪",0,242,5,0,0)
# (3,"真·疯狂小鸡",0,242,5,0,0)
# (4,"真·天使之赐",3,0,0,0,0)
# (5,"巴罗夫的盾牌",1,80,4,0,0)
# (6,"真·爱心回力标",0,242,5,0,0)
# (10,"烈火",0,205,3,0,0)
# (11,"轰天",0,190,3,0,0)
# (12,"雷霆",0,200,3,0,0)
# (13,"神风",0,200,3,0,0)
# (15,"爱心回力标",0,230,4,0,0)
# (16,"牛头怪",0,230,4,0,0)
# (17,"远古竹枪",0,230,4,0,0)
# (20,"真·烈火",0,205,4,0,0)
# (21,"真·轰天",0,190,4,0,0)
# (22,"真·雷霆",0,200,4,0,0)
# (23,"真·神风",0,200,4,0,0)
# (24,"真·黑白家电",0,200,4,0,0)
# (25,"真·司马砸缸",0,200,4,0,0)
# (26,"真·畅通利器",0,200,4,0,0)
# (27,"真·牛顿水果篮",0,195,4,0,0)
# (28,"真·医用工具箱",0,200,4,0,0)
# (30,"极·烈火",0,225,4,0,0)
# (31,"极·轰天",0,209,4,0,0)
# (32,"极·雷霆",0,220,4,0,0)
# (33,"极·神风",0,220,4,0,0)
# (34,"极·黑白家电",0,220,4,0,0)
# (35,"极·司马砸缸",0,220,4,0,0)
# (36,"极·畅通利器",0,220,4,0,0)
# (37,"极·牛顿水果篮",0,215,4,0,0)
# (38,"极·医用工具箱",0,220,4,0,0)
# (40,"极·飞天跑车",0,230,4,0,0)
# (41,"极·工作狂",0,230,4,0,0)
# (42,"极·圣火之炬",0,230,4,0,0)
# (43,"极·飞天帚",0,230,4,0,0)
# (44,"极·魔力水枪",0,230,4,0,0)
# (45,"天天向上",0,230,4,0,0)
# (46,"极·圣诞派",0,230,4,0,0)
# (50,"棒棒糖",0,252,5,0,0)
# (51,"加农神炮",0,252,5,0,0)
# (52,"收割者之镰",0,252,5,0,0)
# (53,"捣蛋鬼",0,252,5,0,0)
# (60,"弹王回力标",0,275,6,0,0)
# (61,"极·爱心回力标",0,285,7,0,0)
# (62,"守护者法杖",0,247,9,0,0)
# (63,"花之恋",0,247,9,0,0)
# (70,"碎石斧",0,175,1,0,0),
# (71,"硬弩弓",0,175,1,0,0),
# (72,"AK-48",0,180,2,0,0),
# (73,"黄金枪",0,180,2,0,0),
# (74,"裂地金斧",0,180,2,0,0),
# (75,"击天金弓",0,180,2,0,0)


# item_id count price shop_limit=0 limit_type=0
# (70,1,100,0,0)
# (72,1,200,0,0)
# (12,1,400,0,0)
# (22,1,1000,0,0)
# (32,1,1500,1,4)
# (32,1,2000,0,0)
# (46,1,3000,0,0)
# (299,1,0,1,1)


# 物品ID    类型    参数1
# weapon
# weapon_id  item_id  uni_id  player_id  strength_lvl
# 自增
#
# shop_limit
# shop_id  player_id  bought_num

class Item:
    def __init__(self, item_id: int, count=0, price=0):
        self.uni_id = None
        self.item_id = item_id
        conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei',
                               charset='utf8mb4')
        cursor = conn.cursor()
        sql = f"SELECT * FROM item_details WHERE item_id = {self.item_id}"
        cursor.execute(sql)
        result = cursor.fetchone()
        self.name = result[1]
        self.type = result[2]
        self.property1 = result[3]
        self.property2 = result[4]
        self.fusion_id = result[5]
        self.fusion_probability = result[6]
        self.count = count
        self.price = price
        self.shop_limit = None
        self.bought_times = None
        self.limit_type = 0
        conn.close()


class Weapon(Item):
    def __init__(self, weapon_id: int):
        self.weapon_id = weapon_id
        conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei',
                               charset='utf8mb4')
        cursor = conn.cursor()
        sql = f"SELECT * FROM weapon WHERE weapon_id = {self.weapon_id}"
        cursor.execute(sql)
        result = cursor.fetchone()
        self.item_id = result[1]
        self.uni_id = result[2]
        self.player_id = result[3]
        self.strength_lvl = result[4]
        self.durability = result[5]
        Item.__init__(self, self.item_id)
        self.baseDamage = self.property1
        self.quality = self.property2
        self.damage = int(self.baseDamage * (1.1 ** self.strength_lvl))

    def refresh(self):
        sql = f"UPDATE weapon SET strength_lvl = {self.strength_lvl},durability = {self.durability} WHERE weapon_id = {self.weapon_id}"
        conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei',
                               charset='utf8mb4')
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()

    def destroy(self):
        sql = f"DELETE FROM weapon WHERE weapon_id = {self.weapon_id}"
        conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei',
                               charset='utf8mb4')
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()


class Shield(Item):
    def __init__(self, weapon_id: int):
        self.weapon_id = weapon_id
        conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei',
                               charset='utf8mb4')
        cursor = conn.cursor()
        sql = f"SELECT * FROM weapon WHERE weapon_id = {self.weapon_id}"
        cursor.execute(sql)
        result = cursor.fetchone()
        self.item_id = result[1]
        self.uni_id = result[2]
        self.user_id = result[3]
        self.strength_lvl = result[4]
        Item.__init__(self, self.item_id)
        self.baseGuard = self.property1
        self.quality = self.property2
        self.guard = int(self.baseGuard * (1.1 ** self.strength_lvl))

    def refresh(self):
        sql = f"UPDATE weapon SET strength_lvl = {self.strength_lvl} WHERE weapon_id = {self.weapon_id}"
        conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei',
                               charset='utf8mb4')
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()

    def destroy(self):
        sql = f"DELETE FROM weapon WHERE weapon_id = {self.weapon_id}"
        conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei',
                               charset='utf8mb4')
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()


# user_detail
# player_id  user_id  group_id  gold  rob_ban


class Person:
    def __init__(self, user_id: int, group_id: int, player_id=None):
        if not (player_id is None):
            sql = f'SELECT (user_id,gold,rob_ban,is_superuser,vip_end_time,group_id)' \
                  f' from user_detail WHERE player_id = player_id'
            conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei',
                                   charset='utf8mb4')
            cursor = conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is None:
                raise Exception("No such player_id")
            else:
                self.user_id = result[0]
                self.group_id = result[5]
                self.gold = result[1]
                self.rob_ban = result[2]
                self.is_superuser = result[3]
                self.vip_end_time = result[4]
            conn.close()
            now = datetime.datetime.now()
            now.strftime("%Y-%m-%d %H:%M:%S")
            self.is_vip = 0 if now > self.vip_end_time else 1
            self.user_id = user_id
            self.group_id = group_id
            self.weapon = self.weapon_query()
            self.shield = self.shield_query()
            self.package = self.query()
        if user_id == 0:
            self.package = {}
            self.gold = 0
            self.weapon = []
            self.shield = []
            self.user_id = 0
        else:
            sql = f'SELECT (player_id,gold,rob_ban,is_superuser,vip_end_time)' \
                  f' from user_detail WHERE user_id = {user_id} AND group_id = {group_id}'
            conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei',
                                   charset='utf8mb4')
            cursor = conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is None:
                sql = f'INSERT INTO user_detail VALUES (Null,{user_id},{group_id},0,0,0)'
                cursor2 = conn.cursor()
                cursor2.execute(sql)
                conn.commit()
                self.__init__(user_id, group_id)
            else:
                self.player_id = result[0]
                self.gold = result[1]
                self.rob_ban = result[2]
                self.is_superuser = result[3]
                self.vip_end_time = result[4]
            conn.close()
            now = datetime.datetime.now()
            now.strftime("%Y-%m-%d %H:%M:%S")
            self.is_vip = 0 if now > self.vip_end_time else 1
            self.user_id = user_id
            self.group_id = group_id
            self.weapon = self.weapon_query()
            self.shield = self.shield_query()
            self.package = self.query()

    def query(self, item_id_list=None, item_type_list=None):
        pack = {}
        if not item_id_list:
            area = ""
        else:
            area = f" AND item_id in ({','.join([str(i) for i in item_id_list])})"
        if not item_type_list:
            types = ""
        else:
            types = f" AND type in ({','.join([str(i) for i in item_id_list])})"
        conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei',
                               charset='utf8mb4')
        cursor = conn.cursor()
        sql = f'SELECT * FROM user_package WHERE user_id = {self.user_id} AND group_id = {self.group_id} AND count > 0' + area + types
        cursor.execute(sql)
        result = cursor.fetchone()
        while result:
            item_id = result[2]
            count = result[3]
            item = Item(item_id)
            item.count = count
            item.uni_id = result[0]
            pack[item_id] = item
            result = cursor.fetchone()
        conn.close()
        return pack

    def refresh(self):
        conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei',
                               charset='utf8mb4')
        cursor = conn.cursor()
        sql = f'UPDATE user_detail SET gold = {self.gold} ' \
              f'AND is_superuser = {self.is_superuser} ' \
              f'AND rob_ban = {self.rob_ban} ' \
              f'AND vip_end_time = {self.vip_end_time.strftime("%Y-%m-%d %H:%M:%S")}' \
              f'WHERE player_id = {self.player_id}'
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return 1

    def refresh_all(self):
        conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei',
                               charset='utf8mb4')
        cursor = conn.cursor()
        sql = f'UPDATE user_detail SET gold = {self.gold} ' \
              f'AND is_superuser = {self.is_superuser} ' \
              f'AND rob_ban = {self.rob_ban} ' \
              f'AND vip_end_time = {self.vip_end_time.strftime("%Y-%m-%d %H:%M:%S")}' \
              f'WHERE player_id = {self.player_id}'
        cursor.execute(sql)
        conn.commit()
        cursor = conn.cursor()
        for item in self.package.values():
            sql2 = f'UPDATE user_package SET count = {item.count} WHERE item_id = {item.item_id}'
            sql3 = f'INSERT INTO user_package VALUES (0,{self.player_id},{item.item_id},0,{item.type}) IF NOT' \
                   f' EXIST (SELECT * FROM user_package WHERE player_id = {self.player_id} AND item_id = {item.item_id})'
            cursor.execute(sql3)
            conn.commit()
            cursor.execute(sql2)
            conn.commit()
        conn.close()
        return 1

    # user_package
    # uni_id  player_id  item_id  count  type

    # weapon
    # weapon_id  item_id  uni_id  player_id  strength_lvl
    # 自增

    def weapon_query(self, item: Item = None, *args):
        weapons = []
        conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei',
                               charset='utf8mb4')
        if item is None:
            field = self.query(None, TYPELIST["weapon"])
        else:
            if len(args):
                field = [item] + [i for i in args]
            else:
                field = [item]
        if len(field) == 0:
            return None
        for item in field:
            if item.count == 0:
                continue
            sql = f"SELECT * FROM weapon WHERE uni_id = {item.uni_id}"
            cursor = conn.cursor()
            cursor.execute(sql)
            for i in range(item.count):
                result = cursor.fetchone()
                weapon_id = result[0]
                weapon = Weapon(weapon_id)
                weapons.append(weapon)
        conn.close()
        return weapons

    def shield_query(self, item: Item = None, *args):
        shields = []
        conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei',
                               charset='utf8mb4')
        if item is None:
            field = self.query(None, TYPELIST["shield"])
        else:
            if len(args):
                field = [item] + [i for i in args]
            else:
                field = [item]
        if len(field) == 0:
            return None
        for item in field:
            if item.count == 0:
                continue
            sql = f"SELECT * FROM weapon WHERE uni_id = {item.uni_id}"
            cursor = conn.cursor()
            cursor.execute(sql)
            for i in range(item.count):
                result = cursor.fetchone()
                weapon_id = result[0]
                weapon = Weapon(weapon_id)
                shields.append(weapon)
        conn.close()
        return shields

    def get_item(self, item: Item, count: int):
        self.package.setdefault(item.item_id, item)
        self.package[item.item_id].count += count

    def signin(self):
        _min = 50
        _max = 800
        today = time.strftime("%Y%m%d", time.localtime())
        today0 = int(today) * 1000000
        month0 = int(time.strftime("%Y%m", time.localtime())) * 10 ** 8
        conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei',
                               charset='utf8mb4')
        sql = f'SELECT * from signin WHERE player_id = {self.player_id} AND time > {today0}'
        cursor = conn.cursor()
        cursor.execute(sql)
        issigned = cursor.fetchone()
        if not issigned:
            gold_num = random.randint(_min, _max)
            self.gold += gold_num
            report = f'[CQ:at,qq={self.user_id}]签到成功，获得{gold_num}金币'
            cursor2 = conn.cursor()
            sql2 = f'INSERT INTO signin player_id VALUES {self.player_id}'
            cursor2.execute(sql2)
            conn.commit()
            cursor3 = conn.cursor()
            sql2 = f'SELECT time FROM signin WHERE player_id = {self.player_id} AND time > {month0}'
            cursor3.execute(sql2)
            signed_times = len(cursor3.fetchall())
            if signed_times == 3:
                report = report + "\n" + "您本月已经签到3天，获得奖励：3级强化石*5"
                self.package.setdefault(203, Item(203))
                self.package[203].count += 5
            elif signed_times == 7:
                report = report + "\n" + "您本月已经签到7天，获得奖励：4级强化石*5"
                self.package.setdefault(204, Item(204))
                self.package[204].count += 5
            elif signed_times == 14:
                report = report + "\n" + "您本月已经签到14天，获得奖励：5级强化石*3"
                self.package.setdefault(205, Item(205))
                self.package[205].count += 3
            elif signed_times == 21:
                report = report + "\n" + "您本月已经签到21天，获得奖励：5级强化石*5,神恩符*3,4000金币，攻击祝福宝珠*3"
                self.package.setdefault(205, Item(205))
                self.package.setdefault(206, Item(206))
                self.package.setdefault(211, Item(211))
                self.package[205] += 5
                self.package[206] += 3
                self.package[211] += 3
                self.gold += 4000
            elif signed_times == 28:
                report = report + "\n" + "您本月已经签到28天，获得奖励：VIP*7天，VIP下商店物品8折，强化成功率提升30%"
                endtime = datetime.datetime.now() + datetime.timedelta(days=7)
                self.vip_end_time = endtime
        else:
            report = f"[CQ:at,qq={self.user_id}]您今天已经签到过了！"
        self.refresh_all()
        return report

    def print_package(self):
        item_num = len(self.package)
        if item_num:
            bag = createImage.init_empty_bag(item_num)
            item_list = [
                {'name': item.item_id, "count": item.count}
                for item in self.package.values()
            ]
            createImage.draw_item_by_list(bag, item_list)
            bag.save('C:/temp/out.png')
            return 1
        else:
            return 0

    def print_package_txt(self):
        return "\n".join([f"{i.item_id}:{i.name}" for i in self.package.values()])


# now = time.strftime("%Y%m%d%H%M%S", time.localtime())
# shop
# shop_id(自增) item_id count=1 price  shop_limit  limit_type(0无限制 1总限制 2月限制 3日限制)

# shop_limit
# shop_id  player_id  bought_time  count


class Shop:
    def __init__(self, player: Person):
        self.show_list = None
        conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei',
                               charset='utf8mb4')
        cursor = conn.cursor()
        sql = f"SELECT * FROM shop"
        cursor.execute(sql)
        result = cursor.fetchall()
        self.goods_list = []
        self.shop_id_list = []
        self.player = player
        self.vip = player.is_vip
        sql = f"SELECT (shop_id,bought_time,count) FROM shop_limit WHERE player_id = {player.player_id}"
        cursor = conn.cursor()
        cursor.execute(sql)
        result2 = cursor.fetchall()

        def bought_times(shop_id, limit_type):
            now = datetime.datetime.now()
            summary = 0
            if limit_type == 1:
                for i in result2:
                    if i[0] == shop_id:
                        summary += i[2]
                return summary
            elif limit_type == 2:
                for i in result2:
                    bought_time = i[1]
                    if i[0] == shop_id and (bought_time - now).month < 1 and bought_time.month == now.month:
                        summary += i[2]
                return summary
            elif limit_type == 3:
                for i in result2:
                    bought_time = i[1]
                    if i[0] == shop_id and (bought_time - now).day < 1 and bought_time.day == now.month:
                        summary += i[2]
                return summary

        conn.close()
        for good in result:
            item = Item(good[1])
            item.shop_id = good[0]
            item.count = good[2]
            item.price = good[3] * (1 - 0.2 * self.vip)
            item.shop_limit = good[4]
            item.limit_type = good[5]
            item.bought_times = bought_times(item.shop_id, item.limit_type)
            self.goods_list.append(item)
            self.shop_id_list.append(item.shop_id)

    def showlist(self):
        report = "您目前具有VIP资格，商店物品8折处理 \n" if self.vip else ""
        report = report + "请选择您要购买的商品编号："
        show_list = []
        for good in self.goods_list:
            if good.limit_type:
                shop_limit = good.shop_limit
                bought_time = good.bought_times
                rest = shop_limit - bought_time
                if rest == 0:
                    continue
                limit_type_txt = [None, "", "本月", "今日"]
                rest_txt = f"({limit_type_txt[good.limit_type]}剩余{rest})"
            else:
                rest_txt = ''
            shopid = good.shop_id
            num = f" *{good.count}" if good.count > 1 else ""
            name = good.name
            price = good.price
            report = report + f"\n{shopid}: {name}{num}({price}金币){rest_txt}"
            show_list.append(good.shop_id)
        self.show_list = show_list
        return report


# signin   player_id  time (current_time_stamp)


@on_command("signin", aliases=("每日签到", '签到'), only_to_me=False)
async def signin(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    _authority = authority(group_id)
    if not _authority[13]:
        return
    elif _authority[13] == 2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    if session.current_arg.strip():
        return
    else:
        player = Person(user_id, group_id)
        report = player.signin()
    await session.send(report)
    return


@on_command("gold_query", aliases=("查询金币", "查金币"), only_to_me=False)
async def goldquery(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    _authority = authority(group_id)
    if not _authority[14]:
        return
    elif _authority[14] == 2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    arg = session.current_arg.strip()
    if arg[0] != '[' or arg[-1] != ']':
        return
    if not arg:
        player = Person(user_id, group_id)
        result = player.gold
        if not result:
            report = '您的金币数为0'
        else:
            report = f"您的金币数为{result}"
    else:
        to_id = get_qq(arg)
        player = Person(to_id, group_id)
        result = player.gold
        if not result:
            report = f'{arg}的金币数为0'
        else:
            report = f"{arg}的金币数为{result}"
    await session.send(report)


@on_command("gold_recharge", aliases="充值金币", only_to_me=False)
async def gold_recharge(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    user = Person(user_id, group_id)
    if not user.is_superuser:
        session.finish("您的权限不足")
        return
    else:
        args = session.current_arg.strip().split()
        num = int(args[0])
        if len(args) == 1:
            user.gold += num
            user.refresh()
            session.finish(f'为[CQ:at,qq={user_id}]充值{num}金币成功')
            return
        else:
            players = ''
            for i, cq in enumerate(args):
                if i == 0:
                    continue
                else:
                    qq_num = get_qq(cq)
                    player = Person(qq_num, group_id)
                    player.gold += num
                    player.refresh()
                    players = players + cq
    await session.send(f'为{players}充值{num}金币成功')


@on_command("dbs", aliases="数据库指令", only_to_me=False)
async def dbs(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    user = Person(user_id, group_id)
    if not user.is_superuser:
        session.finish("您的权限不足")
        return
    sql = session.current_arg.strip()
    conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei', charset='utf8mb4')
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
        await session.send("成功")
    except Exception:
        await session.send("发生错误" + str(Exception))
    conn.close()


@on_command("gold_present", aliases="赠送金币", only_to_me=False)
async def gold_present(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    _authority = authority(group_id)
    if not _authority[15]:
        return
    elif _authority[15] == 2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    arg = session.current_arg.strip()
    args = arg.split()
    to_qq_num = get_qq(args[1])
    num = int(args[0])
    num = (-1 * num) if num < 0 else num
    from_person = Person(user_id, group_id)
    to_person = Person(to_qq_num, group_id)
    if from_person.gold < num:
        session.finish("您的金币不足")
    else:
        from_person.gold -= num
        from_person.refresh()
        to_person.gold += num
        to_person.refresh()
        session.finish("赠送成功")


@on_command("gold_shop", aliases=("金币商店", "金币商城"), only_to_me=False)
async def gold_shop(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    _authority = authority(group_id)
    if not _authority[16]:
        return
    elif _authority[16] == 2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    player = Person(user_id, group_id)
    shop = Shop(player)
    _ = await session.aget(prompt=shop.showlist()[0])
    _1 = _.split()
    try:
        player_choice_shop_id = int(_1[0])
    except ValueError:
        session.finish("购买出错，请输入正确的编号数字")
    else:
        if player_choice_shop_id not in shop.shop_id_list:
            session.finish("购买出错，请输入正确的编号数字")
        else:
            item_to_buy = shop.goods_list[shop.shop_id_list.index(player_choice_shop_id)]
            limit_type_txt = [None, "", "本月", "今日"]
            lmt_txt = limit_type_txt[item_to_buy.limit_type]
            if player_choice_shop_id not in shop.showlist():
                session.finish(f"该物品购买数量已经达到{lmt_txt}上限")
            else:
                rest = item_to_buy.shop_limit - item_to_buy.bought_times
                if len(_1) > 1:
                    player_choice_count = int(_1[1])
                else:
                    player_choice_count = int(await session.aget(prompt=f"请输入购买数量：({lmt_txt}剩余：{rest})"))
                if player_choice_count > rest:
                    player_choice_count = int(
                        await session.aget(prompt=f"购买数量超过{lmt_txt}上限，请重新输入购买数量：({lmt_txt}剩余：{rest})"))
                if player.gold < player_choice_count * item_to_buy.price:
                    session.finish("您的金币不足")
                player.gold -= player_choice_count * item_to_buy.price
                item_to_buy.count *= player_choice_count
                if item_to_buy.item_id in player.package.keys():
                    player.package[item_to_buy.item_id].count += item_to_buy.count
                else:
                    player.package[item_to_buy.item_id] = item_to_buy
                player.refresh_all()
                sql = f'INSERT INTO shop_limit (shop_id,player_id,count) VALUES ({player_choice_shop_id, player.player_id, player_choice_count}) '
                conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei',
                                       charset='utf8mb4')
                cursor = conn.cursor()
                cursor.execute(sql)
                conn.commit()
                conn.close()
                session.finish("购买成功")


@on_command("package", aliases=("查看仓库", "查询仓库", "查看背包"), only_to_me=False)
async def package(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    player = Person(user_id, group_id)
    result = player.print_package()
    report = MessageSegment.at(user_id) + "的仓库如下" + MessageSegment.image(
        "C:/temp/out.png") if result else MessageSegment.at(user_id) + "的仓库为空"
    await session.send(report)
    return


@on_command("rob", aliases="抢劫", only_to_me=False)
async def rob(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    player = Person(user_id, group_id)
    if not authority(group_id)[17]:
        return
    elif authority(group_id)[17] == 2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
    arg = session.current_arg.strip()
    if not arg:
        await session.send(
            MessageSegment.image("C:/resources/rob_help.png") + MessageSegment.image("C:/resources/base_damage.png"))
        return
    else:
        now = datetime.datetime.now()
        today0 = now - datetime.timedelta(seconds=now.second, minutes=now.minute, hours=now.hour)
        today0_txt = today0.strftime('%Y-%m-%d %H:%M:%S')
        sql = f"SELECT time FROM rob_log WHERE player_id= {player.player_id} AND TIME > UNIX_TIMESTAMP('{today0_txt}')"
        conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei',
                               charset='utf8mb4')
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.close()
        if not (result is None) and len(result) >= 3:
            session.finish("您今天已经抢劫三次了，请明天再来")
            return
        if player.rob_ban == 1:
            await session.send("您拥有护身符，不能抢劫，请出售后重试")
            return
        player2 = Person(get_qq(arg), group_id)
        if player2.rob_ban == 1:
            await session.send("您抢劫的目标具有护身符,不能被抢劫，请选择其他人")
            return
        if player.gold <= 0:
            await session.send("您没有金币，不能抢劫")
            return
        if player2.gold <= 0:
            await session.send("对方没有金币，不能抢劫")
        player2.damage = max([weapon.damage for weapon in player2.weapon])
        player2.guard = max(shield.guard for shield in player2.shield)
        report = ''
        for i, weapon in enumerate(player.weapon):
            if weapon.durability == 0:
                continue
            str_lvl = "gold" if weapon.strength_lvl == 13 else f"+{weapon.strength_lvl}"
            report = report + '\n' + f'{i + 1}: {weapon.name}({str_lvl})(耐久：{weapon.durability})'
        weapon_choice_arg = await session.aget("weapon", prompt="请输入您要使用的武器编号：" + report)
        try:
            weapon_choice_int = int(weapon_choice_arg) - 1
        except ValueError:
            session.finish("您输入的武器编号有误")
            return
        else:
            weapon_choice = player.weapon[weapon_choice_int]
            if weapon_choice.durability <= 0:
                await session.send("您选择的武器已经损坏，无法使用,请强化或铸金之后再使用。")
                return
            player.damage = weapon_choice.damage
            base_success_prob = weapon_choice.quality * 50 + 50
            rand = random.randint(0, 999)
            base_lose_prob = player2.guard
            battle_prob = int(player.damage ** 2 * 1000 / (player2.damage ** 2 + player.damage ** 2))
            if rand <= base_success_prob:  # 抢劫基础成功  成功率与武器品质有关
                result = 1
            elif rand >= 1000 - base_lose_prob:  # 抢劫被盾挡下，失败
                result = 3
            elif rand >= 950 - base_lose_prob:  # 抢劫失败事件1,5%
                result = 4
            elif rand >= 900 - base_lose_prob:  # 抢劫失败事件2，5%
                result = 5
            else:
                rand = random.randint(0, 999)
                if rand <= battle_prob:  # 抢劫发生战斗，成功
                    result = 2
                else:  # 抢劫发生战斗，失败
                    result = 6
            # 抢劫获得金币
            group_rob_limit = 2000
            gold_get = min(int(player.gold * 1.5), int(player2.gold * 0.3), group_rob_limit)
            if result <= 2:
                player.gold += gold_get
                player2.gold -= gold_get
                report = f"抢劫成功，获得对方{gold_get}金币"
            elif result == 5:
                player.gold -= 200
                report = "潜伏时不小心受伤，损失医药费200金币，抢劫失败"
            elif result == 4:
                report = "不小心遭遇了强大野兽，只能与之战斗，抢劫失败"
            elif result == 3:
                report = "被对方盾牌挡下，抢劫失败"
            elif result == 6:
                report = "与对方发生战斗，战斗失败，抢劫失败。"
            if not result % 2:
                if weapon_choice.strength_lvl == 13:
                    report = report + "发生战斗，镀金武器不损失耐久"
                else:
                    weapon_choice.durability -= 1
                    weapon_choice.refresh()
                    report = report + "发生战斗，武器耐久损失1点"
            player.refresh()
            player2.refresh()
            await session.send(report)
            sql = f"INSERT INTO rob_log player_id VALUES {player.player_id}"
            conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei',
                                   charset='utf8mb4')
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            return


# legend_box
# item_id  count  rate

# labyrinth
# item_id  count  rate

@on_command("legend_box", aliases="神器盒子", only_to_me=False)
async def legend_box(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    player = Person(user_id, group_id)
    if not authority(group_id)[4]:
        return
    elif authority(group_id)[4] == 2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
    arg = session.current_arg.strip()
    if not arg:
        arg = await session.aget(prompt="请输入您要开启的数量：(每个盒子180金币)")
    try:
        num = int(arg)
    except ValueError:
        session.finish("您输入的数量有误！")
        return
    else:
        if num * 180 > player.gold:
            await session.send("您的金币不足！")
            return
        sql = f'SELECT * FROM legend_box'
        conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei',
                               charset='utf8mb4')
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        box_item_list = {}
        for i in result:
            item_id = i[0]
            count = i[1]
            rate = i[2]
            item = Item(item_id, count)
            box_item_list[item] = rate
        empty_person = Person(0, 0)
        for i in range(num):
            item = overrandom(box_item_list)
            if item.item_id in player.package.keys():
                player.package[item.item_id].count += item.count
            else:
                player.package[item.item_id] = item
            if item.item_id in empty_person.package.keys():
                empty_person.package[item.item_id].count += item.count
            else:
                empty_person.package[item.item_id] = item
        player.gold -= num * 180
        empty_person.print_package()
        player.refresh_all()
        await session.send(MessageSegment.at(user_id) + "您获得的物品如下：" + MessageSegment.image("C:/temp/out.png"))


@on_command("labyrinth", aliases="迷宫寻宝", only_to_me=True)
async def labyrinth(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    player = Person(user_id, group_id)
    if not authority(group_id)[7]:
        return
    elif authority(group_id)[7] == 2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
    arg = session.current_arg.strip()
    if not arg:
        arg = await session.aget(prompt="请输入您要寻宝的次数：(每次250金币)")
    try:
        num = int(arg)
    except ValueError:
        session.finish("您输入的数量有误！")
        return
    else:
        if num * 250 > player.gold:
            await session.send("您的金币不足！")
            return
        sql = f'SELECT * FROM legend_box'
        conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei',
                               charset='utf8mb4')
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        box_item_list = {}
        for i in result:
            item_id = i[0]
            count = i[1]
            rate = i[2]
            item = Item(item_id, count)
            box_item_list[item] = rate
        empty_person = Person(0, 0)
        for i in range(num):
            item = overrandom(box_item_list)
            if item.item_id in player.package.keys():
                player.package[item.item_id].count += item.count
            else:
                player.package[item.item_id] = item
            if item.item_id in empty_person.package.keys():
                empty_person.package[item.item_id].count += item.count
            else:
                empty_person.package[item.item_id] = item
        player.gold -= num * 250
        empty_person.print_package()
        player.refresh_all()
        await session.send(MessageSegment.at(user_id) + "您获得的物品如下：" + MessageSegment.image("C:/temp/out.png"))


@on_command("add_superuser", aliases="添加管理员", only_to_me=False)
async def add_superuser(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    arg = session.current_arg.strip()
    if user_id != 645577403:
        return
    else:
        user_id = get_qq(arg)
        player = Person(user_id, group_id)
        player.is_superuser = 1
        player.refresh()


@on_command("delete_superuser", aliases=("移除管理员", "删除管理员"), only_to_me=False)
async def delete_superuser(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    arg = session.current_arg.strip()
    if user_id != 645577403:
        return
    else:
        user_id = get_qq(arg)
        player = Person(user_id, group_id)
        player.is_superuser = 0
        player.refresh()


@on_command("simulate_fusion", aliases="模拟熔炼", only_to_me=False)
async def simulate_fusion(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    player = Person(user_id, group_id)
    if not authority(group_id)[5]:
        return
    elif authority(group_id)[5] == 2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
    arg = session.current_arg.strip()
    empty_player = Person(0, 0)
    _type = 0
    for item in player.package.values():
        if item.count >= 4 and item.fusion_id != 0:
            empty_player.package[item.item_id] = item
    if arg == "批量":
        _type = 1
    player_choice_txt = await session.aget(prompt="请选择您要熔炼的物品ID\n" + empty_player.print_package_txt())
    item_id_choice = int(player_choice_txt)
    if item_id_choice not in empty_player.package.keys():
        session.finish("物品数量不足")
        return
    else:
        item_choice = player.package[item_id_choice]
        player.package.setdefault(item_choice.fusion_id, Item(item_choice.fusion_id))
        item_product = player.package[item_choice.fusion_id]
        if _type:
            report = "熔炼结果："
            arg = await session.aget("请输入熔炼次数（为防止刷屏，超过30次将自动折叠）")
            if arg == "全部":
                num = item_choice.count // 4
            else:
                num = int(arg)
            if num > 30 or item_choice.fusion_probability == 100:
                _sum = 0
                for i in range(num):
                    if item_choice.count < 4:
                        break
                    else:
                        item_choice.count -= 4
                        rand = random.randint(0, 99)
                        if rand < item_choice.fusion_probability:
                            item_product.count += 1
                            _sum += 1
                report = report + "\n" + f"得到{_sum}个{item_product.name}"
            else:
                for i in range(num):
                    if item_choice.count < 4:
                        report = report + "物品数量不足"
                        break
                    else:
                        item_choice.count -= 4
                        rand = random.randint(0, 99)
                        if rand < item_choice.fusion_probability:
                            report = report + "\n" + f'恭喜您熔炼成功，获得一个{item_product.name}'
                            item_product.count += 1
                        else:
                            report = report + "\n" + "熔炼失败."
            await session.send(report)
            player.refresh_all()


@on_command("guess_coin", only_to_me=False, aliases="猜硬币")
async def guess_coin(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    player = Person(user_id, group_id)
    if session.current_arg.strip():
        return
    if not authority(group_id)[19]:
        return
    if authority(group_id)[20] == 2:
        if 0 < (int(time.time()) // 1800) % 48 < 45:
            await session.send("请在6：30——8:30期间使用本系统")
        return
    else:
        await session.send("游戏介绍：系统将随机投掷一枚硬币，猜测硬币的正反面，猜对了当前下注金币翻倍，猜错了当前下注金币归0")
        _ = await session.aget("gold_num", prompt="请输入您要下注的金币")
        try:
            gold_num = int(_)
        except:
            session.finish("请输入正确的金币数目")
            return
        if gold_num <= 0:
            session.finish("请输入正确的金币数目")
            return
        if player.gold < gold_num:
            session.finish("您的金币不足")
        gold_num_now = gold_num
        player.gold -= gold_num
        await session.apause("请输入“正面”或“反面”猜测，输入其他内容结束游戏并返还当前下注金币。")
        while True:
            if session.current_arg == "取消":
                player.gold += gold_num_now
                player.refresh()
                session.finish(f"游戏结束，[CQ:at,qq={user_id}]您本次共赢得了{gold_num_now - gold_num}金币")
                return
            elif session.current_arg == "正面" or session.current_arg == "反面":
                rand01 = random.randint(0, 119)
                rand = 0 if rand01 < 60 else 1
                _ = ["反面", "正面"]
                arg = 0 if session.current_arg == "反面" else 1
                if rand == arg:
                    gold_num_now *= 2
                    await session.send(f"[CQ:at,qq={user_id}]掷硬币的结果是{_[arg]},恭喜您猜对了，当前下注金为{gold_num_now}")
                    await session.apause("请输入“正面”或“反面”猜测，输入其他内容结束游戏并返还当前下注金币。")
                else:
                    player.refresh()
                    await session.finish(f"[CQ:at,qq={user_id}]掷硬币的结果是{_[rand]},很遗憾您猜错了，您一共输掉了{gold_num}金币")
            else:
                player.gold += gold_num_now
                player.refresh()
                session.finish(f"游戏结束，[CQ:at,qq={user_id}]您本次共赢得了{gold_num_now - gold_num}金币")
                return


@on_command("wawale", only_to_me=False, aliases="挖挖乐")
async def wawale(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    player = Person(user_id, group_id)
    weapons = [Item(i) for i in range(1, 21)]
    weapons_with_rate = {i: (3 ** (8 - i.quality)) for i in weapons}
    weapon = overrandom(weapons_with_rate)
    item_get = []
    if session.current_arg.strip():
        return
    if not authority(group_id)[20]:
        return
    if authority(group_id)[20] == 2:
        if 0 < (int(time.time()) // 1800) % 48 < 45:
            await session.send("请在6：30——8:30期间使用本系统")
        return
    else:
        await session.send("游戏介绍：每次2000金币，系统随机产生10个格子，里面有不超过4个地雷，"
                           "1把随机武器，不超过6个随机金币格子和不超过4个随机道具格子，"
                           "在触碰地雷之前可以一直挖，也可以随时停止。触碰地雷则立即结束且不返还所有物品.")
        _ = ["weapon"]
        # 武器必存在，雷*4，金币*6，物品*4,14选9
        __ = ["mine", "mine", "mine", "mine", "gold", "gold", "gold", "gold", "gold", "gold", "item", "item", "item",
              "item"]
        _ = _ + randomlist(__)[:8]
        award = randomlist(_)
        begin_game = await session.aget(prompt="是否开始？")
        if begin_game != "是":
            session.finish("已取消")
            return
        number = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        remain = number
        gold_num_now = 0
        await session.apause(
            f"[CQ:at,qq={user_id}]请输入您选择的格子序号，输入“取消”停止挖宝，剩余格子序号如下：\n" + f"{'，'.join(num_list_to_str(remain))}")
        while True:
            arg = session.current_arg.strip()
            if arg == "取消":
                _ = []
                player.gold += gold_num_now
                for item in item_get:
                    player.package.setdefault(item.item_id, item)
                    player.package[item.item_id].count += 1
                player.refresh_all()
                session.finish(f"[CQ:at,qq={user_id}]您停止了挖宝，一共获得了{gold_num_now}金币{_}")
                return
            if arg not in num_list_to_str(remain):
                await session.apause(
                    f"[CQ:at,qq={user_id}]请输入正确的剩余格子序号，输入”取消“停止挖宝，剩余格子序号如下：\n" + f"{'，'.join(num_list_to_str(remain))}")
            if arg in num_list_to_str(remain):
                num = int(arg)
                if award[num] == "gold":
                    gold_award = random.randint(400, 1500)
                    gold_num_now += gold_award
                    remain.remove(num)
                    await session.apause(
                        f"[CQ:at,qq={user_id}]恭喜您挖到了{gold_award}金币，" + "继续挖宝请输入您选择的格子序号，输入“取消”停止挖宝，剩余格子序号如下：\n" + f"{'，'.join(num_list_to_str(remain))}")
                if award[num] == "weapon":
                    item_get.append(weapon)
                    remain.remove(num)
                    await session.apause(
                        f"[CQ:at,qq={user_id}]恭喜您挖到了{weapon.name}，" + "继续挖宝请输入您选择的格子序号，输入“取消”停止挖宝，剩余格子序号如下：\n" + f"{'，'.join(num_list_to_str(remain))}")
                if award[num] == "item":
                    item = Item(random.randint(201, 210))
                    item_get.append(item)
                    remain.remove(num)
                    await session.apause(
                        f"[CQ:at,qq={user_id}]恭喜您挖到了{item.name}，" + "继续挖宝请输入您选择的格子序号，输入“取消”停止挖宝，剩余格子序号如下：\n" + f"{'，'.join(num_list_to_str(remain))}")
                if award[num] == "mine":
                    session.finish(f"[CQ:at,qq={user_id}]您不小心挖到了地雷，您去世了，挖到的物品全部丢失。")
                    return


# (201,"1级强化石",2,75,0,202,89),(202,"2级强化石",2,300,0,203,89),(203,"3级强化石",2,1200,0,204,89),
# (204,"4级强化石",2,4800,0,205,100),205,"5级强化石",2,24000,0,0,0),(206,"神恩符",2,0,0,0,0),(207,"幸运符15%",2,15,0,0,0),
# (208,"幸运符25%",2,25,0,0,0),(211,"攻击祝福宝珠",2,20,0,0,0)(210,"护身符",2,0,0,0,0)

@on_command("strengthen", aliases="模拟强化")
async def strengthen(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    player = Person(user_id, group_id)
    report_list = []
    weapon_id_list = []
    if not authority(group_id)[11]:
        return
    elif authority(group_id)[11] == 2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    i = 1
    for weapon in player.weapon:
        if weapon.strength_lvl >= 12:
            continue
        else:
            weapon_id_list.append(weapon.weapon_id)
            report_list.append(f"{i}: {weapon.name}(+{weapon.strength_lvl})")
            i += 1
    report = '\n'.join(report_list)
    choice = int(await session.aget(prompt="请选择您要强化的武器编号：" + report))
    if choice > len(weapon_id_list):
        await session.send("您选择的武器编号不存在")
        return
    else:
        weapon_choice = player.weapon[choice]
        stone_txt = await session.aget(prompt="请选择您要使用的强化石等级（最多3块！），用空格隔开，15代表幸运符15%，25代表幸运符25%，0代表神恩符，例如：5 5 4 15 0")
        stone = [int(i) for i in stone_txt.split()]
        if 0 in stone:
            if not player.package.get(206, 0) or player.package[206].count == 0:
                choice = await session.aget("您的神恩符数量不足，是否不使用神恩符继续强化？")
                if choice not in ["是", "Y", "1", "确定"]:
                    session.finish("已取消")
                    return
                using_shenen = False
            else:
                using_shenen = True
        else:
            using_shenen = False
        if 25 in stone:
            if not player.package.get(208, 0) or player.package[208].count == 0:
                choice = await session.aget("您的幸运符25%数量不足，是否不使用幸运符符继续强化？")
                if choice not in ["是", "Y", "1", "确定"]:
                    session.finish("已取消")
                    return
                lucky = 0
            else:
                lucky = 25
        elif 15 in stone:
            if not player.package.get(206, 0) or player.package[206].count == 0:
                choice = await session.aget("您的幸运符15%数量不足，是否不使用幸运符符继续强化？")
                if choice not in ["是", "Y", "1", "确定"]:
                    session.finish("已取消")
                    return
                lucky = 0
            else:
                lucky = 15
        else:
            lucky = 0
        stone_using = [stone.count(i) for i in range(1, 6)]
        if sum(stone_using) > 3:
            session.finish("您使用的强化石超过3块！")
            return
        strength_stone_exp = [
            75,
            300,
            1200,
            4800,
            24000
        ]

        strength_exp = [
            200,
            700,
            2700,
            10700,
            21300,
            42700,
            85300,
            170700,
            293300,
            512000,
            682700,
            853300
        ]

        player_strength_exp = sum(strength_stone_exp[i] * stone_using[i] for i in range(5)) * (
                1 + 0.3 * player.is_vip) * (100 + lucky)
        success_probability = min(player_strength_exp / strength_exp[weapon_choice.strength_lvl], 100)
        rand = random.uniform(0, 100)
        report = f"强化成功率为{success_probability:.1f}%,是否强化？"
        choice = await session.aget(prompt=report)
        if choice not in ["是", "Y", "1", "确定"]:
            session.finish("已取消")
            return
        if rand < success_probability:
            await session.send("成功  ^_^")
            weapon_choice.strength_lvl += 1
            weapon_choice.refresh()
            return
        else:
            report = "失败...囧"
            if weapon_choice.strength_lvl >= 5 and not using_shenen:
                if weapon_choice.quality <= 3:
                    weapon_choice.strength_lvl = 0
                    await session.send(report + "\n武器品质不足卓越，强化等级归零.")
                else:
                    weapon_choice.strength_lvl -= 1
                    await session.send(report + "\n武器品质高于卓越，武器强化等级降低1")
                weapon_choice.refresh()
            else:
                await session.send(report)
            return


@on_command("extra", aliases="附加功能", only_to_me=False)
async def extra(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    player = Person(user_id, group_id)
    if not player.is_superuser:
        return
    arg = session.current_arg.strip()
    if not arg or arg == "状态":
        permission0 = authority2(group_id)
        status = ["关闭", "开启", "限时开启"]
        permission1 = [f"{EXTRA_MODULES2[i]}:{status[permission0[i]]}" for i in range(len(EXTRA_MODULES3))]
        permission = '\n'.join(permission1)
        await session.finish(f"当前附加功能状态：\n{permission}")
    elif arg == "全部开启":
        change_authority(group_id, EXTRA_MODULES[1:], [1] * (len(EXTRA_MODULES) - 1))
        await session.send("成功开启附加功能")
    elif arg == "全部关闭":
        change_authority(group_id, EXTRA_MODULES[1:], [0] * (len(EXTRA_MODULES) - 1))
        await session.send("成功关闭附加功能")
    elif arg[:2] == "开启":
        arg0 = arg.split(" ")
        modules0 = arg0[1].split(",")
        modules = []
        for module in modules0:
            module_index = EXTRA_MODULES2.index(module)
            if module_index == -1:
                await session.send(f"未找到{module}模块")
            else:
                for i in EXTRA_MODULES3[module_index]:
                    modules.append(EXTRA_MODULES[i])
        change_authority(group_id, modules, [1] * len(modules))
        await session.send("成功")
    elif arg[:2] == "关闭":
        arg0 = arg.split(" ")
        modules0 = arg0[1].split(",")
        modules = []
        for module in modules0:
            module_index = EXTRA_MODULES2.index(module)
            if module_index == -1:
                await session.send(f"未找到{module}模块")
            else:
                for i in EXTRA_MODULES3[module_index]:
                    modules.append(EXTRA_MODULES[i])
        change_authority(group_id, modules, [0] * len(modules))
        await session.send("成功")
    elif arg[:2] == "限时":
        arg0 = arg.split(" ")
        modules0 = arg0[1].split(",")
        modules = []
        for module in modules0:
            module_index = EXTRA_MODULES2.index(module)
            if module_index == -1:
                await session.send(f"未找到{module}模块")
            else:
                for i in EXTRA_MODULES3[module_index]:
                    modules.append(EXTRA_MODULES[i])
        change_authority(group_id, modules, [2] * len(modules))
        await session.send("成功")


@on_command("extra2", aliases="全部附加功能", only_to_me=False)
async def extra2(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    player = Person(user_id, group_id)
    if not player.is_superuser:
        return
    arg = session.current_arg.strip()
    if not arg or arg == "状态":
        permission0 = authority(group_id)
        status = ["关闭", "开启", "限时开启"]
        permission1 = [f"{EXTRA_MODULES[i + 1]}:{status[permission0[i + 1]]}" for i in range(len(EXTRA_MODULES) - 1)]
        permission = '\n'.join(permission1)
        await session.finish(f"当前附加功能状态：\n{permission}")
    elif arg == "全部开启":
        change_authority(group_id, EXTRA_MODULES[1:], [1] * (len(EXTRA_MODULES) - 1))
        await session.send("成功开启附加功能")
    elif arg == "全部关闭":
        change_authority(group_id, EXTRA_MODULES[1:], [0] * (len(EXTRA_MODULES) - 1))
        await session.send("成功关闭附加功能")
    elif arg[:2] == "开启":
        arg0 = arg.split(" ")
        modules = arg0[1].split(",")
        change_authority(group_id, modules, [1] * len(modules))
        await session.send("成功")
    elif arg[:2] == "关闭":
        arg0 = arg.split(" ")
        modules = arg0[1].split(",")
        change_authority(group_id, modules, [0] * len(modules))
        await session.send("成功")
    elif arg[:2] == "限时":
        arg0 = arg.split(" ")
        modules = arg0[1].split(",")
        change_authority(group_id, modules, [2] * len(modules))
        await session.send("成功")
    elif arg[:2] == "设置":
        arg0 = arg.split(" ")
        modules = arg0[1].split(",")
        module_status = arg0[2].split(",")
        change_authority(group_id, modules, module_status)
        await session.send("成功")


@on_command("item_list", aliases="#查询物品列表", only_to_me=False)
async def item_list_query(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    player = Person(user_id, group_id)
    if not player.is_superuser:
        return
    sql = "SELECT (item_id,name) FROM item_details"
    conn = pymysql.connect(host='localhost', user='root', password='xz123456', database='xiaoshimei', charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    message = "\n".join([f'{i[0]}: {i[1]}' for i in result])
    await session.bot.send_private_msg(user_id=user_id, message=message)
    conn.close()


@on_command("item_charge", aliases="充值物品", only_to_me=False)
async def item_charge(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    player = Person(user_id, group_id)
    if not player.is_superuser:
        return
    arg = session.current_arg.strip().split()
    item_id = int(arg[0])
    count = int(arg[1])
    if len(arg) >= 3:
        to_id = get_qq(arg[2])
        player = Person(to_id, group_id)
    item = Item(item_id)
    player.package.setdefault(item_id, item)
    player.package[item_id].count += count
    player.refresh_all()
    session.finish("为" + MessageSegment.at(player.user_id) + f"添加{count}个{item.name}成功")


@on_command("sell", aliases="出售物品", only_to_me=False)
async def sell(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    player = Person(user_id, group_id)
    item_id_list = []
    report = []
    i = 1
    for item in player.package.values():
        report.append(f"{i}: {item.name}(单价{item.price})(剩余{item.count})")
        item_id_list.append(item.item_id)
        i += 1
    choice_txt = await session.aget(prompt="请选择您要出售的物品\n" + "\n".join(report))
    try:
        choice = int(choice_txt)
    except ValueError:
        session.finish("您输入的编号不正确！")
        return
    item_choice = player.package[item_id_list[choice]]
    if item_choice.type not in [0, 1]:
        num_txt = await session.aget(prompt=f"请输入您要出售的数量(剩余：{item_choice.count}),输入“取消”停止.")
        try:
            num = int(num_txt)
        except ValueError:
            if num_txt == "取消":
                session.finish("已取消")
            else:
                session.finish("您输入的数量不正确！")
            return
        if num > item_choice.count:
            session.finish("您输入的数量超过该物品拥有的数量！")
        item_choice.count -= num
        player.gold += num * item_choice.price
        player.refresh_all()
        session.finish("出售成功")
        return
    elif item_choice.type == 0:
        weapons_to_sell = []
        for weapon in player.weapon:
            if weapon.item_id == item_choice.item_id:
                weapons_to_sell.append(weapon)
        report = "请选择您要出售的武器：\n" + "\n".join(
            [f"{i}: {weapon.name}({weapon.strength_lvl})" for i, weapon in enumerate(weapons_to_sell)])
        choice = await session.aget(prompt=report)
        try:
            _ = int(choice)
            weapon_choice = weapons_to_sell[_]
        except ValueError:
            session.finish("您输入的编号不正确！")
            return
        player.gold += weapon_choice.price
        weapon_choice.destroy()
        session.finish("出售成功")
        return
    else:
        weapons_to_sell = []
        for weapon in player.shield:
            if weapon.item_id == item_choice.item_id:
                weapons_to_sell.append(weapon)
        report = "请选择您要出售的盾牌：\n" + "\n".join(
            [f"{i}: {weapon.name}({weapon.strength_lvl})" for i, weapon in enumerate(weapons_to_sell)])
        choice = await session.aget(prompt=report)
        try:
            _ = int(choice)
            weapon_choice = weapons_to_sell[_]
        except ValueError:
            session.finish("您输入的编号不正确！")
            return
        player.gold += weapon_choice.price
        weapon_choice.destroy()
        session.finish("出售成功")
