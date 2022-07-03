import time

from nonebot import on_command, CommandSession, MessageSegment
import random, config
import re
import xiaoshimei.plugins.goldsystem.gold as gold

modules_image = {
    'weapon': ("武器", "武器属性", "武器介绍"),
    'delay': ("d值", "d值计算"),
    'jiashen': ("假神", "假神任务", "假神获取"),
    'jiezhi': ("戒指", "戒指属性"),
    'shouzhuo': ("手镯", "手镯属性"),
    'petskill': ("宠物技能",),
    # 'petgrow': ("宠物属性", "宠物成长"),
    'kaikong': ("开孔", "开孔需求"),
    'xiulian': ("修炼", "修炼属性", "修炼需求"),
    'cardstatus': ("卡牌属性", "卡牌介绍"),
    'lidubiao': ('力度表', '65度打法', '20度打法', '30度打法', '50度打法'),
    'ronglian':("强化活动","强化熔炼活动")
}

modules_text = {
    'shoushi': [("首饰", "首饰属性", "首饰介绍"), '请选择你要查询的首饰类型：\n 戒指 \n 手镯'],
    'pet': [("宠物", "宠物介绍"), "请选择要查询的类型：\n 宠物技能 \n 宠物成长"],
    'card': [("卡牌",), "请选择要查询的类型：\n  卡牌属性 \n  做卡推荐"],
    'cardrecommand': [("做卡推荐22",), """萌新推荐做卡：
任何一种卡升到10级大约需要180盒，升到20级大约需要700盒，升到升到30级大约需要1850盒,加上初步洗点大概需要2000盒。所以商人出售的秒30卡一般指1998盒两组。根据自己的需求来选择做卡。

1.白嫖党：当然不做了，慢慢挂本白嫖就行了。
2.微氪党：魔狼卡/魔鹰卡二选一做一套+其他任意三张二属性卡，主卡一张1级牛头人卡
3.小氪党：任意二属性两套(推荐选运动会2属性)+小恶魔卡+拳王卡，主卡一张1级牛头人卡
4.中氪党：魔狼卡/魔鹰卡二选一做一套+小恶魔卡+拳王卡+任意二属性卡+酋长/裁判/国王/里格理主卡
5.重氪党：上面的基础上二属性卡换成哥布林战士 和 道拉夫上校卡
6.大老板：四神或者五神"""],
}


# 待装饰图片
def text_command(name, aliases0, report, *, only=False):
    @on_command(name, aliases=aliases0, only_to_me=only)
    async def _(session: CommandSession):
        await session.send(report)


def image_command(name, aliases0, url, *, only=False):
    @on_command(name, aliases=aliases0, only_to_me=only)
    async def _(session: CommandSession):
        report = MessageSegment.image(url)
        await session.send(report)


for item in modules_image:
    image_command(f"{item}", modules_image[item], f"C:/resources/{item}.png")

for item in modules_text:
    text_command(item, modules_text[item][0], modules_text[item][1])


@on_command("petgrow", aliases=("宠物属性", "宠物成长"), only_to_me=False)
async def petgrow(session: CommandSession):
    report = MessageSegment.image("C:/resources/petgrow.png") + MessageSegment.image("C:/resources/petstatus2.png")
    await session.send(report)


@on_command("jinglian", aliases=("精炼",), only_to_me=False)
async def jinglian(session: CommandSession):
    report = MessageSegment.image("C:/resources/jinglian.png")

    await session.send(report)
    await session.send("额外补充：4个恢复圣石1级精炼可能出S1宝珠，包括S1伤害")


@on_command("random", aliases=("随机数", "掷骰", "Dice", "dice"), only_to_me=False)
async def randomdice(session: CommandSession):
    num = session.current_arg.strip()
    if not num:
        report = "请输入：\n 1. 掷骰 数字 或 随机数 数字,例如：随机数 16\n 2.掷骰 下限-上限或 随机数 下限-上限，例如：掷骰 1-10"
    else:
        try:
            if "-" not in num:
                randomint = random.randint(1, int(num))
            else:
                num1 = num.split("-")
                randomint = random.randint(int(num1[0]), int(num1[1]))
            report = f"随机数的结果是:{randomint}"
        except:
            report = "请输入：\n 1.掷骰 数字 或 随机数 数字,例如：随机数 16\n 2.掷骰 下限-上限或 随机数 下限-上限，例如：掷骰 1-10"
    await session.send(report)


@on_command("award", aliases=("周贡抽奖", "抽奖"), only_to_me=False, permission=lambda sender: sender.is_superuser)
async def award(session: CommandSession):
    pass


@on_command("version", only_to_me=False)
async def version(session: CommandSession):
    await session.send(f"百花谷小师妹测试版Ver. {config.VERSION}")


@on_command("help", aliases=("帮助", "指令表", "功能", "菜单"), only_to_me=False)
async def jinglian(session: CommandSession):
    arg = session.current_arg.strip()
    if arg:
        return
    report = MessageSegment.image("C:/resources/help.png")
    await session.send(report)
    if not gold.get_permit_group(session.event.group_id):
        report = MessageSegment.image("C:/resources/help2.png")
        await session.send(report)


def randomlist(list1: list):
    for i in range(len(list1) - 1):
        num = random.randint(i, len(list1) - 1)
        _ = list1[num]
        list1[num] = list1[i]
        list1[i] = _
    return list1


@on_command("divide", aliases="分组", only_to_me=False)
async def divide(session: CommandSession):
    arg = session.current_arg.strip()
    group = arg.split(' ')
    if len(group) % 2:
        await session.send("报名人数为奇数！")
        return
    else:
        list0 = randomlist(group)
        list1 = list0[:len(list0) // 2]
        list2 = list0[len(list0) // 2:]
        await session.send(f"分组结果如下：\n第一组：{','.join(list1)}\n第二组：{','.join(list2)}")


@on_command("common_account", aliases="公用号", only_to_me=False)
async def common_account(session: CommandSession):
    if session.event.group_id in [817466507, 940650004]:
        user_id = session.event.user_id
        group_id = session.event.group_id
        prompt = "公用号：可以申请使用山海的公用号带本或带竞技，严禁外借，严禁进行一些其他操作，所有借用公共号的行为都将被系统自动记录.仍要借用请回复1，否则回复0"
        reply = await session.aget("reply", prompt=prompt)
        if reply != '1':
            await session.send("已取消")
            return
        else:
            txt = open("./common_account_usage.txt", "r", encoding="UTF-8-sig")
            now_time = time.time()
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            last_borrow = txt.readline().strip()
            last_borrow_time = last_borrow.split(",")[2].strip("\ufeff")
            last_borrow_id = int(last_borrow.split(",")[0].strip("\ufeff"))
            ts = time.mktime(time.strptime(last_borrow_time, "%Y-%m-%d %H:%M:%S"))
            print(now_time - ts)
            txt.close()
            if now_time - ts <= 2400:
                await session.finish(
                    f"此号距离上一次借用不超过40分钟，请稍后再来尝试，上次借用时间为{last_borrow_time}，借用人:[CQ:at,qq={last_borrow_id}]")
                return
            await session.send(f"[CQ:at,qq={user_id}]消息已下发，请查看私聊消息。")
            report = "昵称：红星闪闪\n账号：jkc1112\n密码：ggggbbbb886\n此消息会在30秒后撤回，请尽快登录"
            _ = await session.bot.send_private_msg(user_id=user_id, message=report)
            msg_id = _["message_id"]
            info = await session.bot.get_group_member_info(group_id=group_id, user_id=user_id)
            nickname = info['card']
            towrite = f'{user_id},{nickname},{now}\n'
            txt = open("./common_account_usage.txt", "a+", encoding="UTF-8")
            txt.seek(0, 0)
            txt.write(towrite)
            txt.close()
            time.sleep(30)
            await session.bot.delete_msg(message_id=msg_id)
    elif session.event.group_id == 953594788:
        user_id = session.event.user_id
        group_id = session.event.group_id
        prompt = "公用号：可以申请使用本公会的公用号带本或带竞技，严禁外借，严禁进行一些其他操作，所有借用公共号的行为都将被系统自动记录.仍要借用请回复1，否则回复0"
        reply = await session.aget("reply", prompt=prompt)
        if reply != '1':
            await session.send("已取消")
            return
        else:
            txt = open("./common_account_usage2.txt", "r", encoding="UTF-8-sig")
            now_time = time.time()
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            last_borrow = txt.readline().strip()
            last_borrow_time = last_borrow.split(",")[2].strip("\ufeff")
            last_borrow_id = int(last_borrow.split(",")[0].strip("\ufeff"))
            ts = time.mktime(time.strptime(last_borrow_time, "%Y-%m-%d %H:%M:%S"))
            print(now_time - ts)
            txt.close()
            if now_time - ts <= 2400:
                await session.finish(
                    f"此号距离上一次借用不超过40分钟，请稍后再来尝试，上次借用时间为{last_borrow_time}，借用人:[CQ:at,qq={last_borrow_id}]")
                return
            await session.send(f"[CQ:at,qq={user_id}]消息已下发，请查看私聊消息。")
            report = '''使用公用号前务必先查看公用号是否在线，严禁顶号！公用号用完后及时下线！
小野梦                账号1CAB880FE6B121636311FE4C505E15E1（0-8点禁止上号）
                          密码shengxiaupup123
回归的萌新          账号13294077370
                          密码1234567890 
盛夏Seprincess   账号lol7860786133（0-10点禁止上号）
                          密码123123
盛夏OnceQueen 账号guxinjinrong1（0-10点禁止上号）
                          密码333233

'''
            _ = await session.bot.send_private_msg(user_id=user_id, message=report)
            msg_id = _["message_id"]
            info = await session.bot.get_group_member_info(group_id=group_id, user_id=user_id)
            nickname = info['card']
            towrite = f'{user_id},{nickname},{now}\n'
            txt = open("./common_account_usage2.txt", "a+", encoding="UTF-8")
            txt.seek(0, 0)
            txt.write(towrite)
            txt.close()
            time.sleep(30)
            await session.bot.delete_msg(message_id=msg_id)
    else:
        return


def get_qq(cq_msg):
    res = re.findall(r'[Qq]{2}=(\w+)\]', cq_msg)
    if len(res):
        return res[0]
    return None


@on_command("group_ban",aliases=("禁言","群组禁言"),only_to_me=False)
async def group_ban(session:CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    msg = session.current_arg.strip()
    if not gold.superuser(user_id,group_id):
        return
    qq_num = int(get_qq(msg))
    index = msg.find("]")
    duration = int(msg[index+1:].strip())
    try:
        await session.bot.set_group_ban(group_id=group_id,user_id=qq_num,duration=duration)
    except Exception:
        print(repr(Exception))
        await session.finish("禁言失败，权限不足")