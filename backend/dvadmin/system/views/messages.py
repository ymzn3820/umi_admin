#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/3 10:41
# @Author  : payne
# @File    : messages.py
# @Description :消息中心
import random

from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.core.paginator import Paginator
from datetime import datetime
from django.conf import settings

from dvadmin.system.models import OmtMessageCenter
from dvadmin.utils.distributed_id_generator.get_id import get_distributed_id
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from dvadmin.utils.tooss import Tooss

worker_id = 300


class OmtMessageCenterManage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message_id = get_distributed_id(worker_id)
        title = request.data.get('title')
        content = request.data.get('content')
        desc = request.data.get('desc')
        creator = request.data.get('creator')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        weight = request.data.get('weight')
        target_users = request.data.get('target_users')
        target_type = request.data.get('target_type')
        cate = request.data.get('cate')
        message_type = request.data.get('message_type')
        image = request.data.get('image')
        is_arousel = request.data.get('is_arousel')
        status = request.data.get('status')
        read_count = random.randint(2000, 20000)
        like_count = int(read_count * random.uniform(0.2, 0.5))
        message_center = OmtMessageCenter(
            message_id=message_id,
            title=title,
            content=content,
            desc=desc,
            cate=cate,
            creator=creator,
            start_time=start_time,
            end_time=end_time,
            weight=weight,
            target_users=target_users,
            target_type=target_type,
            read_count=read_count,
            like_count=like_count,
            message_type=message_type,
            is_arousel=is_arousel,
            image=image,
            status=status,
            create_time=datetime.now(),
            update_time=datetime.now()
        )
        message_center.save()
        ret_data = {
            'message_id': message_id
        }
        return DetailResponse(data=ret_data)

    def delete(self, request):
        message_id = request.data.get('message_id')
        message_center = OmtMessageCenter.objects.get(message_id=message_id)
        message_center.delete()
        ret_data = {
            'message_id': message_id
        }
        return DetailResponse(data=ret_data)

    def get(self, request):
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)
        title = request.query_params.get('title')
        message_id = request.query_params.get('message_id')
        creator = request.query_params.get('creator')
        cate = request.query_params.get('cate')
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        target_type = request.query_params.get('target_type')
        message_type = request.query_params.get('message_type')
        is_arousel = request.query_params.get('is_arousel')
        status = request.query_params.get('status')
        is_read = request.query_params.get('is_read')

        query_params = Q()
        if title:
            query_params &= Q(title__icontains=title)
        if message_id:
            query_params &= Q(message_id=message_id)
        if creator:
            query_params &= Q(creator__icontains=creator)
        if start_time:
            query_params &= Q(start_time__gte=start_time)
        if end_time:
            query_params &= Q(end_time__lte=end_time)
        if target_type:
            query_params &= Q(target_type=target_type)
        if message_type:
            query_params &= Q(message_type=message_type)
        if is_arousel is not None:
            query_params &= Q(is_arousel=is_arousel)
        if status:
            query_params &= Q(status=status)
        if is_read:
            query_params &= Q(status=is_read)
        if cate:
            query_params &= Q(cate=cate)

        messages = OmtMessageCenter.objects.filter(query_params)

        # Pagination
        paginator = Paginator(messages, limit)  # Number of records per page
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
        for message in results:
            data.append({
                'message_id': message.message_id,
                'title': message.title,
                'content': message.content,
                'desc': message.desc,
                'creator': message.creator,
                'cate': message.cate,
                'start_time': message.start_time,
                'end_time': message.end_time,
                'weight': message.weight,
                'target_users': message.target_users,
                'target_type': message.target_type,
                'message_type': message.message_type,
                'is_arousel': message.is_arousel,
                'status': message.status,
                'image': message.image,
                'is_read': message.is_read,
                'create_time': str(message.create_time).replace('T', ' '),
                'update_time': str(message.update_time).replace('T', ' '),
            })
        data = {
            "data": data
        }
        data.update(paginator_data)
        return DetailResponse(data=data)

    def put(self, request):
        message_id = request.data.get('message_id')
        if not message_id:
            return ErrorResponse({"error": "message_id is required"})

        try:
            message_center = OmtMessageCenter.objects.get(message_id=message_id)
        except OmtMessageCenter.DoesNotExist:
            return ErrorResponse({"error": "Message not found"})

        title = request.data.get('title', message_center.title)
        content = request.data.get('content', message_center.content)
        desc = request.data.get('desc', message_center.desc)
        cate = request.data.get('cate', message_center.cate)
        creator = request.data.get('creator', message_center.creator)
        start_time = request.data.get('start_time', message_center.start_time)
        end_time = request.data.get('end_time', message_center.end_time)
        weight = request.data.get('weight', message_center.weight)
        target_users = request.data.get('target_users', message_center.target_users)
        target_type = request.data.get('target_type', message_center.target_type)
        message_type = request.data.get('message_type', message_center.message_type)
        is_arousel = request.data.get('is_arousel', message_center.is_arousel)
        status = request.data.get('status', message_center.status)
        is_read = request.data.get('is_read', message_center.is_read)
        image = request.data.get('image')

        if image != message_center.image:
            try:
                if 'message_center' not in str(image):
                    image = Tooss.main(image, 'message_center', local=False)
                else:
                    image = Tooss.main(image, 'message_center')

                if image:
                    message_center.image = image
            except Exception as e:
                print(e)
                return ErrorResponse()


        message_center.title = title
        message_center.content = content
        message_center.desc = desc
        message_center.cate = cate
        message_center.creator = creator
        message_center.start_time = start_time
        message_center.end_time = end_time
        message_center.weight = weight
        message_center.target_users = target_users
        message_center.target_type = target_type
        message_center.message_type = message_type
        message_center.is_arousel = is_arousel
        message_center.status = status
        message_center.image = image
        message_center.is_read = is_read

        message_center.save()

        ret_data = {
            'message_id': message_id
        }
        return DetailResponse(data=ret_data)

    def get_content(self, request):
        message_id = request.query_params.get('message_id')
        if not message_id:
            return ErrorResponse({"error": "message_id is required"})

        try:
            message_center = OmtMessageCenter.objects.get(message_id=message_id)
        except OmtMessageCenter.DoesNotExist:
            return ErrorResponse({"error": "Message not found"})

        ret_data = {
            'message_id': message_id,
            'content': message_center.content,
            'title': message_center.title
        }
        return DetailResponse(data=ret_data)


class OmtMessageCenterOverviewManage(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        message_id = request.query_params.get('message_id')

        query_params = Q()

        if message_id:
            query_params &= Q(message_id=message_id)

        messages = OmtMessageCenter.objects.filter(query_params)

        # Adding pagination data to results
        data = []
        for message in messages:
            data.append({
                'message_id': message.message_id,
                'title': message.title,
                'content': message.content,
                'desc': message.desc,
                'cate': message.cate,
                'creator': message.creator,
                'start_time': message.start_time,
                'end_time': message.end_time,
                'weight': message.weight,
                'target_users': message.target_users,
                'target_type': message.target_type,
                'message_type': message.message_type,
                'is_arousel': message.is_arousel,
                'status': message.status,
                'is_read': message.is_read,
                'create_time': str(message.create_time).replace('T', ' '),
                'update_time': str(message.update_time).replace('T', ' '),
            })
        return DetailResponse(data=data[0])

    def put(self, request):
        message_id = request.data.get('message_id')
        if not message_id:
            return ErrorResponse({"error": "message_id is required"})

        try:
            message_center = OmtMessageCenter.objects.get(message_id=message_id)
        except OmtMessageCenter.DoesNotExist:
            return ErrorResponse({"error": "Message not found"})

        title = request.data.get('title', message_center.title)
        content = request.data.get('content', message_center.content)
        desc = request.data.get('desc', message_center.desc)
        creator = request.data.get('creator', message_center.creator)
        cate = request.data.get('cate', message_center.cate)
        start_time = request.data.get('start_time', message_center.start_time)
        end_time = request.data.get('end_time', message_center.end_time)
        weight = request.data.get('weight', message_center.weight)
        target_users = request.data.get('target_users', message_center.target_users)
        target_type = request.data.get('target_type', message_center.target_type)
        message_type = request.data.get('message_type', message_center.message_type)
        is_arousel = request.data.get('is_arousel', message_center.is_arousel)
        status = request.data.get('status', message_center.status)
        is_read = request.data.get('is_read', message_center.is_read)
        image = request.data.get('image')
        is_update_pic = request.data.get('is_update_pic')
        if int(is_update_pic):
            try:
                if 'message_center' not in str(image):
                    image = Tooss.main(image, 'message_center', local=False)
                else:
                    image = Tooss.main(image, 'message_center')

                if image:
                    message_center.image = image
            except Exception as e:
                print(e)
                return ErrorResponse()

        message_center.title = title
        message_center.content = content
        message_center.desc = desc
        message_center.creator = creator
        message_center.cate = cate
        message_center.start_time = start_time
        message_center.end_time = end_time
        message_center.weight = weight
        message_center.target_users = target_users
        message_center.target_type = target_type
        message_center.message_type = message_type
        message_center.is_arousel = is_arousel
        message_center.status = status
        message_center.is_read = is_read
        message_center.image = image

        message_center.save()

        ret_data = {
            'message_id': message_id
        }
        return DetailResponse(data=ret_data)
