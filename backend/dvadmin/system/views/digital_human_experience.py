#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/2 09:19
# @Author  : payne
# @File    : contact.py
# @Description : 商务合作后台




from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from dvadmin.system.models import VdDigitalHumanExperience
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from datetime import datetime, timedelta


class DigitalHumanExperienceManage(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)
        user_name = request.query_params.get('user_name')
        mobile = request.query_params.get('mobile')
        is_delete = request.query_params.get('is_delete')

        query_params = Q()

        if user_name:
            query_params &= Q(user_name=user_name)

        if mobile:
            query_params &= Q(mobile=mobile)

        if is_delete is not None:
            query_params &= Q(is_delete=is_delete)

        dhe_instances = VdDigitalHumanExperience.objects.filter(query_params).order_by('-create_time')
        paginator = Paginator(dhe_instances, limit)
        results = paginator.get_page(page)

        data = []
        for dhe in results:
            datetime_str = str(dhe.create_time)
            dt = datetime.fromisoformat(datetime_str)
            new_dt = dt - timedelta(hours=8)
            data.append({
                'id': dhe.id,
                'user_name': dhe.user_name,
                'mobile': dhe.mobile,
                'create_by': dhe.create_by,
                'create_time': new_dt,
                'modify_time': dhe.modify_time,
                'is_delete': dhe.is_delete
            })

        ret_data = {
            'data': data,
            'page': page,
            'limit': limit,
            'total': paginator.count
        }

        return DetailResponse(data=ret_data)




