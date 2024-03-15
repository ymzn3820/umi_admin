import { request } from '@/api/service'

export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      rowKey: 'question_id',
      rowId: 'question_id'
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
        title: '用户ID',
        key: 'user_id',
        width: 100,
        type: 'input',
        search: {
          disabled: false
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请输入用户ID'
          },
          rules: [
            {
              required: false,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '问题集ID',
        key: 'question_id',
        width: 130,
        type: 'select',
        dict: {
          url: '/api/system/info_question_user_detail_dict/',
          getData (url, dict, data) { // 请求拦截器，对请求数据进行处理
            return request({
              url: '/api/system/info_question_user_detail_dict/',
              method: 'get'
            }).then(ret => {
              const data = []

              ret.data.data.forEach(item => {
                const obj = {}
                if (item.assistant_title.trim() !== '') { // 判断assistant_title是否为空
                  obj.label = item.assistant_title
                  obj.value = item.question_id
                } else {
                  obj.label = item.character_name
                  obj.value = item.question_id
                }
                data.push(obj)
              })
              return data
            })
          },
          // value: 'question_id',
          cache: false
        },
        search: {
          disabled: false
        },
        form: {
          component: {
            placeholder: '请选择问题集',
            props: {
              clearable: true,
              filterable: true // 可过滤选择项
            }
          },
          rules: [
            {
              required: false,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '附加问题ID',
        key: 'question_add_ids',
        width: 100,
        type: 'select',
        dict: {
          url: '/api/system/info_question_user_dict/',
          label: 'title',
          value: 'question_add_id',
          cache: false
        },
        search: {
          disabled: true
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请输入附加问题ID'
          },
          rules: [
            {
              required: false,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '行业',
        key: 'industry_id',
        type: 'select',
        dict: {
          url: '/api/system/industry_dict/',
          label: 'name',
          value: 'industry_id',
          cache: false
        },
        search: {
          disabled: true
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请输入行业ID'
          },
          rules: [
            {
              required: false,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '模块',
        key: 'module_id',
        type: 'select',
        dict: {
          url: '/api/system/modules_dict/',
          label: 'name',
          value: 'module_id',
          cache: false
        },
        search: {
          disabled: true
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请输入模块ID'
          },
          rules: [
            {
              required: false,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '职业',
        key: 'occu_id',
        type: 'select',
        dict: {
          url: '/api/system/occupation_dict/',
          label: 'name',
          value: 'occu_id',
          cache: false
        },
        search: {
          disabled: true
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请输入职业ID'
          },
          rules: [
            {
              required: false,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '次要职业',
        key: 'sec_occu_id',
        type: 'select',
        dict: {
          url: '/api/system/sec_occupation_dict/',
          label: 'name',
          value: 'sub_occu_id',
          cache: false
        },
        search: {
          disabled: true
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请输入次要职业ID'
          },
          rules: [
            {
              required: false,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '职业持续时间',
        key: 'occu_duration_id',
        width: 100,
        type: 'select',
        dict: {
          url: '/api/system/duration_dict/',
          label: 'name',
          value: 'occu_duration_id',
          cache: false
        },
        search: {
          disabled: true
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请输入职业持续时间'
          },
          rules: [
            {
              required: false,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '专业水平',
        key: 'expertise_level_id',
        type: 'select',
        dict: {
          url: '/api/system/expertise_level_dict/',
          label: 'name',
          value: 'expertise_level_id',
          cache: false
        },
        search: {
          disabled: true
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请输入专业水平'
          },
          rules: [
            {
              required: false,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '角色头像',
        key: 'character_avatar',
        type: 'input',
        rowSlot: true
      },
      {
        title: '角色名字',
        key: 'character_name',
        type: 'input',
        search: {
          disabled: true
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请输入角色名字'
          },
          rules: [
            {
              required: false,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '角色问候语',
        key: 'character_greetings',
        type: 'input',
        width: 100,
        search: {
          disabled: true
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请输入角色问候语'
          },
          rules: [
            {
              required: false,
              message: '必填项'
            }
          ]
        },
        component: {
          render (h, params) {
            const content = params.row.character_greetings.length > 30 ? params.row.character_greetings.substring(0, 30) + '...' : params.row.character_greetings
            return h('el-tooltip', {
              props: {
                content: params.row.character_greetings,
                placement: 'top'
              }
            }, [
              h('span', {}, content)
            ])
          }
        }
      },
      {
        title: '是否公开',
        key: 'is_public',
        type: 'select',
        dict: {
          data: vm.dictionary('is_public')
        },
        search: {
          disabled: true
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请选择是否公开'
          },
          rules: [
            {
              required: false,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '隐性提示词',
        key: 'hint',
        width: 100,
        type: 'input',
        search: {
          disabled: true
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请输入角色提示'
          },
          rules: [
            {
              required: false,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '示例提问',
        key: 'example_question',
        width: 100,
        type: 'input',
        search: {
          disabled: true
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请输入角色提示'
          },
          rules: [
            {
              required: false,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '角色描述',
        key: 'character_desc',
        type: 'input',
        search: {
          disabled: true
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请输入角色描述'
          },
          rules: [
            {
              required: false,
              message: '必填项'
            }
          ]
        },
        component: {
          render (h, params) {
            const content = params.row.character_desc.length > 30 ? params.row.character_desc.substring(0, 30) + '...' : params.row.character_desc
            return h('el-tooltip', {
              props: {
                content: params.row.character_desc,
                placement: 'top'
              }
            }, [
              h('span', {}, content)
            ])
          }
        }
      },
      {
        title: '角色成就',
        key: 'character_achievements',
        type: 'input',
        search: {
          disabled: true
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请输入角色成就'
          },
          rules: [
            {
              required: false,
              message: '必填项'
            }
          ]
        },
        component: {
          render (h, params) {
            const content = params.row.character_achievements.length > 30 ? params.row.character_achievements.substring(0, 30) + '...' : params.row.character_achievements
            return h('el-tooltip', {
              props: {
                content: params.row.character_achievements,
                placement: 'top'
              }
            }, [
              h('span', {}, content)
            ])
          }
        }
      },
      {
        title: '助手标题',
        key: 'assistant_title',
        type: 'input',
        search: {
          disabled: true
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请输入助手标题'
          },
          rules: [
            {
              required: false,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '助手内容',
        key: 'assistant_content',
        width: 130,
        type: 'input',
        search: {
          disabled: true
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请输入助手内容'
          },
          rules: [
            {
              required: false,
              message: '必填项'
            }
          ]
        },
        component: {
          render (h, params) {
            const content = params.row.assistant_content.length > 30 ? params.row.assistant_content.substring(0, 30) + '...' : params.row.assistant_content
            return h('el-tooltip', {
              props: {
                content: params.row.assistant_content,
                placement: 'top'
              }
            }, [
              h('span', {}, content)
            ])
          }
        }
      },
      {
        title: '相关文档',
        key: 'related_document',
        type: 'input',
        rowSlot: true
      },
      {
        title: '是否删除',
        key: 'is_delete',
        type: 'select',
        dict: {
          data: vm.dictionary('is_delete_number')
        },
        search: {
          disabled: false
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请选择是否删除'
          },
          rules: [
            {
              required: false,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '创建时间',
        key: 'created_at',
        width: 150,
        type: 'datetime',
        form: {
          disabled: true
        },
        component: {
          disabled: true
        }
      },
      {
        title: '更新时间',
        key: 'updated_at',
        width: 150,
        type: 'datetime',
        form: {
          disabled: true
        },
        component: {
          disabled: true
        }
      },
      {
        title: '是否后台请求',
        key: 'is_backend',
        width: 150,
        show: false,
        type: 'input',
        form: {
          itemProps: {
            class: { yxtInput: true }
          },
          editDisabled: true,
          value: 1,
          component: {
            span: 12,
            placeholder: '请输入上传者ID',
            disabled: true // 禁用输入框

          }
        },
        component: {
          disabled: true
        }
      },
      {
        title: '状态',
        key: 'status',
        type: 'select',
        dict: {
          data: vm.dictionary('model_review_status')
        },
        search: {
          disabled: true
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请输入状态'
          },
          rules: [
            {
              required: false,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '拒绝理由',
        key: 'refuse_reason',
        type: 'input',
        search: {
          disabled: true
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请输入拒绝理由'
          },
          rules: [
            {
              required: false,
              message: '必填项'
            }
          ]
        }
      }
    ]
  }
}
