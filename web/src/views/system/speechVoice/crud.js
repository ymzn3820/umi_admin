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
    indexRow: {
      title: '序号',
      align: 'center',
      width: 60
    },
    columns: [
      {
        title: 'engine_code',
        key: 'engine_code',
        search: {
          disabled: false
        },
        minWidth: 130,
        type: 'select',
        form: {
          rules: [{
            required: true,
            message: '必填项'
          }]
        },
        dict: {
          data: [
            { value: '1000010001', label: '普通版' },
            { value: '1000010002', label: '高级版' },
            { value: '1000010003', label: '百度' },
            { value: '1000010004', label: '讯飞星火' },
            { value: '1000010005', label: '阿里巴巴' }
          ]
        }
      },
      {
        title: 'voice_code',
        key: 'voice_code',
        search: {
          disabled: false
        },
        minWidth: 100,
        type: 'input',
        form: {
          disabled: true,
          rules: [{
            required: false,
            message: '必填项'
          }]
        }
      },
      {
        title: '音色',
        key: 'voice',
        search: {
          disabled: true
        },
        minWidth: 90,
        type: 'input',
        form: {
          rules: [{
            required: true,
            message: '必填项'
          }]
        }
      },
      {
        title: '音色名称',
        key: 'voice_name',
        search: {
          disabled: true
        },
        minWidth: 120,
        type: 'input',
        form: {
          rules: [{
            required: true
          }]
        }
      },
      {
        title: '音色Logo',
        key: 'voice_logo',
        type: 'image-uploader',
        search: {
          disabled: true
        },
        minWidth: 300,
        form: {
          rules: [{
            required: true
          }],
          value: '',
          component: {
            props: {
              elProps: {
                multiple: false,
                limit: 1
              },
              span: 24
            }
          }
        }
      },
      {
        title: '音色试听URL',
        key: 'speech_url',
        search: {
          disabled: true
        },
        minWidth: 200,
        type: 'input',
        form: {
          rules: [{
            required: true
          }]
        }
      },
      {
        title: '语言',
        key: 'language',
        search: {
          disabled: true
        },
        minWidth: 100,
        type: 'input',
        form: {
          rules: [{
            required: false
          }]
        }
      },
      {
        title: '描述',
        key: 'desc',
        search: {
          disabled: true
        },
        minWidth: 200,
        type: 'textarea',
        form: {
          rules: [{
            required: true
          }]
        }
      },
      {
        title: '创建人',
        key: 'create_by',
        search: {
          disabled: true
        },
        minWidth: 120,
        type: 'input',
        form: {
          disabled: true,
          itemProps: {
            class: { yxtInput: true }
          },
          editDisabled: true,
          value: vm.$store.state.d2admin.user.info.name,
          component: {
            span: 12,
            disabled: true, // 禁用输入框
            placeholder: '请输入创建人'
          }
        }
      },
      {
        title: '创建日期',
        key: 'create_time',
        search: {
          disabled: true
        },
        minWidth: 150,
        type: 'datetime',
        form: {
          disabled: true
        }
      },
      {
        title: '修改日期',
        key: 'modify_time',
        search: {
          disabled: true
        },
        minWidth: 150,
        type: 'datetime',
        form: {
          disabled: true
        }
      },
      {
        title: '是否删除',
        key: 'is_delete',
        search: {
          disabled: false
        },
        minWidth: 90,
        type: 'radio',
        dict: {
          data: vm.dictionary('button_whether_bool')
        },
        form: {
          value: false
        }
      },
      {
        title: '文件夹',
        show: false,
        key: 'cate',
        // width: 150,
        // type: 'input',
        form: {
          itemProps: {
            class: { yxtInput: true }
          },
          editDisabled: false,
          value: 'model',
          component: {
            placeholder: '请输入上传至文件夹名称',
            disabled: true // 禁用输入框

          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      },
      {
        title: '是否更新图片',
        show: false,
        key: 'is_update_pic',
        // width: 150,
        type: 'select',
        dict: {
          data: [{ value: '1', label: '是', color: 'success' }, { value: '0', label: '否', color: 'danger' }]
        },
        form: {
          itemProps: {
            class: { yxtInput: true }
          },
          disabled: false,
          component: {
            placeholder: '请选择是否涉及到图片'
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      }
    ]
  }
}
