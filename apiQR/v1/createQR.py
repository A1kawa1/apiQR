import qrcode
import os
from PIL import Image
from apiQR.settings import BASE_DIR


def resize_image(input_image_path,
                 output_image_path,
                 size):
    original_image = Image.open(input_image_path)
    resized_image = original_image.resize((size, size))

    resized_image.save(output_image_path)


def create_qr(data, token, date, UID, size, folder):
    if folder is None or folder == '':
        path = f'result/{token[:16]}/{date:%Y-%m-%d}/{UID}.png'
    else:
        path = f'result/{token[:16]}/{folder}/{date:%Y-%m-%d}/{UID}.png'
    filename = os.path.join(BASE_DIR, path)

    try:
        dir_name = os.path.dirname(filename)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
    except:
        return 'error: invalid value folder'

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    resize_image(filename, filename, size)
    return path
