from django.db import transaction
from django.db.models import Q, Max
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from dvadmin.system.models import OpQuestionsSet, OpIndustry, OpSubOccu, OpOccupation, OpEmpDuration, OpExpertiseLevel, \
    OpModules

from dvadmin.utils.distributed_id_generator.get_id import get_distributed_id
from dvadmin.utils.json_response import DetailResponse, ErrorResponse

worker_id = 31


class OpQuestionsSetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        question_id = get_distributed_id(worker_id)
        module_id = request.data.get('module_id')
        industry_id = request.data.get('industry_id')
        occupation_id = request.data.get('occu_id')
        sub_occu_id = request.data.get('sub_occu_id')
        emp_duration_id = request.data.get('emp_duration_id')
        expertise_level_id = request.data.get('expertise_level_id')
        title = request.data.get('title')
        content = request.data.get('content')
        example = request.data.get('example')
        content_hidden = request.data.get('content_hidden')
        is_hidden = request.data.get('is_hidden')
        max_weight = OpQuestionsSet.objects.aggregate(Max('weight'))['weight__max']

        new_question_set = OpQuestionsSet(
            weight=max_weight + 1,
            question_id=question_id,
            module_id=module_id,
            industry_id=industry_id,
            occupation_id=occupation_id,
            sub_occu_id=sub_occu_id,
            emp_duration_id=emp_duration_id,
            expertise_level_id=expertise_level_id,
            title=title,
            content=content,
            example_question=example,
            content_hidden=content_hidden,
            is_hidden=is_hidden,
        )
        new_question_set.save()

        return DetailResponse(data={'question_id': new_question_set.question_id})

    def delete(self, request):
        question_set_id = request.data.get('question_id')

        try:
            question_set = OpQuestionsSet.objects.get(question_id=question_set_id)
            question_set.delete()
        except OpQuestionsSet.DoesNotExist:
            return ErrorResponse({"error": "Question set not found"})

        return DetailResponse(data={'question_id': question_set_id})

    def get(self, request):

        page = request.query_params.get('page', None)
        limit = request.query_params.get('limit', None)
        industry_id = request.query_params.get('industry_id')
        occupation_id = request.query_params.get('occupation_id')
        sub_occu_id = request.query_params.get('sub_occu_id')
        expertise_level_id = request.query_params.get('expertise_level_id')
        emp_duration_id = request.query_params.get('emp_duration_id')
        module_id = request.query_params.get('module_id')
        title = request.query_params.get('title')
        is_delete = request.query_params.get('is_delete')
        is_hidden = request.query_params.get('is_hidden')

        query_params = Q()

        # Splitting and using '__in' filter like the above method
        if industry_id:
            query_params &= Q(industry_id=industry_id)

        if occupation_id:
            query_params &= Q(occupation_id=occupation_id)

        if sub_occu_id:
            query_params &= Q(sub_occu_id=sub_occu_id)

        if emp_duration_id:
            query_params &= Q(emp_duration_id=emp_duration_id)

        if expertise_level_id:
            query_params &= Q(expertise_level_id=expertise_level_id)

        if module_id:
            query_params &= Q(module_id=module_id)

        if title:
            # Using 'icontains' for case-insensitive partial matches
            query_params &= Q(title__icontains=title)

        if is_delete:
            query_params &= Q(is_delete=is_delete)

        if is_hidden:
            query_params &= Q(is_hidden=is_hidden)

        results = OpQuestionsSet.objects.filter(query_params).order_by('-created_at', 'updated_at')

        if page and limit:

            # Pagination
            paginator = Paginator(results, limit)
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
        else:
            paginator_data = {}

        # Adding pagination data to results
        data = []
        for question_set in results:
            industry_name = OpIndustry.objects.filter(industry_id=question_set.industry_id).values_list('name',
                                                                                                        flat=True).first()
            occu_name = OpOccupation.objects.filter(occu_id=question_set.occupation_id).values_list('name',
                                                                                                    flat=True).first()
            sub_occu_name = OpSubOccu.objects.filter(sub_occu_id=question_set.sub_occu_id).values_list('name',
                                                                                                       flat=True).first()
            emp_duration_name = OpEmpDuration.objects.filter(emp_duration_id=question_set.emp_duration_id).values_list(
                'emp_duration_name', flat=True).first()
            expertise_level_name = OpExpertiseLevel.objects.filter(
                expertise_level_id=question_set.expertise_level_id).values_list('name', flat=True).first()
            module_name = OpModules.objects.filter(
                module_id=question_set.module_id).values_list('name', flat=True).first()
            data.append({
                'id': question_set.id,
                'weight': question_set.weight,
                'question_id': question_set.question_id,
                'industry_id': question_set.industry_id,
                'industry_name': industry_name,
                'occu_id': question_set.occupation_id,
                'occu_name': occu_name,
                'sub_occu_id': question_set.sub_occu_id,
                'sub_occu_name': sub_occu_name,
                'emp_duration_id': question_set.emp_duration_id,
                'emp_duration_name': emp_duration_name,
                'expertise_level_id': question_set.expertise_level_id,
                'expertise_level_name': expertise_level_name,
                'module_name': module_name,
                'module_id': question_set.module_id,
                'title': question_set.title,
                'content': question_set.content,
                'example_question': question_set.example_question,
                'content_hidden': question_set.content_hidden,
                'is_hidden': question_set.is_hidden,
                'is_delete': question_set.is_delete,
                'created_at': str(question_set.created_at).replace('T', ' '),
                'updated_at': str(question_set.updated_at).replace('T', ' '),
            })

        data = {
            "data": data
        }
        data.update(paginator_data)
        return DetailResponse(data=data)

    def put(self, request):
        question_id = request.data.get('question_id')
        is_update_weight = request.data.get('is_update_weight')
        updating_weight = request.data.get('updating_weight')
        updated_weight = request.data.get('updated_weight')

        try:
            question_set = OpQuestionsSet.objects.get(question_id=question_id)
        except OpQuestionsSet.DoesNotExist:
            return ErrorResponse({"error": "Question set not found"}, status=404)

        if is_update_weight:
            with transaction.atomic():
                # 找到 weight 为 34 的记录
                obj1 = OpQuestionsSet.objects.get(weight=updating_weight)

                # 找到 weight 为 2 的记录
                obj2 = OpQuestionsSet.objects.get(weight=updated_weight)

                # 交换 weight 值
                obj1.weight, obj2.weight = obj2.weight, obj1.weight

                # 保存更改
                obj1.save()
                obj2.save()

        question_set.question_id = request.data.get('question_id', question_set.question_id)
        question_set.module_id = request.data.get('module_id', question_set.module_id)
        question_set.industry_id = request.data.get('industry_id', question_set.industry_id)
        question_set.occupation_id = request.data.get('occupation_id', question_set.occupation_id)
        question_set.sub_occu_id = request.data.get('sub_occu_id', question_set.sub_occu_id)
        question_set.emp_duration_id = request.data.get('emp_duration_id', question_set.emp_duration_id)
        question_set.expertise_level_id = request.data.get('expertise_level_id', question_set.expertise_level_id)
        question_set.title = request.data.get('title', question_set.title)
        question_set.content = request.data.get('content', question_set.content)
        question_set.example_question = request.data.get('example_question', question_set.example_question)
        question_set.content_hidden = request.data.get('content_hidden', question_set.content_hidden)

        question_set.save()

        return DetailResponse(data={'question_id': question_id})


class OpQuestionsSetDictView(APIView):

    def get(self, request):

        is_delete = 0
        is_hidden = 0

        query_params = Q()

        # Splitting and using '__in' filter like the above method

        if is_delete:
            query_params &= Q(is_delete=is_delete)

        if is_hidden:
            query_params &= Q(is_hidden=is_hidden)

        results = OpQuestionsSet.objects.filter(query_params).order_by('-created_at')

        # Adding pagination data to results
        data = []
        for question_set in results:
            data.append({
                'question_id': question_set.question_id,
                'content': question_set.content,
            })

        data = {
            "data": data
        }
        return DetailResponse(data=data)


class WeightConfigure(APIView):

    def post(self, request):
        question_id = request.data.get('question_id')
        updating_weight = request.data.get('updating_weight')
        updated_weight = request.data.get('updated_weight')

        try:
            OpQuestionsSet.objects.get(question_id=question_id)
        except OpQuestionsSet.DoesNotExist:
            return ErrorResponse({"error": "Question set not found"}, status=404)

        with transaction.atomic():
            # 找到 weight 为 34 的记录
            obj1 = OpQuestionsSet.objects.get(weight=updating_weight)

            # 找到 weight 为 2 的记录
            obj2 = OpQuestionsSet.objects.get(weight=updated_weight)

            # 交换 weight 值
            obj1.weight, obj2.weight = obj2.weight, obj1.weight

            # 保存更改
            obj1.save()
            obj2.save()
        return DetailResponse(data={'question_id': question_id})