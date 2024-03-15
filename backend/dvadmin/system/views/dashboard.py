#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/19 14:25
# @Author  : payne
# @File    : dashboard.py
# @Description : 控制台功能


from datetime import datetime, timedelta
from django.db import connections, connection
from django.db.models.functions import TruncDay
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from dvadmin.utils.json_response import DetailResponse
from dvadmin.system.models import UUUsers, UUUsersTemp, ObBusinessCooperation, PpPayments
from dvadmin.utils.string_util import format_bytes


class DashBoardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ret_data = {}

        ret_data.update(self.count_new_users())
        ret_data.update(self.count_new_guests())
        ret_data.update(self.count_guest_conversion())
        ret_data.update(self.count_pay_conversion())
        ret_data.update(self.count_pay_users())
        return DetailResponse(data=ret_data)

    def count_new_users(self):
        today = datetime.now().date()
        three_days_ago = today - timedelta(days=3)
        one_week_ago = today - timedelta(weeks=1)
        one_month_ago = today - timedelta(weeks=4)

        today_new_users = UUUsers.objects.using('server').filter(create_time__date=today).count()
        three_days_new_users = UUUsers.objects.using('server').filter(create_time__date__gte=three_days_ago).count()
        one_week_new_users = UUUsers.objects.using('server').filter(create_time__date__gte=one_week_ago).count()
        one_month_new_users = UUUsers.objects.using('server').filter(create_time__date__gte=one_month_ago).count()

        ret_data = {
            'today_new_users': today_new_users,
            'three_days_new_users': three_days_new_users,
            'one_week_new_users': one_week_new_users,
            'one_month_new_users': one_month_new_users,
        }

        return {"new_user": ret_data}

    def count_new_guests(self):
        today = datetime.now().date()
        three_days_ago = today - timedelta(days=3)
        one_week_ago = today - timedelta(weeks=1)
        one_month_ago = today - timedelta(weeks=4)

        today_new_guests = UUUsersTemp.objects.using('server').filter(create_time__date=today).count()
        three_days_new_guests = UUUsersTemp.objects.using('server').filter(
            create_time__date__gte=three_days_ago).count()
        one_week_new_guests = UUUsersTemp.objects.using('server').filter(create_time__date__gte=one_week_ago).count()
        one_month_new_guests = UUUsersTemp.objects.using('server').filter(create_time__date__gte=one_month_ago).count()

        ret_data = {
            'today_new_guests': today_new_guests,
            'three_days_new_guests': three_days_new_guests,
            'one_week_new_guests': one_week_new_guests,
            'one_month_new_guests': one_month_new_guests,
        }

        return {"new_guest": ret_data}

    def count_guest_conversion(self):
        today = datetime.now().date()
        today_guests = UUUsersTemp.objects.using('server').filter(create_time__date=today)
        today_guests_count = today_guests.count()
        today_guests_registered = UUUsers.objects.using('server').filter(user_code__in=today_guests.values('user_code')).count()

        # 当日游客注册转化率
        conversion_percentage_today = (
                                              today_guests_registered / today_guests_count
                                      ) * 100 if today_guests_count > 0 else 0
        conversion_percentage_today = round(conversion_percentage_today, 2)

        # 三日游客注册转化率
        three_days_ago = today - timedelta(days=3)
        three_days_guests = UUUsersTemp.objects.using('server').filter(create_time__date__gte=three_days_ago)
        three_days_guests_count = three_days_guests.count()
        three_days_guests_registered = UUUsers.objects.using('server').filter(
            user_code__in=three_days_guests.values('user_code')
        ).count()
        conversion_percentage_three_days = (
                                                   three_days_guests_registered / three_days_guests_count
                                           ) * 100 if three_days_guests_count > 0 else 0
        conversion_percentage_three_days = round(conversion_percentage_three_days, 2)

        # 一周游客注册转化率
        one_week_ago = today - timedelta(weeks=1)
        one_week_guests = UUUsersTemp.objects.using('server').filter(create_time__date__gte=one_week_ago)
        one_week_guests_count = one_week_guests.count()
        one_week_guests_registered = UUUsers.objects.using('server').filter(
            user_code__in=one_week_guests.values('user_code')
        ).count()
        conversion_percentage_one_week = (
                                                 one_week_guests_registered / one_week_guests_count
                                         ) * 100 if one_week_guests_count > 0 else 0
        conversion_percentage_one_week = round(conversion_percentage_one_week, 2)

        # 一月游客注册转化率
        one_month_ago = today - timedelta(weeks=4)
        one_month_guests = UUUsersTemp.objects.using('server').filter(create_time__date__gte=one_month_ago)
        one_month_guests_count = one_month_guests.count()
        one_month_guests_registered = UUUsers.objects.using('server').filter(
            user_code__in=one_month_guests.values('user_code')
        ).count()
        conversion_percentage_one_month = (
                                                  one_month_guests_registered / one_month_guests_count
                                          ) * 100 if one_month_guests_count > 0 else 0
        conversion_percentage_one_month = round(conversion_percentage_one_month, 2)

        ret_data = {
            'guest_conversion_percentage_today': conversion_percentage_today,
            'guest_conversion_percentage_three_days': conversion_percentage_three_days,
            'guest_conversion_percentage_one_week': conversion_percentage_one_week,
            'guest_conversion_percentage_one_month': conversion_percentage_one_month,
        }
        return {"conversion_rate": ret_data}


    def count_pay_conversion(self):
        today = datetime.now().date()
        three_days_ago = today - timedelta(days=3)
        one_week_ago = today - timedelta(weeks=1)
        one_month_ago = today - timedelta(weeks=4)

        # 当日注册用户付费率
        today_registered_users = UUUsers.objects.using('server').filter(create_time__date=today)
        today_registered_users_count = today_registered_users.count()
        today_registered_users_paid = PpPayments.objects.using('server').filter(
            user_id__in=today_registered_users.values_list('user_code', flat=True), status=1
        ).aggregate(count=Count('user_id', distinct=True))['count']
        pay_conversion_percentage_today = (
                                                      today_registered_users_paid / today_registered_users_count) * 100 if today_registered_users_count > 0 else 0
        pay_conversion_percentage_today = round(pay_conversion_percentage_today, 2)

        # 三日注册用户付费率
        three_days_registered_users = UUUsers.objects.using('server').filter(create_time__date__gte=three_days_ago)
        three_days_registered_users_count = three_days_registered_users.count()
        three_days_registered_users_paid = PpPayments.objects.using('server').filter(
            user_id__in=three_days_registered_users.values_list('user_code', flat=True), status=1
        ).aggregate(count=Count('user_id', distinct=True))['count']
        pay_conversion_percentage_three_days = (
                                                           three_days_registered_users_paid / three_days_registered_users_count) * 100 if three_days_registered_users_count > 0 else 0
        pay_conversion_percentage_three_days = round(pay_conversion_percentage_three_days, 2)

        # 一周注册用户付费率
        one_week_registered_users = UUUsers.objects.using('server').filter(create_time__date__gte=one_week_ago)
        one_week_registered_users_count = one_week_registered_users.count()
        one_week_registered_users_paid = PpPayments.objects.using('server').filter(
            user_id__in=one_week_registered_users.values_list('user_code', flat=True), status=1
        ).aggregate(count=Count('user_id', distinct=True))['count']
        pay_conversion_percentage_one_week = (
                                                         one_week_registered_users_paid / one_week_registered_users_count) * 100 if one_week_registered_users_count > 0 else 0
        pay_conversion_percentage_one_week = round(pay_conversion_percentage_one_week, 2)

        # 一月注册用户付费率
        one_month_registered_users = UUUsers.objects.using('server').filter(create_time__date__gte=one_month_ago)
        one_month_registered_users_count = one_month_registered_users.count()
        one_month_registered_users_paid = PpPayments.objects.using('server').filter(
            user_id__in=one_month_registered_users.values_list('user_code', flat=True), status=1
        ).aggregate(count=Count('user_id', distinct=True))['count']
        pay_conversion_percentage_one_month = (
                                                          one_month_registered_users_paid / one_month_registered_users_count) * 100 if one_month_registered_users_count > 0 else 0
        pay_conversion_percentage_one_month = round(pay_conversion_percentage_one_month, 2)

        ret_data = {
            'pay_conversion_percentage_today': pay_conversion_percentage_today,
            'pay_conversion_percentage_three_days': pay_conversion_percentage_three_days,
                                                  'pay_conversion_percentage_one_week': pay_conversion_percentage_one_week,
            'pay_conversion_percentage_one_month': pay_conversion_percentage_one_month,
        }
        return {"pay_conversion_rate": ret_data}

    def count_pay_users(self):
        today = datetime.now().date()
        three_days_ago = today - timedelta(days=3)
        one_week_ago = today - timedelta(weeks=1)
        one_month_ago = today - timedelta(weeks=4)

        # 当日付费用户数量
        today_paid_users = PpPayments.objects.using('server').filter(
            created_at__date=today, status=1
        ).aggregate(count=Count('user_id', distinct=True))['count']

        # 三日付费用户数量
        three_days_paid_users = PpPayments.objects.using('server').filter(
            created_at__date__gte=three_days_ago, status=1
        ).aggregate(count=Count('user_id', distinct=True))['count']

        # 一周付费用户数量
        one_week_paid_users = PpPayments.objects.using('server').filter(
            created_at__date__gte=one_week_ago, status=1
        ).aggregate(count=Count('user_id', distinct=True))['count']

        # 一月付费用户数量
        one_month_paid_users = PpPayments.objects.using('server').filter(
            created_at__date__gte=one_month_ago, status=1
        ).aggregate(count=Count('user_id', distinct=True))['count']

        ret_data = {
            'pay_users_today': today_paid_users,
            'pay_users_three_days': three_days_paid_users,
            'pay_users_one_week': one_week_paid_users,
            'pay_users_one_month': one_month_paid_users,
        }
        return {"pay_users": ret_data}


class LoginUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        用户登录趋势
        :param request:
        :return:
        """
        day = 30
        today = datetime.today()
        seven_days_ago = today - timedelta(days=day)
        users = UUUsers.objects.using('server').filter(login_time__gte=seven_days_ago).annotate(
            day=TruncDay('login_time')).values('day').annotate(count=Count('id')).order_by('-day')
        result = []
        data_dict = {ele.get('day').strftime('%Y-%m-%d'): ele.get('count') for ele in users}
        for i in range(day):
            date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            result.append({'day': date, 'count': data_dict[date] if date in data_dict else 0})
        result = sorted(result, key=lambda x: x['day'])
        return DetailResponse(data={"login_user": result})


class RegisteredUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        用户注册趋势
        :param request:
        :return:
        """
        today = datetime.today()
        seven_days_ago = today - timedelta(days=30)

        users = UUUsers.objects.using('server').filter(create_time__gte=seven_days_ago).annotate(day=TruncDay('create_time')).values(
            'day').annotate(count=Count('id'))

        result = []
        for i in range(30):
            date = today - timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            count = 0
            for user in users:
                user_day = user['day'].strftime('%Y-%m-%d')
                if user_day == date_str:
                    count += user['count']
            result.append({'day': date_str, 'count': count})

        result = sorted(result, key=lambda x: x['day'])
        return DetailResponse(data={"registered_user_list": result})


class UsersTotalView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        用户总数
        :param request:
        :return:
        """
        users_total = UUUsers.objects.using('server').all().count()
        return DetailResponse(data={"users_total": users_total})


class DatabaseTotalView(APIView):

    def get(self, request):
        """
        数据库统计数据
        :param request:
        :return:
        """
        results = []
        for each_db in connections:
            count = len(connections[each_db].introspection.table_names())
            database_type = connection.settings_dict['ENGINE']
            space = 0

            if 'mysql' in database_type:
                sql = "SELECT SUM(data_length + index_length) AS size FROM information_schema.TABLES WHERE table_schema = DATABASE()"
            elif 'postgres' in database_type or 'psqlextra' in database_type:
                sql = """SELECT SUM(pg_total_relation_size(quote_ident(schemaname) || '.' || quote_ident(tablename))) AS size FROM pg_tables WHERE schemaname = current_schema();"""
            elif 'oracle' in database_type:
                sql = "SELECT SUM(bytes) AS size FROM user_segments"
            elif 'microsoft' in database_type:
                sql = "SELECT SUM(size) * 8 AS size FROM sys.database_files"
            else:
                space = 0

            if sql:
                with connections[each_db].cursor() as cursor:
                    try:
                        cursor.execute(sql)
                        result = cursor.fetchone()
                        space = result[0]
                    except Exception as e:
                        print(e)
                        space = '无权限'

            results.append({
                'name': connections[each_db].settings_dict['NAME'],
                'count': count,
                'space': format_bytes(space or 0)
            })

        return DetailResponse(data={'databases': results})
