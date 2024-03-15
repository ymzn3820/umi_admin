export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      rowKey: 'id',
      rowId: 'voice_id'
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
        title: '第三方唯一声音ID',
        key: 'voice_id',
        search: {
          disabled: false
        },
        minWidth: 140,
        form: {
          disabled: false,
          component: {
            placeholder: '请输入第三方唯一声音ID'
          }
        }
      },
      {
        title: '状态',
        key: 'voice_status',
        search: {
          disabled: false
        },
        minWidth: 100,
        type: 'radio',
        dict: {
          data: vm.dictionary('voice_clone')
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请选择状态'
          }
        }
      },
      {
        title: '使用者代码',
        key: 'user_code',
        search: {
          disabled: false
        },
        minWidth: 140,
        form: {
          disabled: true,
          component: {
            placeholder: '请输入使用者代码'
          }
        }
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
        }
      },
      {
        title: '更新时间',
        key: 'modify_time',
        width: 150,
        type: 'datetime',
        form: {
          disabled: true,
          component: {
            placeholder: ''
          }
        }
      },
      {
        title: '是否删除',
        key: 'is_delete',
        search: {
          disabled: false
        },
        width: 100,
        type: 'radio',
        dict: {
          data: vm.dictionary('is_delete')
        },
        form: {
          disabled: true,
          component: {
            placeholder: ''
          }
        }
      }
      // 根据需要可以添加更多列
    ]
  }
}
