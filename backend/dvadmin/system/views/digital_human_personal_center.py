import requests
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from dvadmin.system.models import DhDigitalHumanSecretKey, \
    ScpcSecretKeyPersonalCenter, DhDigitalHumanProduct, OpPictures, Users  # Make sure this import path is correct
from dvadmin.utils.distributed_id_generator.get_id import get_distributed_id
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from datetime import datetime, timedelta, timezone

from dvadmin.utils.string_util import convert_to_desired_format


class DigitalPersonalCenter(APIView):
    permission_classes = [AllowAny]

    worker_id = 20002

    def post(self, request):
        data = request.data
        mobile = data.get('mobile')
        name = data.get('name')
        sign = data.get('sign')
        account_type = data.get('account_type')
        product_type = data.get('product_type')

        random_record = DhDigitalHumanSecretKey.objects.filter(status=0, product_type=product_type).order_by('?').values(
            'product_type', 'account', 'password', 'secrey_key', 'key_id'
        ).first()

        if random_record:
            account = random_record['account']
            password = random_record['password']
            secrey_key = random_record['secrey_key']
            key_id = random_record['key_id']
        else:
            return ErrorResponse(code=40004, msg='没有对应卡密啦')

        check_exists = DhDigitalHumanSecretKey.objects.filter(mobile=mobile, product_type=product_type).exists()

        if check_exists:
            return ErrorResponse(code=40001, msg='已经领取过了')

        # result = DhDigitalHumanProduct.objects.filter(product_type=product_type).values('download_link', 'product_name',
        #                                                                                 'usage_description').first()

        # download_link = result['download_link']
        # usage_description = result['usage_description']
        # product_name = result['product_name']

        sms_context = f"""发卡系统链接: https://www.umi6.com/history.html?{mobile}，点击可查看领取记录详情信息！"""
        send_sms_address = settings.SERVER + settings.SEND_SMS
        data = {
            'mobile': mobile,
            'msg': sms_context
        }
        send_sms = requests.post(url=send_sms_address, data=data)

        if send_sms.status_code == 200:
            data = send_sms.json()
            if data.get('code') == 20000:
                send_success = True
            else:
                send_success = False
        else:
            send_success = False

        if send_success:
            if sign:
                belong_to_seller = Users.objects.filter(id=sign).values_list('name', flat=True)
                sign = belong_to_seller[0]
            else:
                sign = ''

            # 定义东八区时间偏移
            UTC8 = timezone(timedelta(hours=8))
            # 获取当前时间，并转换为东八区时间
            receive_time = datetime.now(UTC8)
            receive_time = receive_time.strftime('%Y-%m-%d %H:%M:%S')

            updated_records = DhDigitalHumanSecretKey.objects.filter(key_id=key_id).update(
                status=1,
                name=name,
                seller_name=sign if sign else '',
                account_type=account_type,
                mobile=mobile,
                receive_time=receive_time
            )

            if updated_records:
                updated_success = True
            else:
                updated_success = False
        else:
            updated_success = False

        if all([send_success, updated_success]):
            return DetailResponse(data={'mobile': mobile})
        else:
            return ErrorResponse(code=40002, msg='领取失败')

    def get(self, request):
        mobile = request.GET.get('mobile')
        limit = request.GET.get('limit', 10)
        page = request.GET.get('page', 1)
        # 首先查询DhDigitalHumanSecretKey模型
        dh_keys = DhDigitalHumanSecretKey.objects.filter(mobile=mobile).values('product_type', 'account', 'account_type',
                                                                                   'password', 'secrey_key','sign',
                                                                                   'valid_time', 'receive_time'
                                                                                   )

        # 然后查询ScpcSecretKeyPersonalCenter模型
        scpc_products = DhDigitalHumanProduct.objects.filter(is_delete=0).values('product_type',
                                                                                 'update_time',
                                                                                 'download_link',
                                                                                 'tutorial',
                                                                                 'usage_description',
                                                                                 'product_name'
                                                                                 )
        merged_data = []
        for key in dh_keys:
            for product in scpc_products:
                if key['product_type'] == product['product_type']:
                    merged_data.append({
                        'product_type': key['product_type'],
                        'account': key['account'],
                        'password': key['password'],
                        'secrey_key': key['secrey_key'],
                        'account_type': key['account_type'],
                        'sign': key['sign'],
                        'valid_time': convert_to_desired_format(key['valid_time']),
                        'receive_time': convert_to_desired_format(key['receive_time']),
                        'download_link': product['download_link'],  # 假设update_time是领取时间
                        'tutorial': product['tutorial'],  # 假设update_time是领取时间
                        'product_name': product['product_name'],  # 假设update_time是领取时间
                        'usage_description': product['usage_description'],  # 假设update_time是领取时间
                    })

        # Pagination
        paginator = Paginator(merged_data, limit)
        results = paginator.get_page(page)

        paginator_data = {
            "is_previous": results.has_previous(),
            "is_next": results.has_next(),
            "limit": paginator.per_page,
            "page": results.number,
            "total": paginator.count,
        }

        ret_data = {
            "data": merged_data
        }
        ret_data.update(paginator_data)

        return DetailResponse(data=ret_data)


class QRCodeManage(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        records = OpPictures.objects.filter(type__in=[6, 7]).values('pic_url', 'type', 'pic_desc')

        data = []

        for each in records:
            pic_url = each['pic_url']
            type = each['type']
            pic_desc = each['pic_desc']

            dict_data = {
                "pic_url": pic_url,
                "type": type,
                "pic_desc":pic_desc
            }
            data.append(dict_data)

        return DetailResponse(data=data)


