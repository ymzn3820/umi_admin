
export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      rowKey: 'info_id',
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
        title: '用户ID',
        key: 'user_id',
        type: 'input',
        search: {
          disabled: false
        },
        form: {
          disabled: true,
          component: {
            placeholder: '请输入用户ID'
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
        title: '问题集',
        key: 'question_id',
        width: 130,
        type: 'select',
        dict: {
          url: '/api/system/info_question_user_detail_dict/',
          label: 'assistant_title',
          value: 'question_id',
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
              required: true,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '附加问题',
        key: 'question_add_id',
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
              required: true,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '标题',
        key: 'title',
        width: 130,
        type: 'input',
        search: {
          disabled: false
        },
        form: {
          component: {
            placeholder: '请输入标题',
            props: {
              clearable: true
            }
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
        title: '附加类型名称',
        key: 'info_type_id',
        type: 'select',
        width: 130,
        dict: {
          label: 'info_type_name',
          value: 'info_type_id',
          cache: false,
          url: '/api/system/info_type_dict/'
        },
        search: {
          disabled: false
        },
        form: {
          component: {
            props: {
              clearable: true,
              filterable: true // 可过滤选择项
            },
            placeholder: '请选择附加类型名称'
          },
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          valueChange (key, value, form, { getColumn, mode, component, immediate, getComponent }) {
            form.occu_id = value // 将“city”的值置空
            // form.county = undefined// 将“county”的值置空
            if (value) {
              getComponent('option_ids').reloadDict() // 执行city的select组件的reloadDict()方法，触发“city”重新加载字典
            }
          }
        }
      },
      {
        title: '附加类型内容',
        key: 'option_ids',
        type: 'select',
        width: 150,
        dict: {
          label: 'option_value',
          value: 'option_id',
          cache: false,
          url: 'api/system/info_option_user_dict/'
        },
        search: {
          disabled: false
        },
        form: {
          component: {
            placeholder: '请选择附加类型内容',
            props: {
              clearable: true,
              filterable: true, // 可过滤选择项
              multiple: true
            }
          },
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          helper: {
            render (h) {
              return (< el-alert title="Input类型选择内容关键字" type="warning" />
              )
            }
          }
        }
      },
      {
        title: '占位符',
        key: 'placeholder',
        type: 'input',
        width: 170,
        search: {
          disabled: false
        },
        form: {
          component: {
            placeholder: '请输入附加问题内容'
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
        title: '是否必填项',
        width: 90,
        key: 'is_required',
        type: 'select',
        dict: {
          data: vm.dictionary('is_required')
        },
        search: {
          disabled: true
        },
        form: {
          component: {
            placeholder: '请选择是否必填'
          },
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          helper: {
            render (h) {
              return (< el-alert title="页面该项是否带*" type="warning" />
              )
            }
          }
        }
      },
      {
        title: '是否删除',
        key: 'is_delete',
        type: 'select',
        dict: {
          data: vm.dictionary('button_whether_bool')
        },
        search: {
          disabled: false
        },
        form: {
          disabled: true,
          component: {
            placeholder: '请选择是否删除'
          },
          value: false,
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
      }
    ]
  }
}
