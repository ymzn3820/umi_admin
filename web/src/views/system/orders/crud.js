
export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      rowKey: 'order_id',
      rowId: 'id'
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
        title: '订单ID',
        key: 'order_id',
        search: {
          disabled: false
        },
        minWidth: 130,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: '请输入订单ID'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '用户ID',
        key: 'user_id',
        minWidth: 160,
        type: 'input',
        search: {
          disabled: false
        },
        form: {
          component: {
            placeholder: '请输入用户ID'
          },
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          editDisabled: false,
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '订单金额',
        key: 'total_amount',
        minWidth: 90,
        search: {
          disabled: false
        },
        type: 'input',
        form: {
          component: {
            placeholder: '请输入订单金额'
          },
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          editDisabled: false,
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '商品名',
        key: 'prod_id',
        minWidth: 90,
        search: {
          disabled: false
        },
        type: 'radio',
        dict: {
          data: vm.dictionary('production')
        },
        form: {
          component: {
            placeholder: '请输入商品ID'
          },
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          editDisabled: false,
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '数量',
        key: 'quantity',
        minWidth: 90,
        search: {
          disabled: true
        },
        type: 'input',
        form: {
          component: {
            placeholder: '请输入数量'
          },
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          editDisabled: false,
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '单价',
        key: 'price',
        minWidth: 90,
        search: {
          disabled: true
        },
        type: 'input',
        form: {
          component: {
            placeholder: '请输入单价'
          },
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          editDisabled: false,
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '订单状态',
        key: 'status',
        search: {
          disabled: false
        },
        minWidth: 70,
        type: 'select',
        dict: {
          data: vm.dictionary('order_status')
        },
        form: {
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            span: 12,
            pagination: true,
            props: { multiple: false }
          },
          helper: '请选择订单状态'
        }
      },
      {
        title: '是否删除',
        search: {
          disabled: false
        },
        key: 'is_delete',
        type: 'radio',
        width: 70,
        dict: {
          data: vm.dictionary('is_delete_number')
        },
        form: {
          disabled: true,
          value: false,
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            span: 12,
            value: false
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      },
      {
        title: '创建时间',
        key: 'created_at',
        width: 150,
        type: 'datetime',
        form: {
          disabled: true,
          component: {
            placeholder: ''
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      },
      {
        title: '更新时间',
        key: 'updated_at',
        width: 150,
        type: 'datetime',
        form: {
          disabled: true,
          component: {
            placeholder: ''
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      },
      {
        title: '开始时间',
        key: 'start_date',
        show: false,
        search: {
          disabled: false
        },
        width: 150,
        type: 'datetime',
        form: {
          disabled: true,
          component: {
            placeholder: '开始时间',
            'value-format': 'yyyy-MM-dd HH:mm:ss' // 添加这一行
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      },
      {
        title: '结束时间',
        key: 'end_date',
        show: false,
        search: {
          disabled: false
        },
        width: 150,
        type: 'datetime',
        form: {
          disabled: true,
          component: {
            placeholder: '结束时间',
            'value-format': 'yyyy-MM-dd HH:mm:ss' // 添加这一行
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      }
    ]
  }
}
