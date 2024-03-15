#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/11 15:47
# @Author  : payne
# @File    : question_edit_new.py
# @Description :
import traceback

from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from dvadmin.utils.distributed_id_generator.get_id import get_distributed_id
from dvadmin.utils.json_response import DetailResponse, ErrorResponse

from dvadmin.system.models import OiInfoTypes, OioInfoOptions, OqQuestionInfoUser, CCChatSquare, CCChatMessages, OpModules, \
    UUUsers


class OiInfoTypesView(APIView):
    permission_classes = [IsAuthenticated]
    worker_id = 32

    @transaction.atomic
    def post(self, request):
        try:
            info_type_id = get_distributed_id(self.worker_id)
            info_type_name = request.data.get('info_type_name')
            info_type_name_cn = request.data.get('info_type_name_cn')

            new_info_type = OiInfoTypes(
                info_type_id=info_type_id,
                info_type_name=info_type_name,
                info_type_name_cn=info_type_name_cn,
            )
            new_info_type.save()

            return DetailResponse(data={'info_type_id': new_info_type.info_type_id})
        except Exception as e:
            transaction.rollback()
            return DetailResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def delete(self, request):
        info_type_id = request.data.get('info_type_id')

        try:
            info_type = OiInfoTypes.objects.get(info_type_id=info_type_id)
            info_type.is_delete = 1
            info_type.save()
            return DetailResponse(data={'info_type_id': info_type_id})
        except OiInfoTypes.DoesNotExist:
            return ErrorResponse({"error": "Info type not found"})
        except Exception as e:
            transaction.rollback()
            return DetailResponse(data={'error': str(e)})

    def get(self, request):
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)
        info_type_id = request.query_params.get('info_type_id')
        info_type_name = request.query_params.get('info_type_name')
        info_type_name_cn = request.query_params.get('info_type_name_cn')
        is_delete = request.query_params.get('is_delete')

        query_params = Q()

        if info_type_id:
            query_params &= Q(info_type_id=info_type_id)

        if info_type_name:
            query_params &= Q(info_type_name=info_type_name)

        if info_type_name_cn:
            query_params &= Q(info_type_name_cn=info_type_name_cn)

        if is_delete is not None:
            query_params &= Q(is_delete=is_delete)

        info_types = OiInfoTypes.objects.filter(query_params).order_by('-created_at')

        # Pagination
        paginator = Paginator(info_types, limit)
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
        for info_type in results:
            data.append({
                'id': info_type.id,
                'info_type_id': info_type.info_type_id,
                'info_type_name': info_type.info_type_name,
                'info_type_name_cn': info_type.info_type_name_cn,
                'is_delete': info_type.is_delete,
                'created_at': str(info_type.created_at).replace('T', ' '),
                'updated_at': str(info_type.updated_at).replace('T', ' '),
            })

        data = {
            "data": data
        }

        data.update(paginator_data)
        return DetailResponse(data=data)

    @transaction.atomic
    def put(self, request):
        info_type_id = request.data.get('info_type_id')

        print(request.data)
        print("request.datarequest.datarequest.data")
        try:
            info_type = OiInfoTypes.objects.get(info_type_id=info_type_id)
        except OiInfoTypes.DoesNotExist:
            return ErrorResponse({"error": "Info type not found"}, status=404)

        info_type.info_type_name = request.data.get('info_type_name', info_type.info_type_name)
        info_type.info_type_name_cn = request.data.get('info_type_name_cn', info_type.info_type_name_cn)
        info_type.is_delete = request.data.get('is_delete', info_type.is_delete)

        try:
            info_type.save()
        except Exception as e:
            transaction.rollback()
            return DetailResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return DetailResponse(data={'info_type_id': info_type_id})


class OioInfoOptionsView(APIView):
    permission_classes = [IsAuthenticated]
    worker_id = 33

    @transaction.atomic
    def post(self, request):
        try:
            option_id = get_distributed_id(self.worker_id)
            info_type_id = request.data.get('info_type_id')
            option_value = request.data.get('option_value')

            new_info_option = OioInfoOptions(
                option_id=option_id,
                info_type_id=info_type_id,
                option_value=option_value,
            )
            new_info_option.save()

            return DetailResponse(data={'option_id': new_info_option.option_id})
        except Exception as e:
            print(traceback.format_exc())
            transaction.rollback()
            return DetailResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def delete(self, request):
        option_id = request.data.get('option_id')

        try:
            info_option = OioInfoOptions.objects.get(option_id=option_id)
            info_option.is_delete = 1
            info_option.save()

            return DetailResponse(data={'option_id': option_id})
        except OioInfoOptions.DoesNotExist:
            return ErrorResponse({"error": "Info option not found"})
        except Exception as e:
            transaction.rollback()
            return DetailResponse(data={'error': str(e)})

    def get(self, request):
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)
        info_type_id = request.query_params.get('info_type_id')
        option_id = request.query_params.get('option_id')
        option_value = request.query_params.get('option_value')
        is_delete = request.query_params.get('is_delete')

        query_params = Q()

        if info_type_id:
            query_params &= Q(info_type_id=info_type_id)

        if option_id:
            query_params &= Q(option_id=option_id)

        if option_value:
            query_params &= Q(option_value=option_value)

        if is_delete is not None:
            query_params &= Q(is_delete=is_delete)

        info_options = OioInfoOptions.objects.filter(query_params).order_by('-created_at')

        # Pagination
        paginator = Paginator(info_options, limit)
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
        for info_option in results:
            data.append({
                'id': info_option.id,
                'option_id': info_option.option_id,
                'info_type_id': info_option.info_type_id,
                'option_value': info_option.option_value,
                'is_delete': info_option.is_delete,
                'created_at': str(info_option.created_at).replace('T', ' '),
                'updated_at': str(info_option.updated_at).replace('T', ' '),
            })

        data = {
            "data": data
        }

        data.update(paginator_data)
        return DetailResponse(data=data)

    @transaction.atomic
    def put(self, request):
        option_id = request.data.get('option_id')

        try:
            info_option = OioInfoOptions.objects.get(option_id=option_id)
        except OioInfoOptions.DoesNotExist:
            return ErrorResponse({"error": "Info option not found"}, status=404)

        info_option.option_id = request.data.get('option_id', info_option.option_id)
        info_option.option_value = request.data.get('option_value', info_option.option_value)
        info_option.is_delete = request.data.get('is_delete', info_option.is_delete)

        try:
            info_option.save()
        except Exception as e:
            transaction.rollback()
            return DetailResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return DetailResponse(data={'option_id': info_option.option_id})


class OqQuestionInfoView(APIView):
    permission_classes = [IsAuthenticated]
    worker_id = 34

    @transaction.atomic
    def post(self, request):
        try:
            question_add_id = get_distributed_id(self.worker_id)
            question_id = request.data.get('question_id')
            info_type_id = request.data.get('info_type_id')
            option_ids = request.data.get('option_ids')
            weight = request.data.get('weight', 0)
            title = request.data.get('title')
            placeholder = request.data.get('placeholder')
            is_required = request.data.get('is_required')

            option_ids = ','.join(map(str, option_ids))
            new_question_info = OqQuestionInfoUser(
                question_add_id=question_add_id,
                question_id=question_id,
                info_type_id=info_type_id,
                option_ids=option_ids,
                weight=weight,
                placeholder=placeholder,
                title=title,
                is_required=is_required
            )
            new_question_info.save()

            return DetailResponse(data={'question_add_id': new_question_info.question_add_id})
        except Exception as e:
            transaction.rollback()
            return DetailResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def delete(self, request):
        question_add_id = request.data.get('question_add_id')

        try:
            question_info = OqQuestionInfoUser.objects.get(question_add_id=question_add_id)
            question_info.is_delete = 1
            question_info.save()

            return DetailResponse(data={'question_add_id': question_add_id})
        except OqQuestionInfoUser.DoesNotExist:
            return ErrorResponse({"error": "Question info not found"})
        except Exception as e:
            transaction.rollback()
            return DetailResponse(data={'error': str(e)})

    def get(self, request):

        data = request.GET
        page = data.get('page', 1)
        limit = data.get('limit', 10)
        title = data.get('title')
        question_add_id = data.get('question_add_id')
        question_id = data.get('question_id')
        info_type_id = data.get('info_type_id')
        placeholder = data.get('placeholder')
        is_delete = data.get('is_delete')

        query_params = Q()

        if question_add_id:
            query_params &= Q(info_id=question_add_id)

        if question_id:
            query_params &= Q(question_id=question_id)

        if info_type_id:
            query_params &= Q(info_type_id=info_type_id)

        if placeholder:
            query_params &= Q(placeholder=placeholder)
        if is_delete is not None:
            query_params &= Q(is_delete=is_delete)

        if title is not None:
            query_params &= Q(title__icontains=title)

        question_infos = OqQuestionInfoUser.objects.filter(query_params).order_by('-created_at')

        # Pagination
        paginator = Paginator(question_infos, limit)
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

        for question_info in results:
            data.append({
                'id': question_info.id,
                'question_add_id': question_info.question_add_id,
                'title': question_info.title,
                'question_id': question_info.question_id,
                'info_type_id': question_info.info_type_id,
                'option_ids': question_info.option_ids,
                'placeholder': question_info.placeholder,
                'is_required': question_info.is_required,
                'weight': question_info.weight,
                'is_delete': question_info.is_delete,
                'created_at': str(question_info.created_at).replace('T', ' '),
                'updated_at': str(question_info.updated_at).replace('T', ' '),
            })

        data = {
            "data": data
        }

        data.update(paginator_data)
        return DetailResponse(data=data)

    def put(self, request):
        question_add_id = request.data.get('question_add_id')

        try:
            question_info = OqQuestionInfoUser.objects.get(question_add_id=question_add_id)
        except OqQuestionInfoUser.DoesNotExist:
            return ErrorResponse({"error": "Question info not found"}, status=404)

        option_ids = request.data.get('option_ids')
        option_ids = ','.join(map(str, option_ids))
        question_info.question_id = request.data.get('question_id', question_info.question_id)
        question_info.info_type_id = request.data.get('info_type_id', question_info.info_type_id)
        question_info.placeholder = request.data.get('placeholder', question_info.placeholder)
        question_info.title = request.data.get('title', question_info.title)
        question_info.weight = request.data.get('weight', question_info.weight)
        question_info.is_delete = request.data.get('is_delete', question_info.is_delete)
        question_info.is_required = request.data.get('is_required', question_info.is_required)
        question_info.option_ids = option_ids

        try:
            question_info.save()
        except Exception as e:
            print(traceback.format_exc())
            return DetailResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return DetailResponse(data={'question_add_id': question_info.question_add_id})


class OiInfoTypesDictView(APIView):
    permission_classes = [AllowAny]
    worker_id = 32

    def get(self, request):

        info_type_id = request.query_params.get('info_type_id')
        is_delete = 0

        query_params = Q()

        if info_type_id:
            query_params &= Q(info_type_id=info_type_id)

        if is_delete is not None:
            query_params &= Q(is_delete=is_delete)

        info_types = OiInfoTypes.objects.filter(query_params).order_by('-created_at')

        # Adding pagination data to results
        data = []
        for info_type in info_types:
            data.append({
                'id': info_type.id,
                'info_type_id': info_type.info_type_id,
                'info_type_name': info_type.info_type_name,
                'info_type_name_cn': info_type.info_type_name_cn,
                'is_delete': info_type.is_delete,
                'created_at': str(info_type.created_at).replace('T', ' '),
                'updated_at': str(info_type.updated_at).replace('T', ' '),
            })

        data = {
            "data": data
        }

        return DetailResponse(data=data)

    @transaction.atomic
    def put(self, request):
        info_type_id = request.data.get('info_type_id')

        print(request.data)
        print("request.datarequest.datarequest.data")
        try:
            info_type = OiInfoTypes.objects.get(info_type_id=info_type_id)
        except OiInfoTypes.DoesNotExist:
            return ErrorResponse({"error": "Info type not found"}, status=404)

        info_type.info_type_name = request.data.get('info_type_name', info_type.info_type_name)
        info_type.info_type_name_cn = request.data.get('info_type_name_cn', info_type.info_type_name_cn)
        info_type.is_delete = request.data.get('is_delete', info_type.is_delete)

        try:
            info_type.save()
        except Exception as e:
            transaction.rollback()
            return DetailResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return DetailResponse(data={'info_type_id': info_type_id})


class OioInfoOptionsDictView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = request.GET
        is_delete = 0
        info_type_id = data.get('info_type_id')
        query_params = Q()

        if is_delete is not None:
            query_params &= Q(is_delete=is_delete)

        if info_type_id is not None:
            query_params &= Q(info_type_id=info_type_id)

        info_options = OioInfoOptions.objects.filter(query_params).order_by('-created_at')

        data = []
        for info_option in info_options:
            data.append({
                'option_id': info_option.option_id,
                'option_value': info_option.option_value,
            })

        data = {
            "data": data
        }

        return DetailResponse(data=data)


class CCChatSquareView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)
        question_id = request.query_params.get('question_id')
        s_status = request.query_params.get('s_status')
        is_delete = request.query_params.get('is_delete')

        query_params = Q()

        if question_id:
            query_params &= Q(question_id=question_id)

        if s_status:
            query_params &= Q(s_status=s_status)
        if is_delete is not None:
            query_params &= Q(is_delete=is_delete)

        chat_squares = CCChatSquare.objects.filter(query_params).order_by('-create_time')

        # Pagination
        paginator = Paginator(chat_squares, limit)
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
        for chat_square in results:

            module_name = OpModules.objects.filter(module_id=chat_square.module_id).values_list('name', flat=True).first()
            created_by = UUUsers.objects.filter(user_code=chat_square.create_by).values_list('nick_name', flat=True).first()
            session_data = CCChatMessages.objects.filter(session_code=chat_square.session_code).values_list('session_data', flat=True).first()


            if session_data:
                question_title = session_data[0].get('content')
                question_answer = session_data[1].get('content')
            else:
                question_title = ''
                question_answer = ''
            data.append({
                'id': chat_square.id,
                'question_id': chat_square.question_id,
                'module_name': module_name,
                'question_title': question_title,
                'question_answer': question_answer,
                'session_code': chat_square.session_code,
                'created_by': created_by,
                'user_id': chat_square.create_by,
                's_status': chat_square.s_status,
                'is_delete': chat_square.is_delete,
                'create_time': str(chat_square.create_time).replace('T', ' '),
                'modify_time': str(chat_square.modify_time).replace('T', ' '),
            })

        data = {
            "data": data
        }

        data.update(paginator_data)
        return DetailResponse(data=data)

    def put(self, request):
        print(11111111111111222)
        session_code = request.data.get('session_code')
        question_id = request.data.get('question_id')

        print(session_code)
        print(question_id)
        print('session_codesession_codesession_codesession_code')
        try:
            chat_square = CCChatSquare.objects.get(session_code=session_code)
        except CCChatSquare.DoesNotExist:
            print(traceback.format_exc())
            return ErrorResponse({"error": f"session_code - question_id : {session_code} - {question_id} not found"}, status=404)

        chat_square.s_status = request.data.get('s_status', chat_square.s_status)
        chat_square.is_delete = request.data.get('is_delete', chat_square.is_delete)

        try:
            chat_square.save()
        except Exception as e:
            print(traceback.format_exc())
            return DetailResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return DetailResponse(data={'question_id': question_id})

    def delete(self, request):
        session_code = request.data.get('session_code')
        question_id = request.data.get('question_id')
        try:
            chat_square = CCChatSquare.objects.get(question_id=question_id,session_code=session_code )
        except CCChatSquare.DoesNotExist:
            print(traceback.format_exc())
            return ErrorResponse({"error": f"session_code - question_id : {session_code} - {question_id} not found"}, status=404)

        try:
            chat_square.is_delete = 1
            chat_square.save()
        except Exception as e:
            print(traceback.format_exc())
            return DetailResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return DetailResponse(data={'question_id': question_id})
