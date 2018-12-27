# -*- coding: utf-8 -*-

import random
from models import Tag


def get_all_tags():
    tag_list = list(Tag.objects.all())
    random.shuffle(tag_list)

    color_array = [
        '0', '1', '2', '3', '4', '5', '6', '7',
        '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'
    ]

    for tag in tag_list:
        tag.color = '#' + ''.join(random.sample(color_array, 6))

    return tag_list
