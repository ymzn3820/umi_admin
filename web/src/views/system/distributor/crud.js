export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      rowKey: 'id',
      rowId: 'id'
    },
    selectionRow: {
      align: 'center',
      width: 46
    },
    rowHandle: {
      width: 180,
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
        width: 90,
        form: {
          disabled: true
        }
      },
      {
        title: '分销等级',
        key: 'd_level',
        type: 'radio',
        dict: {
          data: vm.dictionary('distributor_level')
        },
        form: {
          rules: [
            {
              required: true,
              message: '请输入分销等级'
            }
          ],
          component: {
            placeholder: '请输入分销等级'
          }
        }
      },
      {
        title: '佣金比例',
        key: 'commission_rate',
        type: 'number',
        form: {
          rules: [
            {
              required: true,
              message: '请输入佣金比例'
            }
          ],
          component: {
            placeholder: '请输入佣金比例'
          }
        }
      },
      {
        title: '等级描述',
        key: 'desc',
        type: 'input',
        form: {
          component: {
            placeholder: '请输入等级描述'
          }
        }
      },
      {
        title: '创建人',
        key: 'create_by',
        type: 'input',
        form: {
          component: {
            placeholder: '请输入创建人姓名'
          }
        }
      },
      {
        title: '创建日期',
        key: 'create_time',
        type: 'datetime',
        form: {
          disabled: true
        }
      },
      {
        title: '最近修改日期',
        key: 'modify_time',
        type: 'datetime',
        form: {
          disabled: true
        }
      },
      {
        title: '是否删除',
        key: 'is_delete',
        type: 'radio',
        dict: {
          data: [{ value: true, label: '是' }, { value: false, label: '否' }]
        },
        form: {
          component: {
            span: 12
          }
        }
      }
    ]
  }
}
