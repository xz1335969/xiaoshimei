import math
import random

from xiaoshimei.xiaoshimei_plugins.goldsystem.cls import *

wawale = on_command("wawale",aliases={"挖挖乐"})
guess_coin = on_command("guess_coin",aliases={'猜硬币'})


@guess_coin.handle()
async def _(event:GroupMessageEvent,state:T_State):
    auth = authority(event.group_id, "guess_coin")
    if auth == 0:
        return
    elif auth == 2:
        if not 1 < datetime.datetime.now().hour < 10:
            await guess_coin.finish("请在1:00——10:00期间使用本系统")
    await guess_coin.send("游戏介绍：系统将随机投掷硬币，猜硬币的正反面，猜对了当前下注金变为1.9倍（收取0.1倍服务费），猜错了当前下注金归零")


@guess_coin.got("num",prompt="请输入您下注的金币数量")
async def _(event:GroupMessageEvent,state:T_State):
    try:
        gold_num = int(state["num"])
    except ValueError:
        await guess_coin.reject("请输入正确的下注数量")
    else:
        state["num"] = gold_num
        state["num_now"] = gold_num

@guess_coin.got("coin",prompt="请输入要猜测的正反面，输入“取消”停止游戏")
async def _(event:GroupMessageEvent,state:T_State):
    guess_text = ("反面","正面")
    if state["coin"] in (1,"正面","1","正"):
        guess = 1
    elif state["coin"] in (0,"反面","0","反"):
        guess = 0
    elif state["coin"] in ("取消","不玩了","结束"):
        await guess_coin.finish(f"游戏结束，您一共获得了{state['num_now']}金币")
        return
    else:
        await guess_coin.reject("请输入正确的值，例如”正面“,“正”,“1”等等")
        guess = None
    rand = []
    for i in range(5):
        rand.append(random.normalvariate(0,1))
    randint = 0 if sum(rand)< 0 else 1
    if guess is None:
        pass
    if guess == randint:
        state["num_now"] = int(state["num_now"] * 1.9)
        result = 1
        await guess_coin.reject(f"恭喜您猜中了，当前下注金为{state['num_now']}.")

    else:
        result = 0
        await guess_coin.finish("很遗憾您猜错了，游戏结束.")

