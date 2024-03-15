#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/1 20:37
# @Author  : payne
# @File    : secret_key.py
# @Description : 密钥管理
import json

from django.conf import settings
from django.core.paginator import Paginator
from django_redis import get_redis_connection
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from dvadmin.utils.distributed_id_generator.get_id import get_distributed_id
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from dvadmin.utils.tooss import Tooss

worker_id = 9876


class SdModelsManage(APIView):
    permission_classes = [IsAuthenticated]

    redis_conn = get_redis_connection('sd_models')

    def post(self, request):
        model_id = get_distributed_id(worker_id)
        name = request.data.get('name')
        value = request.data.get('value')
        pic_url = request.data.get('pic_url')
        cate = request.data.get('cate')

        origin_models = self.redis_conn.get('sd_model')

        if origin_models:
            origin_models = json.loads(origin_models)
        else:
            origin_models = []
        try:
            pic_url = Tooss.main(pic_url, cate, local=False)

            if pic_url:
                pic_url = pic_url[1]
        except Exception as e:
            print(e)
            return ErrorResponse()

        data = {
            'model_id': model_id,
            'name': name,
            'value': value,
            'pic_url': pic_url
        }

        origin_models.append(data)
        self.redis_conn.set('sd_model', json.dumps(origin_models))

        ret_data = {
            'pic_url': pic_url
        }
        return DetailResponse(data=ret_data)

    def delete(self, request):
        data = request.data
        model_id = data.get('model_id')

        model = self.redis_conn.get('sd_model')

        if not model:
            return ErrorResponse({"error": "model_id not found"}, status=400)

        model = json.loads(model)

        filtered_data = list(filter(lambda item: int(item['model_id']) != int(model_id), model))

        self.redis_conn.set('sd_model', json.dumps(filtered_data))

        ret_data = {
            'model_id': model_id
        }

        return DetailResponse(data=ret_data)

    def get(self, request):
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)
        model_id = request.query_params.get('model_id')

        found_data = []

        data = self.redis_conn.get('sd_model')

        if not data:
            return DetailResponse(data=found_data)
        data = json.loads(data)

        if model_id:
            for item in data:
                if item['model_id'] == model_id:
                    found_data = item
                    break
        else:
            found_data = data

        for item in found_data:
            if 'umi-intelligence' not in item['pic_url']:
                item['pic_url'] = settings.NETWORK_STATION + '/' + item['pic_url']

        # Pagination
        paginator = Paginator(found_data, limit)
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
        ret_data = {
            "data": found_data
        }
        ret_data.update(paginator_data)
        return DetailResponse(data=ret_data)

    def put(self, request):
        model_id = request.data.get('model_id')
        pic_url = request.data.get('pic_url')
        name = request.data.get('name')
        value = request.data.get('value')
        is_update_icon = request.data.get('is_update_icon')
        cate = request.data.get('cate')
        if not model_id:
            return ErrorResponse({"error": "model_id is required"}, status=400)

        models = json.loads(self.redis_conn.get('sd_model'))

        if int(is_update_icon):

            try:
                oss_icon = Tooss.main(pic_url, cate)

                print(cate)
                if oss_icon:
                    pic_url = oss_icon[1]
            except Exception as e:
                print(e)
                return ErrorResponse()

        for item in models:
            if item['model_id'] == model_id:
                if name:
                    item['name'] = name
                if value:
                    item['value'] = value
                if pic_url:
                    item['pic_url'] = pic_url
                break

        self.redis_conn.set('sd_model', json.dumps(models))

        ret_data = {
            'model_id': model_id
        }
        return DetailResponse(data=ret_data)

