#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/7 19:18
# @Author  : payne
# @File    : industry.py
# @Description :
from django.db import transaction
from django.db.models import Q, Max
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from dvadmin.system.models import OpTab  # 请确保这个导入是正确的
from dvadmin.utils.distributed_id_generator.get_id import get_distributed_id  # 请确保这个导入是正确的
from dvadmin.utils.json_response import DetailResponse, ErrorResponse  # 请确保这个导入是正确的
from dvadmin.utils.tooss import Tooss


class OpTabManage(APIView):
    permission_classes = [IsAuthenticated]
    worker_id = 8777

    def post(self, request):
        tab_id = get_distributed_id(self.worker_id)
        name = request.data.get('name')
        description = request.data.get('description')
        is_hidden = request.data.get('is_hidden', False)
        is_delete = request.data.get('is_delete', False)
        icon = request.data.get('icon')
        cate = request.data.get('cate')

        max_weight = OpTab.objects.aggregate(Max('weight'))['weight__max']

        try:
            pic_url = Tooss.main(icon, cate, local=False)

            if pic_url:
                pic_url = pic_url[1]
        except Exception as e:
            print(e)
            return ErrorResponse()

        tab = OpTab(
            weightd=max_weight+1,
            tab_id=tab_id,
            name=name,
            description=description,
            is_hidden=is_hidden,
            is_delete=is_delete,
            icon=pic_url,
        )
        tab.save()

        return DetailResponse({'tab_id': tab.id})

    def delete(self, request):
        tab_id = request.data
        try:
            tab = OpTab.objects.get(tab_id=tab_id)
            tab.is_delete = True
            tab.save()
        except OpTab.DoesNotExist:
            return ErrorResponse({"error": "Tab 不存在"}, status=404)

        return DetailResponse({'tab_id': tab_id})

    def get(self, request):
        tab_id = request.query_params.get('tab_id')
        name = request.query_params.get('name')
        description = request.query_params.get('description')
        is_hidden = request.query_params.get('is_hidden')
        is_delete = request.query_params.get('is_delete')

        # Pagination
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)

        query_params = Q()

        if tab_id:
            query_params &= Q(tab_id=tab_id)

        if name:
            query_params &= Q(name=name)

        if description:
            query_params &= Q(description=description)

        if is_hidden is not None:
            query_params &= Q(is_hidden=is_hidden)

        if is_delete is not None:
            query_params &= Q(is_delete=is_delete)

        tabs = OpTab.objects.filter(query_params).order_by('weight')

        # Pagination
        paginator = Paginator(tabs, limit)
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

        # Manually constructing the list of dictionaries
        tab_list = [
            {
                'id': tab.id,
                'weight': tab.weight,
                'tab_id': tab.tab_id,
                'name': tab.name,
                'description': tab.description,
                'icon': tab.icon,
                'created_at': tab.created_at,
                'updated_at': tab.updated_at,
                'is_hidden': tab.is_hidden,
                'is_delete': tab.is_delete,
            }
            for tab in results
        ]

        data = {
            'data': tab_list
        }
        data.update(paginator_data)
        return DetailResponse(data=data)

    def put(self, request):
        tab_id = request.data.get('tab_id')
        cate = request.data.get('cate')

        if not tab_id:
            return ErrorResponse({"error": "tab_id is required"})

        try:
            module = OpTab.objects.get(tab_id=tab_id)
        except OpTab.DoesNotExist:
            return ErrorResponse({"error": "Module not found"})

        icon = request.data.get('icon')
        is_update_icon = request.data.get('is_update_icon')

        if int(is_update_icon):

            try:
                if 'oss' not in str(icon):
                    oss_icon = Tooss.main(icon, cate, local=False)
                else:
                    oss_icon = Tooss.main(icon, cate)

                if oss_icon:
                    oss_icon = oss_icon[1]
                    module.icon = oss_icon
            except Exception as e:
                print(e)
                return ErrorResponse()

        for key, value in request.data.items():
            if hasattr(module, key):
                if key == 'icon':
                    continue
                setattr(module, key, value)

        module.save()

        ret_data = {
            'tab_id': tab_id
        }
        return DetailResponse(data=ret_data)


class OpTabManageDict(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        tabs = OpTab.objects.filter(is_delete=False, is_hidden=False).values('tab_id', 'name')

        # Adding pagination data to results
        data = []
        for each in tabs:
            data.append({
                'tab_id': each['tab_id'],
                'name': each['name'],
            })

        data = {
            "data": data
        }
        return DetailResponse(data=data)


class HandleWeight(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        tab_id = request.data.get('tab_id')
        weight = request.data.get('weight')


        data = {
            "data": data
        }
        return DetailResponse(data=data)