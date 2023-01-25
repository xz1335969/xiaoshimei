import base64
import requests

API_KEY = "OtmpsqDbjKURb28MuliThLWu"
SECRET_KEY = "TtLje8tEXMlZYGbYwYk9sEDwZGTQzj8e"


def main(file: str):
    """
    :param file: 图片文件地址
    :return:
    """
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=" + get_access_token()

    # image 可以通过 get_file_content_as_base64("C:\fakepath\QQ截图20221110041958.png") 方法获取
    if file.startswith("http://") or file.startswith("https://"):
        payload = f"url={file}"
    else:
        b64 = get_file_content_as_base64(file)
        payload = f'image={b64}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text


def get_file_content_as_base64(path):
    """
    获取文件base64编码
    :param path: 文件路径
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf8")


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == '__main__':
    pass
