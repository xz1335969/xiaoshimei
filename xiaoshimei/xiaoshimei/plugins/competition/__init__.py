from nonebot import on_command, CommandSession,IntentCommand
import config


@on_command("create_comp", aliases=("创建比赛", "发起比赛"))
async def create_comp(session: CommandSession):
    if session.event.group_id not in config.PERMIT_GROUP:
        return
    else:
        group_id = session.event.group_id
        user_id = session.event.user_id
        info = await session.bot.get_group_member_info(user_id=user_id, group_id=group_id)
        if not session.current_arg.strip():
            comp_name = await session.aget("comp_name", prompt="请输入比赛名称")
        else:
            comp_name = session.current_arg.strip()
        while True:
            try:
                comp_txt = open(f"./competitions/{group_id}_{comp_name}", "x+", encoding="utf-8")
                break
            except FileExistsError:
                _ = await session.aget("comp_name", prompt="比赛名称已存在，是否重新输入名称，选择“否”将跳转到原比赛的介绍")
                if _ == "是":
                    comp_name = await session.aget("comp_name", prompt="请输入比赛名称")
                    continue
                if _ == '否':
                    return IntentCommand(100.0, "comp_introduction", current_arg={comp_name})
            except:
                report = "未知错误"
                await session.send(report)
                return
            comp_txt.write(f"发起人：{info['card']}\n")
            _ = await session.aget("text", prompt="请输入比赛说明：直接发送为换行，发送单个空格视为停止")
            comp_txt.write(f"{_}\n")
            while _.strip():
                _ = await session.aget("text", prompt="请输入比赛说明：输入空格视为停止")
                comp_txt.write(f"{_}\n")
            comp_txt.close()


@on_command("comp_introduction",aliases="比赛说明")
async def comp_introduction(session:CommandSession):
    if session.event.group_id not in config.PERMIT_GROUP:
        return
    else:
        pass


@on_command('all_comp',aliases="全部比赛")
async def all_comp(session:CommandSession):
    if session.event.group_id not in config.PERMIT_GROUP:
        return
    else:
        # 1. 遍历文件夹，找出本群名字开头的文件
        pass


@on_command("parti",aliases=("报名", "比赛报名"))
async def parti(session:CommandSession):
    if session.event.group_id not in config.PERMIT_GROUP:
        return
    else:
        # 1. 列出本群全部比赛列表
        # 2. 选择比赛报名
        # 3. 将报名信息写在文件
        group_id = session.event.group_id
        user_id = session.event.user_id
        info = await session.bot.get_group_member_info(user_id=user_id, group_id=group_id)
