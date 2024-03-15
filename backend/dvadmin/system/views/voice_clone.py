#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/25 16:56
# @Author  : payne
# @File    : voice_clone.py
# @Description :


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/20 17:57
# @Author  : payne
# @File    : activate_code.py
# @Description :

from django.core.paginator import Paginator
from dvadmin.utils.json_response import DetailResponse, ErrorResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from dvadmin.system.models import VtVoiceId


class VtVoiceIdManagement(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 创建记录
        voice_id = request.data.get('voice_id')
        user_code = request.data.get('user_code')

        try:
            vt_voice_id = VtVoiceId(
                voice_id=voice_id,
                user_code=user_code
            )
            vt_voice_id.save()

            ret_data = {
                'voice_id': vt_voice_id.voice_id,
                'voice_status': vt_voice_id.voice_status,
                'user_code': vt_voice_id.user_code
            }

            return DetailResponse(data=ret_data)

        except Exception:
            return ErrorResponse()

    def delete(self, request):
        # 删除记录
        voice_id = request.data.get('voice_id')

        print(voice_id)
        try:
            vt_voice_id = VtVoiceId.objects.get(voice_id=voice_id)
            vt_voice_id.is_delete = 1
            vt_voice_id.save()
            ret_data = {
                'voice_id': voice_id
            }

            return DetailResponse(data=ret_data)

        except Exception as e:
            print(e)
            return ErrorResponse()

    def get(self, request):
        # 查询记录
        voice_id = request.query_params.get('voice_id')
        voice_status = request.query_params.get('voice_status')
        user_code = request.query_params.get('user_code')
        create_by = request.query_params.get('create_by')
        page = request.query_params.get('page')
        limit = request.query_params.get('limit')

        query_params = {}
        if voice_id:
            query_params['voice_id'] = voice_id
        if voice_status is not None:
            query_params['voice_status'] = voice_status
        if user_code:
            query_params['user_code'] = user_code
        if create_by:
            query_params['create_by'] = create_by
        query_params['is_delete'] = 0

        results = VtVoiceId.objects.filter(**query_params)

        if page:
            # 分页处理
            paginator = Paginator(results, int(limit))
            results = paginator.get_page(page)

            # 获取分页信息
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
        for item in results:
            data.append({
                'voice_id': item.voice_id,
                'voice_status': item.voice_status,
                'user_code': item.user_code,
                'create_by': item.create_by,
                'create_time': item.create_time,
                'modify_time': item.modify_time,
                'is_delete': item.is_delete,
                # 其他字段
            })

        ret_data = {'data': data}
        ret_data.update(paginator_data)
        return DetailResponse(ret_data)

    def put(self, request):
        # 更新记录
        voice_id = request.data.get('voice_id')
        new_voice_status = request.data.get('voice_status')
        new_user_code = request.data.get('user_code')

        try:
            vt_voice_id = VtVoiceId.objects.get(voice_id=voice_id)
            vt_voice_id.voice_status = new_voice_status if new_voice_status is not None else vt_voice_id.voice_status
            vt_voice_id.user_code = new_user_code if new_user_code is not None else vt_voice_id.user_code
            vt_voice_id.save()

            ret_data = {
                'voice_id': vt_voice_id.voice_id,
                'voice_status': vt_voice_id.voice_status,
                'user_code': vt_voice_id.user_code
            }

            return DetailResponse(data=ret_data)

        except VtVoiceId.DoesNotExist:
            return ErrorResponse()  # 可以添加更详细的错误信息
        except Exception as e:
            print(e)
            return ErrorResponse()
