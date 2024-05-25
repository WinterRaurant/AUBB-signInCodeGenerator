from flask import Flask, render_template, send_from_directory
import time
import threading
import temp
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

def generate_image():
    while True:
        temp.get()
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
    app.run(debug=True)
