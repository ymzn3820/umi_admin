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
from dvadmin.system.models import VtTextToSpeechVoice
from dvadmin.utils.distributed_id_generator.get_id import get_distributed_id
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from datetime import datetime

from dvadmin.utils.tooss import Tooss


class VtTextToSpeechVoiceManage(APIView):
    permission_classes = [IsAuthenticated]
    worker_id = 10876

    def post(self, request):
        data = request.data
        engine_code = data.get('engine_code')
        voice_code = str(get_distributed_id(self.worker_id))[0:11]
        voice = data.get('voice')
        voice_name = data.get('voice_name')
        voice_logo = data.get('voice_logo')
        speech_url = data.get('speech_url')
        language = data.get('language', '')
        desc = data.get('desc')
        create_by = data.get('create_by')

        cate = request.data.get('cate')

        try:
            voice_logo = Tooss.main(voice_logo, cate, local=False)

            if voice_logo:
                voice_logo = voice_logo[1]
        except Exception as e:
            print(e)
            return ErrorResponse()

        speech_voice = VtTextToSpeechVoice(
            engine_code=engine_code,
            voice_code=voice_code,
            voice=voice,
            voice_name=voice_name,
            voice_logo=voice_logo,
            speech_url=speech_url,
            language=language,
            desc=desc,
            create_by=create_by,
            create_time=datetime.now(),
            modify_time=datetime.now(),
        )
        try:
            speech_voice.save()
            return DetailResponse()
        except Exception as e:
            return ErrorResponse(code=500, msg=e)

    def delete(self, request):
        # 删除音色实例
        voice_code = request.data.get('voice_code')

        try:
            voice = VtTextToSpeechVoice.objects.get(voice_code=voice_code, is_delete=False)
            voice.is_delete = True
            voice.save()
        except VtTextToSpeechVoice.DoesNotExist:
            return ErrorResponse({"error": "Voice not found"}, status=404)

        return DetailResponse({'voice_code': voice_code})

    def get(self, request):
        # 获取音色列表
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)

        query_params = Q(is_delete=False)  # 默认只显示未删除的

        voices = VtTextToSpeechVoice.objects.filter(query_params)

        # 分页
        paginator = Paginator(voices, limit)
        results = paginator.get_page(page)

        # 分页信息
        paginator_data = {
            "is_previous": results.has_previous(),
            "is_next": results.has_next(),
            "limit": limit,
            "page": results.number,
            "total": paginator.count,
        }

        # 构建响应数据
        data = [{
            'id': voice.id,
            'engine_code': voice.engine_code,
            'voice_code': voice.voice_code,
            'voice': voice.voice,
            'voice_name': voice.voice_name,
            'voice_logo': voice.voice_logo,
            'speech_url': voice.speech_url,
            'language': voice.language,
            'desc': voice.desc,
            'create_by': voice.create_by,
            'create_time': voice.create_time.strftime("%Y-%m-%d %H:%M:%S") if voice.create_time else '',
            'modify_time': voice.modify_time.strftime("%Y-%m-%d %H:%M:%S") if voice.modify_time else '',
            'is_delete': voice.is_delete
        } for voice in results]

        response_data = {"data": data}
        response_data.update(paginator_data)

        return DetailResponse(data=response_data)

    def put(self, request):
        # 更新音色实例
        voice_code = request.data.get('voice_code')
        if not voice_code:
            return ErrorResponse({"error": "id is required"}, status=400)

        try:
            voice = VtTextToSpeechVoice.objects.get(voice_code=voice_code, is_delete=False)
        except VtTextToSpeechVoice.DoesNotExist:
            return ErrorResponse({"error": "Voice not found"}, status=404)

        cate = request.data.get('cate', '')
        is_update_pic = request.data.get('is_update_pic')
        voice_logo = request.data.get('voice_logo')

        if int(is_update_pic):

            try:
                oss_voice_logo = Tooss.main(voice_logo, cate, local=False)

                if oss_voice_logo:
                    voice.voice_logo = oss_voice_logo[1]
            except Exception as e:
                print(e)
                return ErrorResponse()

        # 更新字段
        voice.engine_code = request.data.get('engine_code', voice.engine_code)
        voice.voice_code = request.data.get('voice_code', voice.voice_code)
        voice.voice = request.data.get('voice', voice.voice)
        voice.voice_name = request.data.get('voice_name', voice.voice_name)
        voice.voice_logo = request.data.get('voice_logo', voice.voice_logo)
        voice.speech_url = request.data.get('speech_url', voice.speech_url)
        voice.language = request.data.get('language', voice.language)
        voice.desc = request.data.get('desc', voice.desc)
        voice.create_by = request.data.get('create_by', voice.create_by)
        voice.modify_time = datetime.now()

        voice.save()

        return DetailResponse({'voice_code': voice.voice_code})
