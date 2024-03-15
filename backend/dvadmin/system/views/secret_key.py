#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/1 20:37
# @Author  : payne
# @File    : secret_key.py
# @Description : 密钥管理


from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django_redis import get_redis_connection
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from dvadmin.system.models import OpenaiKey
from dvadmin.utils.json_response import DetailResponse, ErrorResponse


class SecretKeyManage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        key = request.data.get('key')
        o_status = request.data.get('o_status')
        key_type = request.data.get('key_type')
        desc = request.data.get('desc')

        key_instance = OpenaiKey(
            key=key,
            o_status=o_status,
            key_type=key_type,
            desc=desc,
        )
        key_instance.save()
        ret_data = {
            'key_id': key_instance.id
        }
        return DetailResponse(data=ret_data)

    def delete(self, request):
        key_id = request.data
        key = OpenaiKey.objects.get(id=key_id)
        key.delete()
        ret_data = {
            'key_id': key_id
        }
        return DetailResponse(data=ret_data)

    def get(self, request):
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)
        key = request.query_params.get('key')
        server_ip = request.query_params.get('server_ip')
        o_status = request.query_params.get('o_status')
        key_type = request.query_params.get('key_type')
        desc = request.query_params.get('desc')

        query_params = Q()

        if key:
            query_params &= Q(key=key)

        if server_ip:
            query_params &= Q(server_ip=server_ip)

        if o_status:
            query_params &= Q(o_status=o_status)

        if key_type:
            query_params &= Q(key_type=key_type)

        if desc:
            query_params &= Q(desc=desc)

        keys = OpenaiKey.objects.filter(query_params)

        # Pagination
        paginator = Paginator(keys, limit)
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
        for key in results:
            data.append({
                'id': key.id,
                'key': key.key,
                'server_ip': key.server_ip,
                'o_status': key.o_status,
                'key_type': key.key_type,
                'desc': key.desc
            })
        data = {
            "data": data
        }
        data.update(paginator_data)
        return DetailResponse(data=data)

    def put(self, request):
        key_id = request.data.get('id')
        if not key_id:
            return ErrorResponse({"error": "id is required"}, status=400)

        try:
            key = OpenaiKey.objects.get(id=key_id)
        except OpenaiKey.DoesNotExist:
            return ErrorResponse({"error": "Key not found"}, status=404)

        key.key = request.data.get('key', key.key)
        key.server_ip = request.data.get('server_ip', key.server_ip)
        key.o_status = request.data.get('o_status', key.o_status)
        key.key_type = request.data.get('key_type', key.key_type)
        key.desc = request.data.get('desc', key.desc)

        key.save()

        ret_data = {
            'key_id': key.id
        }
        return DetailResponse(data=ret_data)


class SecretKeyPublish(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        key_id = data.get("id")  # key表id
        server_ip = data.get("server_ip")  # 服务器ip
        redis_conn = get_redis_connection('secret_key')  # 8号库

        obj = OpenaiKey.objects.filter(id=key_id).first()

        if obj.o_status != 1:
            return ErrorResponse({"error": "status error"}, status=404)

        if obj.key_type == 1:
            key = "40key_{}".format(server_ip)
        else:
            key = "35key_{}".format(server_ip)

        with transaction.atomic():
            OpenaiKey.objects.filter(server_ip=server_ip, o_status=1, key_type=obj.key_type).update(server_ip="")
            obj.server_ip = server_ip
            obj.save()
            redis_conn.set(key, obj.key)
        return DetailResponse()
