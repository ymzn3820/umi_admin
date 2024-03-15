export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      rowKey: 'customer_id',
      rowId: 'customer_id'
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
      defaultSpan: 12
    },
    indexRow: {
      title: '序号',
      align: 'center',
      width: 60
    },
    columns: [
      {
        title: '客户名称',
        key: 'customer_id',
        search: {
          disabled: false
        },
        minWidth: 130,
        type: 'select',
        dict: {
          label: 'company_name',
          value: 'customer_id',
          cache: false,
          url: '/api/system/customer_info_dict/'
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请输入客户ID'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '余额',
        key: 'balance',
        search: {
          disabled: true
        },
        type: 'input',
        form: {
          disabled: false,
          component: {
            placeholder: '请输入余额'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '创建时间',
        key: 'created_at',
        width: 150,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: ''
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      }
    ]
  }
}
