#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/20 17:57
# @Author  : payne
# @File    : activate_code.py
# @Description :
import traceback

from django.conf import settings
from django.core.paginator import Paginator
from django.db import connection, connections
from django.utils.crypto import get_random_string
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from dvadmin.system.models import ActivateCode
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from datetime import datetime

from dvadmin.utils.set_flow import set_flow


class ActivationCodeManagement(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        generated_by = request.data.get('generated_by')
        to_prod_id = request.data.get('to_prod_id')
        code_type = request.data.get('code_type')
        desc = request.data.get('desc')
        expired_date = request.data.get('expired_date')

        print(desc)
        print("descdescdesc")
        try:
            activate_code = get_random_string(length=30)

            # 创建 ActivateCode 对象并保存
            activation_code = ActivateCode(
                generated_by=generated_by,
                desc=desc,
                activate_code=activate_code,
                to_prod_id=to_prod_id,
                code_type=code_type,
                expired_date=expired_date
            )
            activation_code.save()

            ret_data = {
                'generated_by': generated_by,
                'activate_code': activate_code
            }

            return DetailResponse(data=ret_data)

        except Exception:
            return ErrorResponse()

    def delete(self, request):
        data = request.data

        activate_code_ids = data.get('activate_code_ids')
        try:
            # 删除 ActivateCode 对象
            ActivateCode.objects.filter(activate_code_id__in=activate_code_ids).delete()

            ret_data = {
                'activate_code_id': activate_code_ids,
            }

            return DetailResponse(data=ret_data)

        except Exception as e:
            print(e)
            return ErrorResponse()

    def get(self, request):
        # 获取查询参数
        generated_by = request.query_params.get('generated_by')
        consumed_by = request.query_params.get('consumed_by')
        activate_code = request.query_params.get('activate_code')
        activate_code_id = request.query_params.get('activate_code_id')
        to_prod_id = request.query_params.get('to_prod_id')
        status = request.query_params.get('status')
        desc = request.query_params.get('desc')
        code_type = request.query_params.get('code_type')
        page = request.query_params.get('page')
        limit = request.query_params.get('limit')
        # 构建查询条件
        query_params = {}

        if generated_by:
            query_params['generated_by'] = generated_by
        if consumed_by:
            query_params['consumed_by'] = consumed_by
        if activate_code:
            query_params['activate_code'] = activate_code
        if desc:
            query_params['desc'] = desc
        if activate_code_id:
            query_params['activate_code_id'] = activate_code_id
        if to_prod_id:
            query_params['to_prod_id'] = to_prod_id
        if status is not None:
            query_params['status'] = status
        if code_type is not None:
            query_params['code_type'] = code_type

        query_params['is_delete'] = 0
        # 根据查询条件进行过滤
        results = ActivateCode.objects.filter(**query_params)

        results = results.extra(
            where=[f"oa_activate_code.generated_by = {settings.TABLE_PREFIX}system_users.employee_no"])
        results = results.extra(tables=[f"{settings.TABLE_PREFIX}system_users"])
        results = results.extra(select={"name": f"{settings.TABLE_PREFIX}system_users.name"})

        if page:
            # 分页处理
            paginator = Paginator(results, int(limit))  # 每页显示的数据量
            results = paginator.get_page(page)

            # 获取分页信息
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
        # 构造返回数据
        data = []
        for activate_code in results:
            data.append({
                'generated_by': activate_code.generated_by,
                'generated_name': activate_code.name,
                'consumed_by': activate_code.consumed_by,
                'activate_code': activate_code.activate_code,
                'activate_code_id': activate_code.activate_code_id,
                'desc': activate_code.desc,
                'to_prod_id': activate_code.to_prod_id,
                'status': activate_code.status,
                'code_type': activate_code.code_type,
                'expired_date': str(activate_code.expired_date).replace('T', ' '),
                'is_delete': activate_code.is_delete,
                'created_at': str(activate_code.created_at).replace('T', ' '),
                'updated_at': str(activate_code.updated_at).replace('T', ' '),
            })
        ret_data = {
            'data': data
        }
        ret_data.update(paginator_data)
        return DetailResponse(ret_data)


class BatchGenerateCode(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        generated_by = request.data.get('generated_by')
        to_prod_id = request.data.get('to_prod_id')
        code_type = request.data.get('code_type')
        expired_date = request.data.get('expired_date')
        generate_quantity = request.data.get('generate_quantity', 0)
        expired_date = datetime.strptime(expired_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        desc = request.data.get('desc', 0)
        activation_codes = []
        for _ in range(int(generate_quantity)):
            activate_code = get_random_string(length=30)
            activation_codes.append(activate_code)

        try:
            # 创建 ActivateCode 对象列表
            activate_code_objects = [
                ActivateCode(
                    activate_code_id=set_flow(),
                    generated_by=generated_by,
                    activate_code=code,
                    desc=desc,
                    to_prod_id=to_prod_id,
                    code_type=code_type,
                    expired_date=expired_date
                )
                for code in activation_codes
            ]
            # 批量插入 ActivateCode 对象
            ActivateCode.objects.using('default').bulk_create(activate_code_objects)

            ret_data = []
            for code in activation_codes:
                ret_data.append({
                    'generated_by': generated_by,
                    'activate_code': code
                })
            return DetailResponse(data=ret_data)

        except Exception:
            print(traceback.format_exc())
            return ErrorResponse()


class GetActivateCodeTemp(APIView):

    # 临时允许这个接口跳过jwt，活动结束立刻停用
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        to_prod_id = data.get('to_prod_id')
        generated_by = 3
        code_type = 1
        expired_date = "2024-12-22 00:00:00.00"
        try:
            activate_code = get_random_string(length=30)

            # 创建 ActivateCode 对象并保存
            activation_code = ActivateCode(
                generated_by=generated_by,
                activate_code=activate_code,
                to_prod_id=to_prod_id,
                code_type=code_type,
                expired_date=expired_date
            )
            activation_code.save()

            ret_data = {
                'generated_by': expired_date,
                'activate_code': activate_code
            }

            return DetailResponse(data=ret_data)

        except Exception as e:
            print(e)
            return ErrorResponse()


