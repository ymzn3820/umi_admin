
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
      },
      custom: [{
        text: '启用',
        type: 'success',
        size: 'small',
        emit: 'PubSecretKey'
      }]
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
        title: 'Key',
        key: 'key',
        search: {
          disabled: false
        },
        minWidth: 130,
        type: 'input',
        form: {
          disabled: false,
          rules: [ // 表单校验规则
            {
              required: true,
              message: '必填项'
            }
          ],
          component: {
            placeholder: ''
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '状态',
        key: 'o_status',
        // sortable: 'custom',
        minWidth: 70,
        search: {
          disabled: true
        },
        type: 'radio',
        dict: {
          data: vm.dictionary('secret_key')
        },
        form: {
          value: 1,
          component: {
            span: 12,
            placeholder: '请选择状态',
            disabled: true
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '密钥类型',
        key: 'key_type',
        search: {
          disabled: false
        },
        minWidth: 70,
        type: 'radio',
        dict: {
          data: vm.dictionary('secret_key_type')
        },
        form: {
          rules: [{
            required: true,
            message: '必填项'
          }
          ],
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
        title: '描述',
        key: 'desc',
        type: 'input',
        search: {
          disabled: true
        },
        minWidth: 300,
        form: {
          value: '',
          rules: [ // 表单校验规则
          ],
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            props: {
              elProps: { // 与el-uploader 配置一致
                multiple: false,
                limit: 1 // 限制5个文件
              }
              // sizeLimit:  * 1024 // 不能超过限制
            },
            span: 24
          }
        }
      },
      {
        title: '绑定的服务器',
        key: 'server_ip',
        minWidth: 90,
        type: 'input',
        search: {
          disabled: false
        },
        form: {
          disabled: false,
          itemProps: {
            class: { yxtInput: true }
          },
          helper: {
            render (h) {
              return (< el-alert title="如果不是立即启用，请勿填写该字段" type="warning" />
              )
            }
          }
        }
        // disabled: true
      }
    ]
  }
}
