#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/2 09:19
# @Author  : payne
# @File    : contact.py
# @Description : 商务合作后台
import traceback

from django.db.models import Q
from django.db import connections
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from dvadmin.system.models import ObBusinessCooperation
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from datetime import datetime, timezone, timedelta


class BusinessCooperationManage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.data.get('user_id', '')
        type = request.data.get('type')
        name = request.data.get('name')
        referer = request.data.get('from')
        phone = request.data.get('phone')
        cooperation_details = request.data.get('cooperation_details')
        email = request.data.get('email')
        company = request.data.get('company')
        position = request.data.get('position')
        status = request.data.get('status')


        # 定义东八区时间偏移
        UTC8 = timezone(timedelta(hours=8))
        # 获取当前时间，并转换为东八区时间
        created_at = datetime.now(UTC8)
        created_at = created_at.strftime('%Y-%m-%d %H:%M:%S')

        bc_instance = ObBusinessCooperation(
            user_id=user_id,
            type=type,
            name=name,
            phone=phone,
            referer=referer,
            cooperation_details=cooperation_details,
            email=email,
            company=company,
            position=position,
            status=status,
            created_at=created_at,
        )
        bc_instance.save()
        ret_data = {
            'bc_id': bc_instance.id
        }
        return DetailResponse(data=ret_data)

    def delete(self, request):
        bc_id = request.data
        bc = ObBusinessCooperation.objects.get(id=bc_id)
        bc.is_delete = 1
        bc.save()
        ret_data = {
            'bc_id': bc_id
        }
        return DetailResponse(data=ret_data)

    def get(self, request):

        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)
        type = request.query_params.get('type')
        name = request.query_params.get('name')
        referer = request.query_params.get('referer')
        phone = request.query_params.get('phone')
        cooperation_details = request.query_params.get('cooperation_details')
        email = request.query_params.get('email')
        is_delete = request.query_params.get('is_delete')
        company = request.query_params.get('company')
        status = request.query_params.get('status')

        query_params = Q()

        if type:
            query_params &= Q(type=type)

        if name:
            query_params &= Q(name=name)

        if phone:
            query_params &= Q(phone=phone)

        if cooperation_details:
            query_params &= Q(cooperation_details=cooperation_details)

        if email:
            query_params &= Q(email=email)

        if referer:
            query_params &= Q(referer=referer)

        if company:
            query_params &= Q(company=company)

        if status:
            query_params &= Q(status=status)

        if is_delete is not None:

            query_params &= Q(is_delete=is_delete)

        business_cooperations = ObBusinessCooperation.objects.filter(query_params)

        # Pagination
        paginator = Paginator(business_cooperations, limit)
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
        for bc in results:
            data.append({
                'id': bc.id,
                'user_id': bc.user_id,
                'type': bc.type,
                'name': bc.name,
                'referer': bc.referer,
                'phone': bc.phone,
                'cooperation_details': bc.cooperation_details,
                'email': bc.email,
                'company': bc.company,
                'status': bc.status,
                'is_delete': bc.is_delete,
                'created_at': bc.created_at,
            })
        data = {
            "data": data
        }
        data.update(paginator_data)
        return DetailResponse(data=data)

    def put(self, request):
        bc_id = request.data.get('id')
        user_id = request.data.get('user_id')

        print(user_id)
        status = request.data.get('status')
        if not bc_id:
            return ErrorResponse({"error": "id is required"}, status=400)

        try:
            bc = ObBusinessCooperation.objects.get(id=bc_id)
        except ObBusinessCooperation.DoesNotExist:
            print(traceback.format_exc())
            return ErrorResponse({"error": "BusinessCooperation not found"}, status=404)

        cooperration_type = bc.type

        if int(cooperration_type) == 20 and int(status) == 2:
            sql_check_top_distributor = f"""
                select a.user_code, c.commission_rate
                    from (WITH RECURSIVE user_hierarchy AS (
                        SELECT user_code, parent_user_code
                        FROM ud_users_distributor
                        WHERE user_code = {user_id}
                        UNION ALL
                        SELECT u.user_code, u.parent_user_code
                        FROM ud_users_distributor u
                        JOIN user_hierarchy h ON h.parent_user_code = u.user_code
                    )
                    SELECT user_code
                    FROM user_hierarchy
                    WHERE parent_user_code = "") a
                    inner join ud_user_distributor_level b on a.user_code = b.user_code
                    inner join ud_distributor_level c on b.distributor_level_id = c.id
                    where c.d_level = 3 and b.d_status = 1 
            """
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(sql_check_top_distributor)
            print("sql_check_top_distributorsql_check_top_distributorsql_check_top_distributorsql_check_top_distributor")
            try:
                with connections['server'].cursor() as cursor:
                    cursor.execute(sql_check_top_distributor)
                    if cursor.rowcount > 0:
                        top_distributor = True
                    else:
                        top_distributor = False

            except Exception:
                print(traceback.format_exc())
                return ErrorResponse({"error": "update distribution level fail"}, status=500)

            print(top_distributor)
            if top_distributor:
                bc.status = 4
                bc.save()
                return ErrorResponse(msg='top distributor already existed', status=200)

            sql_chage_level = f"""
                UPDATE ud_distributor_level dl
                INNER JOIN ud_user_distributor_level udl
                ON dl.id = udl.distributor_level_id
                SET udl.distributor_level_id = 3, udl.start_time = '{current_date}', 
                udl.expire_time = COALESCE(udl.expire_time, DATE_ADD('{current_date}', INTERVAL 1 YEAR))
                WHERE udl.user_code = '{user_id}'

            """
            try:
                with connections['server'].cursor() as cursor:
                    cursor.execute(sql_chage_level)
                    if cursor.rowcount > 0:
                        update_distribution_level = True
                    else:
                        update_distribution_level = False
            except Exception:
                print(traceback.format_exc())
                return ErrorResponse({"error": "update distribution level fail"}, status=404)

        bc.type = request.data.get('type', bc.type)
        bc.name = request.data.get('name', bc.name)
        bc.phone = request.data.get('phone', bc.phone)
        if int(cooperration_type) == 20 and int(status) == 2:
            bc.cooperation_details = "申请运营商，特定人员处理"
        else:
            bc.cooperation_details = request.data.get('cooperation_details', bc.cooperation_details)
        bc.email = request.data.get('email', bc.email)
        bc.company = request.data.get('company', bc.company)
        bc.status = request.data.get('status', bc.status)

        bc.save()

        ret_data = {
            'bc_id': bc.id
        }

        if user_id and int(cooperration_type) == 20:
            if update_distribution_level and not top_distributor:
                return DetailResponse(data=ret_data)
            else:
                return ErrorResponse(msg='fail to approval')
        else:
            return DetailResponse(data=ret_data)
