from nonebot import on_command, get_bot, on_message, on_keyword, on_regex, on_notice, on_request
from nonebot.adapters import Event, Message, MessageTemplate
from nonebot.adapters.onebot.v11 import MessageSegment, MessageEvent, PrivateMessageEvent, GroupMessageEvent, Bot, \
    GROUP_ADMIN, GROUP_OWNER, GROUP_MEMBER, RequestEvent, GroupRequestEvent
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from nonebot.permission import SUPERUSER, Permission
import json, os

plugin_manager = on_command("插件管理", aliases={"插件设置", "插件开关"}, permission=SUPERUSER)


def get_dir(path: str):
    dirs = os.listdir(path)
    for dir_name in dirs:
        if os.path.isfile(dir_name):
            dirs.remove(dir_name)
    return dirs


@plugin_manager.handle()
async def _(event: GroupMessageEvent, matcher: Matcher, state: T_State):
    with open("plugin_config.json", encoding="utf8", mode="r+") as fp:
        plugin_config_dict = json.load(fp)
    all_plugin = get_dir(".\\plugins")
    text = {}
    open_plugins = plugin_config_dict["plugins"]
    for idx, txt in enumerate(open_plugins):
        open_plugins[idx] = txt[19:]
    for plugins in all_plugin:
        text[plugins] = "开启" if plugins in open_plugins else "关闭"
    txt = "\n".join([f"{a}:{text[a]}" for a in text])
    await plugin_manager.send(f'目前的插件情况有{text}')
    state["open_plugins"] = open_plugins


@plugin_manager.got("plugin_choice", prompt="请选择您要更改状态的插件名称，用空格隔开，取消操作输入”取消“")
async def _(state: T_State):
    plugin_choice = str(state["plugin_choice"]).strip().split(" ")
    if plugin_choice is None or plugin_choice[0] == "取消":
        await plugin_manager.finish("取消")
    else:
        for i in plugin_choice:
            if i not in state["open_plugins"]:
                await plugin_manager.send(f"{i}模块不存在")
