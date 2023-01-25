import json

from xiaoshimei.xiaoshimei_plugins.goldsystem.cls import *
import xiaoshimei.xiaoshimei_plugins.arknights.ocr as ocr
import xiaoshimei.xiaoshimei_plugins.arknights.resources as res

gongzhao = on_command("公招",aliases={"公开招募","公招计算"})

@gongzhao.handle()
async def _(event:MessageEvent,arg:Message = CommandArg()):
    if not arg:
        await gongzhao.finish("""请输入：
        公招+空格+五个tag（用空格隔开）
        如：公招 减速 先锋干员 治疗 重装干员 医疗干员
        或者 公招+空格+仅包含tag的图片""")
        return
    elif "image" in [j.type for j in arg]:
        url = arg[0].data["url"]
        result = json.loads(ocr.main(url))
        tags = [i["words"].strip('.') for i in result["words_result"]]

    elif arg.extract_plain_text():
        tags = arg.extract_plain_text().split()
    else:
        report = "请输入对应标签"
        await gongzhao.finish(report)
        return
    result = res.check(*tags)
    if not result:
        result = "没有必出4星以上的标签，随便选吧"
    await gongzhao.finish(result)


