export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      rowKey: 'order_no',
      rowId: 'order_no'
    },
    selectionRow: {
      align: 'center',
      width: 46
    },
    rowHandle: {
      width: 240,
      fixed: 'right',
      view: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
      edit: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Update')
        }
      },
      remove: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Delete')
        }
      }
    },
    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      defaultSpan: 12 // 默认的表单 span
    },
    indexRow: {
      title: '序号',
      align: 'center',
      width: 60
    },
    columns: [
      {
        title: '用户ID',
        key: 'user_code',
        search: {
          disabled: false
        },
        minWidth: 130,
        type: 'input'
      },
      {
        title: '订单号',
        key: 'order_no',
        search: {
          disabled: false
        },
        minWidth: 130,
        type: 'input'
      },
      {
        title: '提款金额',
        key: 'withdrawal_amount',
        minWidth: 90,
        type: 'input'
      },
      {
        title: '账户金额',
        key: 'account_amount',
        minWidth: 100,
        type: 'input'
      },
      {
        title: '状态',
        key: 'w_status',
        dict: {
          data: vm.dictionary('w_status')
        },
        search: {
          disabled: false
        },
        minWidth: 70,
        type: 'select'
      },
      {
        title: '银行卡代码',
        key: 'name',
        minWidth: 180,
        type: 'input'
      },
      {
        title: '银行卡号',
        key: 'card_number',
        minWidth: 110,
        search: {
          disabled: false
        },
        type: 'input'
      },
      {
        title: '银行',
        key: 'bank',
        minWidth: 100,
        type: 'input'
      },
      {
        title: '银行名',
        key: 'bank_name',
        minWidth: 150,
        search: {
          disabled: false
        },
        type: 'input'
      },
      {
        title: '手机号',
        key: 'mobile',
        width: 150,
        search: {
          disabled: false
        },
        type: 'input'
      },
      {
        title: '创建时间',
        key: 'create_time',
        width: 150,
        type: 'input'
      }
    ]
  }
}
