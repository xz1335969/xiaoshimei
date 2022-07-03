from nonebot import on_command,CommandSession,MessageSegment
import random
from nonebot import on_natural_language,NLPSession,IntentCommand
import xiaoshimei.plugins.goldsystem.gold as gold
import time

@on_command("heisi", aliases=("来张黑丝", "来张嗨丝", "kkhs", "kkt", "看看黑丝", "看看白丝", "看看丝袜"), only_to_me=True)
async def heisi(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    authority = gold.authority(group_id)
    if not authority[21]:
        return
    elif authority[21] ==2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    else:
        user_id = session.event["user_id"]
        if user_id == 1351551853:
            await session.send("大师姐，不要这样嘛")
            return
        elif user_id == 645577403:
            await session.send(MessageSegment.image("C:\\resources\\heisi.jpg"))
            return
        else:
            report = ["没有，爬", "噫，四斋蒸鹅心", "你们就是这样对待小师妹的吗[CQ:face,id=107]"]
            randomnum = random.randint(0, len(report) - 1)
        await session.send(report[randomnum])


@on_command("setu", aliases=("来点涩图", "来张涩图", "kkp", "kkx", "kknz", "kkb"))
async def setujinyan(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    authority = gold.authority(group_id)
    if not authority[1]:
        return
    elif authority[1] ==2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    else:
        if user_id == 1351551853:
            await session.send("师姐不要啦")
            return
        else:
            banner_list_txt = open("./banner_list.txt", "r+", encoding="utf-8")
            banner_list = {}
            for each_line in banner_list_txt:
                banner_list[int(each_line.split(":")[0])] = int(each_line.split(":")[1])
            banner_list_txt.close()
            group_id = session.event.group_id
            if user_id not in banner_list:
                banner_list[user_id] = 1
            else:
                banner_list[user_id] += 1
            if banner_list[user_id] <= 2:
                report = f"[CQ:at,qq={user_id}] 不许涩涩，第{banner_list[user_id]}次警告！"
            else:
                report = f"[CQ:at,qq={user_id}] 不许涩涩，冷静一会去吧"
                try:
                    await session.bot.set_group_ban(group_id=group_id, user_id=user_id, duration=120)
                except:
                    report = report + "\n禁言失败,权限不足"
                banner_list[user_id] = 0
                banner_list_txt1 = open("./banner.txt", "a+", encoding="utf-8")
                banner_list_txt1.write(f"{user_id}\n")
                banner_list_txt1.close()
            banner_list_txt = open("./banner_list.txt", "w+", encoding="utf-8")
            for items in banner_list:
                wr = f"{items}:{banner_list[items]}\n"
                banner_list_txt.write(wr)
            banner_list_txt.close()
            await session.send(report)


@on_natural_language(keywords=("涩图", "色图", "裸照"), only_to_me=False)
async def _(session: NLPSession):
    return IntentCommand(90.0, "setu")