# -*- coding: utf-8 -*-

import json
import random
from models import Tag, Music


def get_tags_and_musics():
    tag_list = list(Tag.objects.all())
    random.shuffle(tag_list)

    color_array, music_list = [
        '0', '1', '2', '3', '4', '5', '6', '7',
        '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'
    ], []

    for tag in tag_list:
        tag.color = '#' + ''.join(random.sample(color_array, 6))

    musics = Music.objects.all()
    for item in musics:
        music_list.append({
            "name": item.name,
            "url": item.url,
            "cover": item.cover,
            "artist": item.artist,
            "lrc": item.lrc,
        })

    return tag_list, json.dumps(music_list)
