import pyshorteners
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from dvadmin.system.models import DhDigitalHumanSecretKey, Users  # Make sure this import path is correct
from dvadmin.utils.distributed_id_generator.get_id import get_distributed_id
from dvadmin.utils.filters import get_user_name_by_id
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from datetime import datetime


class DigitalHumanSecretKeyManage(APIView):
    permission_classes = [IsAuthenticated]

    worker_id = 20001

    def post(self, request):
        product_type = request.data.get('product_type')
        key_id = get_distributed_id(worker_id=self.worker_id)
        account = request.data.get('account')
        account_type = request.data.get('account_type', 0)
        password = request.data.get('password')
        secrey_key = request.data.get('secrey_key')
        status = request.data.get('status')
        # recipient = request.data.get('recipient')
        # receive_time = request.data.get('receive_time')
        valid_time = request.data.get('valid_time')
        valid_time = datetime.fromisoformat(valid_time.replace("Z", "+00:00"))

        key_instance = DhDigitalHumanSecretKey(
            product_type=product_type,
            key_id=key_id,
            account=account,
            account_type=account_type,
            status=status,
            password=password,
            secrey_key=secrey_key,
            valid_time=valid_time
        )
        key_instance.save()

        ret_data = {
            'key_id': key_instance.key_id
        }
        return DetailResponse(data=ret_data)

    def delete(self, request):
        key_id = request.data.get('key_id')
        key_instance = DhDigitalHumanSecretKey.objects.get(key_id=key_id)
        key_instance.delete()
        ret_data = {
            'key_id': key_id
        }
        return DetailResponse(data=ret_data)

    def get(self, request):
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)
        product_type = request.query_params.get('product_type')
        user_name = request.query_params.get('user_name')
        user_id = request.query_params.get('user_id')
        account = request.query_params.get('account')
        status = request.query_params.get('status')

        query_params = Q()

        if product_type:
            query_params &= Q(product_type=product_type)

        if int(user_id) not in [16, 13, 8]:
            if user_name:
                query_params &= Q(seller_name=user_name.strip())

        if account:
            query_params &= Q(account=account)

        if status:
            query_params &= Q(status=status)

        keys = DhDigitalHumanSecretKey.objects.filter(query_params).order_by('-receive_time')

        # Pagination
        paginator = Paginator(keys, limit)
        results = paginator.get_page(page)

        paginator_data = {
            "is_previous": results.has_previous(),
            "is_next": results.has_next(),
            "limit": paginator.per_page,
            "page": results.number,
            "total": paginator.count,
        }

        data = [
            {
                'id': key.id,
                'key_id': key.key_id,
                'product_type': key.product_type,
                'mobile': key.mobile,
                'name': key.name,
                'account': key.account,
                'account_type': key.account_type,
                'password': key.password,
                'status': key.status,
                'sign': key.sign,
                'secrey_key': key.secrey_key,
                'receive_time': key.receive_time,
                'valid_time': key.valid_time,
                'create_time': key.create_time,
                'seller_name': key.seller_name
            }
            for key in results
        ]
        ret_data = {
            "data": data
        }
        ret_data.update(paginator_data)

        return DetailResponse(data=ret_data)

    def put(self, request):
        key_id = request.data.get('key_id')
        if not key_id:
            return ErrorResponse({"error": "id is required"}, status=400)

        try:
            key_instance = DhDigitalHumanSecretKey.objects.get(key_id=key_id)
        except DhDigitalHumanSecretKey.DoesNotExist:
            return ErrorResponse({"error": "SecretKey not found"}, status=404)
        origin_seller_name = key_instance.seller_name

        if origin_seller_name:
            return ErrorResponse(code=40005, msg='该条记录已有对应销售人员')

        key_instance.product_type = request.data.get('product_type', key_instance.product_type)
        key_instance.account = request.data.get('account', key_instance.account)
        key_instance.password = request.data.get('password', key_instance.password)
        key_instance.seller_name = request.data.get('seller_name', key_instance.seller_name)
        key_instance.secrey_key = request.data.get('secrey_key', key_instance.secrey_key)
        key_instance.status = request.data.get('status', key_instance.status)
        key_instance.receive_time = request.data.get('receive_time', key_instance.receive_time)
        key_instance.valid_time = request.data.get('valid_time', key_instance.valid_time)

        key_instance.save()

        ret_data = {
            'key_id': key_instance.key_id
        }
        return DetailResponse(data=ret_data)


class AssignCustomer(APIView):
    permission_classes = [IsAuthenticated]

    worker_id = 20001

    def post(self, request):

        seller_name = request.data.get('seller_name')
        key_id = request.data.get('key_id')
        check_db_data = DhDigitalHumanSecretKey.objects.filter(key_id=key_id).values('status', 'seller_name').first()

        db_status = check_db_data['status']

        db_seller_name = check_db_data['seller_name']

        if int(db_status) == 0:
            return ErrorResponse(code=40006, msg='该条记录尚未被领取，无法分配')

        # if db_seller_name:
        #     return ErrorResponse(code=40007, msg='已经分配过啦')

        key_instance = DhDigitalHumanSecretKey.objects.get(
            key_id=key_id
        )
        key_instance.seller_name = seller_name
        key_instance.save()

        ret_data = {
            'key_id': key_instance.key_id
        }
        return DetailResponse(data=ret_data)

    def get(self, request):
        users_in_dept = Users.objects.filter(dept_id=1).values('name')

        ret_data = []
        for each in users_in_dept:
            name = each.get('name')
            data = {
                'value': name,
                'label': name
            }
            ret_data.append(data)

        return DetailResponse(data=ret_data)


class ShortUrl(APIView):

    def post(self, request):
        """
        获取短链接的方法
        """
        print(111111)
        # 从请求中获取长链接
        original_url = request.data.get('shareUrl')
        print(request.data)
        print(original_url)

        # 使用 pyshorteners 生成短链接
        s = pyshorteners.Shortener()
        short_url = s.tinyurl.short(original_url)

        print(short_url)
        return DetailResponse({"short_url": short_url})




