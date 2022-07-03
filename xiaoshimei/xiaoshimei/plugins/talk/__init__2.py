from nonebot import on_command,CommandSession
import random,config


@on_command("love", aliases=("我爱你", "我喜欢你", "老婆", "cpdd"))
async def love(session: CommandSession):
    if session.event.group_id not in config.PERMIT_GROUP:
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
    if session.event.group_id not in config.PERMIT_GROUP:
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