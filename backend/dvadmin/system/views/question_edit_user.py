#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/11 15:47
# @Author  : payne
# @File    : question_edit_new.py
# @Description :  管理用户建立的模型和问题相关
import traceback

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from dvadmin.utils.distributed_id_generator.get_id import get_distributed_id
from dvadmin.utils.json_response import DetailResponse, ErrorResponse

from dvadmin.system.models import OiInfoTypes, OioInfoOptionsUser, OqQuestionInfoUser, OioInfoOptions, \
    UQDUserQuestionDetails, CEEnterpriseFiles, OpQuestionsSet, OqQuestionInfo


class OioInfoOptionsUserView(APIView):
    permission_classes = [IsAuthenticated]
    worker_id = 3001

    @transaction.atomic
    def post(self, request):
        try:
            option_id = get_distributed_id(self.worker_id)
            info_type_id = request.data.get('info_type_id')
            user_id = request.data.get('user_id')
            option_value = request.data.get('option_value')

            new_info_option = OioInfoOptionsUser(
                option_id=option_id,
                info_type_id=info_type_id,
                user_id=user_id,
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
            info_option = OioInfoOptionsUser.objects.get(option_id=option_id)
            info_option.is_delete = 1
            info_option.save()

            return DetailResponse(data={'option_id': option_id})
        except OioInfoOptionsUser.DoesNotExist:
            return ErrorResponse({"error": "Info option not found"})
        except Exception as e:
            transaction.rollback()
            return DetailResponse(data={'error': str(e)})

    def get(self, request):
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)
        user_id = request.query_params.get('user_id')
        info_type_id = request.query_params.get('info_type_id')
        option_id = request.query_params.get('option_id')
        option_value = request.query_params.get('option_value')
        is_delete = request.query_params.get('is_delete')

        query_params = Q()

        if user_id:
            query_params &= Q(user_id=user_id)

        if info_type_id:
            query_params &= Q(info_type_id=info_type_id)

        if option_id:
            query_params &= Q(option_id=option_id)

        if option_value:
            query_params &= Q(option_value=option_value)

        if is_delete is not None:
            query_params &= Q(is_delete=is_delete)

        info_options = OioInfoOptionsUser.objects.filter(query_params).order_by('-created_at')

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
                'user_id': info_option.user_id,
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
            info_option = OioInfoOptionsUser.objects.get(option_id=option_id)
        except OioInfoOptionsUser.DoesNotExist:
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


class OqQuestionInfoUserView(APIView):
    permission_classes = [IsAuthenticated]
    worker_id = 3002

    @transaction.atomic
    def post(self, request):
        try:
            question_add_id = get_distributed_id(self.worker_id)
            user_id = request.data.get('user_id')
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
                user_id=user_id,
                weight=weight,
                question_id=question_id,
                info_type_id=info_type_id,
                option_ids=option_ids,
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
        user_id = data.get('user_id')
        question_add_id = data.get('question_add_id')
        question_id = data.get('question_id')
        info_type_id = data.get('info_type_id')
        placeholder = data.get('placeholder')
        is_delete = data.get('is_delete')

        query_params = Q()

        if question_add_id:
            query_params &= Q(info_id=question_add_id)

        if user_id:
            query_params &= Q(user_id=user_id)

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
                'user_id': question_info.user_id,
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


class OqQuestionInfoUserDetailDictView(APIView):

    def get(self, request):

        is_delete = 0
        is_hidden = 0

        query_params = Q()

        if is_delete:
            query_params &= Q(is_delete=is_delete)

        if is_hidden:
            query_params &= Q(is_hidden=is_hidden)

        results = UQDUserQuestionDetails.objects.filter(query_params).order_by('-created_at')

        # Adding pagination data to results
        data = []
        for question_set in results:
            data.append({
                'question_id': question_set.question_id,
                'assistant_title': question_set.assistant_title,
                'character_name': question_set.character_name,
            })

        data = {
            "data": data
        }
        return DetailResponse(data=data)


class OqQuestionInfoUserDictView(APIView):

    def get(self, request):

        is_delete = 0
        is_hidden = 0

        query_params = Q()

        if is_delete:
            query_params &= Q(is_delete=is_delete)

        if is_hidden:
            query_params &= Q(is_hidden=is_hidden)

        results = OqQuestionInfoUser.objects.filter(query_params).order_by('-created_at')

        # Adding pagination data to results
        data = []
        for question_set in results:
            data.append({
                'question_add_id': question_set.question_add_id,
                'title': question_set.title,
            })

        data = {
            "data": data
        }
        return DetailResponse(data=data)


class OiInfoTypesDictView(APIView):
    permission_classes = [IsAuthenticated]
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


class OioInfoOptionsUserDictView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        is_delete = 0
        query_params = Q()

        if is_delete is not None:
            query_params &= Q(is_delete=is_delete)

        info_options = OioInfoOptionsUser.objects.filter(query_params).order_by('-created_at')

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


class UQDUserQuestionDetailsView(APIView):
    permission_classes = [AllowAny]
    worker_id = 3005

    @transaction.atomic
    def post(self, request):
        try:
            question_id = get_distributed_id(self.worker_id)
            user_id = request.data.get('user_id')
            industry_id = request.data.get('industry_id')
            module_id = request.data.get('module_id')
            occu_id = request.data.get('occu_id')
            sub_occu_id = request.data.get('sub_occu_id')
            info_questions = request.data.get('info_questions')
            occu_duration_id = request.data.get('emp_duration_id')
            expertise_level_id = request.data.get('expertise_level_id')
            character_avatar = request.data.get('character_avatar')
            character_name = request.data.get('character_name')
            character_greetings = request.data.get('character_greetings')
            is_public = request.data.get('is_public')
            hint = request.data.get('hint')
            example_question = request.data.get('example_question')
            character_desc = request.data.get('character_desc')
            character_achievements = request.data.get('character_achievements')
            assistant_title = request.data.get('assistant_title')
            assistant_content = request.data.get('assistant_content')
            related_document = request.data.get('related_document')
            refuse_reason = request.data.get('refuse_reason')

            # related_document = { "file": [],"video":[],"pics":[],"url": [] }
            urls = []

            if related_document:
                for key, values in related_document.items():
                    code = question_id
                    for each_value in values:
                        file_url = each_value.get('file_url')
                        urls.append(file_url)
                        file_category = 5
                        group_code = key
                        create_by = user_id
                        file_name = each_value.get('file_name')

                        new_file = CEEnterpriseFiles(
                            code=code,
                            file_url=file_url,
                            file_category=file_category,
                            group_code=group_code,
                            create_by=create_by,
                            file_name=file_name,
                        )
                        new_file.save()

            question_add_ids = []

            if info_questions:
                for each_info_question in info_questions:
                    question_add_id = get_distributed_id(self.worker_id)
                    question_add_ids.append(str(question_add_id))

                    each_info_question_type_id = each_info_question.get('type_id')
                    each_info_question_title = each_info_question.get('title')
                    each_info_question_placeholder = each_info_question.get('placeholder')
                    each_info_question_info_options = each_info_question.get('info_options')
                    each_info_question_info_is_required = 1 if each_info_question.get('is_required') else 0
                    each_info_question_info_weight = each_info_question.get('weight', 0)
                    option_ids = []
                    if each_info_question_info_options:
                        for inner_info_question_info_options in each_info_question_info_options:
                            option_id = get_distributed_id(self.worker_id)
                            option_ids.append(str(option_id))
                            info_type_id = each_info_question_type_id
                            option_value = inner_info_question_info_options.get('value')

                            # 提交options
                            new_option = OioInfoOptionsUser(
                                user_id=user_id,
                                option_id=option_id,
                                info_type_id=info_type_id,
                                option_value=option_value)
                            new_option.save()

                    # 提交questions相关
                    new_question = OqQuestionInfoUser(
                        user_id=user_id,
                        question_add_id=question_add_id,
                        info_type_id=each_info_question_type_id,
                        question_id=question_id,
                        option_ids=','.join(option_ids),
                        title=each_info_question_title,
                        placeholder=each_info_question_placeholder,
                        is_required=each_info_question_info_is_required,
                        weight=each_info_question_info_weight
                    )
                    new_question.save()

            # 总入库
            user_question_details = UQDUserQuestionDetails(
                question_id=question_id,
                user_id=user_id,
                question_add_ids=','.join(question_add_ids),
                industry_id=industry_id if industry_id else 0,
                module_id=module_id if module_id else 0,
                occu_id=occu_id if occu_id else 0,
                sec_occu_id=sub_occu_id if sub_occu_id else 0,
                occu_duration_id=occu_duration_id if occu_duration_id else 0,
                expertise_level_id=expertise_level_id if expertise_level_id else 0,
                character_avatar=character_avatar if character_avatar else '',
                character_name=character_name if character_name else '',
                character_greetings=character_greetings if character_greetings else '',
                is_public=is_public,
                hint=hint if hint else '',
                example_question=example_question if example_question else '',
                character_desc=character_desc if character_desc else '',
                character_achievements=character_achievements if character_achievements else '',
                assistant_title=assistant_title if assistant_title else '',
                assistant_content=assistant_content if assistant_content else '',
                related_document=','.join(urls),
                refuse_reason=refuse_reason if refuse_reason else ''
            )
            user_question_details.save()
            return DetailResponse(data={'question_id': user_question_details.question_id})
        except Exception as e:
            print(traceback.format_exc())
            return ErrorResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def delete(self, request):
        question_id = request.data.get('question_id')

        try:
            user_question_details = UQDUserQuestionDetails.objects.get(question_id=question_id)
            user_question_details.is_delete = 1
            user_question_details.save()

            return DetailResponse(data={'question_id': question_id})
        except UQDUserQuestionDetails.DoesNotExist:
            return ErrorResponse({"error": "User Question Details not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return ErrorResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        data = request.GET
        page = data.get('page', 1)
        limit = data.get('limit', 10)
        user_id = data.get('user_id')
        question_id = data.get('question_id')
        is_delete = data.get('is_delete')
        query_params = Q()

        if user_id:
            query_params &= Q(user_id=user_id)

        if question_id:
            query_params &= Q(question_id=question_id)

        if is_delete:
            query_params &= Q(is_delete=is_delete)

        user_question_details = UQDUserQuestionDetails.objects.filter(query_params).order_by('-created_at')

        # Pagination
        paginator = Paginator(user_question_details, limit)
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

        for detail in results:
            data.append(detail.to_dict())

        data = {
            "data": data
        }

        data.update(paginator_data)
        return DetailResponse(data=data)

    def put(self, request):
        question_id = request.data.get('question_id')
        user_id = request.data.get('user_id')

        try:
            user_question_details = UQDUserQuestionDetails.objects.get(question_id=question_id)

            origin_db_status = user_question_details.status

            if not user_question_details:
                return ErrorResponse(data={'error': 'Question not found'}, status=status.HTTP_400_BAD_REQUEST)

            user_question_details.user_id = request.data.get('user_id', user_question_details.user_id)
            user_question_details.industry_id = request.data.get('industry_id', user_question_details.industry_id if user_question_details.industry_id else 0)

            user_question_details.industry_id = request.data.get('industry_id',
                                                               user_question_details.industry_id) if request.data.get(
                'industry_id', user_question_details.industry_id) and request.data.get('industry_id',
                                                                                   user_question_details.industry_id) != '' else 0

            user_question_details.module_id = request.data.get('module_id',
                                                             user_question_details.module_id) if request.data.get(
                'module_id', user_question_details.module_id) and request.data.get('module_id',
                                                                               user_question_details.module_id) != '' else 0

            user_question_details.occu_id = request.data.get('occu_id',
                                                             user_question_details.occu_id) if request.data.get(
                'occu_id', user_question_details.occu_id) and request.data.get('occu_id',
                                                                               user_question_details.occu_id) != '' else 0


            user_question_details.sec_occu_id = request.data.get('sub_occu_id',
                                                             user_question_details.sec_occu_id) if request.data.get(
                'sub_occu_id', user_question_details.sec_occu_id) and request.data.get('sub_occu_id',
                                                                               user_question_details.sec_occu_id) != '' else 0

            user_question_details.occu_duration_id = request.data.get('emp_duration_id',
                                                                 user_question_details.occu_duration_id) if request.data.get(
                'emp_duration_id', user_question_details.occu_duration_id) and request.data.get('emp_duration_id',
                                                                                       user_question_details.occu_duration_id) != '' else 0

            user_question_details.expertise_level_id = request.data.get('expertise_level_id',
                                                                 user_question_details.expertise_level_id) if request.data.get(
                'expertise_level_id', user_question_details.expertise_level_id) and request.data.get('expertise_level_id',
                                                                                       user_question_details.expertise_level_id) != '' else 0

            user_question_details.character_avatar = request.data.get('character_avatar', user_question_details.character_avatar)
            user_question_details.character_avatar = user_question_details.character_avatar if settings.NETWORK_STATION not  \
                                    in user_question_details.character_avatar else user_question_details.character_avatar.replace(settings.NETWORK_STATION, '')


            user_question_details.character_name = request.data.get('character_name',
                                                                    user_question_details.character_name if user_question_details.character_name else '')
            user_question_details.character_greetings = request.data.get('character_greetings',
                                                                         user_question_details.character_greetings if user_question_details.character_greetings else '')
            user_question_details.is_public = request.data.get('is_public', user_question_details.is_public)
            user_question_details.hint = request.data.get('hint', user_question_details.hint if user_question_details.hint else '')
            user_question_details.example_question = request.data.get('example_question', user_question_details.example_question if user_question_details.example_question else '')
            user_question_details.character_desc = request.data.get('character_desc',
                                                                    user_question_details.character_desc if user_question_details.character_desc else '')
            user_question_details.character_achievements = request.data.get('character_achievements',
                                                                            user_question_details.character_achievements if user_question_details.character_achievements else '')
            user_question_details.assistant_title = request.data.get('assistant_title',
                                                                     user_question_details.assistant_title if  user_question_details.assistant_title else '')
            user_question_details.assistant_content = request.data.get('assistant_content',
                                                                       user_question_details.assistant_content if user_question_details.assistant_content else '')
            user_question_details.related_document = request.data.get('related_document',
                                                                      user_question_details.related_document if user_question_details.related_document else '')
            user_question_details.refuse_reason = request.data.get('refuse_reason', user_question_details.refuse_reason)
            user_question_details.status = request.data.get('status', user_question_details.status)

            review_status = request.data.get('status', 0)

            db_review_status = user_question_details.status
            print(db_review_status)
            print("db_review_statusdb_review_statusdb_review_status")

            if origin_db_status == 2:
                user_question_details.status = 0
                user_question_details.refuse_reason = ''

            if int(review_status) == 1:
                try:
                    call_insert_to_public_question = self.insert_to_public_question(request.data, private=0)

                    print(call_insert_to_public_question)
                    print("call_insert_to_public_question")
                    if call_insert_to_public_question == 1:
                        user_question_details.save()
                        return DetailResponse(data={'question_id': question_id})
                    elif call_insert_to_public_question == 4:
                        return DetailResponse(data={'error': 'add to public question error'},
                                              status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return DetailResponse(data={'question_id': question_id})
                except Exception as e:
                    print(traceback.format_exc())
                    return ErrorResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            if int(review_status) == 3:

                try:
                    call_insert_to_public_question = self.insert_to_public_question(request.data, private=1)

                    print(call_insert_to_public_question)
                    print("call_insert_to_public_question")
                    if call_insert_to_public_question == 1:
                        user_question_details.save()
                        return DetailResponse(data={'question_id': question_id})
                    elif call_insert_to_public_question == 4:
                        return DetailResponse(data={'error': 'add to public question error'},
                                              status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return DetailResponse(data={'question_id': question_id})
                except Exception as e:
                    print(traceback.format_exc())
                    return ErrorResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            info_questions = request.data.get('info_questions')
            if info_questions is not None:
                OqQuestionInfoUser.objects.filter(user_id=user_question_details.user_id,
                                                  question_id=question_id).delete()
                question_add_ids = []
                for each_info_question in info_questions:
                    question_add_id = get_distributed_id(self.worker_id)
                    question_add_ids.append(str(question_add_id))

                    each_info_question_type_id = each_info_question.get('type_id')
                    each_info_question_title = each_info_question.get('title')
                    each_info_question_placeholder = each_info_question.get('placeholder')
                    each_info_question_info_options = each_info_question.get('info_options')
                    each_info_question_info_is_required = each_info_question.get('is_required')
                    each_info_question_info_weight = each_info_question.get('weight', 0)
                    option_ids = []
                    if each_info_question_info_options:
                        for inner_info_question_info_options in each_info_question_info_options:
                            option_id = get_distributed_id(self.worker_id)
                            option_ids.append(str(option_id))
                            info_type_id = each_info_question_type_id
                            option_value = inner_info_question_info_options.get('value')

                            new_option = OioInfoOptionsUser(
                                user_id=user_id,
                                option_id=option_id,
                                info_type_id=info_type_id,
                                option_value=option_value)
                            new_option.save()

                    new_question = OqQuestionInfoUser(
                        user_id=user_id,
                        question_add_id=question_add_id,
                        info_type_id=each_info_question_type_id,
                        question_id=question_id,
                        option_ids=','.join(option_ids),
                        title=each_info_question_title,
                        placeholder=each_info_question_placeholder,
                        is_required=each_info_question_info_is_required,
                        weight=each_info_question_info_weight
                    )
                    new_question.save()

                user_question_details.question_add_ids = ','.join(question_add_ids)

            related_document = request.data.get('related_document')

            if related_document and isinstance(related_document, dict):
                CEEnterpriseFiles.objects.filter(code=question_id).delete()
                urls = []
                for key, values in related_document.items():
                    for each_value in values:
                        file_url = each_value.get('file_url')
                        urls.append(file_url)
                        file_category = 5
                        group_code = key
                        create_by = user_id
                        file_name = each_value.get('file_name')

                        new_file = CEEnterpriseFiles(
                            code=question_id,
                            file_url=file_url,
                            file_category=file_category,
                            group_code=group_code,
                            create_by=create_by,
                            file_name=file_name,
                        )
                        new_file.save()
                user_question_details.related_document = ','.join(urls)

            user_question_details.save()
            return DetailResponse(data={'question_id': user_question_details.question_id})
        except UQDUserQuestionDetails.DoesNotExist:
            print(traceback.format_exc())
            return ErrorResponse(data={'error': 'Question not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(traceback.format_exc())
            return ErrorResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # 审核通过后，添加到公共问题集
    @transaction.atomic
    def insert_to_public_question(self, data, private):

        # 先检查库里是否有该问题集
        if OpQuestionsSet.objects.filter(question_id=data.get('question_id')).exists():
            return 3
        if int(data.get('status')) not in [1,3]:
            return 2
        # 插入问题集
        question_id = data.get('question_id')
        module_id = data.get('module_id')
        industry_id = data.get('industry_id')
        occupation_id = data.get('occu_id')
        sub_occu_id = data.get('sec_occu_id')
        emp_duration_id = data.get('occu_duration_id')
        expertise_level_id = data.get('expertise_level_id')
        title = data.get('assistant_title') if data.get('assistant_title') and data.get('assistant_title') != '' else data.get('character_name')
        content = data.get('assistant_content') if data.get('assistant_content') and data.get('cassistant_ontent') != '' else data.get('character_greetings')

        is_hidden = 0


        try:
            if not private:
                new_question_set = OpQuestionsSet(
                    question_id=question_id,
                    module_id=module_id,
                    industry_id=industry_id,
                    occupation_id=occupation_id,
                    sub_occu_id=sub_occu_id,
                    emp_duration_id=emp_duration_id,
                    expertise_level_id=expertise_level_id,
                    title=title,
                    content=content,
                    is_hidden=is_hidden
                )
                new_question_set.save()

            # 插入question_info逻辑更改， 可能会有多条数据， 依次入库
            question_infos = OqQuestionInfoUser.objects.filter(question_id=question_id)
            for question_info in question_infos:
                print(question_info.__dict__)
                option_ids = question_info.option_ids
                print(option_ids)
                new_question_info = OqQuestionInfo(
                    question_add_id=question_info.question_add_id,
                    question_id=question_info.question_id,
                    info_type_id=question_info.info_type_id,
                    option_ids= option_ids,
                    weight=question_info.weight,
                    placeholder=question_info.placeholder,
                    title=question_info.title,
                    is_required=question_info.is_required
                )
                new_question_info.save()
                if option_ids:
                    option_ids = list(option_ids.split(','))

                    for each_option_id in option_ids:
                        option_infos = OioInfoOptionsUser.objects.get(option_id=each_option_id)

                        new_option = OioInfoOptions(
                            option_id=each_option_id,
                            info_type_id=option_infos.info_type_id,
                            option_value=option_infos.option_value)
                        new_option.save()
            return 1
        except Exception:
            print(traceback.format_exc())
            return 4


class UQDUserQuestionDetailsDictView(APIView):

    def get(self, request):

        is_delete = 0
        is_hidden = 0

        query_params = Q()

        if is_delete:
            query_params &= Q(is_delete=is_delete)

        if is_hidden:
            query_params &= Q(is_hidden=is_hidden)

        results = UQDUserQuestionDetails.objects.filter(query_params).order_by('-created_at')

        # Adding pagination data to results
        data = []
        for question_set in results:
            data.append({
                'question_id': question_set.question_id,
                'assistant_title': question_set.assistant_title,
                'character_name': question_set.character_name,
            })

        data = {
            "data": data
        }
        return DetailResponse(data=data)


class GetRelatedDocuments(APIView):

    def get(self, request):

        files = []

        question_id = request.GET.get('question_id')

        if not question_id:
            return DetailResponse(data=files)

        query_params = Q(code=question_id)
        query_params &= Q(file_category=5)

        results = CEEnterpriseFiles.objects.filter(query_params).order_by('-create_time')

        file_dict = {}
        if results:
            for each_file in results:
                file_url = each_file.file_url
                file_type = each_file.group_code

                if file_url and settings.NETWORK_STATION not in file_url and file_type != 'url':
                    file_url = settings.NETWORK_STATION + file_url
                file_name = each_file.file_name
                create_time = each_file.create_time
                file_dict['file_url'] = file_url
                if not file_url:
                    continue
                file_dict['file_type'] = file_type
                file_dict['file_name'] = file_name
                file_dict['create_time'] =create_time
                files.append(file_dict)
        return DetailResponse(data=files)

