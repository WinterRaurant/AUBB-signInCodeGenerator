import time
import qrcode

courseSchedId = ''

def generate_qr_code(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    return img


def get():
    current_timestamp_seconds = time.time()
    current_timestamp_milliseconds = int(current_timestamp_seconds * 1000)

    str = f'http://iclass.buaa.edu.cn:8081/app/course/stu_scan_sign.action?courseSchedId={courseSchedId}&timestamp={current_timestamp_milliseconds}'

    qr_code_img = generate_qr_code(str)
    qr_code_img.save('static/images/plot.png')
