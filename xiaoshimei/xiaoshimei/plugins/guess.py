from nonebot import CommandSession,on_command
import random,config


@on_command("guess_number",aliases='猜数字2')
async def guess_number(session: CommandSession):
    if session.event.group_id not in config.PERMIT_GROUP:
        return
    else:
        temp = 0
        introduction = """猜数字游戏规则介绍:
        选择要猜的数字长度，系统会随机生成一个不含重复数字的数。
        接下来你输入一个数字，系统会反馈给你一个 XAYB 
        其中：
        X代表你输入的数字中，有X个数字正确且位置正确
        Y代表你输入的数字中，有Y个数字正确但位置不正确
        
        最多能进行10次尝试。
        请根据每一步的信息来一步步猜出数字吧。"""
        await session.send(introduction)
        _ = await session.aget('numlength',prompt="请输入你要猜的数字长度(1-9):")
        numlength = int(_)
        while numlength < 1 or numlength > 9:
            _ = await session.aget("numlength",prompt="数字长度错误，请输入1-9之间数字：")
            numlength = int(_)
        str1 = ""
        while temp < numlength:
            temp1 = random.randint(0, 9)
            if str(temp1) not in str1:
                str1 = str1 + str(temp1)
                temp += 1
                pass
        a = 0
        j = 0
        while a < numlength:
            if j == 10:
                report = "对不起，你猜错了10次，你输了"
                break
            else:
                _ = await session.aget("usernum",prompt="请输入你要猜的数字：")
                usernumber = str(_)
                a = 0
                b = 0
                for i in range(numlength):
                    if str1[i] == usernumber[i]:
                        a += 1
                for x in str1:
                    if x in usernumber:
                        b += 1
                b -= a
                await session.send(f"{a}A{b}B")
                j += 1
        else:
            report = f"恭喜您猜对了，您一共用了{j}次"
        await session.send(report+"\n游戏结束")
