from nonebot import on_command,CommandSession
import random
import xiaoshimei.plugins.goldsystem.gold as gold
import time


@on_command("leavemsg", aliases="留言", only_to_me=False)
async def leavemsg(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    authority = gold.authority(group_id)
    if not authority[22]:
        return
    elif authority[22] ==2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    else:
        try:
            while not session.current_arg:
                session.current_arg = await session.aget(key="lvmsg", prompt="请输入留言内容")
            name = "匿名用户"
            if session.event.group_id is None:
                friends = await session.bot.get_friend_list()
                for items in friends:
                    if items['user_id'] == user_id:
                        name = items['nickname']
                        break
            else:
                group_id = session.event.group_id
                info = await session.bot.get_group_member_info(group_id=group_id, user_id=user_id)
                name = info['card']
            if 'CQ:image' in session.current_arg:
                await session.send('禁止留言图片')
                return
            else:
                leavemsg_txt = open("./leavemsg.txt", "a+", encoding="utf-8")
                leavemsg_txt.write(f"{name}: {session.current_arg}\n")
                leavemsg_txt.close()
                await session.send("留言成功")
        except:
            await session.send("留言失败")


@on_command("leave_private_msg", aliases=("私密留言", "匿名留言"), only_to_me=True)
async def leave_private_msg(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    authority = gold.authority(group_id)
    if not authority[23]:
        return
    elif authority[23] ==2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    else:
        while not session.current_arg:
            session.current_arg = await session.aget(key="lvmsg", prompt="请输入留言内容")
        try:
            leavemsg_txt = open("./leavemsg.txt", "a+", encoding="utf-8")
            leavemsg_txt.write(f"匿名用户: {session.current_arg}\n")
            leavemsg_txt.close()
            await session.send("留言成功")
        except:
            await session.send("留言失败")


@on_command("left_msg", aliases=("随机留言", '留言板'), only_to_me=False)
async def left_msg(session: CommandSession):
    group_id = session.event.group_id
    authority = gold.authority(group_id)
    if not authority[24]:
        return
    elif authority[24] ==2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    else:
        leavemsg_txt = open("./leavemsg.txt", "r+", encoding="utf-8")
        leavemsg = []
        for each_line in leavemsg_txt:
            leavemsg.append(each_line)
        leavemsg_txt.close()
        randomint = random.randint(0, len(leavemsg) - 1)
        randomint2 = random.randint(0, 1726)
        if randomint2 == 17 or randomint2 == 1726:
            report = "（隐藏留言）狂：阿晴...我喜欢你~"
        else:
            report = leavemsg[randomint]
        await session.send(report)


@on_command("left_msg_all", aliases="全部留言", only_to_me=False)
async def left_msg(session: CommandSession):
    group_id = session.event.group_id
    authority = gold.authority(group_id)
    if not authority[25]:
        return
    elif authority[25] ==2:
        if 4 < (int(time.time()) // 1800) % 48 < 33 and session.event.group_id != 940650004:
            await session.send("请在0：30——10:00期间使用本系统")
            return
    else:
        leavemsg_txt = open("./leavemsg.txt", "r+", encoding="utf-8")
        leavemsg_all = ''
        for each_line in leavemsg_txt:
            leavemsg_all = leavemsg_all + each_line
        leavemsg_txt.close()
        await session.send(leavemsg_all)
