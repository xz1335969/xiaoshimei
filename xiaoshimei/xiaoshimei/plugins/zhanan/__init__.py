from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
import config
import re


def scan_permit(user_id,name="momo"):
    file0 = open(f"./{name}_cps.txt", "r+", encoding="utf8")
    cps = []
    for each_line in file0:
        cps.append(each_line.strip("\ufeff").strip())
    file0.close()
    if user_id in cps:
        return 1
    else:
        return 0


@on_command("white_list", aliases="添加白名单", only_to_me=False)
async def white_list(session: CommandSession):
    if session.event.user_id not in (3303400017, 645577403):
        return
    qq_num = session.current_arg.strip()[10:-1]
    if scan_permit(qq_num):
        session.finish("添加失败，该QQ已存在")
    else:
        file0 = open("./momo_cps.txt", "a+", encoding="utf8")
        file0.write(str(qq_num) + "\n")
        file0.close()
        session.finish("添加白名单成功")


@on_command("zhananqusi", aliases="渣男去死", only_to_me=False)
async def zhananqusi(session: CommandSession):
    if not gold.get_permit_group(session.event.group_id):
        return
    else:
        user_id = session.event.user_id
        group_id = session.event.group_id
        if session.current_arg == "遗憾":
            await session.bot.set_group_ban(group_id=group_id, user_id=user_id, duration=60)
        elif session.current_arg == "晴" or session.current_arg == "墨墨":
            if scan_permit(str(user_id)):
                pass
            else:
                await session.bot.set_group_ban(group_id=group_id, user_id=user_id, duration=60)
                await session.send(f"[CQ:at,qq={user_id}]小小的警告一下，以后不许皮了")
        elif session.current_arg == "墨墨2":
            if scan_permit(str(user_id)):
                pass
            else:
                await session.bot.set_group_ban(group_id=group_id, user_id=user_id, duration=300)
                await session.send(f"来自墨墨的警告：[CQ:at,qq={user_id}]竟敢对墨墨桑图谋不轨")
        elif session.current_arg == "晴2":
            if scan_permit(str(user_id),name="qing"):
                pass
            else:
                await session.bot.set_group_ban(group_id=group_id, user_id=user_id, duration=300)
                await session.send(f"来自狂的警告：[CQ:at,qq={user_id}]敢动我老婆是吧？")
        elif session.current_arg == "阿狂2":
            if user_id == 1659774763:
                await session.send("阿狂留言：么么阿晴老婆~~")
            else:
                await session.send("狂留言：？？？？？？？？？\n男同爬，我对阿晴一心一意")
        elif user_id == 879907266:
            await session.send("炸弹你一周拉不出[CQ:face,id=59]")


@on_natural_language(only_to_me=False, keywords="老婆")
async def _(session: NLPSession):
    user_id = session.event.user_id
    if user_id in (805037720,):  # 喊老婆就禁言的QQ
        return IntentCommand(98.0, "zhananqusi", current_arg='遗憾')
    else:
        return None


@on_natural_language(only_to_me=False, keywords="晴垢")
async def _(session: NLPSession):
    user_id = session.event.user_id
    if user_id == 879907266:
        return IntentCommand(100.0, "zhananqusi", current_arg='炸弹')
    else:
        return None


@on_natural_language(only_to_me=False, keywords=("cpdd", "我老婆"))
async def lp_ban(session: NLPSession):
    msg = session.msg
    list0 = [("晴", "1659774763"), ('墨墨', "3303400017")]
    for i in list0:
        if msg.find(i[0]) >= 0 or msg.find(i[1]) >= 0:
            return IntentCommand(99.0, "zhananqusi", current_arg=i[0])


@on_natural_language(only_to_me=False, keywords=("kkt", "kkhs","么么","啵啵","kkx","看看腿"))
async def lp_ban(session: NLPSession):
    msg = session.msg
    list0 = [("晴", "1659774763","清霜"), ('墨墨', "3303400017","留空222"),("阿狂", "645577403","狂少")]
    for i in list0:
        if msg.find(i[0]) >= 0 or msg.find(i[1]) >=0 or msg.find(i[2]) >= 0:
            return IntentCommand(99.0, "zhananqusi", current_arg=f"{i[0]}2")


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
    if user_id not in config.SUPERUSERS:
        return
    qq_num = int(get_qq(msg))
    index = msg.find("]")
    duration = int(msg[index+1:].strip())
    try:
        await session.bot.set_group_ban(group_id=group_id,user_id=qq_num,duration=duration)
    except Exception:
        print(repr(Exception))
        await session.finish("禁言失败，权限不足")


if __name__ == "__main__":
    pass
