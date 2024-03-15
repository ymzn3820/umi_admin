#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/18 13:54
# @Author  : payne
# @File    : customer_balance.py
# @Description : 客户余额
import json
from datetime import datetime

from django.core.paginator import Paginator
from django.utils import timezone
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView


from dvadmin.utils.json_response import DetailResponse, ErrorResponse


class CustomerBalance(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.redis_conn = get_redis_connection('customer_balance')

    def post(self, request):
        try:
            customer_id = request.data.get('customer_id')
            balance = request.data.get('balance')
            # 日期时间
            created_at = timezone.now().isoformat()

            customer_data = json.dumps({
                'balance': balance,
                'created_at': created_at
            })
            self.redis_conn.hset("CustomerBalance", customer_id, customer_data)

            return DetailResponse(data={'customer_id': customer_id})
        except Exception as e:
            return ErrorResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        customer_id = request.data.get('customer_id')

        try:
            self.redis_conn.hdel("CustomerBalance", customer_id)

            return DetailResponse(data={'customer_id': customer_id})
        except Exception as e:
            return ErrorResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):

        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)

        # 获取所有数据
        customer_data = self.redis_conn.hgetall("CustomerBalance")

        # 将获取的数据从字节转换为字符串，并转换json字符串为python字典
        customer_data = {key.decode(): json.loads(value.decode()) for key, value in customer_data.items()}
        # 使用Django的Paginator类进行分页
        paginator = Paginator(list(customer_data.items()), limit)
        page_data = paginator.get_page(page)

        data = []
        for item in page_data.object_list:
            if len(item) == 2:

                customer_data_dict = {'customer_id': item[0], 'balance': item[1].get('balance'),
                                  'created_at': item[1].get('created_at')}

                datetime_object = datetime.fromisoformat(customer_data_dict['created_at'])
                standard_time = datetime_object.strftime("%Y-%m-%d %H:%M:%S")
                customer_data_dict['created_at'] = standard_time
                data.append(customer_data_dict)
        response_data = {
            "is_previous": page_data.has_previous(),
            "is_next": page_data.has_next(),
            "limit": int(limit),
            "page": int(page),
            "total": paginator.count,
            "data": data,
        }

        return DetailResponse(data=response_data)

    def put(self, request):
        customer_id = request.data.get('customer_id')
        new_balance = request.data.get('balance')

        created_at = timezone.now().isoformat()

        customer_data = json.dumps({
            'balance': new_balance,
            'created_at': created_at
        })

        self.redis_conn.hset("CustomerBalance", customer_id, customer_data)

        return DetailResponse(data={'customer_id': customer_id})


class CustomerBalancePublic(APIView):

    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.customer_balance = CustomerBalance()

    def post(self, request):
        return self.customer_balance.post(request)

    def delete(self, request):
        return self.customer_balance.delete(request)

    def get(self, request):
        return self.customer_balance.get(request)

    def put(self, request):
        return self.customer_balance.put(request)
