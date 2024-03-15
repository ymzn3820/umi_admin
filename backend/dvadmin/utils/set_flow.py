#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/20 18:35
# @Author  : payne
# @File    : set_flow.py
# @Description :
import random
from datetime import datetime


def set_flow():
    base_code = datetime.now().strftime('%Y%m%d%H%M%S')
    order_list = []
    count = 1
    while True:
        if count > 100:
            break
        count_str = str(count).zfill(8)
        order_list.append(base_code + count_str)
        count += 1
    return random.choice(order_list)