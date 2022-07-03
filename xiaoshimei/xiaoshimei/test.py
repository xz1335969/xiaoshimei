import json
import codecs
import requests as REQ
import re
import os
from multiprocessing.dummy import Pool as ThreadPool

def mkdir(path):
    # 引入模块
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False

def GetMsgFromWeb(url, header, data, decode_type,verify=False):#获得网页内容
    rCount = 0
    is_error_Flag = True
    msg = "error"
    while is_error_Flag:
        try:
            if rCount == 5:
                print("[失效了]:{}".format(url))
                break
            if data == "":
                msg = REQ.get(url=url,headers = header,timeout=600,verify=verify)
            else:
                msg = REQ.post(url=url,headers = header,data=data,timeout=25,verify=verify)
            if decode_type == "":
                msg = msg
            else:
                msg.encoding = decode_type
                msg = msg.text
            is_error_Flag = False
        except Exception as e:
            print("[×:获取出错]" + url + "：")
            print('[×]错误所在的行号：', str(e.__traceback__.tb_lineno) + "")
            print('[×]错误信息', str(e) + "\n")
            rCount+=1
    return msg

    # for i,item in enumerate(result):
    #     path = f"C:/123/image/{i}.jpg"
    #     url = item
    #     msg = REQ.get(url=url)
    #     with open(path,"wb") as f:
    #         f.write(msg.content)
    #     print(f"{i}成功")

file = open("C:/123/123.html","r+",encoding="utf8")
txt = file.read()
file.close()
header = {
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}

result = re.findall(r'<span class="html-tag">&lt;img <span class="html-attribute-name">data-src</span>="<span class="html-attribute-value">(\S+)\?_width=1419&amp;_height=1971</span>', txt)


if __name__ == "__main__":
    print(txt)
    print(result)


