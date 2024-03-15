import { request } from '@/api/service'

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
      defaultSpan: 12 // default form span
    },
    indexRow: {
      title: '序号',
      align: 'center',
      width: 60
    },
    columns: [
      {
        title: '模块名称',
        key: 'module_name',
        type: 'input',
        form: {
          disabled: true,
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '问题ID',
        key: 'question_id',
        show: false,
        type: 'input',
        search: {
          disabled: false
        },
        form: {
          disabled: true,
          component: {
            placeholder: '请输入问题ID'
          },
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '问题内容',
        key: 'question_title',
        minWidth: 90,
        type: 'textarea',
        form: {
          disabled: true,
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ]
        },
        component: {
          render (h, params) {
            const content = params.row.question_title.length > 30 ? params.row.question_title.substring(0, 30) + '...' : params.row.question_title
            return h('el-tooltip', {
              props: {
                content: params.row.question_title,
                placement: 'top'
              }
            }, [
              h('span', {}, content)
            ])
          }
        }
      },
      {
        title: '问题答案',
        key: 'question_answer',
        minWidth: 90,
        type: 'textarea',
        form: {
          disabled: true,
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ]
        },
        component: {
          render (h, params) {
            const content = params.row.question_answer.length > 30 ? params.row.question_answer.substring(0, 30) + '...' : params.row.question_answer
            return h('el-tooltip', {
              props: {
                content: params.row.question_answer,
                placement: 'top'
              }
            }, [
              h('span', {}, content)
            ])
          }
        }
      },
      {
        title: '分享者昵称',
        key: 'created_by',
        type: 'input',
        search: {
          disabled: true
        },
        form: {
          component: {
            placeholder: '请输入分享者'
          },
          disabled: true,
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '分享者ID',
        key: 'user_id',
        type: 'input',
        show: false,
        search: {
          disabled: true
        },
        form: {
          component: {
            placeholder: '请输入分享者'
          },
          disabled: true,
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '会话ID',
        key: 'session_code',
        show: false,
        type: 'input',
        search: {
          disabled: true
        },
        form: {
          component: {
            placeholder: '请输入会话ID'
          },
          disabled: true,
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '状态',
        key: 's_status',
        type: 'select',
        search: {
          disabled: false
        },
        dict: {
          data: vm.dictionary('question_square')
        },
        form: {
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '创建时间',
        key: 'create_time',
        type: 'datetime',
        width: 150,
        form: {
          disabled: true,
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '修改时间',
        key: 'modify_time',
        type: 'datetime',
        width: 150,
        form: {
          disabled: true,
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '是否删除',
        key: 'is_delete',
        type: 'select',
        search: {
          disabled: false
        },
        dict: {
          data: vm.dictionary('button_whether_bool')
        },
        form: {
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ]
        }
      }
    ]
  }
}
