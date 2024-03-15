#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/2 09:19
# @Author  : payne
# @File    : distributor.py
# @Description : 运营商佣金比例管理




from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from dvadmin.system.models import  UDDistributorLevel
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from datetime import datetime, timezone, timedelta


class DistributorLevelManage(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        dl_id = request.data.get('id')
        try:
            dl = UDDistributorLevel.objects.get(id=dl_id)
        except UDDistributorLevel.DoesNotExist:
            return ErrorResponse({"error": "Distributor level not found"}, status=404)

        dl.is_delete = True
        dl.save()

        return DetailResponse(data={'id': dl_id})

    def get(self, request):
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)
        d_level = request.query_params.get('d_level')
        d_level_id = request.query_params.get('d_level_id')
        is_delete = request.query_params.get('is_delete')

        query_params = Q()

        if d_level:
            query_params &= Q(d_level=d_level)

        if d_level_id:
            query_params &= Q(id=d_level_id)

        if is_delete is not None:
            query_params &= Q(is_delete=is_delete)

        distributor_levels = UDDistributorLevel.objects.filter(query_params)

        paginator = Paginator(distributor_levels, limit)
        results = paginator.get_page(page)

        data = [
            {
                'id': dl.id,
                'd_level': dl.d_level,
                'commission_rate': dl.commission_rate,
                'desc': dl.desc,
                'create_by': dl.create_by,
                'create_time': dl.create_time,
                'modify_time': dl.modify_time,
                'is_delete': dl.is_delete,
            }
            for dl in results
        ]

        paginator_data = {
            "is_previous": results.has_previous(),
            "is_next": results.has_next(),
            "limit": limit,
            "page": results.number,
            "total": paginator.count,
        }

        return DetailResponse(data={'data': data, **paginator_data})

    def put(self, request):
        dl_id = request.data.get('d_level_id')
        if not dl_id:
            return ErrorResponse({"error": "id is required"}, status=400)

        try:
            dl = UDDistributorLevel.objects.get(id=dl_id)
        except UDDistributorLevel.DoesNotExist:
            return ErrorResponse({"error": "DistributorLevel not found"}, status=404)

        dl.d_level = request.data.get('d_level', dl.d_level)
        dl.commission_rate = request.data.get('commission_rate', dl.commission_rate)
        dl.desc = request.data.get('desc', dl.desc)
        dl.modify_time = datetime.now(timezone(timedelta(hours=8)))

        dl.save()

        return DetailResponse(data={'id': dl.id})