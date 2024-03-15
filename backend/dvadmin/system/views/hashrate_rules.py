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


class HashratesRules(APIView):
    permission_classes = [IsAuthenticated]

    redis_conn = get_redis_connection('hashrates_rules')

    def get(self, request):
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)
        model = request.query_params.get('model')

        found_data = []

        data = self.redis_conn.hget('hashrateRules', 'pricing')

        if not data:
            return DetailResponse(data=found_data)
        data = json.loads(data)

        if model:
            for item in data:
                if item['model'] == model:
                    found_data.append(item)
                    break
        else:
            found_data = data

        for item in found_data:
            if 'umi-intelligence' not in item['logo']:
                if item['logo']:
                    item['logo'] = settings.NETWORK_STATION + '/' + item['logo']

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
        model = request.data.get('model')
        logo = request.data.get('logo')
        consume_points = request.data.get('consume_points')
        model_name = request.data.get('model_name')
        unit = request.data.get('unit')
        chat_type = request.data.get('chat_type')
        is_update_icon = request.data.get('is_update_icon')
        cate = request.data.get('cate')
        origin_models = self.redis_conn.hget('hashrateRules', 'pricing')
        models = json.loads(origin_models)

        print(model)
        if int(is_update_icon):

            try:
                oss_icon = Tooss.main(logo, cate)

                print(cate)
                if oss_icon:
                    pic_url = oss_icon[1]
                else:
                    pic_url = ''
            except Exception as e:
                print(e)
                return ErrorResponse()

        for item in models:
            if item['model'] == model:
                if model:
                    item['model'] = model
                if logo:
                    item['logo'] = pic_url
                if consume_points:
                    item['consume_points'] = consume_points
                if model_name:
                    item['model_name'] = model_name
                if unit:
                    item['unit'] = unit
                if chat_type:
                    item['chat_type'] = chat_type

                break

        self.redis_conn.hset('hashrateRules', 'pricing', json.dumps(models, ensure_ascii=False))

        ret_data = {
            'model': model
        }
        return DetailResponse(data=ret_data)
