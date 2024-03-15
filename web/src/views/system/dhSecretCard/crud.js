export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      rowKey: 'key_id',
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
      search: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Search')
        }
      },
      remove: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Delete')
        }
      },
      custom: [{
        text: '分配',
        type: 'success',
        size: 'small',
        emit: 'AssignCustomer'
      }]
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
        title: 'ID',
        key: 'id',
        disabled: true,
        form: {
          disabled: true
        }
      },
      {
        title: '手机号',
        key: 'mobile',
        minWidth: 150,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: '请输入卡密'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '领取人',
        key: 'name',
        minWidth: 150,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: '请输入姓名'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '产品名称',
        key: 'product_type',
        minWidth: 130,
        type: 'select',
        dict: {
          data: vm.dictionary('dh_product_type')
        },
        form: {
          component: {
            placeholder: '请选择产品类型'
          },
          // rules: [
          //   {
          //     required: true,
          //     message: '必填项'
          //   }
          // ],
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '所属销售人员',
        key: 'seller_name',
        minWidth: 150,
        type: 'input',
        form: {
          disabled: false,
          editDisabled: true,
          value: '无',
          component: {
            span: 12,
            placeholder: '该项不需要录入',
            disabled: true // 禁用输入框

          },
          // rules: [
          //   {
          //     required: true,
          //     message: '必填项'
          //   }
          // ],
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '类型',
        key: 'account_type',
        minWidth: 100,
        type: 'select',
        // You might want to define the status options
        dict: {
          data: vm.dictionary('account_type')
        },
        form: {
          component: {
            placeholder: '请选择状态'
          },
          // disabled: true,
          // rules: [
          //   {
          //     required: true,
          //     message: '必填项'
          //   }
          // ],
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '状态',
        key: 'status',
        minWidth: 100,
        type: 'select',
        // You might want to define the status options
        dict: {
          data: [
            { label: '已使用', value: 1 }, // Example value
            { label: '未使用', value: 0 } // Example value
          ]
        },
        form: {
          component: {
            placeholder: '请选择状态'
          },
          // disabled: true,
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '账号',
        key: 'account',
        minWidth: 150,
        type: 'input',
        form: {
          component: {
            placeholder: '请输入账号'
          },
          // rules: [
          //   {
          //     required: true,
          //     message: '必填项'
          //   }
          // ],
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '密码',
        key: 'password',
        minWidth: 150,
        type: 'input',
        form: {
          component: {
            type: 'password',
            placeholder: '请输入密码'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '卡密',
        key: 'secrey_key',
        minWidth: 150,
        type: 'input',
        form: {
          component: {
            placeholder: '请输入卡密'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },

      {
        title: '领取时间',
        key: 'receive_time',
        minWidth: 150,
        type: 'datetime',
        form: {
          disabled: true,
          component: {
            type: 'datetime',
            placeholder: '请选择领取时间'
          },
          // rules: [
          //   {
          //     required: true,
          //     message: '必填项'
          //   }
          // ],
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '有效时间',
        key: 'valid_time',
        minWidth: 150,
        type: 'datetime',
        form: {
          // disabled: true,
          component: {
            type: 'datetime',
            placeholder: '请选择有效时间'
          },
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: 'Key ID',
        key: 'key_id',
        minWidth: 130,
        type: 'input-number',
        form: {
          disabled: true,
          component: {
            placeholder: '请输入产品ID'
          },
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '创建时间',
        key: 'create_time',
        minWidth: 150,
        type: 'datetime',
        form: {
          disabled: true,
          component: {
            type: 'datetime',
            placeholder: ''
          },
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          itemProps: {
            class: { yxtInput: true }
          }
        }
      }
    ]
  }
}
