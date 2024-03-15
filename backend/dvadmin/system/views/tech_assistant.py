#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/12 18:03
# @Author  : payne
# @File    : tech_assistant.py
# @Description :
from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from dvadmin.system.models import UpProblem, UpProblemPicture
from dvadmin.utils.json_response import DetailResponse, ErrorResponse


class UpProblemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Extract data from the request
        problem_data = {
            'problem': request.data.get('problem', ''),
            'contact': request.data.get('contact', ''),
            'create_by': request.data.get('create_by', ''),
        }

        # Create a new UpProblem instance
        new_problem = UpProblem(**problem_data)
        new_problem.save()

        return DetailResponse(data={'problem_id': new_problem.id})

    def delete(self, request):
        problem_id = request.data.get('problem_id')

        try:
            problem = UpProblem.objects.get(id=problem_id)
            problem.delete()
        except UpProblem.DoesNotExist:
            return ErrorResponse({"error": "Problem not found"})

        return DetailResponse(data={'problem_id': problem_id})

    def get(self, request):
        # Extract query parameters from the request
        question_type = request.query_params.get('question_type', None)
        status = request.query_params.get('status', None)
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)

        query_params = Q()

        # Construct the query parameters
        if question_type is not None:
            query_params = Q(question_type=question_type)

        if status is not None:
            query_params = Q(status=status)

        # Filter UpProblem objects based on the query parameters
        problems = UpProblem.objects.filter(query_params).order_by('-create_time')

        print(problems)
        # Pagination
        paginator = Paginator(problems, limit)
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

        # Retrieve related UpProblemPicture objects
        problem_ids = [problem.id for problem in results]
        picture_urls = UpProblemPicture.objects.filter(problem_id__in=problem_ids, is_delete=0).values('problem_id',
                                                                                                       'picture_url')

        # Create a dictionary of picture_urls for quick lookup
        picture_url_map = {item['problem_id']: item['picture_url'] for item in picture_urls}

        # Format the data for the response
        data = []
        for problem in results:
            data.append({
                'id': problem.id,
                'problem': problem.problem,
                'contact': problem.contact,
                'question_type': problem.question_type,
                'create_by': problem.create_by,
                'create_time': problem.create_time,
                'modify_time': problem.modify_time,
                'is_delete': problem.is_delete,
                'picture_url': picture_url_map.get(problem.id, ''),  # Retrieve the corresponding picture_url
            })

        data = {
            "data": data,
        }
        data.update(paginator_data)

        return DetailResponse(data=data)

    def put(self, request):
        problem_id = request.data.get('problem_id')

        try:
            problem = UpProblem.objects.get(id=problem_id)
        except UpProblem.DoesNotExist:
            return ErrorResponse({"error": "Problem not found"}, status=404)

        # Update the problem fields
        problem.problem = request.data.get('problem', problem.problem)
        problem.contact = request.data.get('contact', problem.contact)
        problem.create_by = request.data.get('create_by', problem.create_by)
        problem.modify_time = datetime.now()  # Update the modify_time field
        problem.is_delete = request.data.get('is_delete', problem.is_delete)

        problem.save()

        return DetailResponse(data={'problem_id': problem_id})
