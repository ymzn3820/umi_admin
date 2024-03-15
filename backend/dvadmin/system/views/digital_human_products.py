#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/22 09:19
# @Author  : ChatGPT
# @File    : digital_human_product.py
# @Description : 数字人产品管理后台

from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from dvadmin.system.models import DhDigitalHumanProduct  # Assuming this is the correct path for your model
from dvadmin.utils.distributed_id_generator.get_id import get_distributed_id
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from datetime import datetime


class DigitalHumanProductManage(APIView):
    permission_classes = [AllowAny]

    worker_id = 9879

    def post(self, request):
        product_type = request.data.get('product_type')
        download_link = request.data.get('download_link')
        tutorial = request.data.get('tutorial')
        usage_description = request.data.get('usage_description')
        product_name = request.data.get('product_name')

        product_instance = DhDigitalHumanProduct(
            product_type=product_type,
            download_link=download_link,
            product_name=product_name,
            tutorial=tutorial,
            usage_description=usage_description,
        )
        product_instance.save()

        ret_data = {
            'product_id': product_instance.id
        }
        return DetailResponse(data=ret_data)

    def delete(self, request):
        product_id = request.data.get('id')
        product = DhDigitalHumanProduct.objects.get(id=product_id)
        product.is_delete = 1
        product.save()
        ret_data = {
            'product_id': product_id
        }
        return DetailResponse(data=ret_data)

    def get(self, request):
        # Similar to the code you provided, but adjusted for the DhDigitalHumanProduct model attributes
        # I've omitted some attributes for brevity but you can add more as needed.

        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)
        product_type = request.query_params.get('product_type')
        is_delete = request.query_params.get('is_delete', 0)

        query_params = Q()

        if product_type:
            query_params &= Q(product_type=product_type)

        if is_delete is not None:
            query_params &= Q(is_delete=is_delete)

        products = DhDigitalHumanProduct.objects.filter(query_params)

        # Pagination
        paginator = Paginator(products, limit)
        results = paginator.get_page(page)

        # Extract pagination data
        paginator_data = {
            "is_previous": results.has_previous(),
            "is_next": results.has_next(),
            "limit": paginator.per_page,
            "page": results.number,
            "total": paginator.count,
        }

        # Extract product data
        data = [{'id': product.id, 'product_type': product.product_type, 'download_link': product.download_link,
                 'tutorial': product.tutorial, 'usage_description': product.usage_description,
                 'create_time': str(product.create_time).replace('T', ' '), 'product_name': product.product_name,
                 'update_time': str(product.update_time).replace('T', ' '), 'is_delete': product.is_delete
                 } for product in results]
        ret_data = {
            "data": data
        }
        ret_data.update(paginator_data)

        return DetailResponse(data=ret_data)

    def put(self, request):
        product_id = request.data.get('id')
        if not product_id:
            return ErrorResponse({"error": "id is required"}, status=400)

        try:
            product = DhDigitalHumanProduct.objects.get(id=product_id)
        except DhDigitalHumanProduct.DoesNotExist:
            return ErrorResponse({"error": "Product not found"}, status=404)

        # Similar to the code you provided, but adjusted for the DhDigitalHumanProduct model attributes
        # I've omitted some attributes for brevity but you can add more as needed.
        product.product_type = request.data.get('product_type', product.product_type)
        product.product_name = request.data.get('product_name', product.product_name)
        product.download_link = request.data.get('download_link', product.download_link)
        product.tutorial = request.data.get('tutorial', product.tutorial)
        product.usage_description = request.data.get('usage_description', product.usage_description)

        product.save()

        ret_data = {
            'product_id': product.id
        }
        return DetailResponse(data=ret_data)
