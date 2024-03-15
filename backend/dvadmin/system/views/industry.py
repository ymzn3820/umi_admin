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
from dvadmin.system.models import OpIndustry
from dvadmin.utils.distributed_id_generator.get_id import get_distributed_id
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from dvadmin.utils.serializers import OpIndustrySerializer


class OpIndustryManage(APIView):

    permission_classes = [IsAuthenticated]
    worker_id = 10

    def post(self, request):
        industry_id = get_distributed_id(self.worker_id)
        name = request.data.get('name')
        description = request.data.get('description')
        naics_code = request.data.get('naics_code')
        sic_code = request.data.get('sic_code')

        industry = OpIndustry(
            industry_id=industry_id,
            name=name,
            description=description,
            naics_code=naics_code,
            sic_code=sic_code,
        )
        industry.save()

        return DetailResponse({'industry_id': industry.id})

    def delete(self, request):

        industry_id = request.data

        try:
            industry = OpIndustry.objects.get(industry_id=industry_id)
            industry.is_delete = 1
            industry.save()
        except OpIndustry.DoesNotExist:
            return ErrorResponse({"error": "Industry not found"}, status=404)

        return DetailResponse({'industry_id': industry_id})

    def get(self, request):
        simple = request.query_params.get('simple', 'true') == 'true'

        if simple:
            industries = OpIndustry.objects.filter(is_delete=False).values('industry_id', 'name').distinct()
            industry_maps = list(industries)
        else:
            industry_maps = {}
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)
        industry_id = request.query_params.get('industry_id')
        name = request.query_params.get('name')
        description = request.query_params.get('description')
        is_delete = request.query_params.get('is_delete')
        naics_code = request.query_params.get('naics_code')
        sic_code = request.query_params.get('sic_code')

        query_params = Q()

        if industry_id:
            query_params &= Q(industry_id=industry_id)

        if name:
            query_params &= Q(name=name)

        if naics_code:
            query_params &= Q(naics_code=naics_code)

        if sic_code:
            query_params &= Q(sic_code=sic_code)

        if description:
            query_params &= Q(description=description)

        if is_delete:
            query_params &= Q(is_delete=is_delete)

        industries = OpIndustry.objects.filter(query_params)

        # Pagination
        paginator = Paginator(industries, limit)
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

        # Serialize the data
        serializer = OpIndustrySerializer(results, many=True)

        data = {
            "data": serializer.data,
            "industry_maps": industry_maps
        }
        data.update(paginator_data)
        data.update(industry_maps)

        return DetailResponse(data=data)

    def put(self, request):
        industry_id = request.data.get('industry_id')
        if not industry_id:
            return ErrorResponse({"error": "Industry id is required"}, status=400)

        try:
            industry = OpIndustry.objects.get(industry_id=industry_id)
        except OpIndustry.DoesNotExist:
            return ErrorResponse({"error": "Industry not found"}, status=404)

        industry.industry_id = request.data.get('industry_id', industry.industry_id)
        industry.name = request.data.get('name', industry.name)
        industry.description = request.data.get('description', industry.description)
        industry.naics_code = request.data.get('naics_code', industry.naics_code)
        industry.sic_code = request.data.get('sic_code', industry.sic_code)
        industry.is_delete = request.data.get('is_delete', industry.is_delete)

        industry.save()

        return DetailResponse({'industry_id': industry.id})


class OpIndustryManageDict(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        is_delete = 0
        is_hidden = 0

        query_params = Q()

        if is_delete:
            query_params &= Q(is_delete=is_delete)

        if is_hidden:
            query_params &= Q(is_hidden=is_hidden)

        results = OpIndustry.objects.filter(query_params).order_by('-created_at')

        # Adding pagination data to results
        data = []
        for each in results:
            data.append({
                'industry_id': each.industry_id,
                'name': each.name,
            })

        data = {
            "data": data
        }
        return DetailResponse(data=data)