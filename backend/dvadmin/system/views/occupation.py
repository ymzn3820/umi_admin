#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/7 19:18
# @Author  : payne
# @File    : occupation.py
# @Description :

from dvadmin.system.models import OpOccupation, OpIndustry
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime

from dvadmin.utils.distributed_id_generator.get_id import get_distributed_id
from dvadmin.utils.json_response import DetailResponse, ErrorResponse

worker_id = 11


class OpOccupationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        occu_id = get_distributed_id(worker_id)
        name = request.data.get('name')
        description = request.data.get('description')
        industry_id = request.data.get('industry_id')
        is_delete = request.data.get('is_delete', False)

        occupation = OpOccupation(
            occu_id=occu_id,
            name=name,
            description=description,
            industry_id=industry_id,
            is_delete=is_delete,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        occupation.save()

        return DetailResponse(data={'occu_id': occupation.occu_id})

    def delete(self, request):
        occupation_id = request.data
        try:
            occupation = OpOccupation.objects.get(occu_id=occupation_id)
            occupation.is_delete = True
            occupation.save()
        except OpOccupation.DoesNotExist:
            return ErrorResponse({"error": "Occupation not found"}, status=404)

        return DetailResponse(data={'occu_id': occupation_id})

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
            query_params &= Q(occupation_id__in=occupation_ids)

        if name:
            query_params &= Q(name__icontains=name)

        if is_delete:
            query_params &= Q(is_delete=is_delete)

        results = OpOccupation.objects.filter(query_params).order_by('-created_at')
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
        for occupation in results:
            industry_name = OpIndustry.objects.filter(industry_id=occupation.industry_id).values_list('name',
                                                                                                  flat=True).first()
            data.append({
                'occu_id': occupation.occu_id,
                'name': occupation.name,
                'description': occupation.description,
                'industry_id': occupation.industry_id,
                'industry_name': industry_name,
                'is_delete': occupation.is_delete,
                'created_at': str(occupation.created_at).replace('T', ''),
                'updated_at': str(occupation.updated_at).replace('T', ''),
            })
        data = {
            "data": data
        }
        data.update(paginator_data)
        return DetailResponse(data=data)

    def put(self, request):
        occupation_id = request.data.get('occu_id')
        try:
            occupation = OpOccupation.objects.get(occu_id=occupation_id)
        except OpOccupation.DoesNotExist:
            return ErrorResponse({"error": "Occupation not found"}, status=404)

        occupation.occu_id = request.data.get('occu_id', occupation.occu_id)
        occupation.name = request.data.get('name', occupation.name)
        occupation.description = request.data.get('description', occupation.description)
        occupation.industry_id = request.data.get('industry_id', occupation.industry_id)
        occupation.is_delete = request.data.get('is_delete', occupation.is_delete)
        occupation.updated_at = datetime.now()

        occupation.save()

        return DetailResponse(data={'occupation_id': occupation.id})


class OpOccupationDictView(APIView):

    permission_classes = [AllowAny]


    def get(self, request):

        is_delete = 0
        is_hidden = 0

        query_params = Q()

        if is_delete:
            query_params &= Q(is_delete=is_delete)

        if is_hidden:
            query_params &= Q(is_hidden=is_hidden)

        results = OpOccupation.objects.filter(query_params).order_by('-created_at')

        # Adding pagination data to results
        data = []
        for each in results:
            data.append({
                'occu_id': each.occu_id,
                'name': each.name,
            })

        data = {
            "data": data
        }
        return DetailResponse(data=data)