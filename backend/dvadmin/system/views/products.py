#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/2 10:39
# @Author  : payne
# @File    : products.py
# @Description :商品后台管理
import random
import time

from django.db.models import Q, Max
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from dvadmin.system.models import Products
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from dvadmin.utils.set_flow import set_flow
from datetime import datetime


class ProductsManage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 商品表后台管理没有并发， 获取最大的id， 加1
        max_prod_id = Products.objects.all().aggregate(Max('prod_id'))['prod_id__max']
        prod_id = max_prod_id + 1
        prod_name = request.data.get('prod_name')
        platform = request.data.get('platform')
        prod_desc = request.data.get('prod_description')
        prod_details = request.data.get('prod_details')
        prod_origin_price = request.data.get('prod_origin_price')
        continuous_annual_sub_price = request.data.get('continuous_annual_sub_price')
        prod_price = request.data.get('prod_price')
        valid_period_days = request.data.get('valid_period_days')
        prod_cate_id = request.data.get('prod_cate_id')

        product = Products(
            prod_id=prod_id,
            prod_name=prod_name,
            platform=platform,
            prod_description=prod_desc,
            prod_details=prod_details,
            prod_origin_price=prod_origin_price,
            continuous_annual_sub_price=continuous_annual_sub_price,
            prod_price=prod_price,
            valid_period_days=valid_period_days,
            prod_cate_id=prod_cate_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        product.save()

        return DetailResponse({'product_id': product.prod_id})

    def delete(self, request):
        product_id = request.data

        try:
            product = Products.objects.get(prod_id=product_id)
            product.is_delete = 1
            product.save()
        except Products.DoesNotExist:
            return ErrorResponse({"error": "Product not found"}, status=404)

        return DetailResponse({'product_id': product_id})

    def get(self, request):
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)
        prod_id = request.query_params.get('prod_id')
        prod_name = request.query_params.get('prod_name')
        platform = request.query_params.get('platform')
        is_delete = request.query_params.get('is_delete')
        prod_cate_id = request.query_params.get('prod_cate_id')

        query_params = Q()

        if prod_id:
            query_params &= Q(prod_id=prod_id)

        if prod_name:
            query_params &= Q(prod_name=prod_name)

        if platform:
            query_params &= Q(platform=platform)

        if prod_cate_id:
            query_params &= Q(prod_cate_id=prod_cate_id)

        if is_delete:
            query_params &= Q(is_delete=is_delete)

        products = Products.objects.filter(query_params)

        # Pagination
        paginator = Paginator(products, limit)
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
        for product in results:
            data.append({
                'id': product.id,
                'prod_id': product.prod_id,
                'prod_name': product.prod_name,
                'platform': product.platform,
                'prod_description': product.prod_description,
                'prod_details': product.prod_details,
                'prod_origin_price': product.prod_origin_price,
                'continuous_annual_sub_price': product.continuous_annual_sub_price,
                'prod_price': product.prod_price,
                'valid_period_days': product.valid_period_days,
                'prod_cate_id': product.prod_cate_id,
                'created_at': str(product.created_at).replace('T', ''),
                'is_show': product.is_show,
                'is_delete': product.is_delete,
                'updated_at': str(product.updated_at).replace('T', ''),
            })
        data = {
            "data": data
        }
        data.update(paginator_data)
        return DetailResponse(data=data)

    def put(self, request):
        product_id = request.data.get('prod_id')

        if not product_id:
            return ErrorResponse({"error": "id is required"}, status=400)

        try:
            product = Products.objects.get(prod_id=product_id)
        except Products.DoesNotExist:
            return ErrorResponse({"error": "Product not found"}, status=404)

        product.prod_id = request.data.get('prod_id', product.prod_id)
        product.prod_name = request.data.get('prod_name', product.prod_name)
        product.platform = request.data.get('platform', product.platform)
        product.prod_description = request.data.get('prod_description', product.prod_description)
        product.prod_details = request.data.get('prod_details', product.prod_details)
        product.prod_origin_price = request.data.get('prod_origin_price', product.prod_origin_price)
        product.continuous_annual_sub_price = request.data.get('continuous_annual_sub_price',
                                                               product.continuous_annual_sub_price)
        product.prod_price = request.data.get('prod_price', product.prod_price)
        product.valid_period_days = request.data.get('valid_period_days', product.valid_period_days)
        product.prod_cate_id = request.data.get('prod_cate_id', product.prod_cate_id)
        product.is_delete = request.data.get('is_delete', product.is_delete)

        product.save()

        return DetailResponse({'product_id': product.prod_id})
