import requests
import json
import re
from datetime import datetime

student_number = ''


def get_courseShcedID(userId, sessionId, date=datetime.now().strftime("%Y-%m-%d")):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Referer': 'https://iclass.buaa.edu.cn:8346/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
        'sec-ch-ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sessionId': sessionId,
    }

    params = {
        'id': userId,
        'dateStr': date,
    }

    response = requests.get(
        'https://iclass.buaa.edu.cn:8346/app/course/get_stu_course_sched.action',
        params=params,
        headers=headers,
    )
    json_data = json.loads(response.text)
    for item in json_data['result']:
        classBeginTime = item['classBeginTime']
        classEndTime = item['classEndTime']
        start_time = datetime.strptime(classBeginTime, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(classEndTime, "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()
        if start_time <= current_time <= end_time:
            print(item['id'])
            return 1, item['id']
        
    print('现在不在上课！')
    return 2, ''

def get_sessionID():
    url = 'https://iclass.buaa.edu.cn:8346/app/user/login.action'
    para = {
        'password': '',
        'phone': student_number,
        'userLevel': '1',
        'verificationType': '2',
        'verificationUrl': ''
    }

    res = requests.get(url=url, params=para)
    userData = json.loads(res.text)
    id = userData['result']['id']
    sessionId = userData['result']['sessionId']
    return get_courseShcedID(userId=id, sessionId=sessionId)

def func():
    return get_sessionID()

if __name__ == '__main__':
    func()
