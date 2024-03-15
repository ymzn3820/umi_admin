
export const crudOptions = (vm) => {
  // util.filterParams(vm, ['dept_name', 'role_info{name}', 'dept_name_all'])
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      // tableType: 'vxe-table',
      rowKey: 'id',
      rowId: 'user_code'
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
        text: ''
        // disabled () {
        //   return !vm.hasPermissions('Update')
        // }
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
    indexRow: { // 或者直接传true,不显示title，不居中
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
        disabled: false,
        minWidth: 140,
        form: {
          disabled: true,
          component: {
            placeholder: '请输入ID'
          }
        }
      },
      {
        title: '手机',
        key: 'mobile',
        search: {
          disabled: false
        },
        minWidth: 130,
        type: 'input',
        form: {
          // disabled: true,
          component: {
            placeholder: '请输入手机'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '用户名',
        key: 'user_name',
        minWidth: 90,
        type: 'input',
        search: {
          disabled: false
        },
        form: {
          editDisabled: false,
          component: {
            placeholder: '请输入用户名'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
        // disabled: true
      },
      {
        title: '用户昵称',
        key: 'nick_name',
        // sortable: 'custom',
        minWidth: 100,
        search: {
          disabled: false
        },
        type: 'input',
        form: {
          component: {
            span: 12,
            placeholder: '请输入用户昵称'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '来源',
        key: 'source',
        search: {
          disabled: true
        },
        minWidth: 70,
        form: {
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            span: 12,
            pagination: true,
            props: { multiple: false }
          }
        }
      },
      {
        title: '头像地址',
        key: 'avatar_url',
        search: {
          disabled: true
        },
        minWidth: 180,
        form: {
          value: '',
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            span: 24
          }
        }
      },
      {
        title: '微信统一ID',
        key: 'wx_union_id',
        search: {
          disabled: false
        },
        minWidth: 110,
        type: 'input',
        form: {
          disabled: true,
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            placeholder: '请输入微信统一ID',
            clearable: true

          }
        }
      }, {
        title: '用户状态',
        search: {
          disabled: false
        },
        key: 'user_status',
        minWidth: 100,
        type: 'radio',
        dict: {
          data: vm.dictionary('user_status')
        },
        form: {
          disabled: false,
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            span: 12,
            placeholder: '请选择状态'

          }
        }
      },
      {
        title: '最近登陆时间',
        key: 'login_time',
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
        title: '头像ID',
        key: 'avatar_id',
        width: 150,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: ''
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      },
      {
        title: '数据库状态',
        key: 'is_delete',
        search: {
          disabled: false
        },
        width: 150,
        type: 'select',
        dict: {
          data: vm.dictionary('is_delete')
        },
        form: {
          disabled: true,
          component: {
            value: '正常',
            placeholder: ''
          }
        }
        // component: { props: { color: 'auto' } } // 自动染色
      },
      {
        title: '创建时间',
        key: 'create_time',
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
        title: '修改时间',
        key: 'modify_time',
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
        title: '登陆IP',
        key: 'login_ip',
        width: 150,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: '请输入登陆IP'
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      },
      {
        title: '注册来源',
        key: 'source_url',
        width: 150,
        type: 'input',
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
