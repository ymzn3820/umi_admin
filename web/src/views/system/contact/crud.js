
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
    indexRow: { // 或者直接传true,不显示title，不居中
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
        title: '类型',
        key: 'type',
        search: {
          disabled: false
        },
        minWidth: 130,
        type: 'radio',
        dict: {
          data: vm.dictionary('contact_type')
        },
        form: {
          // disabled: true,
          component: {
            placeholder: '请选择类型'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '联系人',
        key: 'name',
        minWidth: 90,
        type: 'input',
        search: {
          disabled: false
        },
        form: {
          editDisabled: false,
          component: {
            placeholder: '请输入联系人名称'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
        // disabled: true
      },
      {
        title: '电话',
        key: 'phone',
        // sortable: 'custom',
        minWidth: 100,
        search: {
          disabled: false
        },
        type: 'input',
        form: {
          component: {
            span: 12,
            placeholder: '请输入联系电话'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '来源',
        key: 'referer',
        // sortable: 'custom',
        minWidth: 100,
        search: {
          disabled: false
        },
        type: 'input',
        form: {
          disabled: true,
          component: {
            span: 12,
            placeholder: '请输入来源'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '详情',
        key: 'cooperation_details',
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
        title: '邮件地址',
        key: 'email',
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
        title: '公司名称',
        key: 'company',
        search: {
          disabled: false
        },
        minWidth: 110,
        type: 'input',
        form: {
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            placeholder: '请输入公司名称',
            clearable: true

          }
        }
      }, {
        title: '职位',
        key: 'position',
        search: {
          disabled: false
        },
        minWidth: 110,
        type: 'input',
        form: {
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            placeholder: '请输入职位',
            clearable: true

          }
        }
      },
      {
        title: '状态',
        search: {
          disabled: false
        },
        key: 'status',
        minWidth: 100,
        type: 'radio',
        dict: {
          data: vm.dictionary('contact_status')
        },
        form: {
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
        title: '数据库状态',
        key: 'is_delete',
        search: {
          disabled: false
        },
        width: 150,
        type: 'radio',
        dict: {
          data: vm.dictionary('is_delete_number')
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
        title: '留言时间',
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
      }
    ]
  }
}
