from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from dvadmin.system.models import OpModules, OpIndustry, OpExpertiseLevel, OpOccupation, OpSubOccu, OpEmpDuration
from dvadmin.utils.distributed_id_generator.get_id import get_distributed_id
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from datetime import datetime
from dvadmin.utils.tooss import Tooss

worker_id = 20


class ModulesManage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        module_id = get_distributed_id(worker_id)
        name = request.data.get('name')
        description = request.data.get('description')
        icon = request.data.get('icon')
        industry_id = request.data.get('industry_id')
        occu_id = request.data.get('occu_id')
        sub_occu_id = request.data.get('sub_occu_id')
        emp_duration_id = request.data.get('emp_duration_id')
        expertise_level_id = request.data.get('expertise_level_id')
        cate = request.data.get('cate')
        contact_qr_code = request.data.get('contact_qr_code')
        interest_group = request.data.get('interest_group')


        try:
            pic_url = Tooss.main(icon, cate, local=False)

            if pic_url:
                pic_url = pic_url[1]
        except Exception as e:
            print(e)
            return ErrorResponse()

        module = OpModules(
            module_id=module_id,
            name=name,
            description=description,
            icon=pic_url,
            industry_id=industry_id,
            occu_id=occu_id,
            sub_occu_id=sub_occu_id,
            emp_duration_id=emp_duration_id,
            expertise_level_id=expertise_level_id,
            contact_qr_code=contact_qr_code,
            interest_group=interest_group,
            is_delete=False
        )
        module.save()
        ret_data = {
            'module_id': module_id
        }
        return DetailResponse(data=ret_data)

    def delete(self, request):
        module_id = request.data.get('module_id')

        module = OpModules.objects.get(module_id=module_id)
        module.is_delete = True
        module.save()
        ret_data = {
            'module_id': module_id
        }
        return DetailResponse(data=ret_data)

    def get(self, request):

        page = request.query_params.get('page', None)
        limit = request.query_params.get('limit', None)
        name = request.query_params.get('name')
        module_id = request.query_params.get('module_id')
        industry_id = request.query_params.get('industry_id')
        expertise_level_id = request.query_params.get('expertise_level_id')
        occu_id = request.query_params.get('occu_id')
        sub_occu_id = request.query_params.get('sub_occu_id')
        emp_duration_id = request.query_params.get('emp_duration_id')
        is_delete = request.query_params.get('is_delete')
        query_params = Q()

        if name:
            query_params &= Q(name__icontains=name)

        if module_id:
            query_params &= Q(module_id=module_id)

        if industry_id:
            # Do the same for the other parameters
            query_params &= Q(industry_id=industry_id)

        if expertise_level_id:
            query_params &= Q(expertise_level_id=expertise_level_id)

        if occu_id:

            query_params &= Q(occu_id=occu_id)

        if sub_occu_id:
            query_params &= Q(sub_occu_id=sub_occu_id)

        if emp_duration_id:
            query_params &= Q(emp_duration_id=emp_duration_id)
        if is_delete:
            query_params &= Q(is_delete=is_delete)

        results = OpModules.objects.filter(query_params)
        if page and limit:
            # Pagination
            paginator = Paginator(results, limit)  # Number of records per page
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

        data = []
        for module in results:
            industry_name = OpIndustry.objects.filter(industry_id=module.industry_id).values_list('name',
                                                                                                  flat=True).first()
            occu_name = OpOccupation.objects.filter(occu_id=module.occu_id).values_list('name', flat=True).first()
            sub_occu_name = OpSubOccu.objects.filter(sub_occu_id=module.sub_occu_id).values_list('name',
                                                                                                 flat=True).first()
            emp_duration_name = OpEmpDuration.objects.filter(emp_duration_id=module.emp_duration_id).values_list(
                'emp_duration_name', flat=True).first()
            expertise_level_name = OpExpertiseLevel.objects.filter(
                expertise_level_id=module.expertise_level_id).values_list('name', flat=True).first()

            data.append({
                'module_id': module.module_id,
                'name': module.name,
                'description': module.description,
                'icon': settings.NETWORK_STATION + '/' + module.icon if not str(module.icon).startswith(
                    'http') else module.icon,
                'industry_id': module.industry_id,
                'industry_name': industry_name,
                'occu_id': module.occu_id,
                'occu_name': occu_name,
                'sub_occu_id': module.sub_occu_id,
                'sub_occu_name': sub_occu_name,
                'emp_duration_id': module.emp_duration_id,
                'emp_duration_name': emp_duration_name,
                'expertise_level_id': module.expertise_level_id,
                'expertise_level_name': expertise_level_name,
                'interest_group': module.interest_group,
                'interest_group_desc': module.interest_group_desc,
                'contact_qr_code': module.contact_qr_code,
                'contact_qr_code_desc': module.contact_qr_code_desc,
                'is_delete': module.is_delete,
                'is_hidden': module.is_hidden,
                'created_at': str(module.created_at).replace('T', ' '),
                'updated_at': str(module.updated_at).replace('T', ' '),
            })

        data = {
            "data": data}
        data.update(paginator_data)
        return DetailResponse(data=data)

    def put(self, request):
        module_id = request.data.get('module_id')
        cate = request.data.get('cate')

        if not module_id:
            return ErrorResponse({"error": "module_id is required"})

        try:
            module = OpModules.objects.get(module_id=module_id)
        except OpModules.DoesNotExist:
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
            'module_id': module_id
        }
        return DetailResponse(data=ret_data)


class ModulesDictManage(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        is_delete = 0
        is_hidden = 0

        query_params = Q()

        if is_delete:
            query_params &= Q(is_delete=is_delete)

        if is_hidden:
            query_params &= Q(is_hidden=is_hidden)

        results = OpModules.objects.filter(query_params).order_by('-created_at')

        # Adding pagination data to results
        data = []
        for each in results:
            data.append({
                'module_id': each.module_id,
                'name': each.name,
            })

        data = {
            "data": data
        }
        return DetailResponse(data=data)