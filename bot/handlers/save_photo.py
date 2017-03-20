import os
from sys import exc_info
# from io import BytesIO
from uuid import uuid4
from telegram import File
import logging

from ..models import save_photo_record
from ..cloud.cloud_storage import upload_to_cloud_storage
from ..config import config

logger = logging.getLogger(__name__)
base_path = os.path.expanduser(config.get("SavePhotoHandler", "BasePath"))
if not os.path.exists(base_path):
    os.makedirs(base_path, exist_ok=True)


def file_path(filename):
    return os.path.join(base_path, filename)

def cloud_file_path(filename):
    return "photos/{}".format(filename)

def handler(bot, update):
    print("{} sent a photo".format(update.message.from_user.name))

    if update.message.photo:
        for ps in update.message.photo:
            try:
                f = bot.getFile(ps.file_id)
                print(f)
                print(dir(f))
                file_uuid = str(uuid4()).upper()
                file_ext = f.file_path.split('/')[-1].split('.')[-1]
                file_name = "{}.{}".format(file_uuid, file_ext)
                file_full_path = file_path(file_name)
                f.download(custom_path=file_full_path)
                fp = open(file_full_path, 'rb')
                fc = fp.read()
                fp.close()
                url = upload_to_cloud_storage(fc, cloud_file_path(file_name))
                save_photo_record(update.message, ps, file_name, file_uuid, url)
            except:
                logger.exception(exc_info()[0])

    