import random
import time
import re
import nonebot.command

from xiaoshimei.plugins.goldsystem.globals import ITEM_NICKNAME, BOX, overrandom
from xiaoshimei.plugins.goldsystem.globals import PRIZE_DRAW, STRENGTH_EXP, STRENGTH_STONE, item_list1, item_list2, \
    item_list3, item_list4, BAOZHU
import pymysql
from nonebot import on_command, CommandSession, MessageSegment
import xiaoshimei.plugins.goldsystem.createImage as createImage
from xiaoshimei.plugins.goldsystem import gold

# 数据库:每个号，昵称，物品唯一标识，物品类型id，


# 熔炼命令
# 出售命令
# 精炼(待完善)

# connection = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
from xiaoshimei.plugins.goldsystem.gold import ITEM_PRICE


def get_qq(cq_msg):
    res = re.findall(r'[Qq]{2}=(\w+)\]', cq_msg)
    if len(res):
        return res[0]
    else:
        return None


def get_weapon_list(user_id, group_id, item_id, whether_12=False):
    """
    给定某人某群及item_id寻找该id下所有武器以及强化等级
    :param whether_12: 是否排除强化12级武器
    :param user_id: QQ
    :param group_id: QQ group
    :param item_id: item_id
    :return: [(weapon_id,强化等级)]
    """
    sql2 = f'SELECT item_uni_id FROM user_package WHERE user_id = {user_id} AND group_id = {group_id} AND item_id = {item_id}'
    conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute(sql2)
    result = cursor.fetchone()
    uni_id = result[0]
    if12 = " AND strength_lvl < 12" if whether_12 else ""
    sql3 = f'SELECT * FROM strength WHERE item_uni_id = {uni_id}' + if12
    cursor2 = conn.cursor()
    cursor2.execute(sql3)
    result2 = cursor2.fetchall()
    weapon_list = [(items[0], items[2], item_id) for items in result2]
    conn.close()
    return weapon_list


def add_strength_lvl(weapon_id, lvl=1):
    sql2 = f'UPDATE strength SET strength_lvl = strength_lvl + {lvl} WHERE weapon_id = {weapon_id}'
    conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute(sql2)
    conn.commit()
    conn.close()


# 仓库命令
@on_command("package", aliases="查看仓库", only_to_me=False)
async def ipackage(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    authority = gold.authority(group_id)
    if not authority[3]:
        return
    elif authority[3] == 2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    else:
        sql2 = f'SELECT * FROM user_package WHERE user_id = {user_id} AND group_id = {group_id}'
        conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
        cursor = conn.cursor()
        cursor.execute(sql2)
        result = cursor.fetchall()  # user_id,group_id,item_id,item_num,item_unique_id
        list_of_pack = []
        if result:
            for items in result:
                if items[3]:
                    list_of_pack.append({'name': str(items[2]), 'count': items[3] if items[3] != 1 else 0})
            j = (len(list_of_pack) + 6) // 7
            bag = createImage.init_empty_bag(j=j)
            createImage.draw_item_by_list(bag, list_of_pack)
            bag.save('C:/temp/out.png')
            report = MessageSegment.at(user_id) + '的仓库如下' + MessageSegment.image("C:/temp/out.png")
        else:
            report = MessageSegment.at(user_id) + ' 仓库为空！'
        await session.send(report)
        conn.close()


# 开盒子命令

@on_command("legend_box", aliases="开神器盒子", only_to_me=False)
async def legend_box(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    authority = gold.authority(group_id)
    if not authority[4]:
        return
    elif authority[4] == 2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    else:
        arg = session.current_arg.strip()
        if not arg:
            arg = await session.aget("num", prompt="请输入开启盒子数量，最大500")
        number = int(arg)
        if number > 500 or number < 1:
            arg = await session.aget("num", prompt="请输入开启盒子数量，最大500")
            number = int(arg)
        if number > 500 or number < 1:
            await session.send("请按要求操作")
            return
        result_gold = gold.cost_gold(user_id, group_id, 50 * number)
        if result_gold:
            await session.send("您的金币不足")
            return
        else:
            conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
            cursor = conn.cursor()
            sql2 = f'SELECT * FROM user_package WHERE user_id = {user_id} AND group_id = {group_id}'
            cursor.execute(sql2)
            result1 = cursor.fetchall()
            items_all = []
            for items in result1:
                if items[3]:
                    items_all.append(items[2])
            report = MessageSegment.at(user_id) + f'您消耗了{50 * number}金币，获得的物品如下：'
            result = [0] * 20
            packs = []
            for i in range(number):
                rand = overrandom(BOX)
                if 0 <= rand < 19:
                    result[rand] += 1
                else:
                    result[19] += ((rand - 20) * (rand - 21) - 5 * (rand - 19) * (rand - 21) + 25 * (rand - 19) * (
                            rand - 20))
            for i in range(20):
                if result[i]:
                    sql = f"UPDATE user_package SET item_num = item_num + {result[i]} WHERE user_id =\
                    {user_id} and group_id = {group_id} and item_id = {i}"
                    if i in items_all:
                        cursor.execute(sql)
                        conn.commit()
                    else:
                        sql = f'INSERT INTO user_package (user_id,group_id,item_id,item_num) VALUES \
                        ({user_id},{group_id},{i},{result[i]})'
                        cursor.execute(sql)
                        conn.commit()
                    packs.append({'name': str(i), 'count': result[i]})
            row_of_bag = (6 + len(packs)) // 7
            bag = createImage.init_empty_bag(row_of_bag)
            createImage.draw_item_by_list(bag, packs)
            bag.save('C:/temp/out.png')
            report = report + MessageSegment.image('C:/temp/out.png')
            conn.close()
            await session.send(report)


# 熔炼命令
# 检查仓库，列出可熔炼物品
# 选择熔炼物品
# 得到物品进行转换
#


@on_command("fake_fusion", aliases='模拟熔炼', only_to_me=False)
async def fake_rl(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    authority = gold.authority(group_id)
    if not authority[5]:
        return
    elif authority[5] == 2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    else:
        arg = session.current_arg.strip()
        sql2 = f'SELECT * FROM user_package WHERE user_id = {user_id} AND group_id = {group_id} AND item_num >= 4 AND ' \
               f'item_id in (0,1,2,3,4,5,6,7,12,13,15,16,22,23,24,25) '
        conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
        cursor = conn.cursor()
        cursor.execute(sql2)
        result = cursor.fetchall()
        report = ''
        conn.close()
        _ = []  # 查询结果得到的物品id列表
        if result:
            i = 1
            for items in result:
                report = report + f'{i}. {ITEM_NICKNAME[items[2]][0]}\n'
                _.append(items[2])
                i += 1
        else:
            report = MessageSegment.at(user_id) + ' 可熔炼物品不足'
            await session.send(report)
            return
        if not arg:
            arg = await session.aget("key", prompt=f"请选择熔炼物品：\n{report}")
        item_num1 = None
        try:
            item_num1 = int(arg)  # 用户输入的编号，123456
            if item_num1 <= 0:
                session.finish("请输入正确的编号！")
            num1 = _[item_num1 - 1]
        except ValueError:
            for i in range(27):
                if arg in ITEM_NICKNAME[i]:
                    num1 = i
                    item_num1 = 1
                    break
        except IndexError:
            session.finish("没有该编号的熔炼物品")
        if item_num1 is None:
            report = '请输入正确的物品序号，或物品名称.'
            await session.send(report)
            return
        else:
            if group_id in [643057141,940650004]:
                times = await session.aget(prompt="请输入熔炼次数(危防止刷屏，次数最多为30次")
                times = int(times)
                if times > 30:
                    await session.finish("为防止刷屏,次数最多30次")
            else:
                times = 1
            report = MessageSegment.at(user_id)
            for i in range(times):
                rand = random.randint(0, 99)
                if 0 <= num1 <= 3 or num1 == 12 or num1 == 15 or 22 <= num1 <= 24:
                    result1 = 0 if rand > 88 else 1
                elif 4 <= num1 <= 7 or num1 == 16:
                    result1 = 0 if rand > 2 else 1
                elif num1 == 13:
                    result1 = 0 if rand > 6 else 1
                elif num1 == 25:
                    result1 = 1
                dict1 = {name: count for name, count in zip(range(12)[4:], [0] * 8)}
                for items in result:
                    dict1[items[2]] = items[3]
                if gold.cost_item(user_id, group_id, num1, 4):
                    report = report + "\n 物品数量不足"
                    break
                if result1:
                    if num1 <= 7:
                        num1 += 4
                    else:
                        num1 += 1
                    gold.get_item(user_id, group_id, num1)
                    report = report + f"恭喜您熔炼成功，获得一个{ITEM_NICKNAME[num1][0]}."+"\n"
                else:
                    report = report + '熔炼失败.' + "\n"
            await session.send(report)


@on_command("sell", aliases=('出售', '出售道具', '出售物品'), only_to_me=False)
async def sell(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    authority = gold.authority(group_id)
    if not authority[6]:
        return
    elif authority[6] == 2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    else:
        arg = session.current_arg.strip()
        sql2 = f'SELECT * FROM user_package WHERE user_id = {user_id} AND group_id = {group_id}'
        conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
        cursor = conn.cursor()
        cursor.execute(sql2)
        result = cursor.fetchall()
        report = ''
        conn.close()
        _ = []  # [3,2,6,19]为得到的物品编号列表
        if result:
            i = 1
            for items in result:
                report = report + f'{i}. {ITEM_NICKNAME[items[2]][0]}\n'
                _.append(items[2])
                i += 1
        else:
            report = MessageSegment.at(user_id) + '无可出售物品'
            await session.send(report)
            return
        if not arg:
            arg = await session.aget("key", prompt=f"请选择要出售的物品：\n{report}")
        item_no = None  # 选择的物品序号
        try:
            item_no = int(arg)
        except:
            for i in range(99):
                if arg in ITEM_NICKNAME[i]:
                    item_no = 0
                    num1 = i
                    break
        if item_no is None:
            report1 = '请输入正确的物品序号，或物品名称:'
            arg = await session.aget("key", prompt=f"{report1}\n{report}")
            try:
                item_no = int(arg)
            except:
                for i in range(99):
                    if arg in ITEM_NICKNAME[i]:
                        item_no = 0
                        num1 = i
                        break
            if item_no is None:
                await session.send("请正确输入名称！")
                return
        if item_no:
            num1 = _[item_no - 1]
        weapons = [8, 9, 10, 11, 14] + [i + 30 for i in range(14)]
        if num1 in weapons:
            wp_list = get_weapon_list(user_id, group_id, num1, True)
            reply = "请选择您要出售的武器："
            for j, str_lvl in enumerate(wp_list):
                str_lvl2 = "gold" if str_lvl[1] == 13 else f"+{str_lvl[1]}"
                reply = reply + "\n" + f"{j + 1}:{ITEM_NICKNAME[num1][0]}({str_lvl2})"
            arg = await session.aget(prompt=reply)
            weapon_no = int(arg) - 1
            weapon_id = wp_list[weapon_no][0]
            gold.cost_weapon(weapon_id)
            gold.get_gold(user_id, group_id, ITEM_PRICE[num1])
            await session.send(f"出售成功，获得{gold.ITEM_PRICE[num1]}金币.")
        else:
            num0 = await session.aget("num", prompt=f'请输入出售数量：')
            try:
                num = int(num0)
            except:
                await session.send("输入格式错误！")
                return
            if not gold.sell(user_id, group_id, num1, num):
                await session.send(f"出售成功,获得{gold.ITEM_PRICE[num1] * num}金币.")
            else:
                await session.send("出售失败，物品数量不足！")


"""
商城：消耗钻头进行以下操作
商城：抽奖
商城：碎片兑换
"""


@on_command("drillshop", aliases="钻头商城", only_to_me=False)
async def drillshop(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    authority = gold.authority(group_id)
    if not authority[7]:
        return
    elif authority[7] == 2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    elif session.current_arg not in ("a1", "a2", "a3"):
        ctg = await session.aget("item", prompt="请输入你要购买的物品：\n1.抽奖\n2.碎片兑换\n3.待添加")
    else:
        ctg = session.current_arg[1]
    if ctg == '1' or ctg == '抽奖':
        orgnum = await session.aget(prompt="钻头抽奖：随机获得金币，碎片，神器等.每次抽奖消耗5枚钻头\n请输入抽奖次数：")
        num = int(orgnum)
        if not gold.cost_item(user_id, group_id, 19, 5 * num):
            a = [0] * 99
            for i in range(num):
                t = overrandom(PRIZE_DRAW)
                if t <= 18:
                    a[t] += 1
                elif t <= 21:
                    a[27] += (10 ** (t - 19))
                else:
                    a[t] += 1
        else:
            await session.send("您的钻头不足，无法抽奖！")
            return
        list_of_result = []
        for i in range(19):
            if a[i]:
                list_of_result.append({'name': str(i), 'count': a[i]})
                gold.get_item(user_id, group_id, i, a[i])
        gold.get_gold(user_id, group_id, a[27])
        for i in range(5):
            if a[i + 22]:
                list_of_result.append({'name': str(i + 22), 'count': a[i + 22]})
                gold.get_item(user_id, group_id, i + 22, a[i + 22])
        for i in range(30):
            if a[i + 28]:
                list_of_result.append({'name': str(i + 28), 'count': a[i + 28]})
                gold.get_item(user_id, group_id, i + 28, a[i + 28])
        if a[27]:
            list_of_result.append({"name": "27", "count": a[27]})
        j = (len(list_of_result) + 6) // 7
        bag = createImage.init_empty_bag(j=j)
        createImage.draw_item_by_list(bag, list_of_result)
        bag.save('C:/temp/out.png')
        report = MessageSegment.at(user_id) + f'您抽奖了{num}次，获得物品如下：' + MessageSegment.image("C:/temp/out.png")
        await session.send(report)

    # 碎片兑换
    elif ctg == '2' or ctg == '碎片兑换':
        junior = [0, 1, 2, 3, 12, 15]
        senior = [4, 5, 6, 7, 13, 16]

        def alt_to_str(list0: list):
            list1 = [''] * len(list0)
            for _i, _item in enumerate(list0):
                list1[_i] = str(_item)
            return list1

        def print_by_list(list1: list):
            _print = ''
            _j = 0
            for _i, _item in enumerate(list1):
                if _item > 0:
                    _j += 1
                    _print = _print + '\n' + f'{_j}:{ITEM_NICKNAME[_i][0]}(还剩{_item}个)'
            return _print

        def non_0_list(list1: list):
            _list = []
            for _i, _item in enumerate(list1):
                if _item > 0:
                    _list.append(_i)
            return _list

        sql2 = f'SELECT * FROM user_package WHERE user_id = {user_id} AND group_id = {group_id}' \
               f' AND item_id IN ({",".join(alt_to_str(junior + senior))})'
        conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
        cursor = conn.cursor()
        cursor.execute(sql2)
        result = cursor.fetchall()
        bag_list = [0] * 20
        conn.close()
        if result is None:
            await session.send("可兑换物品不足！")
            return
        else:
            for items in result:
                bag_list[items[2]] = items[3]
            report1 = ''
            ex = junior + senior
            for i, item in enumerate(ex):
                report1 = report1 + f'\n{i + 1}:{ITEM_NICKNAME[ex[i]][0]}'
            _ = await session.aget("exc_id", prompt=f"兑换物品：可以将任意两片碎片兑换为同等级的任意一片碎片"
                                                    f"请选择您要兑换的碎片：{report1}")
            try:
                num0 = int(_) - 1
                exchange_id = ex[num0]
            except ValueError:
                for i, item in enumerate(ITEM_NICKNAME):
                    if _ in item:
                        exchange_id = i
                        break
                else:
                    exchange_id = None
            except IndexError:
                session.finish("请输入正确的序号")
                return
            if exchange_id is None:
                await session.send("请输入正确的数字或物品名称！")
                return
            else:
                _ = await session.aget("exc_num", prompt="请输入兑换数量：")
                try:
                    exchange_num = int(_)
                except:
                    await session.send("请输入数字！")
                    return
                if exchange_id in junior:
                    for i in senior:
                        bag_list[i] = 0
                    sum0 = sum(bag_list)
                    if sum0 < exchange_num * 2:
                        await session.send("可兑换碎片不足！")
                    else:
                        chosen = [0] * 20
                        lack = exchange_num * 2
                        await session.apause(f"请输入要选择的碎片及数量，用空格隔开（例如： 3 50）,发送cancel取消。"
                                             f"背包现有碎片：{print_by_list(bag_list)}还需要碎片总数：{lack}")
                        while True:
                            if session.current_arg == "cancel" or session.current_arg == "取消":
                                session.finish("已取消")
                                return
                            _ = [int(session.current_arg.split(" ")[0]), int(session.current_arg.split(" ")[1])]
                            _[0] = non_0_list(bag_list)[_[0] - 1]
                            if bag_list[_[0]] < _[1]:
                                await session.send("该碎片数量不足！")
                            else:
                                if lack < _[1]:
                                    chosen[_[0]] += lack
                                    await session.send("使用数量超出需求，只消耗了需求数量！")
                                    for i in range(20):
                                        if chosen[i]:
                                            gold.cost_item(user_id, group_id, i, chosen[i])
                                    gold.get_item(user_id, group_id, exchange_id, exchange_num)
                                    session.finish("兑换成功！")
                                elif lack == _[1]:
                                    chosen[_[0]] += _[1]
                                    for i in range(20):
                                        if chosen[i]:
                                            gold.cost_item(user_id, group_id, i, chosen[i])
                                    gold.get_item(user_id, group_id, exchange_id, exchange_num)
                                    session.finish("兑换成功！")
                                else:
                                    chosen[_[0]] += _[1]
                                    bag_list[_[0]] -= _[1]
                                    lack -= _[1]
                                    await session.apause(f"请输入要选择的碎片及数量，用空格隔开（例如： 3 50）,发送cancel取消。"
                                                         f"背包现有碎片：{print_by_list(bag_list)}还需要碎片总数：{lack}")
                else:
                    for i in junior:
                        bag_list[i] = 0
                    sum0 = sum(bag_list)
                    if sum0 < exchange_num * 2:
                        await session.send("可兑换碎片不足！")
                    else:
                        chosen = [0] * 20
                        lack = exchange_num * 2
                        await session.apause(f"请输入要选择的碎片及数量，用空格隔开（例如： 3 50）,发送cancel取消。"
                                             f"背包现有碎片：{print_by_list(bag_list)}还需要碎片总数：{lack}")
                        while True:
                            if session.current_arg == "cancel" or session.current_arg == "取消":
                                session.finish("已取消")
                                return
                            else:
                                _ = [int(session.current_arg.split(" ")[0]), int(session.current_arg.split(" ")[1])]
                                _[0] = non_0_list(bag_list)[_[0] - 1]
                                if bag_list[_[0]] < _[1]:
                                    await session.send("该碎片数量不足！")
                                    await session.apause(f"请输入要选择的碎片及数量，用空格隔开（例如： 3 50）,发送cancel取消。"
                                                         f"背包现有碎片：{print_by_list(bag_list)}还需要碎片总数：{lack}")
                                else:
                                    if lack < _[1]:
                                        chosen[_[0]] += lack
                                        await session.send("使用数量超出需求，只消耗了需求数量！")
                                        for i in range(20):
                                            if chosen[i]:
                                                gold.cost_item(user_id, group_id, i, chosen[i])
                                        gold.get_item(user_id, group_id, exchange_id, exchange_num)
                                        session.finish("兑换成功！")
                                    elif lack == _[1]:
                                        chosen[_[0]] += _[1]
                                        for i in range(20):
                                            if chosen[i]:
                                                gold.cost_item(user_id, group_id, i, chosen[i])
                                        gold.get_item(user_id, group_id, exchange_id, exchange_num)
                                        session.finish("兑换成功！")
                                    else:
                                        chosen[_[0]] += _[1]
                                        bag_list[_[0]] -= _[1]
                                        lack -= _[1]
                                        await session.apause(f"请输入要选择的碎片及数量，用空格隔开（例如： 3 50）,发送cancel取消。"
                                                             f"背包现有碎片：{print_by_list(bag_list)}还需要碎片总数：{lack}")

    else:
        await session.send("好像还木有做……")
        return


# todos:
# keys没有顺序，所以要稍微改一下。

@on_command("drilldraw", aliases="钻头抽奖", only_to_me=False)
async def drilldraw(session: CommandSession):
    if not session.current_arg.strip():
        await nonebot.command.call_command(session.bot, session.event, name="drillshop", current_arg="a1")


@on_command("drill-exchange", aliases="碎片兑换", only_to_me=False)
async def drillexchange(session: CommandSession):
    if not session.current_arg.strip():
        await nonebot.command.call_command(session.bot, session.event, name="drillshop", current_arg="a2")


@on_command("danwang", aliases="弹王兑换", only_to_me=False)
async def danwang(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    authority = gold.authority(group_id)
    if not authority[8]:
        return
    elif authority[8] == 2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    sql2 = f'SELECT * FROM user_package WHERE user_id = {user_id} AND group_id = {group_id} AND item_id in (8,9,10,11)'
    conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute(sql2)
    result = cursor.fetchall()
    conn.close()
    if len(result) < 4:
        session.finish(f"[CQ:at,qq={user_id}]可兑换物品不足")
    else:
        for i in range(4):
            gold.cost_item(user_id, group_id, i + 8)
        gold.get_item(user_id, group_id, 30)
        session.finish("兑换成功！")


@on_command("chaoshen", aliases="超神兑换", only_to_me=False)
async def chaoshen(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    authority = gold.authority(group_id)
    if not authority[9]:
        return
    elif authority[9] == 2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    sql2 = f'SELECT * FROM user_package WHERE user_id = {user_id} AND group_id = {group_id} AND item_id in (8,9,10,17)'
    conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute(sql2)
    result = cursor.fetchall()
    conn.close()
    if len(result) < 4:
        session.finish(f"[CQ:at,qq={user_id}]可兑换物品不足")
    else:
        arg = "\n".join([
            f"{i + 1}.{ITEM_NICKNAME[i + 32][0]}" for i in range(4)
        ])
        num0 = await session.aget("item", prompt=f"请选择你要兑换的超神：\n{arg}")
        num = int(num0)
        for i in range(3):
            gold.cost_item(user_id, group_id, i + 8)
        gold.cost_item(user_id, group_id, 17)
        gold.get_item(user_id, group_id, num + 31)
        session.finish("兑换成功！")


@on_command("Sboomerang", aliases="终极神器兑换", only_to_me=False)
async def Sboomerang(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    authority = gold.authority(group_id)
    if not authority[10]:
        return
    elif authority[10] == 2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    sql2 = f'SELECT * FROM user_package WHERE user_id = {user_id} AND group_id = {group_id} AND item_id in (30,32,33,34,35)'
    conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute(sql2)
    result = cursor.fetchall()
    conn.close()
    if len(result) < 5:
        session.finish(f"[CQ:at,qq={user_id}]可兑换物品不足，需求：弹王回力标、收割者之镰、捣蛋鬼、加农神炮、棒棒糖各一个")
    else:
        for i in (30, 32, 33, 34, 35):
            gold.cost_item(user_id, group_id, i)
        gold.get_item(user_id, group_id, 31)
        session.finish("兑换成功！")


@on_command("strength", aliases="模拟强化", only_to_me=False)
async def strength(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    authority = gold.authority(group_id)
    if not authority[11]:
        return
    elif authority[11] == 2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    if session.current_arg == "模拟":
        lvl_txt = await session.aget(prompt="请输入模拟强化的目标等级")
        lvl = int(lvl_txt) - 1
        if lvl < 0 or lvl >= 12:
            session.finish("请输入正确的强化等级")
            return
        stone_txt = await session.aget(prompt="请输入放入的强化石等级，用空格隔开，输入15代表15%幸运符，25代表25%幸运符，例如：5 5 4 15")
        stone = stone_txt.split()
        if "15" in stone:
            luck = 0.15
            stone.remove("15")
        elif "25" in stone:
            luck = 0.25
            stone.remove("25")
        else:
            luck = 0
        for i, items in enumerate(stone):
            if items in ["1", "2", "3", "4", "5"]:
                stone[i] = int(items)
            else:
                del stone[i]
        if len(stone) >= 4:
            session.finish("强化石数量最多为3块！")
        elif not stone:
            session.finish("请放入强化石！")
        stone_points = sum(STRENGTH_STONE[i] for i in stone)
        probability = stone_points * (2.25 + luck) * 1000 / STRENGTH_EXP[lvl]
        if probability > 1000:
            probability = 1000
        choice = await session.aget(prompt=f"强化成功概率为{int(probability) / 10}%,是否强化？")
        if choice == "是":
            rand = random.randint(1, 1000)
            result = 1 if rand < probability else 0
            if result:
                await session.send("成功  ^_^")
            else:
                await session.send("失败...囧")
            return
        else:
            session.finish("已取消")
            return
    if not session.current_arg:
        reply = "请选择您要强化的物品:"
        weapons = [8, 9, 10, 11, 14] + [i + 30 for i in range(14)]
        bag_list = gold.query(user_id, group_id, weapons)
        j = 1
        weapon_list = []
        weapons_item_id = []
        for i, num in enumerate(bag_list):
            if num:
                wp_list = get_weapon_list(user_id, group_id, i, True)
                weapon_list = weapon_list + wp_list
                for str_lvl in wp_list:
                    reply = reply + "\n" + f"{j}:{ITEM_NICKNAME[i][0]}(+{str_lvl[1]})"
                    j += 1
                    weapons_item_id.append(i)
        # weapon_list[(武器编号1，强化等级1),(武器编号2，强化等级2),(武器编号3，强化等级3)]
        # weapon_list[选中-1]为所选武器的ID
        if not weapon_list:
            session.finish("您没有可以强化的武器！")
        choice = await session.aget(prompt=reply)
        try:
            num0 = int(choice) - 1
        except ValueError:
            session.finish("请输入正确的序号")
            return
        weapon_id = weapon_list[num0][0]
        lvl = weapon_list[num0][1]
        stone_txt = await session.aget(prompt="请输入放入的强化石等级，用空格隔开，输入15代表15%幸运符，25代表25%幸运符，0代表神恩符，例如：5 5 4 15 0")
        stone = stone_txt.split()
        stone_list = [0] * 5
        shenen = 0
        if "15" in stone:
            if not gold.cost_item(user_id, group_id, 28):
                luck = 0.15
                stone.remove("15")
            else:
                luck = 0
                await session.send("您的幸运符15%数量不足，此次强化不使用幸运符")
        elif "25" in stone:
            if not gold.cost_item(user_id, group_id, 29):
                luck = 0.25
                stone.remove("25")
            else:
                luck = 0
                await session.send("您的幸运符25%数量不足，此次强化不使用幸运符")
        else:
            luck = 0
        if "0" in stone:
            if not gold.cost_item(user_id, group_id, 45):
                shenen = 1
                stone.remove("0")
            else:
                await session.send("您的神恩符数量不足，此次强化不使用神恩符")
        for i, items in enumerate(stone):
            if items in ["1", "2", "3", "4", "5"]:
                stone_lvl = int(items) - 1
                stone_list[stone_lvl] += 1
                stone[i] = int(items)
            else:
                del stone[i]
        if len(stone) >= 4:
            session.finish("强化石数量最多为3块！")
        elif not stone:
            session.finish("请放入强化石！")
        stone_bag_num = gold.query(user_id, group_id, [22, 23, 24, 25, 26])[22:27]
        for i in range(5):
            if stone_bag_num[i] < stone_list[i]:
                session.finish("某一种类强化石个数不足！")
                return
        stone_points = sum(STRENGTH_STONE[i] for i in stone)
        probability = stone_points * (2.25 + luck) * 1000 / STRENGTH_EXP[lvl]
        if probability > 1000:
            probability = 1000
        choice = await session.aget(prompt=f"强化成功概率为{int(probability) / 10}%,是否强化？")
        if choice == "是":
            for i in range(5):
                if stone_list[i] > 0:
                    gold.cost_item(user_id, group_id, i + 22, stone_list[i])
            rand = random.randint(1, 1000)
            result = 1 if rand <= probability else 0
            if result:
                await session.send("成功  ^_^")
                add_strength_lvl(weapon_id)
            else:
                if shenen:
                    pass
                elif weapons_item_id[num0] in [37, 38, 39]:
                    gold.cost_weapon(weapon_id)
                elif lvl == 0:
                    pass
                else:
                    add_strength_lvl(weapon_id, -1)
                await session.send("失败...囧")
            return
        else:
            session.finish("已取消")
            return


@on_command("monijinglian", aliases="模拟精炼", only_to_me=False)
async def monijinglian(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    authority = gold.authority(group_id)
    if not authority[12]:
        return
    elif authority[12] == 2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    if time.localtime().tm_hour not in (2, 17) and time.localtime().tm_min > 10 and group_id != 940650004:
        session.finish("不在游戏时间内，请在2:00-2:10使用")
    else:
        _ = session.current_arg.strip()
        if not _:
            _ = await session.aget(prompt="请选择精炼物品（目前为测试版，所得物品不进入仓库）:\n1：极武器*4\n2：SLv4级宝珠*4\n3：假神*4\n4：Lv4级宝珠*4")
        if _ in ("1", "极武器", "级武器"):
            await session.finish(f"恭喜您精炼成功，获得 {overrandom(item_list1)}")
        elif _ in ("2", "S4", "垃圾S4", "S4宝珠"):
            await session.finish(f"恭喜您精炼成功，获得 {overrandom(item_list2)}")
        elif _ in ("3", "假神", "假神器"):
            await session.finish(f"恭喜您精炼成功，获得 {overrandom(item_list3)}")
        elif _ in ("4", "垃圾4", "4级宝珠"):
            await session.finish(f"恭喜您精炼成功，获得 {overrandom(item_list4)}")
        elif _ in ("批量精炼", "批量"):
            _ = await session.aget(prompt="请选择精炼物品（目前为测试版，所得物品不进入仓库）:\n1：极武器*4\n2：SLv4级宝珠*4\n3：假神*4\n4：Lv4级宝珠*4")
            num0 = await session.aget(prompt="请输入精炼次数")
            num = int(num0)
            if num < 0 or num > 15:
                session.finish("请输入0-15之间的整数")
            else:
                report = ""
                lists = [item_list1, item_list2, item_list3, item_list4]
                for i in range(num):
                    report = report + "\n" + overrandom(lists[int(_) - 1])
                await session.finish("您获得的物品如下：" + report)
        else:
            await session.finish("您输入的序号有误")


@on_command("open_baozhu", aliases=("随机宝珠开启", "开启随机宝珠"), only_to_me=False)
async def monijinglian(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    authority = gold.authority(group_id)
    if not authority[12]:
        return
    elif authority[12] == 2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    bag_num = gold.query(user_id, group_id, [44])[44]
    num = await session.aget(prompt=f"请输入您要开启的数量：（现有:{bag_num}）")
    try:
        num = int(num)
    except ValueError:
        session.finish("输入有误！")
    if num > bag_num[0]:
        session.finish("您的宝珠数量不足")
    if num > 20:
        session.finish("为防止刷屏，每次最多开启20个")
    baozhu_get = [0] * len(BAOZHU)
    reply = '您获得的宝珠如下：'
    baozhu_list = {
        items: prob
        for items, prob in zip(range(len(BAOZHU)), [4] * (len(BAOZHU) // 2) + [1] * (len(BAOZHU) // 2))
    }
    for i in range(num):
        get = overrandom(baozhu_list)
        baozhu_get[get] += 1
        reply = reply + "\n" + BAOZHU[get]
    gold.cost_item(user_id, group_id, 44, num)
    gold.get_baozhu(user_id, group_id, baozhu_get)
    await session.send(f"您获得的宝珠如下：{reply}")


@on_command("blessing", aliases=("模拟铸金", "模拟镀金"), only_to_me=False)
async def blessing(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    authority = gold.authority(group_id)
    if not authority[12]:
        return
    elif authority[12] == 2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
    blessing_num = gold.query(user_id, group_id, [54])[54]
    if not blessing_num:
        await session.finish("攻击祝福宝珠数量不足")
    def get_weapon_list12(user_id, group_id, item_id):
        """
        给定某人某群及item_id寻找该id下所有武器以及强化等级
        :param user_id: QQ
        :param group_id: QQ group
        :param item_id: item_id
        :return: [weapon_id]
        """
        sql2 = f'SELECT item_uni_id FROM user_package WHERE user_id = {user_id} AND group_id = {group_id} AND item_id = {item_id}'
        conn = pymysql.connect(host='localhost', user='root', password='', database='test2', charset='utf8mb4')
        cursor = conn.cursor()
        cursor.execute(sql2)
        result = cursor.fetchone()
        uni_id = result[0]
        sql3 = f'SELECT weapon_id FROM strength WHERE item_uni_id = {uni_id} AND strength_lvl = 12'
        cursor2 = conn.cursor()
        cursor2.execute(sql3)
        result2 = cursor2.fetchall()
        _weapon_list = [i[0] for i in result2]
        conn.close()
        return _weapon_list

    reply = "请选择您要铸金的物品:"
    weapons = [8, 9, 10, 11, 14] + [i + 30 for i in range(14)]
    bag_list = gold.query(user_id, group_id, weapons)
    j = 1
    weapon_list = []
    weapons_item_id = []
    for i, num in enumerate(bag_list):
        if num:
            wp_list = get_weapon_list12(user_id, group_id, i)
            weapon_list = weapon_list + wp_list
            for weapons1 in wp_list:
                reply = reply + "\n" + f"{j}:{ITEM_NICKNAME[i][0]}(+12)"
                j += 1
                weapons_item_id.append(i)
    if not weapon_list:
        session.finish("您没有可以铸金的武器！")
    choice = await session.aget(prompt=reply)
    try:
        num0 = int(choice) - 1
    except ValueError:
        session.finish("请输入正确的序号")
        return
    weapon_id = weapon_list[num0]
    gold.cost_item(user_id,group_id,54)
    result = 1 if random.randint(1, 20) <= 4 else 0
    if result:
        await session.send("成功  ^_^")
        add_strength_lvl(weapon_id)
    else:
        await session.send("失败...囧")


if __name__ == '__main__':
    pass
