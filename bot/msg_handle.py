from pprint import pprint
from uuid import uuid4
from . import Global
from .models import Photo
from traceback import print_exc
import sys


def default_msg_handle(msg):
    pprint(msg)


def msg_get_reply(msg):
    if "reply_to_message" in msg:
        return msg["reply_to_message"]


def msg_get_photo_info(msg):
    photos = msg["photo"]
    if not photos:
        return None

    largest_photo = photos[0]
    for p in photos:
        if p["height"] > largest_photo["height"]:
            largest_photo = p

    return p


def my_msg_handle(msg):
    pprint(msg)
    try:
        text = msg.get('text', '')

        if '#' in text:
            pprint("Tag found!")
            pieces = text.split(' ')
            tag = ''
            for p in pieces:
                if '#' in p:
                    tag = p
                    break
            
            reply = msg_get_reply(msg)
            if reply:
                pprint("Message is a reply")
                reply_from = reply['from']['id']
                reply_from_username = reply['from'].get('username', None)
                photo = msg_get_photo_info(reply)
                file_id = photo['file_id']
                file_name = '%s--%s' % (str(uuid4()).upper(), reply_from)
                origin_text = reply.get('text', '')

                ext = Global.archiever.save_file(file_id, file_name)
                file_name = "%s.%s" % (file_name, ext)
                Photo.save(file_id, file_name, reply_from, reply_from_username, tag, origin_text)
    except Exception as ex:
        print_exc()




