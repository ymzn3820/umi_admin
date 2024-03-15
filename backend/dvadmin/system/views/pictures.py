#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/20 17:57
# @Author  : payne
# @File    : pictures.py
# @Description : 图片管理后台

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import model_to_dict
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from dvadmin.system.models import OpPictures
from dvadmin.utils.distributed_id_generator.get_id import get_distributed_id
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from datetime import datetime
from dvadmin.utils.tooss import Tooss

worker_id = 99


class PicturesManage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pic_id = get_distributed_id(worker_id)
        type = request.data.get('type')
        pic_url = request.data.get('pic_url')
        pic_size = request.data.get('pic_size')
        pic_format = request.data.get('pic_format')
        pic_desc = request.data.get('pic_desc')
        uploader_id = request.data.get('uploader_id')
        cate = request.data.get('cate')

        try:
            pic_url = Tooss.main(pic_url, cate, local=False)

            if pic_url:
                pic_url = pic_url[1]
        except Exception as e:
            print(e)
            return ErrorResponse()

        pic = OpPictures(
            pic_id=pic_id,
            type=type,
            pic_url=pic_url,
            pic_size=pic_size,
            pic_format=pic_format,
            pic_desc=pic_desc,
            uploader_id=uploader_id,
            is_delete=0,
            update_time=datetime.now(),
            create_time=datetime.now()
        )
        pic.save()
        ret_data = {
            'pic_id': pic_id
        }
        return DetailResponse(data=ret_data)

    def delete(self, request):
        pic_id = request.data
        pic = OpPictures.objects.get(pic_id=pic_id)
        pic.is_delete = 1
        pic.save()
        ret_data = {
            'pic_id': pic_id
        }
        return DetailResponse(data=ret_data)

    def get(self, request):

        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)
        type = request.query_params.get('type')
        pic_desc = request.query_params.get('pic_desc')
        pic_id = request.query_params.get('pic_id')
        is_delete = request.query_params.get('is_delete')
        query_params = Q(is_delete=0)
        if type:
            query_params &= Q(type=type)

        if pic_id:
            query_params &= Q(pic_id=pic_id)

        if is_delete:
            query_params &= Q(is_delete=is_delete)

        if pic_desc:
            query_params &= Q(pic_desc=pic_desc) | Q(pic_desc__icontains=pic_desc)

        pics = OpPictures.objects.filter(query_params)

        # Pagination
        paginator = Paginator(pics, limit)  # Number of records per page
        results = paginator.get_page(page)

        # Getting pagination data
        is_next = results.has_next()
        is_previous = results.has_previous()
        limit = paginator.per_page
        page = results.number
        total = paginator.count

        paginator_data = {
            "is_previous": is_previous,
            "is_next": is_next,
            "limit": limit,
            "page": page,
            "total": total,
        }

        # Adding pagination data to results
        data = []
        for pic in results:
            data.append({
                'id': pic.id,
                'pic_id': pic.pic_id,
                'is_delete': pic.is_delete,
                'pic_desc': pic.pic_desc,
                'pic_format': pic.pic_format,
                'pic_size': pic.pic_size,
                'pic_url': settings.NETWORK_STATION + '/' + pic.pic_url,
                'uploader_id': pic.uploader_id,
                'type': pic.type,
                'create_time': str(pic.create_time).replace('T', ' '),
                'update_time': str(pic.update_time).replace('T', ' '),
            })
        data = {
            "data": data
        }
        data.update(paginator_data)
        return DetailResponse(data=data)

    def put(self, request):
        pic_id = request.data.get('pic_id')
        if not pic_id:
            return ErrorResponse({"error": "pic_id is required"})

        try:
            pic = OpPictures.objects.get(pic_id=pic_id)
        except OpPictures.DoesNotExist:
            return ErrorResponse({"error": "Picture not found"})

        type = request.data.get('type', pic.type)
        pic_url = request.data.get('pic_url', pic.pic_url)
        pic_size = request.data.get('pic_size', pic.pic_size)
        pic_format = request.data.get('pic_format', pic.pic_format)
        pic_desc = request.data.get('pic_desc', pic.pic_desc)
        uploader_id = request.data.get('uploader_id', pic.uploader_id)
        cate = request.data.get('cate', '')
        is_update_pic = request.data.get('is_update_pic')

        if int(is_update_pic):

            try:
                if 'oss' not in str(pic_url):
                    oss_pic_url = Tooss.main(pic_url, cate, local=False)
                else:
                    oss_pic_url = Tooss.main(pic_url, cate)

                if oss_pic_url:
                    pic.pic_url = oss_pic_url[1]
            except Exception as e:
                print(e)
                return ErrorResponse()

        pic.type = type
        pic.pic_size = pic_size
        pic.pic_format = pic_format
        pic.pic_desc = pic_desc
        pic.uploader_id = uploader_id

        pic.save()

        ret_data = {
            'pic_id': pic_id
        }
        return DetailResponse(data=ret_data)
