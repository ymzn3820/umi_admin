from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from dvadmin.system.models import OpQuestionsEdit, OpQuestionsSet

from dvadmin.utils.distributed_id_generator.get_id import get_distributed_id
from dvadmin.utils.json_response import DetailResponse, ErrorResponse

worker_id = 32


class OpQuestionsEditView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        try:
            question_id = request.data.get('question_id')
            field_id = get_distributed_id(worker_id)
            field_name = request.data.get('field_name')
            content = request.data.get('content')
            show_order = request.data.get('show_order')
            is_hidden = request.data.get('is_hidden')

            new_question_edit = OpQuestionsEdit(
                question_id=question_id,
                field_id=field_id,
                field_name=field_name,
                content=content,
                show_order=show_order,
                is_hidden=is_hidden,
            )
            new_question_edit.save()

            # 找到对应的OpQuestionsSet记录
            question_set = OpQuestionsSet.objects.get(question_id=question_id)

            # 通过question_id查询所有对应的OpQuestionsEdit记录，然后根据show_order字段进行升序排序
            question_edits = OpQuestionsEdit.objects.filter(question_id=question_id).order_by('show_order')

            # 将新内容添加到OpQuestionsSet中的content_hidden字段
            # 假设content是文本，我们将其合并
            new_content_hidden = ' '.join([edit.content for edit in question_edits])

            # 更新OpQuestionsSet的content_hidden字段
            question_set.content_hidden = new_content_hidden
            question_set.save()

            return DetailResponse(data={'question_id': new_question_edit.question_id})
        except Exception as e:
            # 如果出现任何异常，回滚事务
            transaction.rollback()
            return DetailResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def delete(self, request):
        field_id = request.data.get('field_id')

        try:
            # 将需要删除的question_edit实例获取出来
            question_edit = OpQuestionsEdit.objects.get(field_id=field_id)
            question_id = question_edit.question_id

            # 删除该实例
            question_edit.delete()

            # 获取对应的OpQuestionsSet记录
            question_set = OpQuestionsSet.objects.get(question_id=question_id)

            # 通过question_id查询所有剩余的OpQuestionsEdit记录，然后根据show_order字段进行升序排序
            question_edits = OpQuestionsEdit.objects.filter(question_id=question_id).order_by('show_order')

            # 将新内容添加到OpQuestionsSet中的content_hidden字段
            new_content_hidden = ' '.join([edit.content for edit in question_edits])

            # 更新OpQuestionsSet的content_hidden字段
            question_set.content_hidden = new_content_hidden
            question_set.save()

            return DetailResponse(data={'field_id': field_id})
        except OpQuestionsEdit.DoesNotExist:
            return ErrorResponse({"error": "Question edit not found"})
        except Exception as e:
            # 如果出现任何异常，回滚事务
            transaction.rollback()
            return DetailResponse(data={'error': str(e)})

    def get(self, request):

        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)
        question_id = request.query_params.get('question_id')
        field_id = request.query_params.get('field_id')
        filed_name = request.query_params.get('filed_name')
        is_delete = request.query_params.get('is_delete')
        is_hidden = request.query_params.get('is_hidden')

        query_params = Q()

        if question_id:
            query_params &= Q(question_id=question_id)

        if field_id:
            query_params &= Q(field_id=field_id)

        if filed_name:
            query_params &= Q(filed_name=filed_name)

        if is_delete:
            query_params &= Q(is_delete=is_delete)

        if is_hidden:
            query_params &= Q(is_hidden=is_hidden)

        question_edits = OpQuestionsEdit.objects.filter(query_params).order_by('-created_at')

        # Pagination
        paginator = Paginator(question_edits, limit)
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
        for question_edit in results:
            data.append({
                'id': question_edit.id,
                'question_id': question_edit.question_id,
                'field_id': question_edit.field_id,
                'field_name': question_edit.field_name,
                'content': question_edit.content,
                'show_order': question_edit.show_order,
                'is_hidden': question_edit.is_hidden,
                'is_delete': question_edit.is_delete,
                'created_at': str(question_edit.created_at).replace('T', ' '),
                'updated_at': str(question_edit.updated_at).replace('T', ' '),
            })

        data = {
            "data": data
        }

        data.update(paginator_data)
        return DetailResponse(data=data)

    @transaction.atomic
    def put(self, request):
        field_id = request.data.get('field_id')

        try:
            question_edit = OpQuestionsEdit.objects.get(field_id=field_id)
        except OpQuestionsEdit.DoesNotExist:
            return ErrorResponse({"error": "Question edit not found"}, status=404)

        question_id = question_edit.question_id
        question_edit.field_name = request.data.get('field_name', question_edit.field_name)
        question_edit.content = request.data.get('content', question_edit.content)
        question_edit.show_order = request.data.get('show_order', question_edit.show_order)
        question_edit.is_hidden = request.data.get('is_hidden', question_edit.is_hidden)
        question_edit.is_delete = request.data.get('is_delete', question_edit.is_delete)

        try:
            question_edit.save()

            # 获取对应的OpQuestionsSet记录
            question_set = OpQuestionsSet.objects.get(question_id=question_id)

            # 通过question_id查询所有对应的OpQuestionsEdit记录，然后根据show_order字段进行升序排序
            question_edits = OpQuestionsEdit.objects.filter(question_id=question_id).order_by('show_order')

            # 将新内容添加到OpQuestionsSet中的content_hidden字段
            new_content_hidden = ' '.join([edit.content for edit in question_edits])

            # 更新OpQuestionsSet的content_hidden字段
            question_set.content_hidden = new_content_hidden
            question_set.save()

        except Exception as e:
            # 如果出现任何异常，回滚事务
            transaction.rollback()
            return DetailResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return DetailResponse(data={'field_id': field_id})