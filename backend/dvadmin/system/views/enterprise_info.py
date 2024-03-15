#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/20 17:57
# @Author  : payne
# @File    : activate_code.py
# @Description :
import traceback

from django.conf import settings
from django.core.paginator import Paginator
from django.db import connection, connections
from django.utils.crypto import get_random_string
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from dvadmin.system.models import CEEnterpriseFiles, EnterpriseInfo, EnterpriseProjectInfo, \
    EnterpriseInformationInfo, EnterpriseKnowledgeBase, EnterpriseLabel
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from datetime import datetime


class EnterpriseInfoManage(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 获取查询参数
        company_code = request.query_params.get('company_code')
        company_name = request.query_params.get('company_name')
        status = request.query_params.get('status')
        is_delete = request.query_params.get('is_delete')
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)
        # 构建查询条件
        query_params = {}

        if company_code:
            query_params['company_code'] = company_code
        if company_name:
            query_params['company_name'] = company_name
        if status:
            query_params['status'] = status
        if is_delete:
            query_params['is_delete'] = is_delete

        # 根据查询条件进行过滤
        results = EnterpriseInfo.objects.filter(**query_params)

        if page:
            # 分页处理
            paginator = Paginator(results, int(limit))  # 每页显示的数据量
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
        # 构造返回数据
        data = []

        for company_info in results:
            industry_code = company_info.industry_code
            company_code = company_info.company_code

            enterprise_labels = EnterpriseInfoUtils.get_related_labels(industry_code)
            enterprise_project = EnterpriseInfoUtils.get_enterprise_project(company_code)
            enterprise_info = EnterpriseInfoUtils.get_enterprise_info(company_code)
            enterprise_knowledge_base = EnterpriseInfoUtils.get_enterprise_knowledge_base(company_code)

            data.append({
                'company_code': company_info.company_code,
                'company_name': company_info.company_name,
                'company_abbreviation': company_info.company_abbreviation,
                'position': company_info.position,
                'industry_code': industry_code,
                'enterprise_project': enterprise_project,
                'enterprise_info': enterprise_info,
                'enterprise_knowledge_base': enterprise_knowledge_base,
                'enterprise_labels': enterprise_labels,
                'registered_address': company_info.registered_address,
                'company_desc': company_info.company_desc,
                'company_url': company_info.company_url,
                'ipc_code': company_info.ipc_code,
                'company_mobile': company_info.company_mobile,
                'company_mailbox': company_info.company_mailbox,
                'company_address': company_info.company_address,
                'status': company_info.status,
                'create_by': company_info.create_by,
                'create_time': company_info.create_time,
                'modify_time': company_info.modify_time,
                'is_delete': company_info.is_delete,
            })
        ret_data = {
            'data': data
        }
        ret_data.update(paginator_data)
        return DetailResponse(ret_data)


class EnterpriseInfoUtils:

    # 获取相关关联文件
    @staticmethod
    def get_related_documents(id):

        documents_list = []
        if not id:
            return documents_list

        documents = CEEnterpriseFiles.objects.filter(code=id, is_delete=0)

        if documents:

            for each_document in documents:
                document_dict = {}
                code = each_document.code
                file_url = each_document.file_url
                file_category = each_document.file_category
                group_code = each_document.group_code
                create_by = each_document.create_by
                create_time = each_document.create_time
                modify_time = each_document.modify_time
                is_delete = each_document.is_delete

                if file_url:
                    if settings.NETWORK_STATION not in file_url and group_code not in ('url', 'website'):
                        file_url = settings.NETWORK_STATION + '/' + file_url

                document_dict['code'] = code
                document_dict['file_url'] = file_url
                document_dict['file_category'] = file_category
                document_dict['group_code'] = group_code
                document_dict['create_by'] = create_by
                document_dict['create_time'] = create_time
                document_dict['modify_time'] = modify_time
                document_dict['is_delete'] = is_delete
                documents_list.append(document_dict)
        return documents_list

    @staticmethod
    def get_related_labels(id):

        labels_list = []
        if not id:
            return labels_list

        labels = EnterpriseLabel.objects.filter(label_code=id, is_delete=0)

        if labels:

            for each_label in labels:
                label_dict = {}
                label_code = each_label.label_code
                label = each_label.label
                label_type = each_label.label_type
                create_by = each_label.create_by
                create_time = each_label.create_time
                modify_time = each_label.modify_time
                is_delete = each_label.is_delete
                label_dict['label_code'] = label_code
                label_dict['label'] = label
                label_dict['label_type'] = label_type
                label_dict['create_by'] = create_by
                label_dict['create_time'] = create_time
                label_dict['modify_time'] = modify_time
                label_dict['is_delete'] = is_delete
                labels_list.append(label_dict)
        return labels_list

    # 获取企业项目
    @staticmethod
    def get_enterprise_project(company_id):

        projects_list = []
        if not company_id:
            return projects_list

        projects = EnterpriseProjectInfo.objects.filter(company_code=company_id, is_delete=0)

        if projects:

            for each_project in projects:
                project_dict = {}
                company_code = each_project.company_code
                project_code = each_project.project_code
                category_name = each_project.category_name
                project_name = each_project.project_name
                brief_introduction = each_project.brief_introduction
                create_time = each_project.create_time
                modify_time = each_project.modify_time
                is_delete = each_project.is_delete

                # 获取可能会有的企业文件
                enterprise_documents = EnterpriseInfoUtils.get_related_documents(project_code)

                project_dict['company_code'] = company_code
                project_dict['project_code'] = project_code
                project_dict['category_name'] = category_name
                project_dict['project_name'] = project_name
                project_dict['enterprise_documents'] = enterprise_documents
                project_dict['brief_introduction'] = brief_introduction
                project_dict['create_time'] = create_time
                project_dict['modify_time'] = modify_time
                project_dict['is_delete'] = is_delete
                projects_list.append(project_dict)
        return projects_list

    # 获取企业信息
    @staticmethod
    def get_enterprise_info(company_id):

        info_list = []
        if not company_id:
            return info_list

        infos = EnterpriseInformationInfo.objects.filter(company_code=company_id, is_delete=0)

        if infos:

            for each_info in infos:
                info_dict = {}
                company_code = each_info.company_code
                information_code = each_info.information_code
                label_code = each_info.label_code
                information_name = each_info.information_name
                content_desc = each_info.content_desc
                create_by = each_info.create_by
                create_time = each_info.create_time
                modify_time = each_info.modify_time
                is_delete = each_info.is_delete

                # 获取可能会有的企业文件
                enterprise_documents = EnterpriseInfoUtils.get_related_documents(information_code)
                enterprise_labels = EnterpriseInfoUtils.get_related_labels(label_code)

                info_dict['company_code'] = company_code
                info_dict['information_code'] = information_code
                info_dict['label_code'] = label_code
                info_dict['information_name'] = information_name
                info_dict['enterprise_documents'] = enterprise_documents
                info_dict['enterprise_labels'] = enterprise_labels
                info_dict['content_desc'] = content_desc
                info_dict['create_by'] = create_by
                info_dict['create_time'] = create_time
                info_dict['modify_time'] = modify_time
                info_dict['is_delete'] = is_delete
                info_list.append(info_dict)
        return info_list

    # 获取企业知识库
    @staticmethod
    def get_enterprise_knowledge_base(company_id):

        knowledge_base_list = []
        if not company_id:
            return knowledge_base_list

        knowledge_bases = EnterpriseKnowledgeBase.objects.filter(company_code=company_id, is_delete=0)

        if knowledge_bases:

            for each_knowledge_base in knowledge_bases:
                knowledge_base_dict = {}
                company_code = each_knowledge_base.company_code
                knowledge_code = each_knowledge_base.knowledge_code
                category = each_knowledge_base.category
                category_name = each_knowledge_base.category_name
                content_desc = each_knowledge_base.content_desc
                purpose = each_knowledge_base.purpose
                create_by = each_knowledge_base.create_by
                create_time = each_knowledge_base.create_time
                modify_time = each_knowledge_base.modify_time
                is_delete = each_knowledge_base.is_delete

                # 获取可能会有的企业文件
                enterprise_documents = EnterpriseInfoUtils.get_related_documents(knowledge_code)
                enterprise_labels = EnterpriseInfoUtils.get_related_labels(category)

                knowledge_base_dict['company_code'] = company_code
                knowledge_base_dict['knowledge_code'] = knowledge_code
                knowledge_base_dict['category'] = category
                knowledge_base_dict['category'] = category
                knowledge_base_dict['category_name'] = category_name
                knowledge_base_dict['enterprise_labels'] = enterprise_labels
                knowledge_base_dict['purpose'] = purpose
                knowledge_base_dict['enterprise_documents'] = enterprise_documents
                knowledge_base_dict['create_by'] = create_by
                knowledge_base_dict['create_time'] = create_time
                knowledge_base_dict['modify_time'] = modify_time
                knowledge_base_dict['is_delete'] = is_delete
                knowledge_base_list.append(knowledge_base_dict)
        return knowledge_base_list

