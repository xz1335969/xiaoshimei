from nonebot import on_command,CommandSession
import random
import xiaoshimei.plugins.goldsystem.gold as gold
import time


@on_command("love", aliases=("我爱你", "我喜欢你", "老婆", "cpdd"))
async def love(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    authority = gold.authority(group_id)
    if not authority[26]:
        return
    elif authority[26] ==2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    else:
        if session.event["user_id"] == 1351551853:
            re = "大师姐我也爱你[CQ:face,id=66][CQ:face,id=66]"
        elif session.event.user_id == 1659774763:
            re = "我也喜欢你[CQ:face,id=6]"
        elif session.event.user_id == 3303400017:
            re = "我也喜欢你[CQ:face,id=6]" if random.randint(0,10) <= 5 else "你是个好人[CQ:face,id=201]"
        else:
            report = ["我也喜欢你[CQ:face,id=6]", "你是个好人[CQ:face,id=201]"]
            randomnum = random.randint(0, 10)
            re = report[0] if randomnum == 0 else report[1]
        await session.send(re)


@on_command("kiss", aliases=("亲亲", "么么", "啵啵"))
async def kiss(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    authority = gold.authority(group_id)
    if not authority[27]:
        return
    elif authority[27] ==2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    else:
        if session.event["user_id"] == 1351551853:
            re = "么么大师姐[CQ:face,id=109]"
        elif session.event.user_id == 1659774763:
            re = "么么[CQ:face,id=6]" if random.randint(0,4) <= 3 else "不要欺负小师妹了[CQ:face,id=9]"
        elif session.event.user_id == 3303400017:
            randomnum = random.randint(0, 10)
            report = ["么么~~[CQ:face,id=109]", "不要欺负小师妹了[CQ:face,id=9]"]
            re = report[0] if randomnum <= 3 else report[1]
        elif session.event.user_id == 1260853774:
            re = "色鬼，爬[CQ:face,id=215]"
        else:
            report = ["么么~~[CQ:face,id=109]", "色鬼，爬[CQ:face,id=215]", "不要欺负小师妹了[CQ:face,id=9]"]
            randomnum = random.randint(0, 10)
            if randomnum == 0:
                re = report[0]
            elif randomnum <= 8:
                re = report[1]
            else:
                re = report[2]
        await session.send(re)


@on_command("away", aliases=("爬", "滚开", '我讨厌你'))
async def away(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    authority = gold.authority(group_id)
    if not authority[28]:
        return
    elif authority[28] ==2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    else:
        if session.event["user_id"] == 1351551853:
            re = "嘤嘤嘤[CQ:face,id=9]"
        else:
            report = [f"[CQ:at,qq={user_id}] 爬", "再这样小师妹要生气了"]
            randomnum = random.randint(0, 10)
            re = report[0] if randomnum == 0 else report[1]
            if randomnum == 0:
                await session.bot.set_group_ban(group_id=group_id, user_id=user_id, duration=60)
        await session.send(re)
