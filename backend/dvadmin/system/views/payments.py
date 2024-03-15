#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/2 16:34
# @Author  : payne
# @File    : payments.py
# @Description : 支付后台管理

from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from dvadmin.system.models import PpPayments, UUUsers, UUUsersTemp
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from datetime import datetime


class PpPaymentsManage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        order_id = request.data.get('order_id')
        user_id = request.data.get('user_id')
        amount = request.data.get('amount')
        status = request.data.get('status')
        payment_method = request.data.get('payment_method')
        pre_pay_id = request.data.get('pre_pay_id')
        pay_data = request.data.get('pay_data')
        pay_id = request.data.get('pay_id')
        is_delete = request.data.get('is_delete')

        payment = PpPayments(
            order_id=order_id,
            user_id=user_id,
            amount=amount,
            status=status,
            payment_method=payment_method,
            pre_pay_id=pre_pay_id,
            pay_data=pay_data,
            pay_id=pay_id,
            is_delete=is_delete,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        payment.save()

        return DetailResponse({'payment_id': payment.id})

    def delete(self, request):
        order_id = request.data

        try:
            payment = PpPayments.objects.get(order_id=order_id)
            payment.is_delete = 1
            payment.save()
        except PpPayments.DoesNotExist:
            return ErrorResponse({"error": "Payment not found"}, status=404)

        return DetailResponse({'order_id': order_id})

    def get(self, request):
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)
        order_id = request.query_params.get('order_id')
        user_id = request.query_params.get('user_id')
        is_delete = request.query_params.get('is_delete')
        status = request.query_params.get('status')
        payment_method = request.query_params.get('payment_method')
        pay_id = request.query_params.get('pay_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        query_params = Q()

        if status:
            query_params &= Q(status=status)

        if payment_method:
            query_params &= Q(payment_method=payment_method)

        if pay_id:
            query_params &= Q(pay_id=pay_id)

        if order_id:
            query_params &= Q(order_id=order_id)

        if user_id:
            query_params &= Q(user_id=user_id)

        # Add date range filter if start_date and end_date are provided
        if start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
            end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

            query_params &= Q(created_at__range=(start_date, end_date))

        if is_delete:
            query_params &= Q(is_delete=is_delete)

        payments = PpPayments.objects.filter(query_params)

        # Pagination
        paginator = Paginator(payments, limit)
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
        for payment in results:
            user_create_time = None
            # Try to get user's registration time from UUUsers
            try:
                user = UUUsers.objects.get(user_code=payment.user_id)
                user_create_time = user.create_time
            except UUUsers.DoesNotExist:
                # If user is not found in UUUsers, try to find in UUUsersTemp
                try:
                    user = UUUsersTemp.objects.get(user_code=payment.user_id)
                    user_create_time = user.create_time
                except UUUsersTemp.DoesNotExist:
                    pass

            data.append({
                'id': payment.id,
                'order_id': payment.order_id,
                'user_id': payment.user_id,
                'amount': payment.amount,
                'status': payment.status,
                'payment_method': payment.payment_method,
                'pre_pay_id': payment.pre_pay_id,
                'pay_data': payment.pay_data,
                'pay_id': payment.pay_id,
                'is_delete': payment.is_delete,
                'created_at': str(payment.created_at).replace('T', ''),
                'updated_at': str(payment.updated_at).replace('T', ''),
                'user_create_time': str(user_create_time).replace('T', '') if user_create_time else None,
            })
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
            payment = PpPayments.objects.get(order_id=order_id)
        except PpPayments.DoesNotExist:
            return ErrorResponse({"error": "Payment not found"}, status=404)

        payment.order_id = request.data.get('order_id', payment.order_id)
        payment.user_id = request.data.get('user_id', payment.user_id)
        payment.amount = request.data.get('amount', payment.amount)
        payment.status = request.data.get('status', payment.status)
        payment.payment_method = request.data.get('payment_method', payment.payment_method)
        payment.pre_pay_id = request.data.get('pre_pay_id', payment.pre_pay_id)
        payment.pay_data = request.data.get('pay_data', payment.pay_data)
        payment.pay_id = request.data.get('pay_id', payment.pay_id)
        payment.is_delete = request.data.get('is_delete', payment.is_delete)

        payment.save()

        return DetailResponse({'payment_id': payment.id})
