#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/7 19:18
# @Author  : payne
# @File    : occupation.py
# @Description :
from django.core.paginator import Paginator

from dvadmin.utils.json_response import DetailResponse, ErrorResponse

from dvadmin.system.models import UsersWithdrawalHistory
from django.db import connections
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class UsersBankCardWithdrawalView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order_no = request.query_params.get('order_no')
        card_number = request.query_params.get('card_number')
        bank_name = request.query_params.get('bank_name')
        mobile = request.query_params.get('mobile')
        w_status = request.query_params.get('w_status')
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)

        # construct the WHERE conditions based on provided query parameters
        where_conditions = "a.is_delete=0"
        if order_no:
            where_conditions += f" AND a.order_no = '{order_no}'"
        if card_number:
            where_conditions += f" AND b.card_number = '{card_number}'"
        if bank_name:
            where_conditions += f" AND b.bank_name = '{bank_name}'"
        if mobile:
            where_conditions += f" AND b.mobile = '{mobile}'"
        if w_status:
            where_conditions += f" AND a.w_status = '{w_status}'"

        with connections['server'].cursor() as cursor:
            cursor.execute(f"""
                SELECT COUNT(*) 
                FROM uw_users_withdrawal_history a 
                INNER JOIN ub_users_bank_card b ON a.card_code=b.card_code 
                WHERE {where_conditions}
            """)
            total_count = cursor.fetchone()[0]

            cursor.execute(f"""
                SELECT a.order_no, a.withdrawal_amount, a.user_code, a.account_amount, a.w_status, 
                b.name, b.card_number, b.bank, b.bank_name, b.mobile, 
                DATE_FORMAT(a.create_time, '%%Y-%%m-%%d %%H:%%i:%%s') as create_time 
                FROM uw_users_withdrawal_history a 
                INNER JOIN ub_users_bank_card b ON a.card_code=b.card_code 
                WHERE {where_conditions}
                ORDER BY a.create_time DESC
                LIMIT %s OFFSET %s
            """, [int(limit), (int(page) - 1) * int(limit)])

            result_list = []
            for row in cursor.fetchall():
                result_list.append(dict(zip([column[0] for column in cursor.description], row)))

        # Pagination
        paginator = Paginator(range(total_count), limit)
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

        data = {
            "data": result_list
        }
        data.update(paginator_data)

        return DetailResponse(data)

    def put(self, request):
        order_no = request.data.get('order_no')
        user_id = request.data.get('user_code')
        withdrawal_amount = request.data.get('withdrawal_amount')
        account_amount = request.data.get('account_amount')
        w_status = request.data.get('w_status')

        if not order_no:
            return ErrorResponse(msg="Missing order_no", status=400)

        set_clauses = []
        if withdrawal_amount is not None:
            set_clauses.append(f"withdrawal_amount = '{withdrawal_amount}'")
        if account_amount is not None:
            if int(w_status) == 3:
                set_clauses.append(f"account_amount = 0")
            else:
                set_clauses.append(f"account_amount = '{account_amount}'")
        if w_status is not None:
            set_clauses.append(f"w_status = '{w_status}'")

        if not set_clauses:
            return DetailResponse(msg="No fields to update", status=400)

        if int(w_status) == 3:
            sql_readd = f"""
                update uc_users_commission set  withdraw_balance = withdraw_balance + {withdrawal_amount}  where 
                user_code= {user_id}  
            """
            with connections['server'].cursor() as cursor:
                cursor.execute(sql_readd)
                if cursor.rowcount > 0:
                    readd = True
                else:
                    readd = False
        else:
            readd = True

        update_query = f"""
            UPDATE uw_users_withdrawal_history 
            SET {', '.join(set_clauses)}
            WHERE order_no = '{order_no}'
        """

        with connections['server'].cursor() as cursor:
            cursor.execute(update_query)
            if cursor.rowcount > 0:
                update_withdrawal_history = True
            else:
                update_withdrawal_history = False
        if readd and update_withdrawal_history:
            return DetailResponse(data={'order_no': order_no})
        else:
            return DetailResponse(msg=f'update fail,update_withdrawal_history is '
                                      f'{update_withdrawal_history},readd us {readd}', status=400)
