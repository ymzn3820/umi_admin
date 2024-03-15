#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/5 11:00
# @Author  : payne
# @File    : users.py
# @Description : 用户表后台， 非 后台管理系统的用户管理


from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from datetime import datetime
from dvadmin.system.models import UUUsers
from dvadmin.utils.json_response import DetailResponse, ErrorResponse


class UuUsersManage(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)
        user_code = request.query_params.get('user_code')
        mobile = request.query_params.get('mobile')
        user_name = request.query_params.get('user_name')
        nick_name = request.query_params.get('nick_name')
        source = request.query_params.get('source')
        wx_union_id = request.query_params.get('wx_union_id')
        user_status = request.query_params.get('user_status')
        create_by = request.query_params.get('create_by')
        is_delete = request.query_params.get('is_delete')

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        query_params = Q()

        if user_code:
            query_params &= Q(user_code=user_code)

        if mobile:
            query_params &= Q(mobile=mobile)

        if user_name:
            query_params &= Q(user_name=user_name)

        if nick_name:
            query_params &= Q(nick_name=nick_name)

        if source:
            query_params &= Q(source=source)

        if wx_union_id:
            query_params &= Q(wx_union_id=wx_union_id)

        if user_status:
            query_params &= Q(user_status=user_status)

        if create_by:
            query_params &= Q(create_by=create_by)

        if is_delete:
            query_params &= Q(is_delete=is_delete)

        # Add date range filter if start_date and end_date are provided
        if start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
            end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
            query_params &= Q(created_at__range=(start_date, end_date))

        users = UUUsers.objects.filter(query_params)

        paginator = Paginator(users, limit)
        results = paginator.get_page(page)

        paginator_data = {
            "has_next": results.has_next(),
            "has_previous": results.has_previous(),
            "limit": paginator.per_page,
            "page": results.number,
            "total": paginator.count,
        }

        data = [user.to_dict() for user in results]
        data = {
            "data": data
        }
        data.update(paginator_data)
        return DetailResponse(data=data)

    def post(self, request):
        user = UUUsers(
            user_code=request.data.get('user_code'),
            mobile=request.data.get('mobile'),
            user_name=request.data.get('user_name'),
            nick_name=request.data.get('nick_name'),
            password=request.data.get('password'),
            source=request.data.get('source'),
            avatar_url=request.data.get('avatar_url'),
            wx_union_id=request.data.get('wx_union_id'),
            salt=request.data.get('salt'),
            user_status=request.data.get('user_status', 1),
            create_by=request.data.get('create_by'),
            create_time=datetime.now(),
            modify_time=datetime.now(),
            is_delete=request.data.get('is_delete', 0),
        )
        user.save()
        return DetailResponse({'user_id': user.user_code})

    def delete(self, request):
        user_code = request.data.get('user_code')

        try:
            user = UUUsers.objects.get(user_code=user_code)
            user.is_delete = 1
            user.save()
        except UUUsers.DoesNotExist:
            return ErrorResponse({"error": "User not found"}, status=404)

        return DetailResponse({'user_code': user_code})

    def put(self, request):
        user_code = request.data.get('user_code')

        if not user_code:
            return ErrorResponse({"error": "user_code is required"}, status=400)

        try:
            user = UUUsers.objects.get(user_code=user_code)
        except UUUsers.DoesNotExist:
            return ErrorResponse({"error": "User not found"}, status=404)

        # Update fields if provided
        for field in ['user_code', 'mobile', 'user_name', 'nick_name', 'password', 'source', 'avatar_url',
                      'wx_union_id', 'salt', 'user_status', 'create_by', 'is_delete', 'login_ip', 'create_time', 'create_time' ]:
            if field in request.data:
                if field in ['create_by', 'create_time', 'modify_time']:
                    print(str(request.data[field]).replace('T', ' ').split('.')[0])
                    setattr(user, field, str(request.data[field]).replace('T', ' ').split('.')[0])
                setattr(user, field, request.data[field])
        user.save()

        return DetailResponse({'user_id': user.id})
