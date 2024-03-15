import * as apiQuestion from '../questionSet/api'

export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      rowKey: 'field_id',
      rowId: 'id'
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
      defaultSpan: 12 // default form span
    },
    indexRow: {
      title: '序号',
      align: 'center',
      width: 60
    },
    columns: [
      {
        title: '问题',
        key: 'question_id',
        sortable: true,
        minWidth: 220,
        type: 'select',
        search: {
          disabled: false
        },
        dict: {
          label: 'title',
          value: 'question_id',
          cache: true,
          getData: (url, dict, { form, component }) => {
            return apiQuestion.GetList().then(ret => { return ret.data.question_maps })
          }
        },
        form: {
          rules: [
            { required: true, message: '问题ID必填项' }
          ],
          component: {
            span: 24,
            props: {
              elProps: {
                allowCreate: true,
                filterable: true,
                clearable: true
              }

            }
          }
        }
      },
      {
        title: '字段ID',
        key: 'field_id',
        search: {
          disabled: false
        },
        type: 'input',
        minWidth: 180,
        form: {
          disabled: true,
          value: false,
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            span: 12
          }
        }
      },
      {
        title: '字段名称',
        key: 'field_name',
        type: 'input',
        search: {
          disabled: false
        },
        minWidth: 80,
        form: {
          rules: [
            { required: true, message: '字段名称必填项' }
          ]
        }
      },
      {
        title: '内容',
        key: 'content',
        type: 'textarea',
        minWidth: 180,
        form: {
          rules: [
            { required: true, message: '内容必填项' }
          ],
          component: {
            placeholder: '',
            showWordLimit: true,
            // maxlength: '',
            props: {
              type: 'textarea'
            }
          }
        }
      },
      {
        title: '显示顺序',
        key: 'show_order',
        type: 'number',
        minWidth: 90,
        form: {
          value: 0
        }
      },
      {
        title: '是否隐藏',
        key: 'is_hidden',
        width: 90,
        type: 'radio',
        search: {
          disabled: false
        },
        minWidth: 50,
        dict: {
          data: vm.dictionary('is_delete')
        },
        form: {
          value: false
        }
      },
      {
        title: '是否删除',
        key: 'is_delete',
        search: {
          disabled: false
        },
        width: 90,
        type: 'radio',
        dict: {
          data: vm.dictionary('is_delete')
        },
        form: {
          disabled: true,
          component: {
            placeholder: ''
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      },
      {
        title: '创建时间',
        key: 'created_at',
        sortable: true,
        minWidth: 160,
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
        minWidth: 160,
        key: 'updated_at',
        sortable: true,
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
