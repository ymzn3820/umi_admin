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
from dvadmin.system.models import OpSubOccu, OpIndustry, OpOccupation
from dvadmin.utils.distributed_id_generator.get_id import get_distributed_id
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from datetime import datetime

worker_id = 15


class OpSubOccuView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sub_occu_id = get_distributed_id(worker_id)
        name = request.data.get('name')
        description = request.data.get('description')
        industry_id = request.data.get('industry_id')
        occu_id = request.data.get('occu_id')
        is_delete = request.data.get('is_delete', False)

        sub_occupation = OpSubOccu(
            sub_occu_id=sub_occu_id,
            name=name,
            description=description,
            industry_id=industry_id,
            occu_id=occu_id,
            is_delete=is_delete,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        sub_occupation.save()

        return DetailResponse(data={'sub_occu_id': sub_occupation.sub_occu_id})

    def delete(self, request):
        sub_occupation_id = request.data.get('sub_occu_id')
        try:
            sub_occupation = OpSubOccu.objects.get(sub_occu_id=sub_occupation_id)
            sub_occupation.is_delete = True
            sub_occupation.save()
        except OpSubOccu.DoesNotExist:
            return ErrorResponse({"error": "Sub-Occupation not found"}, status=404)

        return DetailResponse(data={'sub_occu_id': sub_occupation_id})

    def get(self, request):

        page = request.query_params.get('page', None)
        limit = request.query_params.get('limit', None)
        industry_id = request.query_params.get('industry_id')
        occu_id = request.query_params.get('occu_id')
        name = request.query_params.get('name')
        is_delete = request.query_params.get('is_delete')

        query_params = Q()

        if industry_id:
            industry_ids = industry_id.split(',')
            query_params &= Q(industry_id__in=industry_ids)

        if occu_id:
            occupation_ids = occu_id.split(',')
            query_params &= Q(occu_id__in=occupation_ids)

        if name:
            query_params &= Q(name__icontains=name)

        if is_delete:
            query_params &= Q(is_delete=is_delete)

        results = OpSubOccu.objects.filter(query_params).order_by('-created_at')
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
        for sub_occu in results:
            industry_name = OpIndustry.objects.filter(industry_id=sub_occu.industry_id).values_list('name',
                                                                                                  flat=True).first()
            occu_name = OpOccupation.objects.filter(occu_id=sub_occu.occu_id).values_list('name', flat=True).first()
            data.append({
                'sub_occu_id': sub_occu.sub_occu_id,
                'name': sub_occu.name,
                'description': sub_occu.description,
                'industry_id': sub_occu.industry_id,
                'occu_id': sub_occu.occu_id,
                'industry_name': industry_name,
                'occu_name': occu_name,
                'is_delete': sub_occu.is_delete,
                'created_at': str(sub_occu.created_at).replace('T', ''),
                'updated_at': str(sub_occu.updated_at).replace('T', ''),
            })
        data = {
            "data": data
        }
        data.update(paginator_data)
        return DetailResponse(data=data)

    def put(self, request):
        sub_occupation_id = request.data.get('sub_occu_id')
        try:
            sub_occupation = OpSubOccu.objects.get(sub_occupation_id=sub_occupation_id)
        except OpSubOccu.DoesNotExist:
            return ErrorResponse({"error": "Sub-Occupation not found"}, status=404)

        sub_occupation.sub_occu_id = request.data.get('sub_occu_id', sub_occupation.sub_occu_id)
        sub_occupation.name = request.data.get('name', sub_occupation.name)
        sub_occupation.description = request.data.get('description', sub_occupation.description)
        sub_occupation.industry_id = request.data.get('industry_id', sub_occupation.industry_id)
        sub_occupation.occu_id = request.data.get('occu_id', sub_occupation.occu_id)
        sub_occupation.is_delete = request.data.get('is_delete', sub_occupation.is_delete)
        sub_occupation.updated_at = datetime.now()

        sub_occupation.save()

        return DetailResponse(data={'sub_occu_id': sub_occupation.id})

class OpSubOccuDictView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        is_delete = 0
        is_hidden = 0

        query_params = Q()

        if is_delete:
            query_params &= Q(is_delete=is_delete)

        if is_hidden:
            query_params &= Q(is_hidden=is_hidden)

        results = OpSubOccu.objects.filter(query_params).order_by('-created_at')

        # Adding pagination data to results
        data = []
        for each in results:
            data.append({
                'sub_occu_id': each.sub_occu_id,
                'name': each.name,
            })

        data = {
            "data": data
        }
        return DetailResponse(data=data)