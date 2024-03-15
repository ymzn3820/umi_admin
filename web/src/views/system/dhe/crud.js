
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
        title: '用户名',
        key: 'user_name',
        search: {
          disabled: false
        },
        minWidth: 130,
        type: 'input',
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
        title: '联系电话',
        key: 'mobile',
        minWidth: 90,
        type: 'input',
        search: {
          disabled: false
        },
        form: {
          editDisabled: false,
          component: {
            placeholder: '请输入联系人电话'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
        // disabled: true
      },
      {
        title: '创建人',
        key: 'create_by',
        // sortable: 'custom',
        minWidth: 100,
        search: {
          disabled: false
        },
        type: 'input',
        form: {
          component: {
            span: 12,
            placeholder: '请输入创建人'
          },
          itemProps: {
            class: { yxtInput: true }
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
        title: '留言时间',
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
      }
    ]
  }
}
