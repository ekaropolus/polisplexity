import os
import secrets
from PIL import Image
from flask import current_app

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext[1]
    picture_path = os.path.join(current_app.root_path, 'static/profile_images', picture_fn)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def send_reset_email(user):
    pass