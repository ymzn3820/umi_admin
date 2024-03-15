#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/2 16:34
# @Author  : payne
# @File    : orders.py
# @Description : 订单后台管理


from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from dvadmin.system.models import POOrder, POOrderItem
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from datetime import datetime


class POOrderManage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')
        user_id = request.data.get('user_id')
        total_amount = request.data.get('total_amount')
        status = request.data.get('status')

        order = POOrder(
            order_id=order_id,
            user_id=user_id,
            total_amount=total_amount,
            status=status,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        order.save()

        # Iterate through each order_item in the order_items list
        order_items = request.data.get('order_items', [])
        for order_item_data in order_items:
            prod_id = order_item_data.get('prod_id')
            quantity = order_item_data.get('quantity')
            price = order_item_data.get('price')

            order_item = POOrderItem(
                order_id=order_id,
                prod_id=prod_id,
                quantity=quantity,
                price=price,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            order_item.save()

        return DetailResponse({'order_id': order.order_id})

    def delete(self, request):
        order_id = request.data.get('order_id')

        try:
            order = POOrder.objects.get(order_id=order_id, is_delete=0)
            order.is_delete = 1
            order.save()

            # Also soft delete related order items
            POOrderItem.objects.filter(order_id=order_id, is_delete=0).update(is_delete=1)
        except POOrder.DoesNotExist:
            return ErrorResponse({"error": "Order not found"}, status=404)

        return DetailResponse({'order_id': order_id})

    def get(self, request):
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)
        order_id = request.query_params.get('order_id')
        user_id = request.query_params.get('user_id')
        is_delete = request.query_params.get('is_delete', 0)  # Default to 0
        status = request.query_params.get('status')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        query_params = Q()

        if status is not None:
            query_params &= Q(status=status)

        if order_id is not None:
            query_params &= Q(order_id=order_id)

        if user_id is not None:
            query_params &= Q(user_id=user_id)

        # Add date range filter if start_date and end_date are provided
        if start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
            end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
            query_params &= Q(created_at__range=(start_date, end_date))

        query_params &= Q(is_delete=is_delete)

        orders = POOrder.objects.filter(query_params)

        # Pagination
        paginator = Paginator(orders, limit)
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
        for order in results:
            # Append all the fields of the order
            order_data = {
                'id': order.id,
                'order_id': order.order_id,
                'user_id': order.user_id,
                'total_amount': order.total_amount,
                'status': order.status,
                'is_delete': order.is_delete,
                'created_at': str(order.created_at).replace('T', ' '),
                'updated_at': str(order.updated_at).replace('T', ' '),
            }

            # Get all order items for the current order
            order_items = POOrderItem.objects.filter(order_id=order.order_id, is_delete=0)

            for order_item in order_items:
                order_data['prod_id'] = order_item.prod_id
                order_data['quantity'] = order_item.quantity
                order_data['price'] = order_item.price
            data.append(order_data)

        data = {
            "data": data
        }
        data.update(paginator_data)
        return DetailResponse(data=data)

    def put(self, request):
        order_id = request.data.get('order_id')
        if not order_id:
            return ErrorResponse({"error": "id is required"}, status=400)

        try:
            order = POOrder.objects.get(order_id=order_id, is_delete=0)
        except POOrder.DoesNotExist:
            return ErrorResponse({"error": "Order not found"}, status=404)

        order.order_id = request.data.get('order_id', order.order_id)
        order.user_id = request.data.get('user_id', order.user_id)
        order.total_amount = request.data.get('total_amount', order.total_amount)
        order.status = request.data.get('status', order.status)
        order.is_delete = request.data.get('is_delete', order.is_delete)

        order.save()

        # Handle updates to order items
        order_items = request.data.get('order_items', [])
        for order_item_data in order_items:
            try:
                order_item = POOrderItem.objects.get(id=order_item_data.get('id'), is_delete=0)
            except POOrderItem.DoesNotExist:
                continue  # Skip any order items not found

            order_item.prod_id = order_item_data.get('prod_id', order_item.prod_id)
            order_item.quantity = order_item_data.get('quantity', order_item.quantity)
            order_item.price = order_item_data.get('price', order_item.price)
            order_item.is_delete = order_item_data.get('is_delete', order_item.is_delete)

            order_item.save()

        return DetailResponse({'order_id': order.order_id})
