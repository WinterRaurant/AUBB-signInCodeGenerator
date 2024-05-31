from flask import Flask, render_template, send_from_directory
import time
import threading
import draw
import getIdByRoom
import getIdByShced

roomid = None
def pre():
    global roomid
    opt=input('是否启用自动获取courseID?(y/n):\n')
    if opt == 'y' or opt == 'Y':
        opt2 = input('获取课表上正在直播的课输入1，根据教室获取2：\n')
        if opt2 == '1':
            flag, msg = getIdByShced.func()
            if flag == 1:
                roomid = msg
            else:
                print('获取失败，请手动输入教室')
                roomid = getIdByRoom.func()
                if roomid == None:
                    raise Exception("获取失败！请手动输入courseSchedId！")
        elif opt2 == '2':
            roomid = getIdByRoom.func()
            if roomid == None:
                raise Exception("获取失败！请手动输入courseSchedId！")
                

pre()
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

def generate_image():
    while True:
        draw.get(roomid)
        time.sleep(1.5)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/image')
def get_image():
    return send_from_directory('static/images', 'plot.png')

if __name__ == '__main__':
    thread = threading.Thread(target=generate_image)
    thread.start()
    app.run(debug=False)
