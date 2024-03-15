export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      rowKey: 'customer_id',
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
        title: '客户ID',
        key: 'customer_id',
        search: {
          disabled: true
        },
        minWidth: 130,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: '请输入客户ID'
          }
        }
      },
      {
        title: '公司名称',
        key: 'company_name',
        search: {
          disabled: false
        },
        minWidth: 200,
        type: 'input',
        form: {
          disabled: false,
          component: {
            placeholder: '请输入公司名称'
          }
        }
      },
      {
        title: '地址',
        key: 'address',
        search: {
          disabled: true
        },
        minWidth: 200,
        type: 'input',
        form: {
          disabled: false,
          component: {
            placeholder: '请输入地址'
          }
        }
      },
      {
        title: '账户',
        key: 'account',
        search: {
          disabled: true
        },
        minWidth: 130,
        type: 'input',
        form: {
          disabled: false,
          component: {
            placeholder: '请输入账户'
          }
        }
      },
      {
        title: '密码',
        key: 'password',
        search: {
          disabled: true
        },
        show: false,
        minWidth: 130,
        type: 'password',
        form: {
          disabled: true,
          component: {
            placeholder: '请输入密码'
          }
        }
      },
      {
        title: '联系人',
        key: 'contact_person',
        search: {
          disabled: false
        },
        minWidth: 130,
        type: 'input',
        form: {
          disabled: false,
          component: {
            placeholder: '请输入联系人'
          }
        }
      },
      {
        title: '联系电话',
        key: 'contact_number',
        search: {
          disabled: false
        },
        minWidth: 130,
        type: 'input',
        form: {
          disabled: false,
          component: {
            placeholder: '请输入联系电话'
          }
        }
      },
      {
        title: '状态',
        key: 'status',
        search: {
          disabled: false
        },
        minWidth: 130,
        type: 'select',
        dict: {
          data: vm.dictionary('customer_status')
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请输入状态'
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
        component: { props: { color: 'auto' } }
      },
      {
        title: '更新时间',
        key: 'updated_at',
        width: 150,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: ''
          }
        }
      }
    ]
  }
}
