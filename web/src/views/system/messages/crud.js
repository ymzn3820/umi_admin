export const crudOptions = (vm) => {
  return {
    indexRow: {
      width: 60,
      title: '序号',
      align: 'center'
    },
    options: {
      tableType: 'vxe-table',
      rowKey: true,
      height: '100%'
    },
    rowHandle: {
      width: 160,
      fixed: 'right',
      view: {
        thin: true,
        text: '',
        show: true,
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
      edit: {
        thin: true,
        text: '',
        show: true,
        disabled () {
          return !vm.hasPermissions('Update')
        }
      },
      remove: {
        thin: true,
        text: '',
        show: true,
        disabled () {
          return !vm.hasPermissions('Delete')
        }
      },
      custom: [
        {
          thin: true,
          text: null,
          icon: 'el-icon-view',
          size: 'small',
          disabled () {
            return !vm.hasPermissions('Retrieve')
          },
          order: 1,
          emit: 'onView'
        }
      ]
    },
    columns: [
      {
        title: '消息ID',
        key: 'message_id',
        width: 140,
        form: { disabled: true }
      },
      {
        title: '标题',
        key: 'title',
        search: {
          disabled: false
        },
        width: 200,
        form: {
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          component: { span: 24, placeholder: '请输入标题' }
        }
      },
      {
        title: '分类',
        key: 'cate',
        search: {
          disabled: false
        },
        width: 200,
        type: 'select',
        dict: {
          data: [{ value: 'fun', label: '趣闻轶事' }, { value: 'free_resources', label: '免费资源' },
            { value: 'applications', label: '垂直应用' }, { value: 'hashrates_share', label: '算力分享' },
            { value: 'llm', label: '大模型' }, { value: 'drawing', label: 'AI绘画' },
            { value: 'meta_universe', label: '元宇宙' }, { value: 'AIGC', label: 'AIGC' },
            { value: 'AGI', label: 'AGI' }, { value: 'announcement', label: '公告' }
          ]
        },
        form: {
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          component: { span: 24, placeholder: '请输入分类' },
          editDisabled: false,
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '描述',
        key: 'desc',
        search: {
          disabled: true
        },
        width: 200,
        form: {
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          component: { span: 24, placeholder: '请输入描述', type: 'textarea', row: 4 }
        }
      },
      {
        title: '首页图片',
        key: 'image',
        type: 'image-uploader',
        search: {
          disabled: true
        },
        minWidth: 300
      },
      {
        title: '是否更新首页图片',
        show: false,
        key: 'is_update_pic',
        // width: 150,
        type: 'select',
        dict: {
          data: [{ value: '1', label: '是', color: 'success' }, { value: '0', label: '否', color: 'danger' }]
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请选择是否涉及到更新首页图片'
          },
          helper: {
            render (h) {
              return (< el-alert title="如果更新了首页图片，这里请选择是" type="info" />
              )
            }
          }
        }
      },
      {
        title: '创建者',
        key: 'creator',
        search: {
          disabled: false
        },
        width: 200,
        type: 'input',
        form: {
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          component: { span: 24, placeholder: '请输入创建者', disabled: true }, // 禁用输入框
          editDisabled: true,
          value: vm.$store.state.d2admin.user.info.name,
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '开始时间',
        key: 'start_time',
        search: {
          disabled: false
        },
        width: 200,
        type: 'datetime',
        form: {
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          disabled: false,
          component: {
            placeholder: '开始时间',
            'value-format': 'yyyy-MM-dd HH:mm:ss', // 添加这一行
            span: 24,
            type: 'date'
          }
        }
      },
      {
        title: '结束时间',
        key: 'end_time',
        search: {
          disabled: false
        },
        type: 'datetime',
        width: 200,
        form: {
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          disabled: false,
          component: {
            placeholder: '结束时间',
            'value-format': 'yyyy-MM-dd HH:mm:ss', // 添加这一行
            span: 24,
            type: 'date'
          }
        }
      },
      {
        title: '权重',
        key: 'weight',
        search: {
          disabled: true
        },
        width: 100,
        form: {
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          component: { span: 24, placeholder: '请输入权重', type: 'number' },
          helper: {
            render (h) {
              return (< el-alert title="数值越大，显示顺序越靠前" type="info" />
              )
            }
          }
        }
      },
      {
        title: '目标用户',
        key: 'target_users',
        show: false,
        search: {
          disabled: true
        },
        width: 200,
        form: {
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          component: {
            span: 24,
            placeholder: '请输入目标用户'
            // show: false
          }
        }
      },
      {
        title: '目标类型',
        key: 'target_type',
        search: {
          disabled: false
        },
        type: 'select',
        dict: {
          data: vm.dictionary('target_type')
        },
        width: 200,
        form: {
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          component: { span: 24, placeholder: '请输入目标类型', type: 'select' }
        }
      },
      {
        title: '消息类型',
        key: 'message_type',
        search: {
          disabled: false
        },
        type: 'select',
        dict: {
          data: vm.dictionary('message_type')
        },
        width: 200,
        form: {
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          component: { span: 24, placeholder: '请输入消息类型', type: 'select' }
        }
      },
      {
        title: '是否轮播',
        key: 'is_arousel',
        search: {
          disabled: false
        },
        width: 200,
        type: 'select',
        dict: {
          data: vm.dictionary('button_whether_bool')
        },
        form: {
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          component: { span: 24, placeholder: '请输入是否轮播', type: 'select' }
        }
      },
      {
        title: '状态',
        key: 'status',
        search: {
          disabled: false
        },
        type: 'select',
        dict: {
          data: vm.dictionary('message_status')
        },
        width: 100,
        form: {
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          component: { span: 24, placeholder: '请输入状态', type: 'select' }
        }
      },
      {
        title: '更新时间',
        key: 'update_time',
        width: 150,
        search: {
          disabled: true
        },
        type: 'datetime',
        form: {
          show: false,
          editDisabled: true,
          component: {
            span: 12,
            disabled: true // 禁用输入框

          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      },
      {
        title: '内容',
        key: 'content',
        minWidth: 300,
        type: 'editor-quill', // 富文本图片上传依赖file-uploader，请先配置好file-uploader
        form: {
          rules: [ // 表单校验规则
            {
              required: true,
              message: '必填项'
            }
          ],
          component: {
            disabled: () => {
              return vm.getEditForm().disable
            },
            props: {
              uploader: {
                type: 'form' // 上传后端类型【cos,aliyun,oss,form】
              }
            },
            events: {
              'text-change': (event) => {
                console.log('text-change:', event)
                let content = event.scope.form.content

                if (content.includes('http://127.0.0.1:8000/')) {
                  content = content.replace(/http:\/\/127\.0\.0\.1:8000\//g, '')
                  vm.getEditForm().content = content // 更新内容
                }

                if (content.includes('http://39.108.174.55:8080/')) {
                  content = content.replace(/http:\/\/39\.108\.174\.55:8080\//g, '')
                  vm.getEditForm().content = content // 更新内容
                }
              }
            }
          }
        },
        component: {
          render (h, params) {
            const content = params.row.content.length > 30 ? params.row.content.substring(0, 30) + '...' : params.row.content
            return h('el-tooltip', {
              props: {
                content: params.row.content,
                placement: 'top'
              }
            }, [
              h('span', {}, content)
            ])
          }
        }
      }
    ]
  }
}
