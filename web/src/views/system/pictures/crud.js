
export const crudOptions = (vm) => {
  // util.filterParams(vm, ['dept_name', 'role_info{name}', 'dept_name_all'])
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      // tableType: 'vxe-table',
      rowKey: 'pic_id',
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
        text: '复制对象地址',
        type: 'success',
        size: 'small',
        emit: 'copyToClipboard'
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
        title: '图片ID',
        key: 'pic_id',
        search: {
          disabled: false
        },
        minWidth: 130,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: '请输入图片ID'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '类型',
        key: 'type',
        minWidth: 90,
        type: 'radio',
        dict: {
          data: vm.dictionary('pictures')
        },
        search: {
          disabled: false
        },
        form: {
          rules: [ // 表单校验规则
            {
              required: true,
              message: '必填项'
            }
          ],
          editDisabled: false,
          itemProps: {
            class: { yxtInput: true }
          }
        }
        // disabled: true
      },
      {
        title: '图片大小',
        key: 'pic_size',
        // sortable: 'custom',
        minWidth: 70,
        search: {
          disabled: true
        },
        type: 'input',
        form: {
          component: {
            span: 12,
            placeholder: '请输入大小'
          },
          helper: '单位为KB，支持浮点数',
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '图片格式',
        key: 'pic_format',
        search: {
          disabled: true
        },
        minWidth: 70,
        form: {
          placeholder: '请输入格式',
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            span: 12,
            pagination: true,
            props: { multiple: false }
          },
          helper: '请填写大写'

        }
      },
      {
        title: '图片',
        key: 'pic_url',
        type: 'file-uploader',
        search: {
          disabled: true
        },
        minWidth: 300
      },
      {
        title: '图片描述',
        key: 'pic_desc',
        search: {
          disabled: false
        },
        minWidth: 110,
        type: 'input',
        form: {
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            placeholder: '请输入图片描述',
            clearable: true

          }
        }
      }, {
        title: '上传者',
        key: 'uploader_id',
        minWidth: 100,
        form: {
          itemProps: {
            class: { yxtInput: true }
          },
          editDisabled: true,
          value: vm.$store.state.d2admin.user.info.name,
          component: {
            span: 12,
            placeholder: '请输入上传者ID',
            disabled: true // 禁用输入框

          }
        }
      },
      {
        title: '数据库状态',
        search: {
          disabled: false
        },
        key: 'is_delete',
        type: 'radio',
        width: 70,
        dict: {
          data: vm.dictionary('is_delete')
        },
        form: {
          disabled: true,
          value: false,
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            span: 12,
            value: false
            // disabled: true
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      },
      {
        title: '更新时间',
        key: 'update_time',
        width: 150,
        type: 'datetime',
        form: {
          disabled: true,
          component: {
            placeholder: ''
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      }, {
        title: '创建时间',
        key: 'create_time',
        width: 150,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: ''
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
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
          disabled: false,
          component: {
            placeholder: '请输入上传至文件夹名称'
          },
          helper: '如果不涉及图片更新，此处可不填'

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
            placeholder: '请选择是否涉及到更新图片'
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      }
    ]
  }
}
