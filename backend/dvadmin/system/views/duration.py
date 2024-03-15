#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/7 19:18
# @Author  : payne
# @File    : industry.py
# @Description :


from dvadmin.system.models import OpEmpDuration, OpIndustry, OpOccupation, OpSubOccu
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from dvadmin.utils.distributed_id_generator.get_id import get_distributed_id
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from datetime import datetime

worker_id = 16


class OpEmpDurationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        emp_duration_id = get_distributed_id(worker_id)
        emp_duration_name = request.data.get('emp_duration_name')
        emp_duration_desc = request.data.get('emp_duration_desc')
        industry_id = request.data.get('industry_id')
        occu_id = request.data.get('occu_id')
        sub_occu_id = request.data.get('sub_occu_id')
        is_delete = request.data.get('is_delete', False)

        emp_duration = OpEmpDuration(
            emp_duration_id=emp_duration_id,
            emp_duration_name=emp_duration_name,
            emp_duration_desc=emp_duration_desc,
            industry_id=industry_id,
            occu_id=occu_id,
            sub_occu_id=sub_occu_id,
            is_delete=is_delete,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        emp_duration.save()

        return DetailResponse(data={'emp_duration_id': emp_duration.emp_duration_id})

    def delete(self, request):
        emp_duration_id = request.data.get('emp_duration_id')
        try:
            emp_duration = OpEmpDuration.objects.get(emp_duration_id=emp_duration_id)
            emp_duration.is_delete = True
            emp_duration.save()
        except OpEmpDuration.DoesNotExist:
            return ErrorResponse({"error": "Employment duration not found"}, status=404)

        return DetailResponse(data={'emp_duration_id': emp_duration_id})

    def get(self, request):

        page = request.query_params.get('page', None)
        limit = request.query_params.get('limit', None)
        industry_id = request.query_params.get('industry_id')
        occu_id = request.query_params.get('occu_id')
        sub_occu_id = request.query_params.get('sub_occu_id')
        emp_duration_id = request.query_params.get('emp_duration_id')
        emp_duration_name = request.query_params.get('emp_duration_name')
        is_delete = request.query_params.get('is_delete')

        query_params = Q()

        # Splitting and using '__in' filter like the above method
        if industry_id:
            industry_ids = industry_id.split(',')
            query_params &= Q(industry_id__in=industry_ids)

        if occu_id:
            occupation_ids = occu_id.split(',')
            query_params &= Q(occupation_id__in=occupation_ids)

        if sub_occu_id:
            sub_occu_ids = sub_occu_id.split(',')
            query_params &= Q(sub_occu_id__in=sub_occu_ids)

        if emp_duration_id:
            emp_duration_ids = emp_duration_id.split(',')
            query_params &= Q(emp_duration_id__in=emp_duration_ids)

        if emp_duration_name:
            query_params &= Q(emp_duration_name__icontains=emp_duration_name)
        if is_delete:
            query_params &= Q(is_delete=is_delete)

        results = OpEmpDuration.objects.filter(query_params).order_by('-created_at')

        if page and limit:
            # Pagination
            paginator = Paginator(results, limit)
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
        else:
            paginator_data = {}

        # Adding pagination data to results
        data = []
        for emp_duration in results:
            industry_name = OpIndustry.objects.filter(industry_id=emp_duration.industry_id).values_list('name',
                                                                                                  flat=True).first()
            occu_name = OpOccupation.objects.filter(occu_id=emp_duration.occu_id).values_list('name', flat=True).first()
            sub_occu_name = OpSubOccu.objects.filter(sub_occu_id=emp_duration.sub_occu_id).values_list('name',
                                                                                                 flat=True).first()
            data.append({
                'emp_duration_id': emp_duration.emp_duration_id,
                'emp_duration_name': emp_duration.emp_duration_name,
                'emp_duration_desc': emp_duration.emp_duration_desc,
                'industry_id': emp_duration.industry_id,
                'occu_id': emp_duration.occu_id,
                'sub_occu_id': emp_duration.sub_occu_id,
                'industry_name': industry_name,
                'occu_name': occu_name,
                'sub_occu_name': sub_occu_name,
                'is_delete': emp_duration.is_delete,
                'created_at': str(emp_duration.created_at).replace('T', ''),
                'updated_at': str(emp_duration.updated_at).replace('T', ''),
            })
        data = {
            "data": data
        }
        data.update(paginator_data)
        return DetailResponse(data=data)

    def put(self, request):
        emp_duration_id = request.data.get('emp_duration_id')
        try:
            emp_duration = OpEmpDuration.objects.get(emp_duration_id=emp_duration_id)
        except OpEmpDuration.DoesNotExist:
            return ErrorResponse({"error": "Employment duration not found"}, status=404)

        emp_duration.emp_duration_name = request.data.get('emp_duration_name', emp_duration.emp_duration_name)
        emp_duration.emp_duration_desc = request.data.get('emp_duration_desc', emp_duration.emp_duration_desc)
        emp_duration.industry_id = request.data.get('industry_id', emp_duration.industry_id)
        emp_duration.occu_id = request.data.get('occu_id', emp_duration.occu_id)
        emp_duration.sub_occu_id = request.data.get('sub_occu_id', emp_duration.sub_occu_id)
        emp_duration.is_delete = request.data.get('is_delete', emp_duration.is_delete)
        emp_duration.updated_at = datetime.now()

        emp_duration.save()

        return DetailResponse(data={'emp_duration_id': emp_duration.emp_duration_id})


class OpEmpDurationDictView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        is_delete = 0
        is_hidden = 0

        query_params = Q()

        if is_delete:
            query_params &= Q(is_delete=is_delete)

        if is_hidden:
            query_params &= Q(is_hidden=is_hidden)

        results = OpEmpDuration.objects.filter(query_params).order_by('-created_at')

        # Adding pagination data to results
        data = []
        for each in results:
            data.append({
                'occu_duration_id': each.emp_duration_id,
                'name': each.emp_duration_name,
            })

        data = {
            "data": data
        }
        return DetailResponse(data=data)