#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/18 09:57
# @Author  : payne
# @File    : customer_information.py
# @Description :

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.hashers import make_password

from dvadmin.system.models import OCICustomerInformation
from dvadmin.utils.distributed_id_generator.get_id import get_distributed_id
from dvadmin.utils.json_response import DetailResponse

worker_id = 987


class OCICustomerInformationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            new_customer_info = OCICustomerInformation(
                customer_id=get_distributed_id(worker_id),
                company_name=request.data.get('company_name'),
                address=request.data.get('address'),
                account=request.data.get('account'),
                password=make_password(request.data.get('password')),
                contact_person=request.data.get('contact_person'),
                contact_number=request.data.get('contact_number'),
                status=request.data.get('status'),
            )
            new_customer_info.save()

            return DetailResponse(data={'customer_id': new_customer_info.customer_id})
        except Exception as e:
            transaction.rollback()
            return DetailResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        customer_id = request.data.get('customer_id')

        try:
            customer_info = OCICustomerInformation.objects.get(customer_id=customer_id)
            customer_info.status = 0

            return DetailResponse(data={'customer_id': customer_id})
        except OCICustomerInformation.DoesNotExist:
            return DetailResponse({"error": "Customer information not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            transaction.rollback()
            return DetailResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)
        company_name = request.query_params.get('company_name')
        customer_id = request.query_params.get('customer_id')
        contact_number = request.query_params.get('contact_number')
        contact_person = request.query_params.get('contact_person')

        query_params = Q()

        if company_name:
            query_params &= Q(company_name__icontains=company_name)
        if contact_number:
            query_params &= Q(contact_number=contact_number)
        if contact_person:
            query_params &= Q(contact_person__icontains=contact_person)

        if customer_id:
            query_params &= Q(customer_id=customer_id)

        customer_info_list = OCICustomerInformation.objects.filter(query_params).order_by('-created_at')

        paginator = Paginator(customer_info_list, limit)
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
        for customer_info in results:
            data.append({
                'id': customer_info.id,
                'customer_id': customer_info.customer_id,
                'company_name': customer_info.company_name,
                'address': customer_info.address,
                'account': customer_info.account,
                'password': customer_info.password,
                'contact_person': customer_info.contact_person,
                'contact_number': customer_info.contact_number,
                'status': customer_info.get_status_display(),
                'created_at': str(customer_info.created_at).replace('T', ' '),
                'updated_at': str(customer_info.updated_at).replace('T', ' '),
            })

        data = {
            "data": data
        }

        data.update(paginator_data)
        return DetailResponse(data=data)

    def put(self, request):
        customer_id = request.data.get('customer_id')

        try:
            customer_info = OCICustomerInformation.objects.get(customer_id=customer_id)
        except OCICustomerInformation.DoesNotExist:
            return DetailResponse({"error": "Customer information not found"}, status=status.HTTP_404_NOT_FOUND)

        customer_info.status = request.data.get('status', customer_info.status)
        customer_info.company_name = request.data.get('company_name', customer_info.company_name)
        customer_info.address = request.data.get('address', customer_info.address)
        customer_info.account = request.data.get('account', customer_info.account)
        customer_info.password = request.data.get('password', customer_info.password)
        customer_info.contact_person = request.data.get('contact_person', customer_info.contact_person)
        customer_info.contact_number = request.data.get('contact_number', customer_info.contact_number)

        try:
            customer_info.save()
        except Exception as e:
            transaction.rollback()
            return DetailResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return DetailResponse(data={'customer_id': customer_id})


class CustomerInfoDict(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        company_name = request.query_params.get('company_name')
        customer_id = request.query_params.get('customer_id')

        query_params = Q()

        if company_name:
            query_params &= Q(company_name__icontains=company_name)

        if customer_id:
            query_params &= Q(customer_id=customer_id)

        customer_info_list = OCICustomerInformation.objects.filter(query_params).order_by('-created_at')

        data = []
        for customer_info in customer_info_list:
            data.append({
                'customer_id': customer_info.customer_id,
                'company_name': customer_info.company_name
            })

        data = {
            "data": data
        }
        return DetailResponse(data=data)
