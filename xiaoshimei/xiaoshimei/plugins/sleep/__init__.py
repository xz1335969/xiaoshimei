from nonebot import on_command,CommandSession
from nonebot import on_natural_language,NLPSession,IntentCommand
import time,config,os
from jieba import posseg
import xiaoshimei.plugins.goldsystem as gold


CN_NUMS = {"一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "零": 0, "十": 10}


def cn_to_num(cn_num):
    """
    2位数以内的汉字转阿拉伯数字
    :param cn_num: 汉字版数字
    :return: 阿拉伯数字
    """
    if len(cn_num) == 1:
        num_out = CN_NUMS[cn_num]
    else:
        if cn_num[0] == "十":
            num_out = 10 + CN_NUMS[cn_num[1]]
        elif cn_num[-1] == "十":
            num_out = 10 * CN_NUMS[cn_num[0]]
        else:
            num = cn_num.split("十")
            num_out = 10 * CN_NUMS[num[0]] + CN_NUMS[num[1]]
    return num_out


def str_cn_to_num(str0):
    """
    字符串中，所有的汉字版数字转化为阿拉伯数字
    :param str0: 待转化字符串
    :return: 带阿拉伯数字的字符串
    """
    i = 0
    new_str = ''
    while i < len(str0):
        if str0[i] in CN_NUMS:
            if str0[i + 1] not in CN_NUMS:
                new_str = new_str + str(cn_to_num(str0[i:i + 1]))
                i += 1
            elif str0[i + 2] not in CN_NUMS:
                new_str = new_str + str(cn_to_num(str0[i:i + 2]))
                i += 2
            else:
                new_str = new_str + str(cn_to_num(str0[i:i + 3]))
                i += 3
        else:
            new_str = new_str + str0[i]
            i += 1
    return new_str


@on_command("sleeptime", aliases="精致睡眠套餐")
async def sleeptime(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    authority = gold.authority(group_id)
    if not authority[29]:
        return
    elif authority[29] ==2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    else:
        if not session.current_arg:
            _ = await session.aget("time0", prompt="请输入睡眠时间，单位：小时")
            time2 = float(_)
        else:
            time2 = float(session.current_arg)
        if 11 > float(time2) >= 5:
            time1 = int(time2 * 60 * 60)
            try:
                await session.bot.set_group_ban(group_id=group_id, user_id=user_id, duration=time1)
                sleep_list_txt = open(f"./sleep_list_{group_id}.txt", "a+", encoding="utf-8")
                release_time = time.time() + time1
                sleep_list_txt.write(f"{user_id}:{release_time}\n")
                sleep_list_txt.close()
                return
            except:
                report = "禁言失败，权限不足"
        else:
            report = "合理的睡眠时间为5—11小时哦~"
        await session.send(report)


@on_command("sleeplist", aliases=("睡眠名单", "睡觉名单", "睡眠列表"), only_to_me=False)
async def sleeplist(session: CommandSession):
    group_id = session.event.group_id
    user_id = session.event.user_id
    player = gold.Person(user_id,group_id)
    authority = gold.authority(group_id)
    if not player.is_superuser:
        return
    if not authority[29]:
        return
    elif authority[29] ==2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    else:
        try:
            sleep_list_txt = open(f"./sleep_list_{group_id}.txt", "r+", encoding="utf-8")
            sleep_list = {}
            report = ''
            for each_line in sleep_list_txt:
                if time.time() < float(each_line.split(":")[1]):
                    sleep_list[int(each_line.split(":")[0])] = float(each_line.split(":")[1])
                    card_info = await session.bot.get_group_member_info(group_id=group_id,
                                                                        user_id=int(each_line.split(":")[0]))
                    release_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(each_line.split(":")[1])))
                    report = report + f"{card_info['card']}  解封时间：{release_time}\n"
            sleep_list_txt.close()
            new_sleep_list_txt = open(f"./sleep_list_{group_id}.txt", "w+", encoding="utf-8")
            for item in sleep_list:
                new_sleep_list_txt.write(f"{item}:{sleep_list[item]}\n")
        except:
            report = "没有人在睡眠禁言"
        await session.send(report)


@on_command("repeat", aliases="复读")
async def repeat(session: CommandSession):
    text = session.current_arg.strip()
    await session.send(text)


@on_command("repeat_group", aliases="群组复读")
async def repeat_group(session: CommandSession):
    text = session.current_arg.strip()
    await session.bot.send_group_msg(group_id=817466507, message=text)


@on_natural_language(keywords="睡眠套餐")
async def __(session: NLPSession):
    group_id = session.event.group_id
    authority = gold.authority(group_id)
    if not authority[29]:
        return
    elif authority[29] ==2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    else:
        now = time.time()
        hour = (int(now / 60 / 60)) % 24
        if 20 >= hour >= 15:
            stripped_msg = session.msg_text.strip()
            stripped_msg1 = str_cn_to_num(stripped_msg)
            words = posseg.lcut(stripped_msg1)
            i = 0
            hours = 0
            minutes = 0
            for word in words:
                if word.word == "小时":
                    hours = int(words[i - 1].word)
                elif word.word == "分钟":
                    minutes = int(words[i - 1].word)
                    print(word)
                i += 1
            dura_time = f"{hours + minutes / 60:.5f}"
            return IntentCommand(90.0, "sleeptime", current_arg=dura_time)
        else:
            return IntentCommand(100.0, "repeat", current_arg="不在睡眠时间内，23:00——4:00再来试试吧.")


@on_command("release_all", aliases="全部起床", only_to_me=False)
async def group_release_all(session: CommandSession):
    group_id = session.event.group_id
    authority = gold.authority(group_id)
    if not authority[20]:
        return
    elif authority[20] ==2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    else:
        if session.event.user_id == 1351551853 or session.event.user_id == 645577403:
            sleep_list_txt = open(f"./sleep_list_{group_id}.txt", "r+", encoding="utf-8")
            for each_line in sleep_list_txt:
                if time.time() < float(each_line.split(":")[1]):
                    await session.bot.set_group_ban(group_id=group_id, user_id=int(each_line.split(":")[0]), duration=1)
            sleep_list_txt.close()
            try:
                os.remove(f"./sleep_list_{group_id}.txt")
            except:
                await session.send("已全部起床")
        else:
            await session.send("权限不足")