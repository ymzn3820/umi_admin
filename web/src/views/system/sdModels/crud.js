
export const crudOptions = (vm) => {
  // util.filterParams(vm, ['dept_name', 'role_info{name}', 'dept_name_all'])
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      // tableType: 'vxe-table',
      rowKey: 'model_id',
      rowId: 'model_id'
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
        title: '模型ID',
        key: 'model_id',
        search: {
          disabled: false
        },
        minWidth: 130,
        type: 'input',
        form: {
          disabled: true
        }
      },
      {
        title: '标题',
        key: 'name',
        minWidth: 70,
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
        },
        search: {
          disabled: true
        },
        type: 'input'
      },
      {
        title: '名称',
        key: 'value',
        search: {
          disabled: true
        },
        minWidth: 90,
        type: 'input',
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
        title: '图片',
        key: 'pic_url',
        type: 'image-uploader',
        search: {
          disabled: true
        },
        minWidth: 300,
        form: {
          value: '',
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
          },
          helper: '更换新图片请将是否更新图片设置为【是】'
        }
      },
      {
        title: '是否更新图片',
        show: false,
        key: 'is_update_icon',
        // width: 150,
        type: 'select',
        dict: {
          data: [{ value: '1', label: '是', color: 'success' }, { value: '0', label: '否', color: 'danger' }]
        },
        form: {
          itemProps: {
            class: { yxtInput: true }
          },
          value: '0',
          disabled: false,
          component: {
            placeholder: '请选择是否涉及到更新ICON'
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      }
    ]
  }
}
