#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/7 19:18
# @Author  : payne
# @File    : industry.py
# @Description :


from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from dvadmin.system.models import OpExpertiseLevel, OpIndustry, OpOccupation, OpSubOccu, OpEmpDuration, OpModules
from dvadmin.utils.distributed_id_generator.get_id import get_distributed_id
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from datetime import datetime

worker_id = 18


class OpExpertiseLevelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        expertise_level_id = get_distributed_id(worker_id)
        industry_id = request.data.get('industry_id')
        occu_id = request.data.get('occu_id')
        sub_occu_id = request.data.get('sub_occu_id')
        emp_duration_id = request.data.get('emp_duration_id')
        name = request.data.get('name')
        description = request.data.get('description')

        expertise_level = OpExpertiseLevel(
            industry_id=industry_id,
            occu_id=occu_id,
            sub_occu_id=sub_occu_id,
            emp_duration_id=emp_duration_id,
            expertise_level_id=expertise_level_id,
            name=name,
            description=description
        )
        expertise_level.save()

        return DetailResponse(data={'expertise_level_id': expertise_level_id})

    def delete(self, request):
        expertise_level_id = request.data.get('expertise_level_id')
        try:
            expertise_level = OpExpertiseLevel.objects.get(expertise_level_id=expertise_level_id)
            expertise_level.is_delete = True
            expertise_level.save()
        except OpExpertiseLevel.DoesNotExist:
            return ErrorResponse({"error": "Expertise level not found"}, status=404)

        return DetailResponse(data={'expertise_level_id': expertise_level_id})

    def get(self, request):

        page = request.query_params.get('page', None)
        limit = request.query_params.get('limit', None)
        industry_id = request.query_params.get('industry_id', None)
        occu_id = request.query_params.get('occu_id', None)
        sub_occu_id = request.query_params.get('sub_occu_id', None)
        emp_duration_id = request.query_params.get('emp_duration_id', None)
        name = request.query_params.get('name', None)
        expertise_level_id = request.query_params.get('expertise_level_id', None)
        is_delete = request.query_params.get('is_delete', None)

        query_params = Q()
        # Splitting and using '__in' filter like the above method
        if industry_id:
            query_params &= Q(industry_id=industry_id)

        if occu_id:
            query_params &= Q(occu_id=occu_id)

        if sub_occu_id:
            query_params &= Q(sub_occu_id=sub_occu_id)

        if expertise_level_id:
            query_params &= Q(expertise_level_id=expertise_level_id)

        if emp_duration_id:
            query_params &= Q(emp_duration_id=emp_duration_id)

        if name:
            query_params &= Q(name__icontains=name)

        if is_delete:
            query_params &= Q(is_delete=is_delete)

        results = OpExpertiseLevel.objects.filter(query_params).order_by('-created_at')

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
        for expertise_level in results:
            industry_name = OpIndustry.objects.filter(industry_id=expertise_level.industry_id).values_list('name',
                                                                                                           flat=True).first()
            occu_name = OpOccupation.objects.filter(occu_id=expertise_level.occu_id).values_list('name',
                                                                                                 flat=True).first()
            sub_occu_name = OpSubOccu.objects.filter(sub_occu_id=expertise_level.sub_occu_id).values_list('name',
                                                                                                          flat=True).first()
            emp_duration_name = OpEmpDuration.objects.filter(
                emp_duration_id=expertise_level.emp_duration_id).values_list(
                'emp_duration_name', flat=True).first()
            expertise_level_name = OpExpertiseLevel.objects.filter(
                expertise_level_id=expertise_level.expertise_level_id).values_list('name', flat=True).first()

            data.append({
                'expertise_level_id': expertise_level.expertise_level_id,
                'expertise_level_name': expertise_level_name,
                'name': expertise_level.name,
                'description': expertise_level.description,
                'industry_id': expertise_level.industry_id,
                'occu_id': expertise_level.occu_id,
                'sub_occu_id': expertise_level.sub_occu_id,
                'emp_duration_id': expertise_level.emp_duration_id,
                'industry_name': industry_name,
                'occu_name': occu_name,
                'sub_occu_name': sub_occu_name,
                'emp_duration_name': emp_duration_name,
                'is_delete': expertise_level.is_delete,
                'created_at': str(expertise_level.created_at).replace('T', ' '),
                'updated_at': str(expertise_level.updated_at).replace('T', ' '),
            })

        data = {
            "data": data
        }
        data.update(paginator_data)
        return DetailResponse(data=data)

    def put(self, request):
        expertise_level_id = request.data.get('expertise_level_id')
        try:
            expertise_level = OpExpertiseLevel.objects.get(expertise_level_id=expertise_level_id)
        except OpExpertiseLevel.DoesNotExist:
            return ErrorResponse({"error": "Expertise level not found"}, status=404)

        expertise_level.industry_id = request.data.get('industry_id', expertise_level.industry_id)
        expertise_level.occu_id = request.data.get('occu_id', expertise_level.occu_id)
        expertise_level.sub_occu_id = request.data.get('sub_occu_id', expertise_level.sub_occu_id)
        expertise_level.emp_duration_id = request.data.get('emp_duration_id', expertise_level.emp_duration_id)
        expertise_level.name = request.data.get('name', expertise_level.name)
        expertise_level.description = request.data.get('description', expertise_level.description)
        expertise_level.is_delete = request.data.get('is_delete', expertise_level.is_delete)
        expertise_level.updated_at = datetime.now()

        expertise_level.save()

        return DetailResponse(data={'expertise_level_id': expertise_level_id})


class OpExpertiseLevelDictView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        is_delete = 0
        is_hidden = 0

        query_params = Q()

        if is_delete:
            query_params &= Q(is_delete=is_delete)

        if is_hidden:
            query_params &= Q(is_hidden=is_hidden)

        results = OpExpertiseLevel.objects.filter(query_params).order_by('-created_at')

        # Adding pagination data to results
        data = []
        for each in results:
            data.append({
                'expertise_level_id': each.expertise_level_id,
                'name': each.name,
            })

        data = {
            "data": data
        }
        return DetailResponse(data=data)