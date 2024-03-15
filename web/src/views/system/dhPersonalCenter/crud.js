export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      rowKey: 'product_id',
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
        title: '产品类型',
        key: 'product_type',
        minWidth: 130,
        type: 'select',
        form: {
          component: {
            placeholder: '请选择产品类型'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        },
        dict: {
          data: [
            { label: '无人直播', value: 1 },
            { label: '短视频矩阵', value: 2 },
            { label: '数字人直播', value: 3 }
          ]
        }
      },
      {
        title: '下载地址',
        key: 'download_link',
        minWidth: 150,
        type: 'input',
        form: {
          component: {
            placeholder: '请输入下载地址'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '使用教程',
        key: 'tutorial',
        minWidth: 150,
        type: 'input',
        form: {
          component: {
            placeholder: '请输入使用教程链接'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '使用说明',
        key: 'usage_description',
        minWidth: 200,
        type: 'textarea',
        form: {
          component: {
            placeholder: '请输入产品的使用说明'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
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
        title: '更新日期',
        key: 'update_time',
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
            { label: '是', value: 1 },
            { label: '否', value: 0 }
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
