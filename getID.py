import requests
import re
import json

import cookie2dict

data = []
cookies = ''

def getCourseSchedId(dorm_id=1075):

    assert dorm_id != None
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
    }

    params = {
        'method': 'videoList1',
        'dorm_id': dorm_id,
        'bt': '1',
        'userRole': '1',
    }

    response = requests.get(
        'http://10.20.11.166:88/ve/back/video/teachingVisits.shtml',
        params=params,
        cookies=cookies,
        headers=headers,
        verify=False,
    )

    response_content = response.text
    match = re.search(r"var courseSchedId = '(\d+)';", response_content)

    if match:
        courseSchedId = match.group(1)
        print(f"courseSchedId: {courseSchedId}")
        return courseSchedId
    else:
        print("未找到匹配的内容")
        return None


def filter(data, key, value=0):
    if value != 0:
        return [item for item in data if item[key] == value]
    
    unique_data = {item[key] for item in data}
    dict = [{'id': idx + 1, key: item} for idx, item in enumerate(unique_data)]
    return dict

def getRoomID():
    # global data
    with open('roomID.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    campus = input('学院路输入1，沙河输入2：\n')
    while campus != '1' and campus != '2':
        print('两个数字有这么难打？')
    if campus == '1':
        data_campus = filter(data=data, key='campus', value='学院路校区')
    else:
        data_campus = filter(data=data, key='campus', value='沙河校区')

    list_building = filter(data=data_campus, key='building')
    str = '输入教学楼id:'
    for item in list_building:
        str += f"\n \t{item['building']}:\t{item['id']}"
    print(str)
    building_id = int(input())
    campus_value = next((item['building'] for item in list_building if item['id'] == building_id), None)
    data_classroom = filter(data=data_campus, key='building', value=campus_value)

    list_classroom = filter(data=data_classroom, key='classroom')
    str = '输入教室id:'
    for item in list_classroom:
        str += f"\n \t{item['classroom']}:\t{item['id']}"
    print(str)
    classroom = int(input())
    room_name =  next((item['classroom'] for item in list_classroom if item['id'] == classroom), None)
    # print(room_name)

    roomid =  next((item['id'] for item in data_classroom if item['classroom'] == room_name), None)
    # print(roomid)
    return roomid

def func():
    global cookies
    id = getRoomID()
    str = input('cookie:\n')
    cookies = cookie2dict.split_string_to_dict(str)
    return getCourseSchedId(id)
    

if __name__ == '__main__':
    func()
    