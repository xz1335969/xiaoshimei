from xiaoshimei.xiaoshimei_plugins.goldsystem.cls import *
from nonebot import require

scheduler = require("nonebot_plugin_apscheduler").scheduler


async def league_scheduler():
    bot = get_bot("2842320249")
    await bot.call_api("send_group_msg", group_id=817466507, message=f"大家新年快乐！在此祝愿各位新的一年里身体健康。事业顺利，万事如意！")
    await bot.call_api("send_group_msg", group_id=643057141, message=f"大家新年快乐！在此祝愿各位新的一年里身体健康。事业顺利，万事如意！")
    await bot.call_api("send_group_msg", group_id=414279693, message=f"大家新年快乐！在此祝愿各位新的一年里身体健康。事业顺利，万事如意！")


scheduler.add_job(league_scheduler, "cron", second=0, hour=0, minute=0, day_of_week="sun")


async def scheduler2():
    bot = get_bot("2842320249")
    await bot.call_api("send_group_msg", group_id=186891950, message=f"大家新年快乐！小师妹在此祝愿各位新的一年里身体健康。事业顺利，万事如意！")

scheduler.add_job(scheduler2,"cron",second=0,hour=23,minute=47,day=1,month=1)

