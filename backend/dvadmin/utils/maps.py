#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/30 10:05
# @Author  : payne
# @File    : maps.py
# @Description : 映射


class Maps:
    mapStatus = {
        0: "未激活",
        1: "激活"
    }
    mapCodeType = {
        1: "会员抵消卡",
        2: "消费劵",
        3: "其他",
    }
    reverseMapStatus = {
        "未激活": 0,
        "激活": 1
    }
    reverseMapCodeType = {
        "会员抵消卡": 1,
        "消费劵": 2,
        "其他": 3
    }

