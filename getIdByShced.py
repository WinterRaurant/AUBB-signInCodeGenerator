import requests
from bs4 import BeautifulSoup
import re

import getIdByRoom
import cookie2dict

def get_room_id(cookie):
    assert cookie != None
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
    }
    url = "http://10.20.11.166:88/ve/back/rp/common/myTimeTableDetail.shtml?method=skipIndex"

    response = requests.get(
        url, 
        headers=headers,
        cookies=cookie,
        verify=False,
    )

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find(class_='table-j table-live')
        if table:
            onclick_event = table.get('onclick')
            if onclick_event:
                match = re.search(r"intoVideo\('\w+','(\w+)'\)", onclick_event)
                if match:
                    second_param = match.group(1)
                    print("获取成功！courseSchedId=", second_param)
                    return 1, second_param
                else:
                    return 2, '未找到直播中的课'
            else:
                return 2, '未找到直播中的课'
        else:
            return 2, '未找到直播中的课'
    else:
        # print("请求失败，状态码:", response.status_code)
        return 3, response.status_code

def func():
    str = input('cookie:\n')
    cookie = cookie2dict.split_string_to_dict(str)
    flag, str = get_room_id(cookie=cookie)
    if flag == 1:
        return 1, getIdByRoom.getCourseSchedId(dorm_id=str, cookies=cookie)
    return flag, str

if __name__ == '__main__':
    pass