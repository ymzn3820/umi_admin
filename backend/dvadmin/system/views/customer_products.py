#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/18 09:57
# @Author  : payne
# @File    : customer_products.py
# @Description :
import json

import requests
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Q

from dvadmin.system.models import CPCustomerProducts, Products
from dvadmin.utils.json_response import DetailResponse


class CPCustomerProductsView(APIView):
    permission_classes = [IsAuthenticated]

    # TODO 添加事务管理， CPCustomerProducts 插入成功之后远程调用接口失败， 撤回CPCustomerProducts插入
    @transaction.atomic
    def post(self, request):
        savepoint_id = transaction.savepoint()  # 开始一个新的事务

        try:
            customer_id = request.data.get('customer_id')
            customer_prod_status = request.data.get('status')
            prod_id = request.data.get('prod_id')

            # Get product information from Products table
            try:
                product_info = Products.objects.get(prod_id=prod_id)
            except Products.DoesNotExist:
                return DetailResponse({"error": "Product not found in Products table"}, status=status.HTTP_404_NOT_FOUND)

            new_product = CPCustomerProducts(
                customer_id=customer_id,
                prod_id=product_info.prod_id,
                prod_name=product_info.prod_name,
                platform=product_info.platform,
                prod_desc=product_info.prod_description,
                prod_details=product_info.prod_details,
                prod_origin_price=product_info.prod_origin_price,
                continuous_annual_sub_price=product_info.continuous_annual_sub_price,
                prod_price=product_info.prod_price,
                valid_period_days=product_info.valid_period_days,
                prod_cate_id=product_info.prod_cate_id,
                is_show=product_info.is_show,
                is_delete=product_info.is_delete,
                status=customer_prod_status
            )
            new_product.save()

            # 调用接口， 给客户数据库添加给定产品
            for_data = {
                'customer_id': customer_id,
                'prod_id': product_info.prod_id,
                'prod_name': product_info.prod_name,
                'platform': product_info.platform,
                'prod_desc': product_info.prod_description,
                'prod_details': product_info.prod_details,
                'prod_origin_price': product_info.prod_origin_price,
                'continuous_annual_sub_price': product_info.continuous_annual_sub_price,
                'prod_price': product_info.prod_price,
                'valid_period_days': product_info.valid_period_days,
                'prod_cate_id':product_info.prod_cate_id,
                'is_show': product_info.is_show,
                'is_delete': product_info.is_delete,
                'status': customer_prod_status
            }
            if settings.DEBUG:
                call_reote_api = requests.post(url=settings.REMOTE_INSERT_PRODUCT_LOCAL, data=for_data)
            else:
                call_reote_api = requests.post(url=settings.SERVER_ADDRESS_PROD, data=for_data)

            if call_reote_api.status_code == 200:
                call_reote_api_body = json.loads(call_reote_api.text)
                if call_reote_api_body.get('code') == 20000:
                    return DetailResponse(data={'prod_id': new_product.prod_id})
                else:
                    transaction.savepoint_rollback(savepoint_id)  # 如果远程接口返回的代码不是20000，回滚事务
                    return DetailResponse(data={'error': '远程添加产品失败'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                transaction.savepoint_rollback(savepoint_id)  # 如果远程接口返回的代码不是20000，回滚事务
                return DetailResponse(data={'error': '远程添加产品失败'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            transaction.rollback()
            return DetailResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        prod_id = request.data.get('prod_id')

        try:
            product = CPCustomerProducts.objects.get(prod_id=prod_id)
            product.is_delete = 1

            return DetailResponse(data={'prod_id': prod_id})
        except CPCustomerProducts.DoesNotExist:
            return DetailResponse({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            transaction.rollback()
            return DetailResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):

        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)
        prod_id = request.query_params.get('prod_id')
        prod_name = request.query_params.get('prod_name')
        platform = request.query_params.get('platform')
        is_delete = request.query_params.get('is_delete')
        prod_cate_id = request.query_params.get('prod_cate_id')
        customer_id = request.query_params.get('customer_id')

        query_params = Q()

        if prod_id:
            query_params &= Q(prod_id=prod_id)

        if prod_name:
            query_params &= Q(prod_name=prod_name)

        if platform:
            query_params &= Q(platform=platform)

        if prod_cate_id:
            query_params &= Q(prod_cate_id=prod_cate_id)

        if customer_id:
            query_params &= Q(customer_id=customer_id)

        if is_delete:
            query_params &= Q(is_delete=is_delete)

        products = CPCustomerProducts.objects.filter(query_params).order_by('-created_at')

        paginator = Paginator(products, limit)
        results = paginator.get_page(page)

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

        data = []
        for product in results:
            data.append({
                'prod_id': product.prod_id,
                'customer_id': product.customer_id,
                'prod_name': product.prod_name,
                'platform': product.get_platform_display(),
                'id': product.id,
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
                'status': product.status,
            })

        data = {
            "data": data
        }

        data.update(paginator_data)
        return DetailResponse(data=data)

    @transaction.atomic
    def put(self, request):
        prod_id = request.data.get('prod_id')

        try:
            product = CPCustomerProducts.objects.get(prod_id=prod_id)
        except CPCustomerProducts.DoesNotExist:
            return DetailResponse({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        product.status = request.data.get('status', product.status)
        product.is_show = request.data.get('is_show', product.is_show)
        product.is_delete = request.data.get('is_delete', product.is_delete)

        try:
            product.save()
        except Exception as e:
            transaction.rollback()
            return DetailResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return DetailResponse(data={'prod_id': prod_id})
