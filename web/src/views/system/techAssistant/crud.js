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
      defaultSpan: 12
    },
    indexRow: {
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
        title: '问题描述',
        key: 'problem',
        minWidth: 130,
        type: 'input',
        form: {
          component: {
            placeholder: '请输入问题描述'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '联系方式',
        key: 'contact',
        search: {
          disabled: false
        },
        minWidth: 90,
        type: 'input',
        form: {
          component: {
            placeholder: '请输入联系方式'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '截图',
        key: 'picture_url',
        search: {
          disabled: true
        },
        minWidth: 90,
        type: 'image-uploader',
        form: {
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      // {
      //   title: '创建人',
      //   key: 'create_by',
      //   minWidth: 100,
      //   type: 'input',
      //   form: {
      //     component: {
      //       placeholder: '请输入创建人'
      //     },
      //     itemProps: {
      //       class: { yxtInput: true }
      //     }
      //   }
      // },
      {
        title: '创建日期',
        key: 'create_time',
        minWidth: 150,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: ''
          }
        }
      },
      {
        title: '最近修改日期',
        key: 'modify_time',
        minWidth: 150,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: ''
          }
        }
      },
      {
        title: '是否删除',
        key: 'is_delete',
        minWidth: 100,
        type: 'radio',
        dict: {
          data: [
            { label: '是', value: true },
            { label: '否', value: false }
          ]
        },
        form: {
          component: {
            value: false,
            placeholder: '请选择是否删除'
          }
        }
      }
    ]
  }
}
