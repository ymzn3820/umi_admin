#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/19 16:16
# @Author  : payne
# @File    : 111.py
# @Description :

import os,django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()
from django.core.management.base import BaseCommand
from dvadmin.system.models import UUUsers
from django.apps import apps

from datetime import datetime, timezone, timedelta

# 定义东八区时间偏移
UTC8 = timezone(timedelta(hours=8))

# 获取当前时间，并转换为东八区时间
receive_time = datetime.now(UTC8)

formatted_time1 = receive_time.strftime('%Y-%m-%d %H:%M:%S')
print(formatted_time1)
