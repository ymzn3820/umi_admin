#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/1 13:49
# @Author  : payne
# @File    : oss.py
# @Description : upload pics

from django.conf import settings
from django.core.paginator import Paginator
from django.utils.crypto import get_random_string
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from dvadmin.system.models import OpPictures
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from datetime import datetime

from dvadmin.utils.set_flow import set_flow
from dvadmin.utils.tooss import Tooss


class OSS(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        img_url = request.data.get('img_url')
        cate = request.data.get('cate')
        local = request.data.get('local')
        local_path = request.data.get('local_path')
        type = request.data.get('type')
        file_obj = request.FILES['file_obj']
        ret_data = {}

        try:
            do_upload = Tooss.main(img_url, cate, local, local_path, file_obj)
            if do_upload[0]:
                pic_id = set_flow()
                op_pic = OpPictures(
                    pic_id=pic_id,
                    type=type,
                    pic_url=do_upload[1]
                )
                op_pic.save()

                ret_data['img_url'] = do_upload[1]
                ret_data['pic_id'] = pic_id
                return DetailResponse(data=ret_data)
            else:
                return ErrorResponse(code=30001, data='上传失败')

        except Exception as e:
            return ErrorResponse(data=e)



