import { request } from '@/api/service'

export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      // tableType: 'vxe-table',
      rowKey: 'activate_code_id', // 必须设置，true or false
      rowId: 'id',
      height: '100%', // 表格高度100%, 使用toolbar必须设置
      highlightCurrentRow: false
    },
    selectionRow: {
      align: 'center',
      width: 46
    },
    rowHandle: {
      fixed: 'right',
      view: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
      width: 70,
      edit: {
        thin: true,
        text: '',
        show: false,
        disabled () {
          return !vm.hasPermissions('Update')
        }
      },
      remove: {
        thin: true,
        text: '删除',
        show: false,
        disabled () {
          return !vm.hasPermissions('Delete')
        }
      },
      batchRemove: { // 添加这个配置项，开启批量删除
        thin: true,
        text: '批量删除',
        type: 'danger',
        show: () => {
          return vm.hasPermissions('BatchDelete') // 根据你的权限设置决定是否显示
        }
      }
    },
    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      disabled: false,
      labelWidth: '120',
      saveRemind: true,
      defaultSpan: 12 // 默认的表单 span
    },
    indexRow: { // 或者直接传true,不显示title，不居中
      title: '序号',
      align: 'center',
      width: 70
    },
    columns: [
      {
        title: '创建人ID',
        key: 'generated_by',
        show: false,
        disabled: false,
        width: 90,
        type: 'select',
        dict: {
          data: vm.dictionary('admin_user')
        },
        search: {
          disabled: true
        },
        form: {
          itemProps: {
            class: { yxtInput: true }
          },
          editDisabled: true,
          value: vm.$store.state.d2admin.user.info.id,
          component: {
            span: 12,
            disabled: true // 禁用输入框

          }
        }
      },
      {
        title: '创建人',
        key: 'generated_name',
        show: true,
        disabled: false,
        width: 90,
        type: 'input',
        search: {
          disabled: false
        },
        form: {
          disabled: true,
          itemProps: {
            class: { yxtInput: true }
          },
          editDisabled: true,
          value: vm.$store.state.d2admin.user.info.id,
          component: {
            span: 12,
            disabled: true, // 禁用输入框
            placeholder: '请输入创建人'
          }
        }
      },
      {
        title: '产品类别',
        key: 'code_type',
        show: false,
        minWidth: 90,
        type: 'select',
        dict: {
          data: vm.dictionary('prod')
        },
        search: {
          disabled: false
        },
        form: {
          component: {
            placeholder: '请选择产品类别',
            props: { color: 'auto' }
          },
          rules: [
            {
              required: true,
              message: '必填项'
            }],
          itemProps: {
            class: { yxtInput: true }
          },
          valueChange (key, value, form, { getColumn, mode, component, immediate, getComponent }) {
            form.prod_cate_id = value
            if (value) {
              getComponent('to_prod_id').reloadDict()
            }
          }
        }
      }, {
        title: '产品名',
        key: 'to_prod_id',
        search: {
          disabled: false
        },
        show: false,
        minWidth: 130,
        type: 'select',
        dict: {
          label: 'prod_name',
          value: 'prod_id',
          cache: false,
          url: '/api/system/product/',
          getData: (url, dict, { form, component }) => {
            return request({ url: url, params: { prod_cate_id: form.prod_cate_id, is_show: 1, is_delete: 0, page: 1, limit: 1000 } }).then(ret => {
              const data = []
              // if ('emp_duration_id' in vm.crud.keys && vm.crud.keys.emp_duration_id !== undefined) {
              //   vm.crud.keys.emp_duration_id += ',' + form.emp_duration_id
              // } else {
              //   vm.crud.keys.emp_duration_id = form.emp_duration_id
              // }
              for (const item of ret.data.data) {
                const obj = {}
                obj.prod_id = item.prod_id
                obj.prod_name = item.prod_name
                data.push(obj)
              }
              return data
            })
          }
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请选择产品'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '激活码id',
        key: 'activate_code_id',
        width: 90,
        disabled: true,
        form: {
          disabled: true
        }
      },
      {
        title: '激活码',
        key: 'activate_code',
        search: {
          disabled: false
        },
        width: 200,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: '请输入激活码名称'
          }
        }
      }, {
        title: '描述',
        key: 'desc',
        search: {
          disabled: false
        },
        width: 200,
        type: 'input',
        form: {
          disabled: false,
          component: {
            placeholder: '描述'
          }
        }
      },
      {
        title: '对应产品',
        key: 'to_prod_id',
        width: 80,
        type: 'radio',
        dict: {
          data: vm.dictionary('production')
        },
        search: {
          disabled: false
        },
        form: {
          disabled: true,
          component: {
            placeholder: '请输入产品名'
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      },
      {
        title: '使用者',
        key: 'consumed_by',
        search: {
          disabled: true
        },
        width: 100,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: '请输入使用者名称'
          }
        }
      }, {
        title: '创建时间',
        key: 'created_at',
        width: 150,
        type: 'input',
        form: {
          editDisabled: true,
          disabled: true,
          component: {
            placeholder: ''
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      }, {
        title: '过期时间',
        key: 'expired_date',
        width: 150,
        type: 'datetime',
        form: {
          component: {
            placeholder: ''
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      }, {
        title: '激活时间',
        key: 'updated_at',
        width: 150,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: ''
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      }, {
        title: '状态',
        fixed: 'right',
        key: 'status',
        width: 80,
        type: 'radio',
        dict: {
          data: vm.dictionary('code_status')
        },
        search: {
          disabled: false
        },
        form: {
          editDisabled: true,
          disabled: true,
          component: {
            placeholder: '请选择状态'
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      }, {
        title: '生成数量',
        key: 'generate_quantity',
        disabled: true,
        width: 80,
        type: 'number',
        search: {
          disabled: true
        },
        form: {
          disabled: false,
          component: {
            placeholder: '0'
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      }
    ]
  }
}
